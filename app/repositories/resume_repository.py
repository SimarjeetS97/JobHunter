from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume


class ResumeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, filename: str, mime_type: str, raw_text: str, parsed_data: dict) -> Resume:
        resume = Resume(filename=filename, mime_type=mime_type, raw_text=raw_text, parsed_data=parsed_data)
        self._session.add(resume)
        await self._session.commit()
        await self._session.refresh(resume)
        return resume

    async def get_by_id(self, resume_id: UUID) -> Resume | None:
        return await self._session.get(Resume, resume_id)
