import aws_cdk as core
import aws_cdk.assertions as assertions

from pushover_api_wrapper.pushover_api_wrapper_stack import PushoverApiWrapperStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pushover_api_wrapper/pushover_api_wrapper_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PushoverApiWrapperStack(app, "pushover-api-wrapper")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
