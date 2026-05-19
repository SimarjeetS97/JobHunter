from __future__ import annotations

import io

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader


class FileParserService:
    SUPPORTED_MIME_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    async def parse(self, file: UploadFile) -> str:
        if file.content_type not in self.SUPPORTED_MIME_TYPES:
            raise ValueError("Unsupported file type")
        content = await file.read()
        if file.content_type == "application/pdf":
            return self._parse_pdf(content)
        return self._parse_docx(content)

    def _parse_pdf(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        return text.strip()

    def _parse_docx(self, content: bytes) -> str:
        document = Document(io.BytesIO(content))
        text = "\n".join(paragraph.text for paragraph in document.paragraphs)
        return text.strip()
