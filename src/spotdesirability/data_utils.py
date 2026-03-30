import os
import importlib.resources as pkg_resources
from typing import Tuple

import pandas as pd


def get_data_folder_path() -> str:
    """Returns the absolute path to the data folder located in the package."""
    # Assume the 'data' directory is within the same package directory
    current_file_path = os.path.abspath(__file__)
    package_dir = os.path.dirname(current_file_path)
    data_folder_path = os.path.join(package_dir, "data")
    return data_folder_path


def load_compressor_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads the normalized compressor datasets X and Z.

    This function reads df_x_normalized.csv and df_z_normalized.csv from the
    spotdesirability.datasets module and returns them as pandas DataFrames.
    The datasets represent the values of $X$ and $Z$ respectively.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the datasets X and Z
        as pandas DataFrames respectively.

    Raises:
        FileNotFoundError: If the datasets cannot be found.
        RuntimeError: If there is an issue reading the CSV data.

    Example:
        ```python
        import spotdesirability.data_utils as du

        df_x, df_z = du.load_compressor_data()
        ```
    """
    try:
        x_path = pkg_resources.files("spotdesirability.datasets") / "df_x_normalized.csv"
        z_path = pkg_resources.files("spotdesirability.datasets") / "df_z_normalized.csv"

        with pkg_resources.as_file(x_path) as p_x, pkg_resources.as_file(z_path) as p_z:
            df_x = pd.read_csv(p_x)
            df_z = pd.read_csv(p_z)

        return df_x, df_z
    except FileNotFoundError as fnf_err:
        raise fnf_err
    except Exception as err:
        raise RuntimeError(f"Error loading compressor datasets: {err}") from err
