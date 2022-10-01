import pytest

from deepClassifier.pipeline import stage_01_data_ingestion
from deepClassifier.pipeline import stage_02_prepare_base_model
from deepClassifier.pipeline import stage_03_training


def test_training():
    stage_01_data_ingestion.main()
    stage_02_prepare_base_model.main()
    stage_03_training.main()
    assert True
