from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.deps import require_roles
from db.db_helper import db_helper
from model import Part, User, Categories
from schemas.common import Page
from schemas.parts import PartRead, PartUpdate, PartCreate

router = APIRouter(
    prefix="/api_v1/parts",
    tags=["parts"],
)

@router.get("/", response_model=Page[PartRead])
async def get_parts(
        search: str | None = None,
        category_id: int | None = None,
        limit: int = Query(20, ge =1, le = 100),
        offset: int = Query(0, ge = 0),
        _: User = Depends(require_roles("admin", "storekeeper" , "master")),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    query = select(Part)
    if search:
        pattern = f"%{search}%"
        query = query.where(Part.name.ilike(pattern) | Part.sku.ilike(pattern))
    if category_id is not None:
        query = query.where(Part.category_id == category_id)

    total = await session.scalar(select(func.count()).select_from(query.subquery()))

    result = await session.execute(query.order_by(Part.name).limit(limit).offset(offset))

    return Page(items = result.scalars().all(), total = total, limit = limit, offset = offset)


@router.get("/{part_id}", response_model=PartRead)
async def get_part_by_id(part_id: int,
                         user: User = Depends(require_roles("admin", "storekeeper" , "master")),
                         session: AsyncSession = Depends(db_helper.session_getter)
                         ):
    part = await session.get(Part, part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@router.post("/", response_model=PartRead, status_code = status.HTTP_201_CREATED)
async def create_part(data: PartCreate,
                      _:User = Depends(require_roles("admin")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    category = await session.get(Categories, data.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Part not found")

    part = Part(**data.model_dump())
    session.add(part)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Part already exists")
    await session.refresh(part)
    return part



@router.patch("/{part_id}", response_model=PartRead)
async def update_part(part_id: int, data: PartUpdate,
                      _: User = Depends(require_roles("admin", "storekeeper")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    part = await session.get(Part, part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    values = data.model_dump(exclude_unset=True)

    if "category_id" in values and await session.get(Categories, values["category_id"]) is None:
        raise HTTPException(status_code=422, detail="Category not found")
    for key,value in values.items():
        setattr(part, key, value)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Part is in use")
    await session.refresh(part)
    return part

@router.delete("/{part_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_part(part_id: int,
                      _: User = Depends(require_roles("admin")),
                      session: AsyncSession = Depends(db_helper.session_getter)):
    part = await session.get(Part, part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")
    await session.delete(part)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Part is in use")


