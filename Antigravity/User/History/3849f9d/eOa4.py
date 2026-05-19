from typing import TypedDict
import pandas as pd

class AgentState(TypedDict):
    dataframes: dict[str, pd.DataFrame]
    summaries: dict[str, dict]
