import numpy as np
import pytest
from spotdesirability.functions.zdt import zdt1

def test_zdt1_shape_and_type():
    x = np.random.rand(30)
    result = zdt1(x)
    assert isinstance(result, np.ndarray)
    assert result.shape == (2,)

def test_zdt1_known_input():
    x = np.zeros(30)
    expected_f1 = 0.0
    g = 1 + 9 * np.sum(x[1:]) / (len(x) - 1)
    expected_f2 = g * (1 - np.sqrt(expected_f1 / g))
    result = zdt1(x)
    np.testing.assert_allclose(result, [expected_f1, expected_f2])

def test_zdt1_all_ones():
    x = np.ones(30)
    expected_f1 = 1.0
    g = 1 + 9 * np.sum(x[1:]) / (len(x) - 1)
    expected_f2 = g * (1 - np.sqrt(expected_f1 / g))
    result = zdt1(x)
    np.testing.assert_allclose(result, [expected_f1, expected_f2])

def test_zdt1_invalid_dimension():
    x = np.random.rand(10)
    with pytest.raises(IndexError):
        zdt1(x)

def test_zdt1_values_between_0_and_1():
    x = np.linspace(0, 1, 30)
    result = zdt1(x)
    assert 0 <= result[0] <= 1
    assert result[1] >= 0