from typing import Callable, Any, Awaitable
from aiofiles.os import wrap as method_as_method_coro, \
  wrap as func_as_corofunc
from functools import wraps

try:
  from asyncio import to_thread

except ImportError:
  from asyncio import get_running_loop

  async def to_thread(func: Callable, *args, **kwargs) -> Any:
    return await loop.run_in_executor(
      None,
      func,
      *args,
      **kwargs
    )


CoroutineResult = Awaitable[Any]
CoroutineFunction = Callable[..., CoroutineResult]
CoroutineMethod = Callable[..., CoroutineResult]


def func_as_method_coro(func: Callable) -> CoroutineMethod:
  @wraps(func)
  async def method(self, *args, **kwargs) -> Any:
    return await to_thread(func, *args, **kwargs)

  return method


def coro_as_method_coro(coro: CoroutineFunction) -> CoroutineMethod:
  @wraps(coro)
  async def method(self, *args, **kwargs) -> Any:
    return await coro(*args, **kwargs)

  return method
