from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Resume
from core.shemas.resume import (
    ResumeCreate,
    ResumeUpdate,
)


async def create_resume(
    resume_create: ResumeCreate,
    session: AsyncSession,
    user_id: int,
):
    resume = Resume(**resume_create.model_dump(), user_id=user_id)
    session.add(resume)
    await session.commit()
    await session.refresh(resume)
    return resume


async def get_resumes(
    session: AsyncSession,
    user_id: int,
) -> Sequence[Resume]:
    stmt = select(Resume).order_by(Resume.id)
    if user_id is not None:
        stmt = stmt.where(Resume.user_id == user_id)
    result = await session.scalars(stmt)
    return result.all()


async def get_resume(
    session: AsyncSession,
    resume_id: int,
) -> Resume | None:
    return await session.get(Resume, resume_id)


async def update_resume(
    session: AsyncSession,
    resume_id: int,
    resume_update: ResumeUpdate,
) -> Resume | None:
    resume = await session.get(Resume, resume_id)
    if not resume:
        return None
    for key, value in resume_update.model_dump(exclude_unset=True).items():
        setattr(resume, key, value)
    await session.commit()
    await session.refresh(resume)
    return resume


async def delete_resume(session: AsyncSession, resume_id: int) -> Resume | None:
    resume = await session.get(Resume, resume_id)
    if not resume:
        return None
    await session.delete(resume)
    await session.commit()
    return resume
