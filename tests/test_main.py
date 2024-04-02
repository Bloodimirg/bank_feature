import pytest
from src.main import open_json_file, filter_vacancies, mask_operation_from, mask_operation_to


@pytest.fixture
def test_data():
    return [{'state': 'EXECUTED'}, {'state': 'EXECUTED'}, {'state': 'CANCELLED'}]


def test_open_json_file(test_data):
    """Проверка функции open_json_file()"""
    data = open_json_file('data/operations.json')
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)
        assert len(item) != 1


def test_filter_vacancies(test_data):
    assert len(filter_vacancies(test_data)) == 2


def test_mask_operation(test_data):
    assert mask_operation_from(test_data[0]) == "Без номера ->"
    assert mask_operation_to(test_data[0]) == "Без номера"


@pytest.mark.parametrize("operation_to, expected_result", [
    ({'to': '1234567890123456'}, ' 1234 56** **** 3456')
])
def test_mask_operation_to(operation_to, expected_result):
    assert mask_operation_to(operation_to) == expected_result
