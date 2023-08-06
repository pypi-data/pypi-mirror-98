from typing import Any, Awaitable, Optional, Type

from .deco import test_wrapper


class Assertion:
    def __init__(
        self,
        msg: Optional[str] = None,
        exception: Type[Exception] = AssertionError,
        timeout: float = 0.0,
        msg_length_max: int = 100,
        delay_init: float = 0.125,
        delay_max: float = 5.0,
    ) -> None:
        self.msg = msg
        self.exception = exception
        self.timeout = timeout
        self.msg_length_max = msg_length_max
        self.delay_init = delay_init
        self.delay_max = delay_max

    def _get_exception(
        self,
        fail_desc: str,
        msg: Optional[str],
        exception: Optional[Type[Exception]],
    ) -> Exception:
        # Do not use ``or`` here to allow for ``msg=""``.
        if msg is None:
            msg = self.msg

        exc = exception or self.exception

        if len(fail_desc) > self.msg_length_max:
            fail_desc = fail_desc[: self.msg_length_max - 4] + " ..."

        return exc(msg + ": " + fail_desc if msg else fail_desc)

    @test_wrapper
    def true(  # type: ignore[return]
        self,
        a: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not bool(a):
            raise self._get_exception(f"{a!r} != True", msg, exception)

    @test_wrapper
    def false(  # type: ignore[return]
        self,
        a: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if bool(a):
            raise self._get_exception(f"{a!r} != False", msg, exception)

    @test_wrapper
    def equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a == b):
            raise self._get_exception(f"{a!r} != {b!r}", msg, exception)

    @test_wrapper
    def not_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a != b):
            raise self._get_exception(f"{a!r} == {b!r}", msg, exception)

    @test_wrapper
    def less(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        # CAREFUL: For some parameters ``a >= b`` is _not_ equal to ``not (a < b)``!
        # The same is true for other comparisons.
        if not (a < b):
            raise self._get_exception(f"{a!r} !< {b!r}", msg, exception)

    @test_wrapper
    def less_or_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a <= b):
            raise self._get_exception(f"{a!r} !<= {b!r}", msg, exception)

    @test_wrapper
    def greater(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a > b):
            raise self._get_exception(f"{a!r} !> {b!r}", msg, exception)

    @test_wrapper
    def greater_or_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a >= b):
            raise self._get_exception(f"{a!r} !>= {b!r}", msg, exception)

    @test_wrapper
    def in_(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a not in b:
            raise self._get_exception(f"{a!r} not in {b!r}", msg, exception)

    @test_wrapper
    def not_in(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a in b:
            raise self._get_exception(f"{a!r} in {b!r}", msg, exception)

    @test_wrapper
    def is_(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a is not b:
            raise self._get_exception(f"{a!r} is not {b!r}", msg, exception)

    @test_wrapper
    def is_not(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a is b:
            raise self._get_exception(f"{a!r} is {b!r}", msg, exception)

    def _get_new_delay(self, old_delay: float) -> float:
        return min(self.delay_max, 2 * old_delay)
