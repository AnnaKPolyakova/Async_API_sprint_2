import uuid
from functools import wraps
from http import HTTPStatus
import requests
from fastapi import HTTPException

from src.core.config import settings


def authentication_required(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        authorization = kwargs['request'].headers.get('authorization')
        response = getattr(requests, 'get')(
            settings.AUTH_HOST,
            headers={
                "Authorization": authorization,
                # 'X-Request-Id': str(uuid.uuid4())
            }
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
            )
        return await func(*args, **kwargs)

    return wrapped
