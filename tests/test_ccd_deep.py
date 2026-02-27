import os
from unittest.mock import patch
from spotdesirability.plot.ccd import plotCCD


def test_plotCCD_runs():
    """Test that plotCCD runs without error when showing."""
    with patch("matplotlib.pyplot.show") as mock_show:
        plotCCD()
        assert mock_show.called


def test_plotCCD_saves_file(tmp_path):
    """Test that plotCCD saves a file correctly."""
    filename = tmp_path / "test_ccd.png"
    plotCCD(filename=str(filename))
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0

    filename_pdf = tmp_path / "test_ccd.pdf"
    plotCCD(filename=str(filename_pdf))
    assert os.path.exists(filename_pdf)
    assert os.path.getsize(filename_pdf) > 0


def test_plotCCD_docstring_example():
    """Test that the code example in the plotCCD docstring is correct."""
    import re

    doc = plotCCD.__doc__
    # Extract code between ```{python} and ```
    match = re.search(r"```{python}\n(.*?)\n\s*```", doc, re.DOTALL)
    assert match, "Living code example not found in docstring"

    code = match.group(1)
    import textwrap

    code = textwrap.dedent(code).strip()

    # Execute the code, mocking plt.show to avoid blocking
    with patch("matplotlib.pyplot.show") as mock_show:
        # We need to make sure the environment has what it needs
        # The example uses 'from spotdesirability.plot.ccd import plotCCD'
        # which should work if we are running with uv run pytest
        exec_globals = {}
        exec(code, exec_globals)
        assert mock_show.called
