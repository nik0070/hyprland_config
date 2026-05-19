from src/state/agent_state import AgentState
import pandas as pd

def earnings_catalyst_node(state: AgentState) -> dict:
    """Load upcoming earnings data and flag companies for analysis."""
