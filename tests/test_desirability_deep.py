import numpy as np
import pytest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
from spotdesirability import DesirabilityBase, DMax, DMin, DTarget, DArb, DBox, DCategorical, DOverall


def test_desirability_base_print():
    """Test the print_class_attributes method of DesirabilityBase."""

    class SimpleDesirability(DesirabilityBase):
        def __init__(self, val):
            super().__init__()
            self.val = val

    obj = SimpleDesirability(10)
    f = StringIO()
    with redirect_stdout(f):
        obj.print_class_attributes()
    output = f.getvalue()
    assert "Class: SimpleDesirability" in output
    assert "val: 10" in output

    # Test recursive printing
    child = SimpleDesirability(5)
    parent = SimpleDesirability(child)
    f = StringIO()
    with redirect_stdout(f):
        parent.print_class_attributes()
    output = f.getvalue()
    assert "val:" in output
    assert "  Class: SimpleDesirability" in output
    assert "  val: 5" in output


def test_desirability_base_extend_range():
    """Test the extend_range method of DesirabilityBase."""
    base = DesirabilityBase()
    values = [0, 10]
    extended = base.extend_range(values, factor=0.1)
    assert extended == [-1.0, 11.0]

    values = [5, 5]
    extended = base.extend_range(values, factor=0.1)
    assert extended == [5.0, 5.0]


@patch("matplotlib.pyplot.show")
def test_desirability_base_plot(mock_show):
    """Test the plot method of DesirabilityBase (via DMax)."""
    dmax = DMax(low=0, high=10)
    # This should run without error and call plt.show()
    dmax.plot()
    assert mock_show.called


def test_dmax_deep():
    """Deep tests for DMax."""
    dmax = DMax(low=0, high=10, scale=2)
    assert dmax.predict(-1) == 0
    assert dmax.predict(11) == 1
    assert dmax.predict(5) == pytest.approx(0.25)
    assert dmax.predict(0) == 0
    assert dmax.predict(10) == 1

    # Vectorized
    inputs = np.array([-1, 0, 5, 10, 11])
    expected = np.array([0, 0, 0.25, 1, 1])
    np.testing.assert_allclose(dmax.predict(inputs), expected)

    # Missing values
    dmax_missing = DMax(low=0, high=10, missing=0.5)
    assert dmax_missing.predict(np.array([np.nan])) == 0.5

    # Tolerance
    dmax_tol = DMax(low=0, high=10, tol=1e-6)
    assert dmax_tol.predict(0) == 1e-6

    # Errors
    with pytest.raises(ValueError, match="low value must be less than the high value"):
        DMax(10, 0)
    with pytest.raises(ValueError, match="scale parameter must be greater than zero"):
        DMax(0, 10, scale=0)


def test_dmin_deep():
    """Deep tests for DMin."""
    dmin = DMin(low=0, high=10, scale=2)
    assert dmin.predict(-1) == 1
    assert dmin.predict(11) == 0
    assert dmin.predict(5) == pytest.approx(0.25)  # ((5-10)/(0-10))^2 = (-5/-10)^2 = 0.5^2 = 0.25
    assert dmin.predict(0) == 1
    assert dmin.predict(10) == 0

    # Vectorized
    inputs = np.array([-1, 0, 5, 10, 11])
    expected = np.array([1, 1, 0.25, 0, 0])
    np.testing.assert_allclose(dmin.predict(inputs), expected)


def test_dtarget_deep():
    """Deep tests for DTarget."""
    dtarget = DTarget(low=0, target=5, high=10, low_scale=1, high_scale=1)
    assert dtarget.predict(-1) == 0
    assert dtarget.predict(11) == 0
    assert dtarget.predict(2.5) == 0.5
    assert dtarget.predict(5) == 1
    assert dtarget.predict(7.5) == 0.5

    # Different scales
    dtarget_scales = DTarget(low=0, target=5, high=10, low_scale=2, high_scale=0.5)
    assert dtarget_scales.predict(2.5) == 0.25  # (2.5/5)^2
    assert dtarget_scales.predict(7.5) == pytest.approx(np.sqrt(0.5))  # ((7.5-10)/(5-10))^0.5 = (2.5/5)^0.5

    # Errors
    with pytest.raises(ValueError, match="low value must be less than the target"):
        DTarget(5, 5, 10)
    with pytest.raises(ValueError, match="target value must be less than the high value"):
        DTarget(0, 10, 10)


