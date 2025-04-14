import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import *


def plot_energy_contributions(prob, solar_data):
    # Extract variables from the solved model
    S = prob.variablesDict()["Solar_Capacity"].varValue
    B_energy = prob.variablesDict()["Battery_Energy"].varValue
    G = prob.variablesDict()["Gas_Capacity"].varValue

    # Calculate total energy contributions (MWh over 25 years)
    total_solar = S * sum(solar_data)  # Defined in model.py
    total_battery = B_energy * BATTERY_EFFICIENCY * 365 * YEARS  # Defined in model.py
    total_gas = G * HOURS_PER_YEAR * YEARS  # Derived from model's gas constraint

    # Calculate total demand for validation
    total_demand = HOURLY_DEMAND * HOURS_PER_YEAR * YEARS
    
    # Create pie chart
    labels = ["Solar", "Battery", "Gas"]
    sizes = [total_solar, total_battery, total_gas]
    colors = ["#FFD700", "#4CAF50", "#FF5722"]

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title(f"Total Energy Contribution (25 Years)\nRenewables: {((total_gas)/total_demand*100):.1f}%")
    plt.savefig("results/energy_contribution.png")
    plt.close()

def plot_financials(results):
    costs = {
        "Solar CAPEX": SOLAR_CAPEX * results["Solar (MW)"],
        "Battery CAPEX": BATTERY_CAPEX * results["Battery (MWh)"],
        "Gas CAPEX": GAS_CAPEX * results["Gas (MW)"],
        "OPEX (25y)": results["Total cost in Billion"] * 1e9 - (SOLAR_CAPEX * results["Solar (MW)"] + BATTERY_CAPEX * results["Battery (MWh)"] + GAS_CAPEX * results["Gas (MW)"])
    }
    
    plt.figure(figsize=(15, 5))
    plt.bar(costs.keys(), costs.values())
    plt.ylabel("Cost ($)")
    plt.title("Cost Breakdown")
    plt.xticks(rotation=0)
    plt.savefig("results/cost_breakdown.png")
    plt.close()