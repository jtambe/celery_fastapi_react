import pytest
from unittest.mock import patch
from celery_tasks.celery_task import process

@patch("celery_tasks.celery_task.sleep")
def test_process_success(mock_sleep):
    result = process(3, 4)
    assert result == 25

@patch("celery_tasks.celery_task.sleep")
def test_process_failure(mock_sleep):
    with pytest.raises(ValueError, match="Simulated task failure"):
        process(-1, 4)