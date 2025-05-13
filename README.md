
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


---

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
├── requirements-dev.txt         # Dev + test dependencies
├── src/                         # Lambda handler entrypoint
│   └── handler.py
├── layer/                       # Lambda Layer
│   ├── pushover_model.py
│   └── pushover_utils.py
├── schemas/                     # JSON schema for request validation
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

### 3. Configure AWS Credentials

```bash
aws configure
```

Ensure `~/.aws/credentials` is set correctly. CDK uses these for deployments.

---

## 🚀 Deployment

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
  -d '{"message": "Hello from Lambda"}'
```

---

