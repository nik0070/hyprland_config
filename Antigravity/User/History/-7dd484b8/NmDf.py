import pandas as pd
import json
# pyrefly: ignore [missing-import]
from src.state.agent_state import AgentState
# pyrefly: ignore [missing-import]
from utils.helper_functions import normalize, get_path
# pyrefly: ignore [missing-import]
from api_fetch.fetch_financials import fetch_quarterly_financials, fetch_kpis

def fundamental_check_node(state: AgentState) -> dict:
    ''' Merges the company lists from both tracks and gets financial data '''
    
    # We will store everything in here and return it to update the AgentState
    financial_data = {}

    ###############################
    # Earnings track
    ###############################
    earnings_company_list = [comp['company'] for comp in state.get('earnings_picks', [])]
    print(f"\n[Fundamental Check] Processing {len(earnings_company_list)} Earnings Picks")

    earnings_path = get_path('src/data/company_financials/earnings')
    earnings_path.mkdir(parents=True, exist_ok=True)

    for comp_name in earnings_company_list:
        comp_normalized = normalize(comp_name)
        financial_data[comp_name] = {}
        
        # 1. Get Quarterly Financials (Already Downloaded)
        qtr_file = earnings_path / f"{comp_normalized}_QTR.csv"
        legacy_qtr_file = earnings_path / f"{comp_normalized}.csv" 
        
        if legacy_qtr_file.exists():
            df = pd.read_csv(legacy_qtr_file)
            financial_data[comp_name]["quarterly_financials"] = df.to_dict(orient="records")
        else:
            print(f"Warning: Missing pre-downloaded earnings CSV for {comp_name}")
            financial_data[comp_name]["quarterly_financials"] = None

        # 2. Get KPIs (Fetch and Cache)
        kpi_file = earnings_path / f"{comp_normalized}_KPI.json" # Saving KPIs as JSON since it's a simple dict
        if kpi_file.exists():
            with open(kpi_file, "r") as f:
                financial_data[comp_name]["kpis"] = json.load(f)
        else:
            print(f"Fetching KPIs for {comp_name}...")
            kpis = fetch_kpis(comp_name)
            financial_data[comp_name]["kpis"] = kpis
            
            # Save to cache
            if kpis.get("status") == "Success":
                with open(kpi_file, "w") as f:
                    json.dump(kpis, f, indent=4)


    ##############################
    # Sector track
    ##############################
    sector_company_list = [comp['company'] for comp in state.get('sector_picks', [])]
    print(f"\n[Fundamental Check] Processing {len(sector_company_list)} Sector Picks")

    sector_path = get_path('src/data/company_financials/sector')
    sector_path.mkdir(parents=True, exist_ok=True)

    for comp_name in sector_company_list:
        comp_normalized = normalize(comp_name)
        # Avoid overwriting if a company happens to be in both earnings and sector
        if comp_name not in financial_data:
            financial_data[comp_name] = {}
        
        # 1. Get Quarterly Financials (Fetch and Cache)
        qtr_file = sector_path / f"{comp_normalized}_QTR.json"
        if qtr_file.exists():
            with open(qtr_file, "r") as f:
                financial_data[comp_name]["quarterly_financials"] = json.load(f)
        else:
            print(f"Fetching QTR Financials for {comp_name}...")
            qtr_data = fetch_quarterly_financials(comp_name)
            financial_data[comp_name]["quarterly_financials"] = qtr_data
            
            if qtr_data.get("status") == "Success":
                with open(qtr_file, "w") as f:
                    json.dump(qtr_data, f, indent=4)

        # 2. Get KPIs (Fetch and Cache)
        kpi_file = sector_path / f"{comp_normalized}_KPI.json"
        if kpi_file.exists():
            with open(kpi_file, "r") as f:
                financial_data[comp_name]["kpis"] = json.load(f)
        else:
            print(f"Fetching KPIs for {comp_name}...")
            kpis = fetch_kpis(comp_name)
            financial_data[comp_name]["kpis"] = kpis
            
            if kpis.get("status") == "Success":
                with open(kpi_file, "w") as f:
                    json.dump(kpis, f, indent=4)

    
    # Finally, return the master dictionary to update AgentState
    return {"financial_data": financial_data}
