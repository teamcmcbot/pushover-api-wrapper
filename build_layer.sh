#!/bin/bash

set -e

LAYER_DIR="layer/python"
TARGET_SO="pydantic_core/_pydantic_core.cpython-312-x86_64-linux-gnu.so"

echo "🧹 Cleaning previous layer build in $LAYER_DIR..."
find "$LAYER_DIR" -mindepth 1 ! -name 'pushover_model.py' ! -name 'pushover_utils.py' ! -name 'requirements.txt' -exec rm -rf {} +

echo "🐳 Installing dependencies using AWS Lambda compatible Docker image (linux/amd64)..."
docker run --rm \
  --platform linux/amd64 \
  -v "$PWD/$LAYER_DIR":/var/task \
  -w /var/task \
  public.ecr.aws/sam/build-python3.12 \
  pip install -r requirements.txt -t .

echo "🔍 Verifying critical shared object file..."
if [[ -f "$LAYER_DIR/$TARGET_SO" ]]; then
  echo "✅ Verified: $TARGET_SO exists."
else
  echo "❌ Error: Expected .so file for pydantic_core not found!"
  echo "   Expected: $TARGET_SO"
  exit 1
fi

echo "✅ Build complete."
