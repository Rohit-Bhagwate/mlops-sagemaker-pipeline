import boto3
import json
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

REGION = os.getenv("AWS_DEFAULT_REGION")
ENDPOINT_NAME = os.getenv(
    "ENDPOINT_NAME",
    "telecom-churn-endpoint"
)

TEST_INPUT_FILE = "training/test_input.json"


# --------------------------------------------------
# Validate Configuration
# --------------------------------------------------

if not REGION:
    raise RuntimeError(
        "AWS_DEFAULT_REGION environment variable is not set."
    )


# --------------------------------------------------
# Load Test Input
# --------------------------------------------------

print("Loading test input...")

with open(TEST_INPUT_FILE, "r") as file:
    test_data = json.load(file)

print("Test input loaded successfully.")


# --------------------------------------------------
# AWS Session
# --------------------------------------------------

print()
print("AWS Region:", REGION)

print("Creating AWS session using EC2 IAM role...")

session = boto3.Session(
    region_name=REGION
)

runtime = session.client("sagemaker-runtime")


# --------------------------------------------------
# Invoke SageMaker Endpoint
# --------------------------------------------------

print()
print("Invoking SageMaker Endpoint...")
print("Endpoint Name:", ENDPOINT_NAME)

response = runtime.invoke_endpoint(
    EndpointName=ENDPOINT_NAME,
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps(test_data)
)


# --------------------------------------------------
# Read Response
# --------------------------------------------------

result = response["Body"].read().decode("utf-8")


# --------------------------------------------------
# Display Prediction
# --------------------------------------------------

print()
print("SageMaker Endpoint Response:")
print(result)


# --------------------------------------------------
# Validate Response
# --------------------------------------------------

prediction = json.loads(result)

if "predictions" not in prediction:
    raise RuntimeError(
        "Endpoint response does not contain 'predictions'."
    )

print()
print("Prediction:")
print(prediction["predictions"])

print()
print("SageMaker Endpoint test completed successfully.")