import pytest
import numpy as np
from spotdesirability.functions.rsm import conversion_pred
from spotdesirability.functions.rsm import activity_pred
from unittest.mock import Mock
from spotdesirability.functions.rsm import rsm_opt, conversion_pred, activity_pred


def test_conversion_pred_valid_input_list():
    x = [1.0, 2.0, 3.0]
    result = conversion_pred(x)
    expected = (
        81.09
        + 1.0284 * x[0]
        + 4.043 * x[1]
        + 6.2037 * x[2]
        - 1.8366 * x[0] ** 2
        + 2.9382 * x[1] ** 2
        - 5.1915 * x[2] ** 2
        + 2.2150 * x[0] * x[1]
        + 11.375 * x[0] * x[2]
        - 3.875 * x[1] * x[2]
    )
    assert pytest.approx(result, rel=1e-6) == expected


def test_conversion_pred_valid_input_numpy_array():
    x = np.array([1.0, 2.0, 3.0])
    result = conversion_pred(x)
    expected = (
        81.09
        + 1.0284 * x[0]
        + 4.043 * x[1]
        + 6.2037 * x[2]
        - 1.8366 * x[0] ** 2
        + 2.9382 * x[1] ** 2
        - 5.1915 * x[2] ** 2
        + 2.2150 * x[0] * x[1]
        + 11.375 * x[0] * x[2]
        - 3.875 * x[1] * x[2]
    )
    assert pytest.approx(result, rel=1e-6) == expected


def test_conversion_pred_invalid_input_not_list_or_array():
    with pytest.raises(ValueError, match="Input x must be a list or numpy array."):
        conversion_pred("invalid_input")


def test_conversion_pred_invalid_input_wrong_shape():
    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        conversion_pred([1.0, 2.0])  # Less than 3 elements

    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        conversion_pred([1.0, 2.0, 3.0, 4.0])  # More than 3 elements
        def test_activity_pred_valid_input_list():
            x = [1.0, 2.0, 3.0]
            result = activity_pred(x)
            expected = (
                59.85
                + 3.583 * x[0]
                + 0.2546 * x[1]
                + 2.2298 * x[2]
                + 0.83479 * x[0] ** 2
                + 0.07484 * x[1] ** 2
                + 0.05716 * x[2] ** 2
                - 0.3875 * x[0] * x[1]
                - 0.375 * x[0] * x[2]
                + 0.3125 * x[1] * x[2]
            )
            assert pytest.approx(result, rel=1e-6) == expected


def test_activity_pred_valid_input_numpy_array():
    x = np.array([1.0, 2.0, 3.0])
    result = activity_pred(x)
    expected = (
        59.85
        + 3.583 * x[0]
        + 0.2546 * x[1]
        + 2.2298 * x[2]
        + 0.83479 * x[0] ** 2
        + 0.07484 * x[1] ** 2
        + 0.05716 * x[2] ** 2
        - 0.3875 * x[0] * x[1]
        - 0.375 * x[0] * x[2]
        + 0.3125 * x[1] * x[2]
    )
    assert pytest.approx(result, rel=1e-6) == expected


def test_activity_pred_invalid_input_not_list_or_array():
    with pytest.raises(ValueError, match="Input x must be a list or numpy array."):
        activity_pred("invalid_input")


def test_activity_pred_invalid_input_wrong_shape():
    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        activity_pred([1.0, 2.0])  # Less than 3 elements

    with pytest.raises(ValueError, match="Input x must be a 3-element vector."):
        activity_pred([1.0, 2.0, 3.0, 4.0])  # More than 3 elements


def test_rsm_opt_valid_square_space():
    # Mock DOverall object
    d_object = Mock()
    d_object.predict.return_value = 0.8

    # Input parameters
    x = [1.0, 1.0, 1.0]
    prediction_funcs = [conversion_pred, activity_pred]

    # Call the function
    result = rsm_opt(x, d_object, prediction_funcs, space="square")

    # Extract the arguments passed to predict
    d_object.predict.assert_called_once()
    called_args = d_object.predict.call_args[0][0]

    # Assertions
    expected_args = np.array([[conversion_pred(x), activity_pred(x)]])
    np.testing.assert_array_almost_equal(called_args, expected_args)
    assert result == -0.8


def test_rsm_opt_valid_circular_space():
    # Mock DOverall object
    d_object = Mock()
    d_object.predict.return_value = 0.9

    # Input parameters (valid for circular space)
    x = [1.0, 1.0, 0.5]  # Norm: sqrt(1.0^2 + 1.0^2 + 0.5^2) ≈ 1.5 <= 1.682
    prediction_funcs = [conversion_pred, activity_pred]

    # Call the function
    result = rsm_opt(x, d_object, prediction_funcs, space="circular")

    # Extract the arguments passed to predict
    d_object.predict.assert_called_once()
    called_args = d_object.predict.call_args[0][0]

    # Assertions
    expected_args = np.array([[conversion_pred(x), activity_pred(x)]])
    np.testing.assert_array_almost_equal(called_args, expected_args)
    assert result == -0.9


def test_rsm_opt_square_space_constraint_violation():
    # Mock DOverall object
    d_object = Mock()
    d_object.predict.return_value = 0.8

    # Input parameters
    x = [2.0, 0.0, 0.0]  # Violates square space constraint
    prediction_funcs = [conversion_pred, activity_pred]

    # Call the function
    result = rsm_opt(x, d_object, prediction_funcs, space="square")

    # Assertions
    d_object.predict.assert_not_called()  # Predict should not be called
    assert result == 0.0


def test_rsm_opt_circular_space_constraint_violation():
    # Mock DOverall object
    d_object = Mock()
    d_object.predict.return_value = 0.7

    # Input parameters
    x = [2.0, 2.0, 2.0]  # Violates circular space constraint
    prediction_funcs = [conversion_pred, activity_pred]

    # Call the function
    result = rsm_opt(x, d_object, prediction_funcs, space="circular")

    # Assertions
    d_object.predict.assert_not_called()  # Predict should not be called
    assert result == 0.0


def test_rsm_opt_invalid_space():
    # Mock DOverall object
    d_object = Mock()

    # Input parameters
    x = [1.0, 1.0, 1.0]
    prediction_funcs = [conversion_pred, activity_pred]

    # Call the function with an invalid space
    with pytest.raises(ValueError, match="space must be 'square' or 'circular'"):
        rsm_opt(x, d_object, prediction_funcs, space="invalid_space")