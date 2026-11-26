import pandas as pd
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from src.loaders.data_loader import get_all_dataframes
from src.langgraph_nodes.summarize_data_node import summarize_data_node
from src.langgraph_nodes.market_intel_node import analyze_market_node
from src.state import AgentState


def main():
    print("Hello from trading-agent!")

    graph = StateGraph(AgentState)
    graph.add_node("load_data", get_all_dataframes)
    graph.add_node("summarize_data", summarize_data_node)
    graph.add_node("market_intel", analyze_market_node)

    graph.add_edge(START, "load_data")
    graph.add_edge("load_data", "summarize_data")
    graph.add_edge("summarize_data", "market_intel")
    graph.add_edge("market_intel", END)

    app = graph.compile()

    result = app.invoke({})
    print("\n✅ Graph executed successfully!")
    print("-" * 60)
    print(f'result keys : {result.keys()}')
    for name, summary in result["summaries"].items():
        print(f"📄 {name}: {summary['rows']} rows, columns={summary['columns']}")

    print("\nMarket Intel:")
    print(result["sector_analysis"])

if __name__ == "__main__":
    main()
