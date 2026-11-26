from src.state.agent_state import AgentState
import pandas as pd

def earnings_catalyst_node(state: AgentState) -> dict:
    """Load upcoming earnings data and flag companies for analysis."""

    # Approximate lookup of dictionary key containing the financial result, since contains variable date in name
    upcoming_df = None

    for key, df in state['dataframes'].items():
        if key.startswith("upcoming_qtr_financial_results"):
            upcoming_df = df
            break
    
    if upcoming_df is None:
        return {"earnings_picks": []}   # return empty list if no earnings data found

    
    target_date = '2025-10-03'
    comp_with_upc_fin = upcoming_df[upcoming_df['date'] == target_date]['Company Name'].tolist()

    output_list = [{"company": i, "catalyst": "Earnings Today"} for i in comp_with_upc_fin]

    return {"earnings_picks": output_list}


    
    