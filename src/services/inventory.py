from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from model import Part, Supplier, Operations, User
from schemas.operations import OperationCreate


async def apply_operation(session: AsyncSession, data: OperationCreate, user: User) -> Operations:
    if data.type == "receipt":
        supplier = await session.get(Supplier, data.supplier_id)
        if supplier is None:
            raise HTTPException(status_code=404, detail="Supplier not found")

    result = await session.execute(
        select(Part).where(Part.part_id == data.part_id).with_for_update()
    )
    part = result.scalar_one_or_none()
    if part is None:
        raise HTTPException(status_code=404, detail="Part not found")

    if data.type == "receipt":
        part.quantity += data.quantity
    else:
        raise HTTPException(status_code=501, detail="Operation not supported")

    operation = Operations(**data.model_dump(), user_id=user.user_id)
    session.add(operation)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Operation violates data constraints")
    await session.refresh(operation)
    return operation