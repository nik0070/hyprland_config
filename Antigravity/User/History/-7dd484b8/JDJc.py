# pyrefly: ignore [missing-import]
from src.state.agent_state import AgentState

def fundamental_check_node(state: AgentState) -> dict:
    ''' Merges the company lists from both tracks(earnings_picks + sector_picks) & get financial data'''
    