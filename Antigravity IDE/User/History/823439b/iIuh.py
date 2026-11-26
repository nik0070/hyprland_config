from utils.helper_functions import get_path
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def latest_qtr_result():
    response = requests.get('https://www.screener.in/company/536659/')

    soup = BeautifulSoup(response.text)

    qty_res_table_soup = soup.find_all('table', class_="data-table responsive-text-nowrap")


    dfs = []  # list to store all dataframes

    for table in qty_res_table_soup:
        # Extract headers
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        
        # Extract all rows
        rows = []
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td"])
            if not cells:
                continue
            row = [td.get_text(strip=True) for td in cells]
            rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)
        dfs.append(df)

    # --- optional: unpack them for clarity ---
    quarterly_df = dfs[0]
    annual_df = dfs[1]

    output_dir = get_path("src/data/static")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"pvvinfra_qtr_results_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.csv"
    quarterly_df.to_csv(file_path, index=False)
    return quarterly_df

if __name__ == "__main__":
    latest_qtr_result()


