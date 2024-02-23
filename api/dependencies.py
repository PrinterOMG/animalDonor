from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session


db_session_dep = Annotated[AsyncSession, Depends(get_async_session)]