def test_darb_deep():
    """Deep tests for DArb."""
    x = [0, 5, 10]
    d = [0, 1, 0.5]
    darb = DArb(x, d)
    assert darb.predict(-1) == 0
    assert darb.predict(11) == 0.5
    assert darb.predict(2.5) == 0.5
    assert darb.predict(7.5) == 0.75

    # Errors
    with pytest.raises(ValueError, match="desirability values must be 0 <= d <= 1"):
        DArb([0, 1], [-1, 1])
    with pytest.raises(ValueError, match="x and d must have the same length"):
        DArb([0, 1], [0.5])


def test_dbox_deep():
    """Deep tests for DBox."""
    dbox = DBox(low=0, high=10)
    assert dbox.predict(-1) == 0
    assert dbox.predict(11) == 0
    assert dbox.predict(0) == 1
    assert dbox.predict(5) == 1
    assert dbox.predict(10) == 1


def test_dcategorical_deep():
    """Deep tests for DCategorical."""
    values = {"A": 0.1, "B": 0.9}
    dcat = DCategorical(values)
    assert dcat.predict(["A"]) == 0.1
    assert dcat.predict(["B"]) == 0.9

    with pytest.raises(ValueError, match="Value 'C' not in allowed values"):
        dcat.predict(["C"])


def test_doverall_deep():
    """Deep tests for DOverall."""
    dmax = DMax(low=0, high=10)
    dmin = DMin(low=0, high=10)
    doverall = DOverall(dmax, dmin)

    # geometric mean of 0.5 and 0.5 is 0.5
    inputs = np.array([[5, 5]])
    assert doverall.predict(inputs) == pytest.approx(0.5)

    # geometric mean of 1.0 and 0.0 is 0.0
    inputs = np.array([[10, 10]])
    assert doverall.predict(inputs) == 0.0

    # Batch
    inputs = np.array([[5, 5], [10, 10]])
    expected = np.array([0.5, 0.0])
    np.testing.assert_allclose(doverall.predict(inputs), expected)

    # All outputs
    indiv, overall = doverall.predict(inputs, all=True)
    assert len(indiv) == 2
    assert overall.shape == (2,)


def test_living_code_example():
    """Verify a 'living' code example like the one that will be in docstrings."""
    from spotdesirability import DMax
    import numpy as np

    # Create a DMax object
    dmax = DMax(low=0, high=10, scale=1)

    # Predict desirability for a range of inputs
    inputs = np.array([-5, 0, 5, 10, 15])
    desirability = dmax.predict(inputs)

    expected = np.array([0.0, 0.0, 0.5, 1.0, 1.0])
    np.testing.assert_allclose(desirability, expected)


def test_predict_list_input():
    """Test that all desirability functions handle list inputs in predict."""
    # DMax
    dmax = DMax(low=0, high=10)
    assert np.allclose(dmax.predict([0, 5, 10]), [0, 0.5, 1])

    # DMin
    dmin = DMin(low=0, high=10)
    assert np.allclose(dmin.predict([0, 5, 10]), [1, 0.5, 0])

    # DTarget
    dtarget = DTarget(low=0, target=5, high=10)
    assert np.allclose(dtarget.predict([0, 5, 10]), [0, 1, 0])

    # DArb
    darb = DArb([0, 10], [0, 1])
    assert np.allclose(darb.predict([0, 5, 10]), [0, 0.5, 1])

    # DBox
    dbox = DBox(low=0, high=10)
    assert np.allclose(dbox.predict([-1, 5, 11]), [0, 1, 0])

    # DCategorical
    dcat = DCategorical({"A": 0.1, "B": 0.9})
    assert np.allclose(dcat.predict(["A", "B"]), [0.1, 0.9])
