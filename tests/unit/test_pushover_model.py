import pytest
from pydantic import ValidationError
from pushover_model import PushoverRequest


def test_valid_minimal_payload():
    data = {"message": "Hello!"}
    model = PushoverRequest(**data)
    assert model.message == "Hello!"


def test_invalid_priority_value():
    data = {"message": "Urgent!", "priority": 99}  # Invalid, not in -2 to 2
    with pytest.raises(ValidationError) as exc_info:
        PushoverRequest(**data)

    assert "priority" in str(exc_info.value)


def test_invalid_html_type():
    data = {"message": "HTML test", "html": "yes"}  # Invalid, must be 0 or 1
    with pytest.raises(ValidationError) as exc_info:
        PushoverRequest(**data)

    assert "html" in str(exc_info.value)


def test_missing_required_message():
    data = {"title": "Oops"}
    with pytest.raises(ValidationError) as exc_info:
        PushoverRequest(**data)

    assert "message" in str(exc_info.value)
