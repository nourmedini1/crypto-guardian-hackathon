"""
Data loading and preprocessing functions
"""
import pandas as pd
from datetime import datetime

def load_data(file_path="preprocessed_ethereum_data.csv"):
    """
    Load preprocessed data from CSV file
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        DataFrame with preprocessed data
    """
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    df.sort_index(inplace=True)
    return df

def update_historical_data(new_data, csv_path="preprocessed_ethereum_data.csv"):
    """
    Update historical data with new data point
    
    Args:
        new_data: Dictionary with new data point
        csv_path: Path to the CSV file
    
    Returns:
        Updated DataFrame
    """
    df = load_data(csv_path)
    
    new_row = pd.DataFrame({
        "Open": [new_data["open"]],
        "High": [new_data["high"]],
        "Low": [new_data["low"]],
        "Close": [new_data["close"]],
        "Volume": [new_data["volume"]]
    }, index=[pd.to_datetime(new_data["date"], format="%b %d, %Y")])
    
    df = pd.concat([df, new_row])
    df.sort_index(inplace=True)
    
    df.to_csv(csv_path)
    return df