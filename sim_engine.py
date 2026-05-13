import pandas as pd
import numpy as np

def generate_cycle_data(cycle_length=32):
    """
    Simulates distal skin temperature and HRV signals based on Oura Ring 
    measurement patterns. Distal skin temp typically shows a biphasic 
    shift similar to core BBT but with higher sensor variance.
    """
    ovulation_day = cycle_length - 14 
    days = np.arange(1, cycle_length + 1)
    
    # Skin Temp: Reflecting Oura's +/- 0.x Celsius/Fahrenheit deviations
    # Base temp 97.4 follicular, shifts to ~98.1 luteal
    skin_temp = [97.4 + np.random.normal(0, 0.08) if d < ovulation_day 
                 else 98.1 + np.random.normal(0, 0.08) for d in days]
    
    # HRV: Reflecting the autonomic nervous system shift (drop in luteal phase)
    hrv = [65 + np.random.normal(0, 5) if d < ovulation_day 
           else 48 + np.random.normal(0, 5) for d in days]
    
    return pd.DataFrame({
        'CycleDay': days,
        'SkinTemp': skin_temp,
        'HRV': hrv
    })