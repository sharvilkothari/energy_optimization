import pandas as pd
from config import YEARS, HOURS_PER_YEAR, SOLAR_DEGRADATION

def load_solar_data():
    df = pd.read_csv("data/solar_availability.csv")
    base_data = df['output'].tolist()[:HOURS_PER_YEAR]
    
    degradation_factors = [(1 - SOLAR_DEGRADATION) ** y for y in range(YEARS)]
    
    full_data = [v * degradation_factors[y] for y in range(YEARS) for v in base_data]
    return full_data