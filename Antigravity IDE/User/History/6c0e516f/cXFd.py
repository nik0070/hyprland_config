from bs4 import BeautifulSoup, Tag
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import requests
from utils.helper_functions import get_path
import re

def parse_industry_html(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.find("nav", id="subnav") or soup.find("nav", class_=re.compile(r"subsec_nav", re.I))
    if not nav:
        raise RuntimeError("Could not find nav#subnav in HTML")

    industries = []
    seen = set()

    # 1. Grab visible industries (Auto, Banking, Energy, etc.)
    for div in nav.find_all("div", class_=re.compile(r"subLevel", re.I)):
        a = div.find("a")
        if not a:
            continue
        name = a.get_text(" ", strip=True)
        href = a.get("href")
        if not href or href.startswith("javascript") or name == "More":
            continue
        if href.startswith("/"):
            href = "https://economictimes.indiatimes.com" + href
        if href not in seen:
            seen.add(href)
            industries.append({"industry": name, "link": href})

    # 2. Grab dropdown industries from the 'More' menu (Transportation, Tech, Telecom, etc.)
    more_btn = nav.find(string=re.compile(r"^More", re.I))
    if more_btn:
        more_container = more_btn.find_parent("div")
        for a in more_container.find_all("a", class_=re.compile(r"subsec1", re.I)):
            name = a.get_text(" ", strip=True)
            href = a.get("href")
            if not href or href.startswith("javascript"):
                continue
            if href.startswith("/"):
                href = "https://economictimes.indiatimes.com" + href
            if href not in seen:
                seen.add(href)
                industries.append({"industry": name, "link": href})

    return pd.DataFrame(industries)

def parse_section_headlines(html: str) -> pd.DataFrame:
    """
    Parse ET section pages (handles both list-based and card-based layouts).
    """
    soup = BeautifulSoup(html, "html.parser")
    rows, seen = [], set()

    # Pattern A: Standard sections (Auto, Banking, Energy, Transport, etc.)
    for header in soup.find_all(['h2', 'h3']):
        section = header.get_text(" ", strip=True)
        # Skip site headers or oversized banner text
        if not section or len(section) < 3 or len(section) > 60:
            continue

        next_header = header.find_next(['h2', 'h3'])
        sib = header.next_sibling
        collected_anchors = []

        while sib is not None and sib is not next_header:
            if isinstance(sib, Tag):
                # Collect all article links (handles both <li> lists and <div> cards)
                collected_anchors.extend(sib.find_all('a'))
            sib = sib.next_sibling

        for anchor in collected_anchors:
            text = anchor.get_text(" ", strip=True)
            href = anchor.get("href", "")
            if not text or text == section or len(text) < 15 or text.startswith("More From"):
                continue
            # Ensure it is an actual news article link
            if any(k in href for k in ['/article', '/news/', '/industry/', '/tech/']):
                key = (section, text)
                if key not in seen:
                    seen.add(key)
                    rows.append({"section": section, "headline": text})

    # Pattern B: Card-based sections fallback (Renewables subsec divs)
    if len(rows) < 5:
        for ss in soup.find_all('div', class_=re.compile(r'subsec', re.I)):
            title_elem = ss.find(['h2', 'h3', 'h4'])
            section = title_elem.get_text(" ", strip=True) if title_elem else "General"
            for a in ss.find_all('a'):
                text = a.get_text(" ", strip=True)
                if not text or len(text) < 15 or text.startswith("More From"):
                    continue
                key = (section, text)
                if key not in seen:
                    seen.add(key)
                    rows.append({"section": section, "headline": text})

    return pd.DataFrame(rows, columns=["section", "headline"])


def et_news_scraper():
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

if __name__ == "__main__":
    et_news_scraper()

