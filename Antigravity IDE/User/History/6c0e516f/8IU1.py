from bs4 import BeautifulSoup, Tag
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import requests
from utils.helper_functions import get_path

def parse_industry_html(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.find("nav", id="subnav") or soup.find("nav", class_="subsec_nav")
    if not nav:
        raise RuntimeError("Could not find nav#subnav in HTML")

    industries = []
    # select anchors under each subLevel block
    for a in nav.select('div.subLevel > a[itemprop="url"], div.subLevel > a'):
        href = a.get("href")
        if not href or href.startswith("javascript"):
            continue
        name = a.get_text(" ", strip=True)
        # normalize relative links
        if href.startswith("/"):
            href = "https://economictimes.indiatimes.com" + href
        industries.append({"industry": name, "link": href})

    return pd.DataFrame(industries)

def parse_section_headlines(html: str) -> pd.DataFrame:
    """
    Parse ET industry/auto page HTML and return DataFrame with section & headline.
    Each <h2>/<h3> header defines a section, and the following <li> items contain headlines.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows, seen = [], set()

    # loop through each section header (h2/h3 with <a>)
    for header in soup.find_all(['h2', 'h3']):
        a = header.find('a')
        if not a:
            continue
        section = a.get_text(" ", strip=True)

        # find next header to know where this section ends
        next_header = header.find_next(['h2', 'h3'])
        sib = header.next_sibling
        collected_lis = []

        # collect all <li> until the next header
        while sib is not None and sib is not next_header:
            if isinstance(sib, Tag):
                collected_lis.extend(sib.find_all('li'))
            sib = sib.next_sibling

        for li in collected_lis:
            for anchor in li.find_all('a'):
                text = anchor.get_text(" ", strip=True)
                if not text or text == section or len(text) < 3:
                    continue
                key = (section, text)
                if key in seen:
                    continue
                seen.add(key)
                rows.append({"section": section, "headline": text})

    return pd.DataFrame(rows, columns=["section", "headline"])

if __name__ == "__main__":
    industry_page_url = "https://m.economictimes.com/industry"
    headers = {"User-Agent": "Mozilla/5.0"}
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response_industry = requests.get(industry_page_url, headers=headers)

    # print(f'Status Code - Industry Page : {response_industry.status_code}')

    df_ind = parse_industry_html(response_industry.text)

    output_df = pd.DataFrame()

    for _, row in tqdm(df_ind.iterrows(), total=len(df_ind)):
        response_headlines = requests.get(row['link'], headers=headers)

        df_head = parse_section_headlines(response_headlines.text)

        temp_df = pd.DataFrame({
            'Datetime': datetime_now, 
            'Industry': row['industry'],
            'Section': df_head['section'],
            'Headline': df_head['headline']
        })

        output_df = pd.concat([output_df, temp_df], axis=0)

    output_dir = get_path("src/data/dynamic/current_news")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"current_economic_news_{datetime_now}.csv"
    output_df.to_csv(file_path, index=False)
