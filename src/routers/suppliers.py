from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.deps import require_roles
from db.db_helper import db_helper
from model import Supplier, User
from schemas.supplier import SupplierRead, SupplierCreate, SupplierUpdate

router = APIRouter(prefix="/api_v1/suppliers", tags=["Suppliers"])

@router.get("/" , response_model=List[SupplierRead])
async def get_suppliers(_: User = Depends(require_roles("admin", "storekeeper")) ,
                        session: AsyncSession = Depends(db_helper.session_getter)):
    supplier = await session.execute(select(Supplier).order_by(Supplier.name))
    result = supplier.scalars().all()
    return result

@router.post("/", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
async def create_supplier(data: SupplierCreate,
                          _:User = Depends(require_roles("admin")),
                          session: AsyncSession = Depends(db_helper.session_getter),
                          ):
    try:
        supplier = Supplier(**data.model_dump())
        session.add(supplier)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="This supplier is in use")
    await session.refresh(supplier)
    return supplier

@router.patch("/{supplier_id}" , response_model=SupplierRead)
async def update_supplier(supplier_id: int, data: SupplierUpdate,
                          session: AsyncSession = Depends(db_helper.session_getter),
                          _:User = Depends(require_roles("admin"))):
    supplier = await session.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(supplier, key, value)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="This supplier already exists")
    await session.refresh(supplier)
    return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int,
                          session: AsyncSession = Depends(db_helper.session_getter),
                          _:User = Depends(require_roles("admin"))):
    supplier = await session.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    await session.delete(supplier)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="This supplier is in use")


