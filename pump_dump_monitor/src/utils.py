from typing import Dict
from config import MAX_VALUES

def is_valid_erc20(address: str) -> bool:
    """Check if the provided address is a valid ERC20 token address."""
    return address is not None and address.startswith("0x") and len(address) == 42

def sanitize_features(features: Dict) -> Dict:
    """Cap feature values to predefined maximums to prevent outliers."""
    sanitized = {}
    for key, value in features.items():
        if isinstance(value, (int, float)):
            sanitized[key] = min(value, MAX_VALUES.get(key, float('inf')))
        else:
            sanitized[key] = value
    return sanitized