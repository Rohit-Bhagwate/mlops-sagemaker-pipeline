import boto3
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

REGION = os.getenv("AWS_DEFAULT_REGION")

MODEL_NAME = os.getenv("MODEL_NAME")

INSTANCE_TYPE = "ml.m5.large"
INITIAL_INSTANCE_COUNT = 1


# --------------------------------------------------
# Validate Required Values
# --------------------------------------------------

if not REGION:
    raise RuntimeError(
        "AWS_DEFAULT_REGION environment variable is not set."
    )

if not MODEL_NAME:
    raise RuntimeError(
        "MODEL_NAME environment variable is not set."
    )


# --------------------------------------------------
# Generate Endpoint Configuration Name
# --------------------------------------------------

ENDPOINT_CONFIG_NAME = (
    f"telecom-churn-endpoint-config-{MODEL_NAME}"
)


# --------------------------------------------------
# AWS Session
# --------------------------------------------------

print("AWS Region:", REGION)

print("Creating AWS session using EC2 IAM role...")

session = boto3.Session(
    region_name=REGION
)

sagemaker = session.client("sagemaker")


# --------------------------------------------------
# Display Configuration
# --------------------------------------------------

print("Model Name:", MODEL_NAME)

print("Endpoint Configuration Name:")
print(ENDPOINT_CONFIG_NAME)

print("Instance Type:", INSTANCE_TYPE)

print("Initial Instance Count:", INITIAL_INSTANCE_COUNT)


# --------------------------------------------------
# Create Endpoint Configuration
# --------------------------------------------------

print()
print("Creating SageMaker Endpoint Configuration...")

response = sagemaker.create_endpoint_config(
    EndpointConfigName=ENDPOINT_CONFIG_NAME,

    ProductionVariants=[
        {
            "VariantName": "AllTraffic",

            "ModelName": MODEL_NAME,

            "InitialInstanceCount": INITIAL_INSTANCE_COUNT,

            "InstanceType": INSTANCE_TYPE,

            "InitialVariantWeight": 1.0
        }
    ]
)


# --------------------------------------------------
# Save Endpoint Configuration Name
# --------------------------------------------------

with open("endpoint_config_name.txt", "w") as file:
    file.write(ENDPOINT_CONFIG_NAME)


# --------------------------------------------------
# Success
# --------------------------------------------------

print()
print("SageMaker Endpoint Configuration created successfully.")

print("Endpoint Configuration ARN:")
print(response["EndpointConfigArn"])

print()
print("Endpoint Configuration Name:")
print(ENDPOINT_CONFIG_NAME)

print()
print("Endpoint configuration name saved to:")
print("endpoint_config_name.txt")
