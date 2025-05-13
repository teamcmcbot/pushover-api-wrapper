from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct
import json
from pathlib import Path


class PushoverApiWrapperStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ✅ Get stage name from context (default to 'dev')
        stage_name = self.node.try_get_context("stage") or "dev"

        # Create the Lambda Layer (code from layer/)
        pushover_layer = _lambda.LayerVersion(
            self,
            "PushoverUtilsLayer",
            code=_lambda.Code.from_asset("layer"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="Pushover utils and Pydantic model",
            removal_policy=None,  # optional: you can set to DESTROY for dev
        )

        # Lambda Function definition (attach the layer here)
        lambda_function = _lambda.Function(
            self,
            "PushoverLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("src"),
            log_retention=logs.RetentionDays.ONE_WEEK,
            layers=[pushover_layer],
        )

        # IAM permissions to read SSM parameters at runtime
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/PushoverToken",
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/PushoverUser",
                ],
            )
        )

        # API Gateway setup (disable proxy to manually manage resources)
        api = apigw.RestApi(
            self,
            "PushoverApi",
            deploy_options=apigw.StageOptions(stage_name=stage_name),
        )

        # Load JSON Schema for validation
        schema_path = Path(__file__).parent.parent / "schemas" / "pushover_schema.json"
        with schema_path.open() as f:
            pushover_schema = json.load(f)

        request_model = apigw.Model(
            self,
            "PushoverRequestModel",
            rest_api=api,
            content_type="application/json",
            schema=apigw.JsonSchema.from_dict(pushover_schema),
        )

        # Define POST /message endpoint
        message_resource = api.root.add_resource("message")
        message_resource.add_method(
            "POST",
            apigw.LambdaIntegration(lambda_function),
            request_models={"application/json": request_model},
            request_validator_options=apigw.RequestValidatorOptions(
                validate_request_body=True
            ),
        )

        # Optional: output the API URL
        self.api_url_output = api.url
