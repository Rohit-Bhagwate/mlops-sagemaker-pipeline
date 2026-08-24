import os
import json
import joblib
import pandas as pd


def model_fn(model_dir):
    model_path = os.path.join(model_dir, "model.joblib")
    return joblib.load(model_path)


def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        return pd.DataFrame([json.loads(request_body)])

    raise ValueError(f"Unsupported content type: {request_content_type}")


def predict_fn(input_data, model):
    return model.predict(input_data)


def output_fn(prediction, accept):
    if accept == "application/json":
        return {
            "predictions": prediction.tolist()
        }

    raise ValueError(f"Unsupported accept type: {accept}")