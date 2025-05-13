# 📦 Pushover API Wrapper (AWS CDK - Python)

This project wraps the [Pushover](https://pushover.net/) API in an AWS Lambda function and exposes it via **Amazon API Gateway**. It's built with **AWS CDK (Python)** and demonstrates best practices including:

* ✅ Runtime JSON validation via API Gateway using **OpenAPI schema**
* ✅ SSM Parameter Store for securely storing secrets
* ✅ Lambda Layers for reusable logic (Pushover utils and Pydantic models)
* ✅ Modular testable code with `pytest` and `pydantic`
* ✅ Multi-stage deployment support using `--context stage=...`

---

## 🧰 Project Structure

```
.
├── app.py                       # CDK app entrypoint
├── cdk.json                     # CDK context + app config
├── requirements.txt             # CDK + runtime dependencies
├── requirements-dev.txt        # Dev + test dependencies
├── src/                         # Lambda handler entrypoint
│   └── handler.py
├── layer/                       # Lambda Layer root
│   └── python/                  # Python folder required by Lambda Layer structure
│       ├── pushover_model.py
│       ├── pushover_utils.py
│       └── requirements.txt     # Layer-specific dependencies (e.g. pydantic, requests)
├── build_layer.sh               # 🐳 Docker-based script to build layer for correct architecture
├── schemas/                     # JSON schema (optional, not currently used in CDK)
│   └── pushover_schema.json
├── pushover_api_wrapper/       
│   └── pushover_api_wrapper_stack.py
├── tests/                       # Unit tests
│   └── unit/
└── .vscode/                     # Shared VSCode settings (optional)
```

---

## 🐍 Getting Started

### 1. Set up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Install Lambda Layer Dependencies

```bash
cd layer/python
pip install -r requirements.txt -t .
````

---

## 🧱 Build Lambda Layer (Docker-safe for AWS Lambda x86\_64)

Since your local machine (e.g. M1/M2 Mac) may not match AWS Lambda’s runtime architecture, use Docker to build your layer dependencies correctly:

```bash
./build_layer.sh
```

This script:

* 🧹 Cleans existing dependencies in `layer/python/`
* 🐳 Installs Python packages using the `public.ecr.aws/sam/build-python3.12` image
* ✅ Ensures architecture compatibility with AWS Lambda (`linux/x86_64`)
* 🔍 Verifies that `pydantic_core/_pydantic_core.cpython-312-x86_64-linux-gnu.so` is present

### 4. Configure AWS Credentials

```bash
aws configure
```

Ensure `~/.aws/credentials` is set correctly. CDK uses these for deployments.

---

## 🚀 Deployment

### Bootstrap CDK (One-time setup per account/region)

```bash
cdk bootstrap
```

### Synthesize CloudFormation

```bash
cdk synth
```

### Deploy to AWS

```bash
cdk deploy --context stage=dev
```

You can change the stage (e.g., `--context stage=prod`) to deploy to different environments.

---

## ✅ Testing

```bash
pytest -vv tests
```

This runs both handler logic and model validation unit tests.

---

## 📘 Useful Commands

| Command         | Description                           |
| --------------- | ------------------------------------- |
| `cdk ls`        | List stacks                           |
| `cdk synth`     | Generate CF template                  |
| `cdk deploy`    | Deploy stack to AWS                   |
| `cdk destroy`   | Tear down stack from AWS              |
| `cdk diff`      | Show difference from deployed version |
| `cdk bootstrap` | Prepare environment for CDK usage     |

---

## 🔒 SSM Parameters Required

Before deploying, create the following parameters in **SSM Parameter Store**:

* `/PushoverToken` — your application token
* `/PushoverUser` — your user/group key

Mark both as **SecureString**.

---

## 🧪 Try It Out

Once deployed, use tools like `curl` or Postman:

```bash
curl -X POST https://<your-api>/prod/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from Lambda", "title": "PushOver API Test"}'
```

---



## ⚙️ Custom CDK Deploy Script

To simplify deployments and verify the deployed API is working, use the provided helper script:

```bash
./cdk_deploy.sh <stage>
```

For example:

```bash
./cdk_deploy.sh prod
```

This script:

* Deploys the CDK stack using the provided stage context.
* Extracts the deployed API Gateway URL from the CloudFormation outputs.
* Sends a test `POST /message` request to verify the deployment.
* Automatically sets:

  * **Title**: `CDK Deploy <stage>`
  * **Message**: `Shakedown successful at <timestamp>` (based on Singapore time)

---

### 📦 Prerequisites

Ensure you have the following CLI tools installed:

* **jq**: Used to format and send the JSON payload to the API.

Install it via Homebrew (macOS):

```bash
brew install jq
```

You can also verify installation:

```bash
jq --version
```

---

