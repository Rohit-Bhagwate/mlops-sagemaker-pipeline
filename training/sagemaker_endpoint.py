import boto3
import os


# --------------------------------------------------
# Configuration
# --------------------------------------------------

REGION = os.getenv("AWS_DEFAULT_REGION")

ENDPOINT_CONFIG_NAME = os.getenv("ENDPOINT_CONFIG_NAME")

ENDPOINT_NAME = "telecom-churn-endpoint"


# --------------------------------------------------
# Validate Required Values
# --------------------------------------------------

if not REGION:
    raise RuntimeError(
        "AWS_DEFAULT_REGION environment variable is not set."
    )

if not ENDPOINT_CONFIG_NAME:
    raise RuntimeError(
        "ENDPOINT_CONFIG_NAME environment variable is not set."
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

print()
print("Endpoint Name:")
print(ENDPOINT_NAME)

print()
print("Endpoint Configuration Name:")
print(ENDPOINT_CONFIG_NAME)


# --------------------------------------------------
# Check Whether Endpoint Already Exists
# --------------------------------------------------

print()
print("Checking whether SageMaker Endpoint already exists...")

endpoint_exists = False

try:
    sagemaker.describe_endpoint(
        EndpointName=ENDPOINT_NAME
    )

    endpoint_exists = True

    print("Endpoint already exists.")

except sagemaker.exceptions.ClientError as error:

    error_code = error.response["Error"]["Code"]

    if error_code == "ValidationException":
        print("Endpoint does not exist.")
    else:
        raise


# --------------------------------------------------
# Create or Update Endpoint
# --------------------------------------------------

if endpoint_exists:

    print()
    print("Updating existing SageMaker Endpoint...")
    print("This can take several minutes.")

    response = sagemaker.update_endpoint(
        EndpointName=ENDPOINT_NAME,
        EndpointConfigName=ENDPOINT_CONFIG_NAME
    )

    print()
    print("SageMaker Endpoint update started.")

else:

    print()
    print("Creating SageMaker Endpoint...")
    print("This can take several minutes.")

    response = sagemaker.create_endpoint(
        EndpointName=ENDPOINT_NAME,
        EndpointConfigName=ENDPOINT_CONFIG_NAME
    )

    print()
    print("SageMaker Endpoint creation started.")


# --------------------------------------------------
# Save Endpoint Name
# --------------------------------------------------

with open("endpoint_name.txt", "w") as file:
    file.write(ENDPOINT_NAME)


# --------------------------------------------------
# Display Result
# --------------------------------------------------

print()
print("Endpoint ARN:")
print(response["EndpointArn"])

print()
print("Endpoint Name:")
print(ENDPOINT_NAME)

print()
print("Endpoint name saved to:")
print("endpoint_name.txt")