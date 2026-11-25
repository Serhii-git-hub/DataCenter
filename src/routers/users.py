from typing import List

from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.deps import require_roles
from auth.security import hash_password
from db.db_helper import db_helper
from model import User
from schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/api_v1/users", tags=["users"])

@router.get("/", response_model=List[UserRead])
async def get_user(_: User = Depends(require_roles("admin")),
                   session: AsyncSession = Depends(db_helper.session_getter)):
    user = await session.execute(select(User).order_by(User.full_name))
    result = user.scalars().all()
    return result

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    _: User = Depends(require_roles("admin")),
    session: AsyncSession = Depends(db_helper.session_getter)
):
   user = await session.get(User, user_id)
   if user is None:
        raise HTTPException(status_code=404, detail="User not found")
   return user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate,
                      _: User = Depends(require_roles("admin")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    values = data.model_dump()
    password = values.pop("password")
    user = User(**values, password_hash=hash_password(password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Login already exists")
    await session.refresh(user)
    return user

@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user(user_id: int,data: UserUpdate,
                      _: User = Depends(require_roles("admin")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    values = data.model_dump(exclude_unset=True)
    if "password" in values:
        user.password_hash = hash_password(values.pop("password"))
    for key, value in values.items():
        setattr(user, key, value)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Login already exists")
    await session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      current: User = Depends(require_roles("admin")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    user = await session.get(User, user_id)
    if current.user_id == user_id:
        raise HTTPException(status_code=409, detail="You can't delete yourself")
    elif user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="User is in use")
