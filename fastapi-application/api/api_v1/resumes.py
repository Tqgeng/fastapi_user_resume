from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.shemas.resume import (
    ResumeCreate,
    ResumeUpdate,
    ResumeRead,
)
from core.config import settings
from .fastapi_users_router import current_active_user
from crud import resumes as resumes_crud
from core.models import db_helper, User

router = APIRouter(
    prefix=settings.api.v1.resumes,
    tags=["Resumes"],
)


@router.post("", response_model=ResumeRead)
async def create_resume(
    resume: ResumeCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resume = await resumes_crud.create_resume(
        resume_create=resume,
        session=session,
        user_id=user.id,
    )
    return resume


@router.get("/{resume_id}", response_model=ResumeRead)
async def get_resume(
    resume_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resume = await resumes_crud.get_resume(
        session=session,
        resume_id=resume_id,
    )
    if not resume or resume.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )
    return resume


@router.get("", response_model=list[ResumeRead])
async def get_resumes(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resumes = await resumes_crud.get_resumes(session=session, user_id=user.id)
    return resumes


@router.patch("/{resume_id}", response_model=ResumeRead)
async def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resume = await resumes_crud.get_resume(session=session, resume_id=resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )
    resume = await resumes_crud.update_resume(
        session=session,
        resume_id=resume_id,
        resume_update=resume_update,
    )
    return resume


@router.delete("/{resume_id}", response_model=ResumeRead)
async def delete_resume(
    resume_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resume = await resumes_crud.get_resume(session=session, resume_id=resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )
    resume = await resumes_crud.delete_resume(
        session=session,
        resume_id=resume_id,
    )
    return resume


@router.post("/{resume_id}/improve")
async def improve_resume(
    resume_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(current_active_user),
):
    resume = await resumes_crud.get_resume(session=session, resume_id=resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    improve_text = f"Improve version of resume: {resume.content[:100]}"
    return {
        "resume_id": resume_id,
        "original": resume.content,
        "improved": improve_text,
    }
