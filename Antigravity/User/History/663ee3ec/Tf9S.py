from src.state.agent_state import AgentState
from pathlib import Path
import pandas as pd

def stock_matcher_node(state: AgentState) -> dict: 
    '''load the stock to sector mapping from static and match with state market intel summary'''
    
    base_dir = 'src/data/static'
    base_path = Path(__file__).resolve().parent.parent.parent #project root
    data_path = base_path / base_dir

    mapping_df = pd.read_csv(data_path / "stock_sectors.csv")
    market_intel = state['sector_analysis']

    # selecting only those stocks whose sector analysis says the sector is bullish
    bullish_sectors = [sector for sector, analysis in market_intel.items() if analysis['trend'] == 'up']

    bullish_stocks = mapping_df[mapping_df['sector'].isin(bullish_sectors)]

    stock_picks_dict = bullish_stocks.to_dict(orient='records')

    #update the state with stock picks
    state['stock_picks'] = stock_picks_dict

    return state
