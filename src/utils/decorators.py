from functools import wraps

from services.auth_handler import get_permissions


def auth_required(action: str):
    """Decorator to get user permisssions by provided token."""
    def wrapper(fn):
        @wraps(fn)
        async def decorator(*args, **kwargs):
            token = kwargs.get('token')
            if await get_permissions(action, token):
                return await fn(*args, **kwargs)

        return decorator

    return wrapper
