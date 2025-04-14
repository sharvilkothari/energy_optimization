import sys
from pathlib import Path
from scripts.data_loader import load_solar_data
from scripts.model import build_model
from scripts.solver import solve_model
from scripts.utils import *
from config import *
def main():
    try:
        
        print("1. Loading solar data...")
        solar_data = load_solar_data()
        
        print("2. Building optimization model...")
        model = build_model(solar_data)
        
        print("3. Solving model (this may take a few minutes)...")
        results = solve_model(model)
        # After solving the model:
        
        plot_energy_contributions(model, solar_data)
        plot_financials(results)
        
        print("\n=== Results ===")
        for k, v in results.items():
            print(f"{k}: {v}")
            
        return 0
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())