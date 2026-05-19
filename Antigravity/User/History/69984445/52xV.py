from src.state.agent_state import AgentState

def analyze_market_node(state: AgentState) -> AgentState:
    return state['summaries']
