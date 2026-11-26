from langgraph.graph import StateGraph, START, END
# pyrefly: ignore [missing-import]
from src.state.agent_state import AgentState

# Importing all the nodes =================================================
# pyrefly: ignore [missing-import]
from src.loaders.data_loader import get_all_dataframes
# pyrefly: ignore [missing-import]
from src.langgraph_nodes.summarize_data_node import summarize_data_node

# Track 1 -------------
# pyrefly: ignore [missing-import]
from src.langgraph_nodes.market_intel_node import analyze_market_node
# pyrefly: ignore [missing-import]
from src.langgraph_nodes.sector_catalyst_node import sector_catalyst_node

# Track 2 -------------
# pyrefly: ignore [missing-import]
from src.langgraph_nodes.earnings_catalyst_node import earnings_catalyst_node

# pyrefly: ignore [missing-import]
from src.langraph_nodes.fundamental_check_node import fundamental_check_node

graph = StateGraph(AgentState)
graph.add_node("load_data", get_all_dataframes)
graph.add_node("summarize_data", summarize_data_node)
graph.add_node("market_intel", analyze_market_node)

graph.add_edge(START, "load_data")
graph.add_edge("load_data", "summarize_data")
graph.add_edge("summarize_data", "market_intel")
graph.add_edge("market_intel", END)

app = graph.compile()
