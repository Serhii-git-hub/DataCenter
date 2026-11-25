from typing import Callable

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.security import decode_token
from db.db_helper import db_helper
from model.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db_helper.session_getter)) -> User:
    try:
        payload = decode_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail = "Invalid token")
    user_id = int(payload["sub"])
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail = "User not found")
    return user

def require_roles(*roles: str)-> Callable[..., User]:
    def checker(user: User = Depends(get_current_user) ) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail = "You do not have permission to perform this action")
        return user
    return checker

