from src/state/agent_state import AgentState
import pandas as pd
from pathlib import Path

def earnings_catalyst_node(state: AgentState) -> dict:
    """Load upcoming earnings data and flag companies for analysis."""

    file_path = 'src/data/future_fin_res'
    base_path = Path(__file__).resolve().parent.parent.parent # project root
    file_path = base_path / file_path

    earnings_df = pd.read_csv(file_path)
    
    