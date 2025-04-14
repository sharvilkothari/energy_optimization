import pulp
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
from config import *

def build_model(solar_data):
    prob = LpProblem("25yr_Energy_Optimization", LpMinimize)
    
    
    S = LpVariable("Solar_Capacity", lowBound=100)  
    B_energy = LpVariable("Battery_Energy", lowBound=300) 
    G = LpVariable("Gas_Capacity", lowBound=5, upBound=25) 

    
    total_cost = 0
    
    
    total_cost += SOLAR_CAPEX * S 
    total_cost += BATTERY_CAPEX * B_energy
    total_cost += GAS_CAPEX * G
    total_cost += S * LAND_COST
    
    
    for y in range(YEARS):
        discount_factor = 1 / ((1 + DISCOUNT_RATE) ** y)
        opex_growth = (1 + OPEX_GROWTH_RATE) ** y
        
        
        total_cost += (OPEX_SOLAR * S) * opex_growth * discount_factor
        total_cost += (OPEX_BATTERY * B_energy) * opex_growth * discount_factor
        total_cost += (OPEX_GAS * G) * opex_growth * discount_factor
        
        
        if y > 0 and y % BATTERY_REPLACEMENT_YEARS == 0:
            battery_degradation = (1 - BATTERY_COST_DEG) ** y
            total_cost += (BATTERY_CAPEX * B_energy* battery_degradation) * discount_factor

    final_discount = 1 / ((1 + DISCOUNT_RATE) ** YEARS)
    total_cost -= 0.1 * SOLAR_CAPEX * S * final_discount
    total_cost -= 0.1 * GAS_CAPEX * G * final_discount
    
    prob += total_cost

    
    total_solar_generation = S * sum(solar_data)
    
    total_battery_discharge = B_energy * BATTERY_EFFICIENCY * (365 * YEARS)
    
    total_demand = HOURLY_DEMAND * HOURS_PER_YEAR * YEARS
    prob += total_solar_generation + total_battery_discharge >= RENEWABLE_SHARE * total_demand
    annual_gas_energy = total_demand * (1 - RENEWABLE_SHARE) / YEARS
    prob += G * HOURS_PER_YEAR >= annual_gas_energy

    prob += S * LAND_PER_SOLAR_MW <= MAX_LAND_AVAILABLE
    return prob