import pytest

from deepClassifier.pipeline import stage_01_data_ingestion
from deepClassifier.pipeline import stage_02_prepare_base_model


def test_base_model():
    stage_01_data_ingestion.main()
    stage_02_prepare_base_model.main()
    assert True
