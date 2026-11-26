from langgraph.graph import StateGraph, START, END
from src.state.agent_state import AgentState

# Importing all the nodes =================================================
from src.loaders.data_loader import get_all_dataframes
from src.langgraph_nodes.summarize_data_node import summarize_data_node

# Track 1 -------------
from src.langgraph_nodes.market_intel_node import analyze_market_node
from src.langgraph_nodes.sector_catalyst_node import sector_catalyst_node

# Track 2 -------------
from src.langgraph_nodes.earnings_catalyst_node import earnings_catalyst_node
from src.langgraph_nodes.fundamental_check_node import fundamental_check_node

graph = StateGraph(AgentState)
graph.add_node("load_data", get_all_dataframes)
graph.add_node("summarize_data", summarize_data_node)
graph.add_node("market_intel", analyze_market_node)
graph.add_node('sector_catalyst', sector_catalyst_node)
graph.add_node('earnings_catalyst', earnings_catalyst_node)
graph.add_node('fundamental_check', fundamental_check_node)

graph.add_edge(START, "load_data")
graph.add_edge("load_data", "summarize_data")
graph.add_edge("summarize_data", "market_intel")
graph.add_edge("market_intel", "sector_catalyst")
graph.add_edge("sector_catalyst", "earnings_catalyst")
graph.add_edge("earnings_catalyst", "fundamental_check")
graph.add_edge("fundamental_check", END)

app = graph.compile()
