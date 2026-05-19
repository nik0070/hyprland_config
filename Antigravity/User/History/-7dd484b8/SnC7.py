# pyrefly: ignore [missing-import]
from src.state.agent_state import AgentState
# pyrefly: ignore [missing-import]
from utils.helper_functions import normalize, get_file_stem
   

def fundamental_check_node(state: AgentState) -> dict:
    ''' Merges the company lists from both tracks(earnings_picks + sector_picks) & get financial data'''

    # Earnings
    earnings_company_list = [comp['company'] for comp in state['earnings_picks']]
    print(f"\n[Fundamental Check] {len(earnings_company_list)} Earnings Picks")

    earnings_company_files_path = 'src/data/company_financials/earnings'
    earnings_company_files_names =  [normalize(stem) for stem in get_file_stem(earnings_company_files_path)]

    for comp_name in earnings_company_list:
        comp_normalized = normalize(comp_name)
        if comp_normalized in earnings_company_files_names:
            



    
    
