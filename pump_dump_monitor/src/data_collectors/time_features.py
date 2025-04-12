import numpy as np
from datetime import datetime
from typing import Dict

class TimeFeatureCollector:
    def calculate_time_features(self) -> Dict:
        """Generate cyclical time features based on current time."""
        now = datetime.now()
        return {
            'hour_sin': np.sin(2 * np.pi * now.hour / 24),
            'hour_cos': np.cos(2 * np.pi * now.hour / 24),
            'minute_sin': np.sin(2 * np.pi * now.minute / 60),
            'minute_cos': np.cos(2 * np.pi * now.minute / 60)
        }