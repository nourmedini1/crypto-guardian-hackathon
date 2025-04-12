from pydantic import BaseModel
import pandas as pd

class PredictionRequest(BaseModel):
    std_rush_order : float
    avg_rush_order : float
    std_trades : float
    std_volume : float
    avg_volume : float
    std_price : float
    avg_price : float
    avg_price_max : float
    hour_sin : float
    hour_cos : float
    minute_sin : float
    minute_cos : float

    def to_df(self, feature_columns : list):
        return pd.DataFrame(list(self.model_dump().values()), columns=feature_columns)
        

