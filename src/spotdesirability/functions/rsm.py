import numpy as np


def conversion_pred(x) -> float:
    """
    Predicts the percent conversion based on the input vector x.

    Args:
        x (list or numpy array): A vector of three input values [x1, x2, x3].

    Returns:
        float: The predicted percent conversion.

    Examples:
        >>> from spotdesirability.functions.rsm import conversion_pred
        >>> x = [1.0, 2.0, 3.0]
        >>> conversion = conversion_pred(x)
        >>> print(conversion)
    """
    # check if x is a list or numpy array
    if isinstance(x, list):
        x = np.array(x)
    elif not isinstance(x, np.ndarray):
        raise ValueError("Input x must be a list or numpy array.")
    # check if x has the correct shape
    if x.shape != (3,):
        raise ValueError("Input x must be a 3-element vector.")
    return 81.09 + 1.0284 * x[0] + 4.043 * x[1] + 6.2037 * x[2] - 1.8366 * x[0] ** 2 + 2.9382 * x[1] ** 2 - 5.1915 * x[2] ** 2 + 2.2150 * x[0] * x[1] + 11.375 * x[0] * x[2] - 3.875 * x[1] * x[2]


def activity_pred(x) -> float:
    """
    Predicts the thermal activity based on the input vector x.

    Args:
        x (list or numpy array): A vector of three input values [x1, x2, x3].

    Returns:
        float: The predicted thermal activity.

    Examples:
        >>> from spotdesirability.functions.rsm import activity_pred
        >>> x = [1.0, 2.0, 3.0]
        >>> activity = activity_pred(x)
        >>> print(activity)
    """
    # check if x is a list or numpy array
    if isinstance(x, list):
        x = np.array(x)
    elif not isinstance(x, np.ndarray):
        raise ValueError("Input x must be a list or numpy array.")
    # check if x has the correct shape
    if x.shape != (3,):
        raise ValueError("Input x must be a 3-element vector.")
    # Calculate the predicted thermal activity
    return 59.85 + 3.583 * x[0] + 0.2546 * x[1] + 2.2298 * x[2] + 0.83479 * x[0] ** 2 + 0.07484 * x[1] ** 2 + 0.05716 * x[2] ** 2 - 0.3875 * x[0] * x[1] - 0.375 * x[0] * x[2] + 0.3125 * x[1] * x[2]


def rsm_opt(x, d_object, prediction_funcs, space="square") -> float:
    """
    Optimization function to calculate desirability.
    Optimizers minimize, so we return negative desirability.

    Args:
        x (list or np.ndarray): Input parameters (e.g., time, temperature, catalyst).
        d_object (DOverall): Overall desirability object.
        prediction_funcs (list of callables): List of prediction functions to calculate outcomes.
        space (str): Design space ("square" or "circular").

    Returns:
        float: Negative desirability.

    Raises:
        ValueError: If `space` is not "square" or "circular".

    Examples:
        >>> from spotdesirability.utils.desirability import DOverall, rsm_opt, DTarget
        >>> from spotdesirability.utils.desirability import conversion_pred, activity_pred
        >>> d_object = DOverall(DTarget(0, 0.5, 1), DTarget(0, 0.5, 1))
        >>> prediction_funcs = [conversion_pred, activity_pred]
        >>> x = [1.0, 2.0, 3.0]
        >>> desirability = rsm_opt(x, d_object, prediction_funcs)
        >>> print(desirability)
        -0.5
    """
    # Apply space constraints first. We use 1.682 = (2^3)^(1/4), see Mont01 a, p.457, as the limit for both circular and square spaces.
    if space == "circular":
        if np.sqrt(np.sum(np.array(x) ** 2)) > 1.682:
            return 0.0
    elif space == "square":
        if np.any(np.abs(np.array(x)) > 1.682):
            return 0.0
    else:
        raise ValueError("space must be 'square' or 'circular'")

    # Calculate predictions for all provided functions
    predictions = [func(x) for func in prediction_funcs]

    # Predict desirability using the overall desirability object
    desirability = d_object.predict(np.array([predictions]))

    # Return negative desirability
    return -desirability
