#!/bin/bash

set -e

STAGE=$1

if [ -z "$STAGE" ]; then
  echo "❌ Please provide a stage name: ./cdk_deploy.sh <stage>"
  exit 1
fi

echo "🚀 Deploying CDK stack with stage: $STAGE..."
echo "--------------------------------------------"

# Run CDK deploy and capture the output
DEPLOY_OUTPUT=$(cdk deploy --context stage=$STAGE --require-approval never 2>&1 | tee /dev/tty)

# Try to extract API URL from known output line
API_URL=$(echo "$DEPLOY_OUTPUT" | grep "PushoverApiWrapperStack.PushoverApiEndpoint =" | awk -F '= ' '{print $2}' | xargs)

if [[ -z "$API_URL" ]]; then
  echo "❌ Deployment succeeded but API URL not found in output."
  exit 1
fi

echo ""
echo "✅ Found API URL: $API_URL"
echo ""
echo "📡 Sending test request to $API_URL/message..."
echo "--------------------------------------------"

# Format current time in SGT
TIMESTAMP=$(TZ=Asia/Singapore date '+%Y-%m-%d %H:%M:%S')

# Construct dynamic JSON payload
JSON_PAYLOAD=$(jq -n \
  --arg title "CDK Deploy ${STAGE}" \
  --arg msg "Shakedown successful at ${TIMESTAMP} SGT" \
  '{title: $title, message: $msg, priority: 1}')

# Call the deployed API endpoint
RESPONSE=$(curl -s -w "\nHTTP Status: %{http_code}\n" -X POST "${API_URL}message" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

echo "$RESPONSE"
