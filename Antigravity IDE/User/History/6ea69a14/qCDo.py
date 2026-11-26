import requests
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import json

def parse_date(date_str):
    """Convert date string to datetime object."""
    try:
        return datetime.strptime(date_str.strip(), "%d %b %Y")  # Example: '29 Jul 2025'
    except:
        return None

def scrape_prs_bills(years, session_types):
    base_url = "https://prsindia.org/sessiontrack"
    all_bills = []

    for year in years:
        for session in tqdm(session_types):
            url = f"{base_url}/{session}-session-{year}/bill-legislation"
            print("Fetching:", url)
            resp = requests.get(url)
            if resp.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # The table on PRS site has class "table"
            table = soup.find("table", {"class": "table"})
            if not table:
                print("No table found at", url)
                continue

            # Headers
            headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

            # Rows
            for row in table.find("tbody").find_all("tr"):
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(cols) != len(headers):
                    continue
                bill = {headers[i]: cols[i] for i in range(len(headers))}
                bill["session_type"] = session.capitalize()  # add session_type column
                bill["year"] = year  # add year column
                all_bills.append(bill)

    return all_bills

def prs_bills_scraper():
        # Example: scrape 2025, sessions "monsoon" and "budget"
    years = [2025]
    session_types = ["monsoon", "budget", "special", "winter", "first"]

    bills = scrape_prs_bills(years, session_types)

    # Group bills year-wise and session-wise
    output = {}
    for bill in bills:
        year = bill.pop("year")
        session = bill.pop("session_type")

        if year not in output:
            output[year] = {}
        if session not in output[year]:
            output[year][session] = []

        output[year][session].append(bill)

    # Pretty print JSON
    # print(json.dumps(output, indent=2, ensure_ascii=False))

    # Save to file
    with open(f"outputs/prs_bills_{str(years)}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    output_dir = get_path("src/data/dynamic/legislative_bills")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"prs_bills_{str(years)}.json"
    output_df.to_csv(file_path, index=False)

if __name__ == "__main__":


    # print("Saved prs_bills_2025_grouped.json")

