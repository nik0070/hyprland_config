import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def upcoming_qtr_result_lst():

    # --- get list of dates ---
    dt = datetime.now()
    dates_str = [(dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]

    req_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    }

    output_df = pd.DataFrame()

    for date in dates_str: 
        base_url = f"https://www.moneycontrol.com/markets/earnings/results-calendar/?activeDate={date}"
        resp = requests.get(base_url, headers=req_headers)
        print(date, resp.status_code)

        soup = BeautifulSoup(resp.text, "html.parser")

        tmp = soup.find_all("div", class_="undefined tab-content")
        if not tmp:
            continue
        table_soup = tmp[0].find("table")
        if not table_soup:
            continue

        # Extract headers
        table_headers = [th.get_text(strip=True) for th in table_soup.find("thead").find_all("th")]
        table_headers.append("link_to_financial_data")
        table_headers.insert(0, "date")   # add date as first column

        rows = []
        for tr in table_soup.find("tbody").find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            link = tr.find("a")["href"] if tr.find("a") else None
            cells.append(link)  # add link at end
            cells.insert(0, date)  # add date at start

            # Pad or trim to match header length
            if len(cells) < len(table_headers):
                cells += [""] * (len(table_headers) - len(cells))
            elif len(cells) > len(table_headers):
                cells = cells[:len(table_headers)]
            
            rows.append(cells)

        df = pd.DataFrame(rows, columns=table_headers)
        output_df = pd.concat([output_df, df], ignore_index=True)
        output_df.to_csv(f'outputs/dynamic/future_fin_res/upcoming_qtr_financial_results_{date}.csv', index=False)
