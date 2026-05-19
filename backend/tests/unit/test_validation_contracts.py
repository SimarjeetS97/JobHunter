import pytest
from pydantic import BaseModel, EmailStr, Field, ValidationError, constr


class CandidateCreateDTO(BaseModel):
    email: EmailStr
    name: constr(min_length=2, max_length=120)
    years_experience: int = Field(ge=0, le=80)


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "bad", "name": "Valid Name", "years_experience": 2},
        {"email": "good@example.com", "name": "x", "years_experience": 2},
        {"email": "good@example.com", "name": "Valid Name", "years_experience": -1},
    ],
)
def test_candidate_create_dto_rejects_invalid_input(payload):
    with pytest.raises(ValidationError):
        CandidateCreateDTO(**payload)


def test_candidate_create_dto_accepts_valid_input():
    dto = CandidateCreateDTO(email="good@example.com", name="Valid Name", years_experience=5)
    assert dto.years_experience == 5
