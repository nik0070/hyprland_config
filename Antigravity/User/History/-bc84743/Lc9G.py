from src.state.agent_state import AgentState
from utils.helper_functions import get_path
import pandas as pd
import json

def get_all_dataframes(state: AgentState) -> AgentState:
    """
    Traverse all subfolders under base_dir and load all CSV and JSON files.

    Returns:
        dict[str, pd.DataFrame]: A dictionary where
            keys = filenames (without extension)
            values = pandas DataFrames
    Example:
        dfs = get_all_dataframes()
        dfs['tata'].head()
    """
    
    base_dir = "src/data/dynamic"
    data_path = get_path(base_dir)  #project root / src/data/dynamic

    dfs = {}
    # Traverse all subfolders recursively
    for file_path in data_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".csv", ".json"]:
            name = file_path.stem  # filename without extension

            if file_path.suffix.lower() == ".csv":
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    # Normalize JSON into tabular DataFrame
                    df = pd.json_normalize(raw) if isinstance(raw, (list, dict)) else pd.DataFrame([{"raw": raw}])
            dfs[name] = df
    return {"dataframes": dfs}  # wrapped for LangGraph



if __name__ == '__main__':
    base_dir = "src/data/dynamic"
    data_path = get_path(base_dir)
    for file_path in data_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in ['.csv', '.json']:
            print(f'Processing file in name == main : {file_path.stem}')
    
    state = {"dataframes": {}, "summaries": {}}
    output = get_all_dataframes(state)
    print(output)


