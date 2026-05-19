from typing import TypedDict
import pandas as pd

class AgentState(TypedDict):
    dataframes: dict[str, pd.DataFrame]
    summaries: dict[str, dict]
    sector_analysis: dict
    sector_to_stock: dict[str, list[str]]
    final_report: str
    sector_picks: list[dict]
    earnings_picks: list[dict]
