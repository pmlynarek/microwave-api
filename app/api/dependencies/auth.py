from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt

from app.api.errors import ForbiddenError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        _ = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ForbiddenError()
