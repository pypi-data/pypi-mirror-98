import inspect
from typing import Any, Callable


async def await_if_coroutine(obj: Callable, *args, **kwargs) -> Any:
    """if obj is coroutine await it"""
    if inspect.iscoroutinefunction(obj):
        return await obj(*args, **kwargs)
    else:
        return obj(*args, **kwargs)
