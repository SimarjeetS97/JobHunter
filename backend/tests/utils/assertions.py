from collections.abc import Mapping


def assert_validation_error(payload: Mapping[str, object], *, field: str) -> None:
    detail = payload.get("detail")
    assert isinstance(detail, list), "Expected FastAPI validation detail list"
    assert any(field in str(entry.get("loc", [])) for entry in detail if isinstance(entry, dict))


def assert_error_shape(payload: Mapping[str, object]) -> None:
    assert "error" in payload or "detail" in payload
