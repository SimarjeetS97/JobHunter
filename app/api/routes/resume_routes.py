from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies import get_resume_service
from app.dtos.resume import ResumeUploadResponseDTO
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload", response_model=ResumeUploadResponseDTO, summary="Upload and parse a resume")
async def upload_resume(
    file: UploadFile = File(...),
    service: ResumeService = Depends(get_resume_service),
) -> ResumeUploadResponseDTO:
    return await service.upload_resume(file=file)
