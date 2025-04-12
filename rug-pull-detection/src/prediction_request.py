from pydantic import BaseModel
import numpy as np

class PredictionRequest(BaseModel):
    coin_age_months: float
    trust_in_owners : float
    no_of_transactions : float 
    volume_usd : float 
    no_of_holders : float
    max_volume_usd : float
    time_hr_diff : float
    time_day_diff : float
    price_usd : float
    price_volatility : float
    liquidity_drawdown : float
    liquidity_recovery : float
    price_total_variation : float


    def to_numpy_array(self):
        features =  [
            self.coin_age_months,
            self.trust_in_owners,
            self.no_of_transactions,
            self.volume_usd,
            self.no_of_holders,
            self.max_volume_usd,
            self.time_hr_diff,
            self.time_day_diff,
            self.price_usd,
            self.price_volatility,
            self.liquidity_drawdown,
            self.liquidity_recovery,
            self.price_total_variation
        ]
        return np.array(features).reshape(1, -1)


   
    
