import boto3
import sagemaker
import logging
import os

from sagemaker.train import ModelTrainer
from sagemaker.train.configs import SourceCode, Compute, InputData
from sagemaker.core.helper.session_helper import Session
from sagemaker.core import image_uris


# ============================================================
# DEBUG LOGGING
# ============================================================

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ============================================================
# CONFIGURATION
# ============================================================

#PROFILE_NAME = "mlops-engineer"
REGION = "ap-south-1"

ROLE_ARN = (
    "arn:aws:iam::419022575435:role/"
    "telecom-churn-sagemaker-role"
)

TRAINING_DATA = (
    "s3://rohit-telecom-churn-data-2026/"
    "processed/customer_clean.csv"
)

FRAMEWORK_VERSION = "1.4-2"
INSTANCE_TYPE = "ml.m5.large"

ENTRY_POINT = "train.py"
#SOURCE_DIR = "sagemaker_source"
SOURCE_DIR = "training/sagemaker_source"


# ============================================================
# FIX FOR WINDOWS CRLF IN SDK-GENERATED sm_train.sh
# ============================================================
#
# SageMaker SDK ModelTrainer generates sm_train.sh using:
#
#     open(..., "w")
#
# On Windows this produces CRLF line endings.
# SageMaker training containers run Linux/bash and require LF.
#
# We keep the ModelTrainer architecture exactly the same and
# normalize ONLY the generated sm_train.sh before the SDK
# packages/uploads the sm_drivers directory.
# ============================================================

_original_prepare_train_script = ModelTrainer._prepare_train_script


def _prepare_train_script_lf(
    self,
    tmp_dir,
    source_code,
    distributed=None
):
    # Let the official SageMaker SDK generate the script first.
    _original_prepare_train_script(
        self,
        tmp_dir,
        source_code,
        distributed
    )

    # The SDK-generated training driver.
    train_script_path = os.path.join(
        tmp_dir.name,
        "sm_train.sh"
    )

    # Convert Windows CRLF/CR to Unix LF.
    with open(train_script_path, "rb") as f:
        content = f.read()

    content = content.replace(b"\r\n", b"\n")
    content = content.replace(b"\r", b"\n")

    with open(train_script_path, "wb") as f:
        f.write(content)

    print(
        "Fixed SDK-generated sm_train.sh line endings: LF"
    )


# Apply the patch to this Python process only.
ModelTrainer._prepare_train_script = _prepare_train_script_lf


# ============================================================
# 1. CREATE BOTO3 SESSION
# ============================================================

boto_session = boto3.Session(
    #profile_name=PROFILE_NAME,
    region_name=REGION
)

print("AWS Region:", boto_session.region_name)
#print("AWS Profile:", PROFILE_NAME)


# ============================================================
# 2. CREATE SAGEMAKER V3 SESSION
# ============================================================

sagemaker_session = Session(
    boto_session=boto_session
)

print("SageMaker v3 Session created successfully")


# ============================================================
# 3. GET SCIKIT-LEARN TRAINING IMAGE
# ============================================================

training_image = image_uris.retrieve(
    framework="sklearn",
    region=REGION,
    version=FRAMEWORK_VERSION,
    py_version="py3",
    instance_type=INSTANCE_TYPE
)

print("Training image:", training_image)


# ============================================================
# 4. DEFINE TRAINING SOURCE CODE
# ============================================================

source_code = SourceCode(
    source_dir=SOURCE_DIR,
    entry_script=ENTRY_POINT
)

print("Training source configured successfully")


# ============================================================
# 5. DEFINE COMPUTE
# ============================================================

compute = Compute(
    instance_type=INSTANCE_TYPE,
    instance_count=1
)

print("Compute configured successfully")


# ============================================================
# 6. CREATE SAGEMAKER V3 MODEL TRAINER
# ============================================================

trainer = ModelTrainer(
    training_image=training_image,
    source_code=source_code,
    compute=compute,
    role=ROLE_ARN,
    sagemaker_session=sagemaker_session,
    base_job_name="telecom-churn"
)

print("ModelTrainer created successfully")


# ============================================================
# 7. DEFINE TRAINING DATA
# ============================================================

training_data = InputData(
    channel_name="train",
    data_source=TRAINING_DATA,
    content_type="text/csv"
)

print("S3 training data configured successfully")


# ============================================================
# 8. START SAGEMAKER TRAINING JOB
# ============================================================

print("Starting SageMaker training job...")

trainer.train(
    input_data_config=[training_data],
    wait=True,
    logs=False
)


# ============================================================
# 9. TRAINING COMPLETE
# ============================================================

print("Training job completed successfully!")

if trainer._latest_training_job is not None:
    print("Training job details:")
    print(trainer._latest_training_job)
