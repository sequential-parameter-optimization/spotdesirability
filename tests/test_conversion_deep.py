import pytest
import numpy as np
from spotdesirability.functions.rsm import conversion_pred

def test_conversion_pred_origin():
    # Test at origin (0,0,0) - should return intercept
    x = [0.0, 0.0, 0.0]
    result = conversion_pred(x)
    assert pytest.approx(result) == 81.09

def test_conversion_pred_linearity():
    # Test linear terms separately
    # x1 only
    assert pytest.approx(conversion_pred([1.0, 0.0, 0.0])) == 81.09 + 1.0284 - 1.8366
    # x2 only
    assert pytest.approx(conversion_pred([0.0, 1.0, 0.0])) == 81.09 + 4.043 + 2.9382
    # x3 only
    assert pytest.approx(conversion_pred([0.0, 0.0, 1.0])) == 81.09 + 6.2037 - 5.1915

def test_conversion_pred_interactions():
    # Test interaction terms
    # x1 * x2
    expected = 81.09 + 1.0284 + 4.043 - 1.8366 + 2.9382 + 2.2150
    assert pytest.approx(conversion_pred([1.0, 1.0, 0.0])) == expected
    
    # x1 * x3
    expected = 81.09 + 1.0284 + 6.2037 - 1.8366 - 5.1915 + 11.375
    assert pytest.approx(conversion_pred([1.0, 0.0, 1.0])) == expected
    
    # x2 * x3
    expected = 81.09 + 4.043 + 6.2037 + 2.9382 - 5.1915 - 3.875
    assert pytest.approx(conversion_pred([0.0, 1.0, 1.0])) == expected

def test_conversion_pred_numpy_types():
    # Test different numpy dtypes
    x_float32 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    x_float64 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert pytest.approx(conversion_pred(x_float32)) == conversion_pred(x_float64)

@pytest.mark.parametrize("x1,x2,x3", [
    (1.682, 0, 0),
    (-1.682, 0, 0),
    (0, 1.682, 0),
    (0, -1.682, 0),
    (0, 0, 1.682),
    (0, 0, -1.682),
])
def test_conversion_pred_boundaries(x1, x2, x3):
    # Test at design space boundaries (alpha = 1.682)
    x = [x1, x2, x3]
    result = conversion_pred(x)
    assert isinstance(result, (float, np.float64))

def test_conversion_pred_invalid_types():
    with pytest.raises(ValueError, match="Input x must be a list or numpy array."):
        conversion_pred({"x1": 1.0, "x2": 2.0, "x3": 3.0})
    with pytest.raises(ValueError, match="Input x must be a list or numpy array."):
        conversion_pred(1.0)

def test_conversion_pred_invalid_shapes():
    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        conversion_pred(np.array([[1, 2, 3]])) # 2D array
    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        conversion_pred([1, 2, 3, 4])
