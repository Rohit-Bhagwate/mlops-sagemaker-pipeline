import boto3
import os
from sagemaker.core.helper.session_helper import Session
from sagemaker.serve.model_builder import ModelBuilder, SourceCode
from sagemaker.core import image_uris


# --------------------------------------------------
# Configuration
# --------------------------------------------------

REGION = "ap-south-1"

ROLE = "arn:aws:iam::419022575435:role/telecom-churn-sagemaker-role"

MODEL_ARTIFACT = os.getenv("MODEL_ARTIFACT")

if not MODEL_ARTIFACT:
    raise RuntimeError(
        "MODEL_ARTIFACT environment variable is not set."
    )

print("Model artifact:", MODEL_ARTIFACT)

INSTANCE_TYPE = "ml.m5.large"


# --------------------------------------------------
# AWS session
# --------------------------------------------------

boto_session = boto3.Session(
    #profile_name="mlops-engineer",
    region_name=REGION
)

sagemaker_session = Session(
    boto_session=boto_session
)


# --------------------------------------------------
# Inference container
# --------------------------------------------------

image = image_uris.retrieve(
    framework="sklearn",
    region=REGION,
    version="1.4-2-py312",
    image_scope="inference",
    instance_type=INSTANCE_TYPE
)

print("Inference image:")
print(image)

source_code = SourceCode(
    source_dir="inference_code",
    entry_script="inference.py"
)

# --------------------------------------------------
# Build SageMaker Model
# --------------------------------------------------

model_builder = ModelBuilder(
    role_arn=ROLE,
    sagemaker_session=sagemaker_session,
    image_uri=image,
    s3_model_data_url=MODEL_ARTIFACT,
    source_code=source_code,
    instance_type=INSTANCE_TYPE
)

print("Building SageMaker Model...")

model = model_builder.build()

print("SageMaker Model created successfully.")
print(model)
