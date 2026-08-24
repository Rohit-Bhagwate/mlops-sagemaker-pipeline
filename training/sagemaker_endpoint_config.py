import boto3

# ----------------------------
# Configuration
# ----------------------------

REGION = "ap-south-1"
PROFILE = "mlops-engineer"

MODEL_NAME = "model-943a0204"
ENDPOINT_CONFIG_NAME = "telecom-churn-endpoint-config-myversion"

INSTANCE_TYPE = "ml.m5.large"
INITIAL_INSTANCE_COUNT = 1


# ----------------------------
# AWS Session
# ----------------------------

session = boto3.Session(
    profile_name=PROFILE,
    region_name=REGION
)

sagemaker = session.client("sagemaker")


# ----------------------------
# Create Endpoint Configuration
# ----------------------------

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

print("Endpoint Configuration created successfully.")
print("Name:", response["EndpointConfigArn"])