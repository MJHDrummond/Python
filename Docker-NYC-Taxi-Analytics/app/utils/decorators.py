from functools import wraps
import asyncio

def log_step(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print(f"Starting async {func.__name__}...")
            result = await func(*args, **kwargs)
            print(f"Finished async {func.__name__}.")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            print(f"Starting {func.__name__}...")
            result = func(*args, **kwargs)
            print(f"Finished {func.__name__}.")
            return result
        return sync_wrapper
