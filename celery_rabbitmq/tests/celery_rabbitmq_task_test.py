import pytest
from unittest.mock import patch
from celery_rabbitmq.celery_rabbitmq_task import process2

@patch("celery_rabbitmq.celery_rabbitmq_task.sleep", return_value=None)
def test_process2_success(mock_sleep):
    result = process2.run(2, 3)
    assert result == 5

@patch("celery_rabbitmq.celery_rabbitmq_task.sleep", return_value=None)
def test_process2_failure(mock_sleep):
    with pytest.raises(ValueError, match="Simulated task failure"):
        process2.run(-1, 3)