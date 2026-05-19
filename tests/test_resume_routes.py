import io
from datetime import datetime, UTC
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_resume_service
from app.dtos.resume import ResumeStructuredDataDTO, ResumeUploadResponseDTO
from app.main import app


class MockResumeService:
    async def upload_resume(self, file):
        return ResumeUploadResponseDTO(
            id=uuid4(),
            filename=file.filename or "resume.pdf",
            mime_type=file.content_type or "application/pdf",
            parsed_data=ResumeStructuredDataDTO(
                full_name="Jane Doe",
                email="jane@example.com",
                phone="999",
                skills=["FastAPI"],
                summary="Summary",
                experience=[],
                education=[],
            ),
            created_at=datetime.now(UTC),
        )


@pytest.mark.asyncio
async def test_upload_route() -> None:
    app.dependency_overrides[get_resume_service] = lambda: MockResumeService()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/resumes/upload",
            files={"file": ("resume.pdf", io.BytesIO(b"dummy"), "application/pdf")},
        )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["parsed_data"]["full_name"] == "Jane Doe"
