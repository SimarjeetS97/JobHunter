from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ExperienceDTO(BaseModel):
    company: str = Field(min_length=1, max_length=255)
    title: str = Field(min_length=1, max_length=255)
    start_date: str = Field(min_length=4, max_length=20)
    end_date: str | None = Field(default=None, max_length=20)
    highlights: list[str] = Field(default_factory=list)


class EducationDTO(BaseModel):
    institution: str = Field(min_length=1, max_length=255)
    degree: str = Field(min_length=1, max_length=255)
    graduation_year: int | None = Field(default=None, ge=1900, le=2100)


class ResumeStructuredDataDTO(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)
    skills: list[str] = Field(default_factory=list)
    summary: str | None = Field(default=None, max_length=5000)
    experience: list[ExperienceDTO] = Field(default_factory=list)
    education: list[EducationDTO] = Field(default_factory=list)


class ResumeUploadResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    mime_type: str
    parsed_data: ResumeStructuredDataDTO
    created_at: datetime
