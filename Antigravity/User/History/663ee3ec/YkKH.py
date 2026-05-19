from src.state.agent_state import AgentState
from utils.helper_functions import get_path
from pathlib import Path
import pandas as pd

def stock_matcher_node(state: AgentState) -> dict: 
    '''load the stock to sector mapping from static and match with state market intel summary'''
    
    base_dir = 'src/data/static'
    data_path = get_path(base_dir)

    mapping_df = pd.read_csv(data_path / "stock_sectors.csv")
    market_intel = state['sector_analysis']

    # selecting only those stocks whose sector analysis says the sector is bullish
    bullish_sectors = [sector for sector, analysis in market_intel.items() if analysis['trend'] == 'up']

    bullish_stocks = mapping_df[mapping_df['sector'].isin(bullish_sectors)]
    bullish_stocks = bullish_stocks.drop(columns=bullish_stocks.columns[0]) # removing the Unnamed:0 column - the index

    sector_picks_dict = bullish_stocks.to_dict(orient='records')

    # Add catalyst tags
    for stock in sector_picks_dict:
        stock['catalyst'] = 'Sector News'

    return {'sector_picks': sector_picks_dict}


