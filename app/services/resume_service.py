from fastapi import HTTPException, UploadFile, status

from app.dtos.resume import ResumeUploadResponseDTO
from app.openai_client.resume_extractor import ResumeExtractor
from app.repositories.resume_repository import ResumeRepository
from app.services.file_parser_service import FileParserService


class ResumeService:
    def __init__(
        self,
        repository: ResumeRepository,
        parser_service: FileParserService,
        extractor: ResumeExtractor,
    ) -> None:
        self._repository = repository
        self._parser_service = parser_service
        self._extractor = extractor

    async def upload_resume(self, file: UploadFile) -> ResumeUploadResponseDTO:
        try:
            raw_text = await self._parser_service.parse(file)
        except ValueError as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error

        if not raw_text:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume contains no parsable text")

        parsed = await self._extractor.extract(raw_text)
        entity = await self._repository.create(
            filename=file.filename or "unknown",
            mime_type=file.content_type or "application/octet-stream",
            raw_text=raw_text,
            parsed_data=parsed.model_dump(mode="json"),
        )
        return ResumeUploadResponseDTO(
            id=entity.id,
            filename=entity.filename,
            mime_type=entity.mime_type,
            parsed_data=parsed,
            created_at=entity.created_at,
        )
