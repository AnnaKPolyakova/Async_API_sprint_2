from functools import wraps
from http import HTTPStatus
import requests
from fastapi import HTTPException

from src.core.config import settings


def authentication_required(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        authorization = kwargs['request'].headers.get('authorization')
        try:
            response = getattr(requests, 'get')(
                settings.AUTH_HOST,
                headers={
                    "Authorization": authorization,
                }
            )
        except requests.exceptions.ConnectionError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
            )
        else:
            if response.status_code != HTTPStatus.OK:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                )
        return await func(*args, **kwargs)

    return wrapped
