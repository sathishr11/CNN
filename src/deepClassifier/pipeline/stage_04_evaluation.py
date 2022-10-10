from deepClassifier.config import ConfigurationManager
from deepClassifier.components import Evaluation
from deepClassifier import logger
from deepClassifier.exception import CustomException
import sys


STAGE_NAME = "Evaluation"


def main():
    config = ConfigurationManager()
    val_config = config.get_validation_config()
    evaluation = Evaluation(val_config)
    evaluation.evaluation()
    evaluation.save_score()
    evaluation.log_into_mlflow()


if __name__ == "__main__":
    try:
        logger.info("*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys) from e
