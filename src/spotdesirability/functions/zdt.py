import numpy as np


def zdt1(x) -> np.ndarray:
    """
    Calculates the objective values for the ZDT1 problem.

    Args:
        x (np.ndarray): A 30-dimensional numpy array with values between 0 and 1.

    Returns:
        np.ndarray: A 2-dimensional numpy array containing the objective values f1 and f2.

    Raises:
        IndexError: If the input array does not have exactly 30 dimensions.

    Examples:
        >>> import numpy as np
        >>> from spotdesirability.functions.zdt import zdt1
        >>> x = np.random.rand(30)
        >>> f = zdt1(x)
        >>> print(f)
    """
    if len(x) != 30:
        raise IndexError(f"Input array must have exactly 30 dimensions, got {len(x)}")
    f1 = x[0]
    g = 1 + 9 * np.sum(x[1:]) / (len(x) - 1)
    f2 = g * (1 - np.sqrt(f1 / g))
    return np.array([f1, f2])
