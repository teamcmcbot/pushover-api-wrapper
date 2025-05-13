import json
from dotenv import load_dotenv
from src.handler import lambda_handler
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

# Load .env values
load_dotenv()


def test_lambda_handler_sends_pushover_message_with_env_token():
    sgt_time = datetime.now(timezone.utc) + timedelta(hours=8)
    formatted_time = sgt_time.strftime("%Y-%m-%d %H:%M:%S")

    event = {
        "body": json.dumps(
            {
                "message": f"Test from unit test at {formatted_time} SGT",
                "title": "Lambda Test",
            }
        )
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["status"] == 1
    assert "request" in body


def test_lambda_handler_missing_body_returns_400():
    event = {}  # missing "body"
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "error" in body
    assert "Invalid JSON" in body["error"]


def test_lambda_handler_invalid_json_returns_400():
    event = {"body": "{invalid:json"}  # invalid JSON
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "error" in body
    assert "Invalid JSON" in body["error"]


@patch("pushover_utils.requests.post")
def test_lambda_handler_pushover_500_returns_500(mock_post):
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {
        "error": "Failed to send Pushover message"
    }

    event = {"body": json.dumps({"message": "Fail test"})}

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "error" in body
    assert "Failed to send Pushover message" in body["error"]


@patch("pushover_utils.requests.post", side_effect=Exception("Network error"))
def test_lambda_handler_post_exception_returns_500(mock_post):
    event = {"body": json.dumps({"message": "Exception test"})}
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 500
    assert "error" in body
    assert "Network error" in body["error"]
