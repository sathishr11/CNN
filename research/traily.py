from dotenv import load_dotenv
import mlflow
import os
from mlflow.tracking.client import MlflowClient
 


load_dotenv()

mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
client = MlflowClient()

model_name = "VGGmodel16"

print(client.get_latest_versions(model_name, stages=['Production']))