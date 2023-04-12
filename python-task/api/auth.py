import secrets
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials
)
from fastapi import (
    Depends,
    HTTPException,
    status
)
from typing import Annotated

from core.env import env


security = HTTPBasic()


async def is_authenticated(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = env('AUTH_USER').encode()
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = env('AUTH_PASS').encode()
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username