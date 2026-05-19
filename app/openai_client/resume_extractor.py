from __future__ import annotations

from collections.abc import Awaitable, Callable

from openai import AsyncOpenAI
from pydantic import TypeAdapter
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import get_settings
from app.dtos.resume import ResumeStructuredDataDTO

settings = get_settings()


class RateLimiter:
    def __init__(self, max_per_minute: int) -> None:
        self._max_per_minute = max_per_minute
        self._calls = 0

    async def check(self) -> None:
        self._calls += 1
        if self._calls > self._max_per_minute:
            raise RuntimeError("OpenAI rate limit exceeded in process limiter")


class ResumeExtractor:
    def __init__(self, client: AsyncOpenAI, rate_limiter: RateLimiter) -> None:
        self._client = client
        self._rate_limiter = rate_limiter
        self._adapter = TypeAdapter(ResumeStructuredDataDTO)

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=6),
        retry=retry_if_exception_type(Exception),
    )
    async def extract(self, raw_text: str) -> ResumeStructuredDataDTO:
        await self._rate_limiter.check()
        response = await self._client.responses.parse(
            model=settings.openai_model,
            input=[
                {
                    "role": "system",
                    "content": "Extract resume data into the requested JSON schema.",
                },
                {"role": "user", "content": raw_text[:25000]},
            ],
            text_format=ResumeStructuredDataDTO,
        )
        return self._adapter.validate_python(response.output_parsed.model_dump())


def get_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key)


def get_rate_limiter() -> RateLimiter:
    return RateLimiter(max_per_minute=settings.openai_requests_per_minute)
