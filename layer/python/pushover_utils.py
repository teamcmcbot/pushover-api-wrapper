import json
import logging
import requests
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client("ssm")


def get_ssm_parameter(name: str) -> str:
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]


def send_pushover_message(request):
    try:
        token = request.token or get_ssm_parameter("PushoverToken")
        user = request.user or get_ssm_parameter("PushoverUser")
    except (BotoCoreError, ClientError) as e:
        logger.error("SSM fetch failed: %s", str(e))
        raise Exception(f"SSM fetch failed: {str(e)}")

    payload = {"token": token, "user": user, "message": request.message}

    for field in request.__class__.model_fields:
        value = getattr(request, field)
        if value is not None and field not in ["token", "user", "message"]:
            payload[field] = value

    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json", data=payload
        )
        logger.info("Pushover response: %s", response.status_code)
        return response.status_code, response.json()
    except Exception as e:
        logger.error("HTTP error when sending Pushover message: %s", str(e))
        raise
