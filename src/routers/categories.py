from typing import List, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.deps import get_current_user, require_roles
from db.db_helper import db_helper
from model import Categories, User
from schemas.categories import CategoriesRead, CategoriesCreate, CategoriesUpdate

router = APIRouter(prefix="/api_v1/categories", tags=["categories"])

@router.get("/", response_model=List[CategoriesRead])
async def get_categories(_: User = Depends(get_current_user) ,
                         session: AsyncSession = Depends(db_helper.session_getter)):
    result = await session.execute(select(Categories).order_by(Categories.name))
    category = result.scalars().all()
    return category

@router.post("/", response_model=CategoriesRead, status_code=status.HTTP_201_CREATED)
async def create_category(data: CategoriesCreate, _:User = Depends(require_roles("admin")),
                          session: AsyncSession = Depends(db_helper.session_getter),
                         ):
    try:
        category = Categories(**data.model_dump())
        session.add(category)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Category already exists")
    await session.refresh(category)
    return category


@router.patch("/{category_id}", response_model=CategoriesRead)
async def update_category(category_id: int, data: CategoriesUpdate,
                          session: AsyncSession = Depends(db_helper.session_getter),
                          _:User = Depends(require_roles("admin"))):

        category = await session.get(Categories, category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        for key,value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=409, detail="Category already exists")
        await session.refresh(category)
        return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int,
                          session: AsyncSession = Depends(db_helper.session_getter),
                          _:User = Depends(require_roles("admin"))):
    category = await session.get(Categories, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Category is in use")

