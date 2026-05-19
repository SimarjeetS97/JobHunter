from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.openai_client.resume_extractor import (
    ResumeExtractor,
    get_openai_client,
    get_rate_limiter,
)
from app.repositories.resume_repository import ResumeRepository
from app.services.file_parser_service import FileParserService
from app.services.resume_service import ResumeService


def get_resume_repository(session: AsyncSession = Depends(get_db_session)) -> ResumeRepository:
    return ResumeRepository(session=session)


def get_file_parser_service() -> FileParserService:
    return FileParserService()


def get_resume_extractor() -> ResumeExtractor:
    return ResumeExtractor(client=get_openai_client(), rate_limiter=get_rate_limiter())


def get_resume_service(
    repository: ResumeRepository = Depends(get_resume_repository),
    parser_service: FileParserService = Depends(get_file_parser_service),
    extractor: ResumeExtractor = Depends(get_resume_extractor),
) -> ResumeService:
    return ResumeService(repository=repository, parser_service=parser_service, extractor=extractor)
