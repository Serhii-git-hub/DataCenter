
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.deps import require_roles
from db.db_helper import db_helper
from model import User
from schemas.operations import OperationRead, OperationCreate
from services.inventory import apply_operation

router = APIRouter(prefix="/api_v1/operations", tags=["Operations"])


@router.post("/", response_model=OperationRead, status_code=status.HTTP_201_CREATED)
async def create_operation(
        data: OperationCreate,
        user: User = Depends(require_roles('admin', 'storekeeper' , 'master')),
        session: AsyncSession = Depends(db_helper.session_getter)):
    return  await apply_operation(session, data, user)