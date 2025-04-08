from unittest.mock import Mock

from src.utils import json_transactions


def test_json_transactions(test_json):
    mock_way = Mock(return_value=r"../POPI-main/data/operations.jso")
    test_way = r"../POPI-main/data/operations.json"
    not_correct_way = r"../POPI-main/tests/test_operations.json"
    assert json_transactions(mock_way) == []
    assert json_transactions(test_way) == test_json
    assert json_transactions(not_correct_way) == []
