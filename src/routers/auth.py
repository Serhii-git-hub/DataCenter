
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.deps import get_current_user
from src.auth.security import verify_password, create_access_token
from db.db_helper import db_helper

from model.users import User
from schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.session_getter)):
    result = await session.execute(select(User).where(User.login == form.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.user_id, user.role)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model = UserRead )
async def me(user: User = Depends (get_current_user)) -> User:
    return user
