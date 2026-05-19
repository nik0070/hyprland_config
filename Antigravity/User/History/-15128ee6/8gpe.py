# src/langgraph_nodes/summarize_data_node.py
import pandas as pd

def summarize_data_node(state: dict) -> dict:
    """Summarize the dataframes from state."""
    dfs: dict[str, pd.DataFrame] = state.get("dataframes", {})
    summaries = {}

    for name, df in dfs.items():
        summaries[name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "sample": df.head(3).to_dict(orient="records"),
        }

    return {"summaries": summaries}
