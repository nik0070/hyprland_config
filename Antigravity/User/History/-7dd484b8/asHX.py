# pyrefly: ignore [missing-import]
from src.state.agent_state import AgentState

def fundamental_check_node(state: AgentState) -> dict:
    ''' Merges the company lists from both tracks(earnings_picks + sector_picks) & get financial data'''
    sector_dict = state['sector_picks']
    earnings_dict = state['earnings_picks']

    if not sector_dict and not earnings_dict:
        return {"final_picks": []}   

    
    
