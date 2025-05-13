import json
from pushover_model import PushoverRequest
from pydantic import ValidationError
import logging
import pushover_utils  # from Lambda layer

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    headers = {"Content-Type": "application/json"}

    try:
        body = json.loads(event.get("body", ""))
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON: %s", e)
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": f"Invalid JSON: {str(e)}"}),
        }

    try:
        request = PushoverRequest(**body)
    except ValidationError as e:
        logger.error("Validation failed: %s", e)
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": f"Invalid input: {str(e)}"}),
        }

    try:
        status_code, response_body = pushover_utils.send_pushover_message(request)
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": json.dumps(response_body),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)}),
        }
