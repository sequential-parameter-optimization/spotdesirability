import pandas as pd
import spotdesirability.data_utils as du

def test_load_compressor_data():
    """Test if load_compressor_data returns two pandas DataFrames with expected data."""
    df_x, df_z = du.load_compressor_data()
    
    assert isinstance(df_x, pd.DataFrame), "Expected df_x to be a pandas DataFrame."
    assert isinstance(df_z, pd.DataFrame), "Expected df_z to be a pandas DataFrame."
    
    assert not df_x.empty, "df_x DataFrame is empty."
    assert not df_z.empty, "df_z DataFrame is empty."
    
    # Check that they have a reasonable number of columns or rows, ensuring successful parse
    assert len(df_x.columns) > 0, "df_x has no columns."
    assert len(df_z.columns) > 0, "df_z has no columns."
