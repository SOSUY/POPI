import pytest
from src.decorators import my_function

@pytest.fixture
def b():
    return 2

def test_my_function(b):
    assert my_function(1, b) == 3
    assert my_function(2, b) == 4
    assert my_function(3, b) == 5
    assert my_function(4, b) == 6
    assert my_function(5, b) == 7
