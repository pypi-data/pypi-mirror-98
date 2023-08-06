import asyncio
import time
from asyncio import iscoroutinefunction
from functools import partial, wraps
from inspect import isawaitable
from time import monotonic
from typing import Awaitable, Callable, Optional, Type, Union


# coro partials: https://stackoverflow.com/a/52422903/20954
def is_coro_or_partial(obj):
    # fix partial() for Python 3.7
    while isinstance(obj, partial):
        obj = obj.func  # pragma: no cover
    return iscoroutinefunction(obj)


class DummyAwaitable:
    def __await__(self):
        yield


dummy_awaitable = DummyAwaitable()


def test_wrapper(func) -> Union[Callable, Awaitable]:
    async def async_tester(self, test, tests, msg, timeout, exception):
        tests = list(tests)

        # replace all awaitables (can only be awaited once)
        awaitable_results = await asyncio.gather(*[a for a in tests if isawaitable(a)])
        for i, a in enumerate(tests):
            if isawaitable(a):
                tests[i] = awaitable_results.pop()

        time_start = monotonic()
        delay = self.delay_init
        while True:
            awaitable_results = await asyncio.gather(
                *[a() for a in tests if is_coro_or_partial(a)]
            )
            evaluated = []
            for a in tests:
                if iscoroutinefunction(a):
                    evaluated.append(awaitable_results.pop())
                elif callable(a):
                    evaluated.append(a())
                else:
                    evaluated.append(a)

            try:
                test(self, *evaluated, msg=msg, timeout=timeout, exception=exception)
            except self.exception:
                time_diff = monotonic() - time_start
                if time_diff >= timeout:
                    raise  # exception()  # TimeoutError()
                else:
                    await asyncio.sleep(min(delay, timeout - time_diff + 0.01))
                    delay = self._get_new_delay(delay)
            else:
                break

    def sync_tester(self, test, tests, msg, timeout, exception):
        time_start = monotonic()
        delay = self.delay_init
        while True:
            evaluated = []
            for t in tests:
                if callable(t):
                    evaluated.append(t())
                else:
                    evaluated.append(t)

            try:
                test(self, *evaluated, msg=msg, timeout=timeout, exception=exception)
                # return dummy awaitable to keep redundant awaits happy
                return dummy_awaitable
            except self.exception:
                time_diff = monotonic() - time_start
                if time_diff >= timeout:
                    raise  # exception()  # TimeoutError()
                else:
                    time.sleep(min(delay, timeout - time_diff + 0.01))
                    delay = self._get_new_delay(delay)

    @wraps(func)
    def wrapper(
        self,
        *tests,
        msg: Optional[str] = None,
        timeout: Optional[str] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if timeout is None:
            timeout = self.timeout

        for t in tests:
            if isawaitable(t) or iscoroutinefunction(t):
                return async_tester(self, func, tests, msg, timeout, exception)
        else:
            return sync_tester(self, func, tests, msg, timeout, exception)

    return wrapper
