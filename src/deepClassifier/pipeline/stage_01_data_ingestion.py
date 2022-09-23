from deepClassifier.config import ConfigurationManager
from deepClassifier.components import DataIngestion
from deepClassifier import logger
from deepClassifier.exception import CustomException
import sys


STAGE_NAME = "Data Ingestion stage"


def main():
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_file()
    data_ingestion.unzip_and_clean()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\n")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys) from e
