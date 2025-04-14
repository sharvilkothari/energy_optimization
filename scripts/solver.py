import pulp
from pulp import COIN_CMD
from config import *

def solve_model(prob):
    solver = COIN_CMD(msg=True, timeLimit=600)
    status = prob.solve(solver)
    
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError("Optimization failed")
    
    S = prob.variablesDict()["Solar_Capacity"].varValue
    B_energy = prob.variablesDict()["Battery_Energy"].varValue
    G = prob.variablesDict()["Gas_Capacity"].varValue
    
    total_energy = HOURLY_DEMAND * 24 * 365 * YEARS / 1e6  # in TWh
    
    total_cost = 0
    
    total_cost += (SOLAR_CAPEX * S + BATTERY_CAPEX * B_energy + GAS_CAPEX * G + S * LAND_PER_SOLAR_MW * LAND_COST)
    
    for y in range(YEARS):
        discount_factor = 1 / ((1 + DISCOUNT_RATE) ** y)
        opex_growth = (1 + OPEX_GROWTH_RATE) ** y
        
        total_cost += (OPEX_SOLAR * S + OPEX_BATTERY * B_energy + OPEX_GAS * G) * opex_growth * discount_factor
        total_cost += (GAS_HEAT_RATE * GAS_PRICE_MMBTU * G * HOURS_PER_YEAR) * discount_factor
        
        if y > 0 and y % BATTERY_REPLACEMENT_YEARS == 0:
            battery_degradation = (1 - BATTERY_COST_DEG) ** y
            total_cost += (BATTERY_CAPEX * B_energy * battery_degradation) * discount_factor
    
    
    final_discount = 1 / ((1 + DISCOUNT_RATE) ** YEARS)
    total_cost -= (0.1 * SOLAR_CAPEX * S + 0.1 * GAS_CAPEX * G) * final_discount
    
    return {
        "Solar (MW)": round(S, 2),
        "Battery (MWh)": round(B_energy, 2),
        "Gas (MW)": round(G, 2),
        "LCOE ($/MWh)": round((total_cost)/(total_energy*1e6), 2),
        "Total energy in TWh": total_energy,
        "Total cost in Billion": total_cost/1e9
    }
