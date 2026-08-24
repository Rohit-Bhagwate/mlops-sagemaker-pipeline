import boto3

# ----------------------------
# Configuration
# ----------------------------

REGION = "ap-south-1"
PROFILE = "mlops-engineer"

ENDPOINT_CONFIG_NAME = "telecom-churn-endpoint-config-myversion"
ENDPOINT_NAME = "telecom-churn-endpoint"


# ----------------------------
# AWS Session
# ----------------------------

session = boto3.Session(
    profile_name=PROFILE,
    region_name=REGION
)

sagemaker = session.client("sagemaker")


# ----------------------------
# Create Endpoint
# ----------------------------

print("Creating SageMaker Endpoint...")
print("This can take several minutes.")

response = sagemaker.create_endpoint(
    EndpointName=ENDPOINT_NAME,
    EndpointConfigName=ENDPOINT_CONFIG_NAME
)

print("SageMaker Endpoint creation started.")
print("Endpoint ARN:", response["EndpointArn"])