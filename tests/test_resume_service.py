from datetime import UTC, datetime
import io
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException, UploadFile

from app.dtos.resume import ResumeStructuredDataDTO
from app.services.resume_service import ResumeService


class DummyParser:
    async def parse(self, file: UploadFile) -> str:
        return "John Doe\nPython"


class DummyExtractor:
    async def extract(self, raw_text: str) -> ResumeStructuredDataDTO:
        return ResumeStructuredDataDTO(
            full_name="John Doe",
            email="john@example.com",
            phone="123",
            skills=["Python"],
            summary="Engineer",
            experience=[],
            education=[],
        )


class DummyRepo:
    async def create(self, filename: str, mime_type: str, raw_text: str, parsed_data: dict) -> SimpleNamespace:
        return SimpleNamespace(
            id=uuid4(),
            filename=filename,
            mime_type=mime_type,
            raw_text=raw_text,
            parsed_data=parsed_data,
            created_at=datetime.now(UTC),
        )


@pytest.mark.asyncio
async def test_upload_resume_success() -> None:
    service = ResumeService(DummyRepo(), DummyParser(), DummyExtractor())
    file = UploadFile(filename="resume.pdf", file=io.BytesIO(b"dummy"))
    file.content_type = "application/pdf"

    result = await service.upload_resume(file)

    assert result.filename == "resume.pdf"
    assert result.parsed_data.full_name == "John Doe"


@pytest.mark.asyncio
async def test_upload_resume_raises_for_empty_text() -> None:
    class EmptyParser(DummyParser):
        async def parse(self, file: UploadFile) -> str:
            return ""

    service = ResumeService(DummyRepo(), EmptyParser(), DummyExtractor())
    file = UploadFile(filename="resume.pdf", file=io.BytesIO(b"dummy"))
    file.content_type = "application/pdf"

    with pytest.raises(HTTPException):
        await service.upload_resume(file)
