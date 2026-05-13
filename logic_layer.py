def detect_ovulation(df):
    """
    Algorithm: Sliding window detector.
    Identifies the first day where Skin Temp is 0.3°F above the 
    6-day follicular baseline for a sustained 3-day period.
    """
    window_size = 6
    # Create a smoothed series to handle sensor noise/outliers
    df['Temp_Smooth'] = df['SkinTemp'].rolling(window=3).mean()
    
    detected_day = None
    for i in range(window_size, len(df) - 3):
        baseline = df['SkinTemp'].iloc[i-window_size:i].mean()
        if all(df['SkinTemp'].iloc[i:i+3] > baseline + 0.3):
            detected_day = df['CycleDay'].iloc[i]
            break
            
    return detected_day

def get_fertility_window(ovulation_day):
    if ovulation_day is None:
        return None, None
    return max(1, ovulation_day - 5), ovulation_day