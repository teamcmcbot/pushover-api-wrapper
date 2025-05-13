#!/usr/bin/env python3
import os

import aws_cdk as cdk
from pushover_api_wrapper.pushover_api_wrapper_stack import PushoverApiWrapperStack

app = cdk.App()

# ✅ Use the current CLI-configured account and region for deployment
PushoverApiWrapperStack(
    app,
    "PushoverApiWrapperStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

app.synth()
