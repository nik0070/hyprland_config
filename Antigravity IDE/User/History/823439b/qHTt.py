from utils.helper_functions import get_path
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def get_screener_url(company_or_ticker: str) -> str:
    # Using screener api to get the exact url to hit for the required company
    results = requests.get(
        f"https://www.screener.in/api/company/search/?q={company_or_ticker}"
    )
    valid_results = [
        res for res in results.json()
        if not any(term in res["name"].lower() for term in ["partly", "paid", "rights", "warrant", "re-"])
    ]
    
    if not valid_results:
        print(f"No valid company found for ticker: {company_or_ticker}")
        return ''

    primary_company = valid_results[0]
    primary_company_path = primary_company['url']
    complete_screener_url = f"https://www.screener.in{primary_company_path}"
    
    return complete_screener_url

def latest_qtr_result(screener_url: str) -> pd.DataFrame:
    response = requests.get(screener_url)

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


