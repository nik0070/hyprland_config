from src.state.agent_state import AgentState

def analyze_market_node(state: AgentState) -> AgentState:
    dummy_analysis = {
        "Tech": {
            "reason": "AIboom",
            "trend": "up"
        },
        "Healthcare": {
            "reason": "New drug approvals",
            "trend": "sideways"
        },
        "Finance": {
            "reason": "Interest rate hikes",
            "trend": "down"
        }
    }
    return {"sector_analysis": dummy_analysis}
