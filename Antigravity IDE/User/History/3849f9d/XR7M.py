from typing import TypedDict, Annotated
import pandas as pd

def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """Safely merges two dictonaries instead of overwriting"""
    # If there's no previous state, dict1 might be None in Langgraph, so we protect against it
    if dict1 is None: 
        dict1 = {}

    merged = dict1.copy()
    merged.update(dict2)
    return merged

class AgentState(TypedDict):
    dataframes: dict[str, pd.DataFrame]
    summaries: dict[str, dict]
    sector_analysis: dict
    sector_to_stock: dict[str, list[str]]
    final_report: str
    sector_picks: list[dict]
    earnings_picks: list[dict]
    financial_data: Annotated[dict[str, dict], merge_dicts]
