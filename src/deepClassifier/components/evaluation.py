from deepClassifier.entity.config_entity import EvaluationConfig
import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from deepClassifier.utils import save_json
import time
from mlflow.tracking.client import MlflowClient
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )


    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)


    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)

    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)

    @staticmethod
    def _wait_until_ready(model_name, model_version):
        client = MlflowClient()
        for _ in range(10):
            model_version_details = client.get_model_version(
            name=model_name,
            version=model_version,
            )
            status = ModelVersionStatus.from_string(model_version_details.status)
            print("Model status: %s" % ModelVersionStatus.to_string(status))
            if status == ModelVersionStatus.READY:
                break
            time.sleep(1)

    def log_into_mlflow(self):
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        with mlflow.start_run() as run:
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics(
                {"loss": self.score[0], "accuracy": self.score[1]}
            )
            # Model registry does not work with file store
            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.keras.log_model(self.model, "model", registered_model_name="DogCatClassifier")
                model_uri = "runs:/{}/model".format(run.info.run_id)
                model_details = mlflow.register_model(model_uri, "DogCatClassifier")
                self._wait_until_ready(model_details.name, model_details.version)
                client = MlflowClient()
                client.update_model_version(
                    name=model_details.name,
                    version=model_details.version,
                    description="VGG16 model"
                    )
            else:
                mlflow.keras.log_model(self.model, "model")
