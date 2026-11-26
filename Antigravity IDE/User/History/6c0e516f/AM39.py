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
    Parses the Headlines from the Industry links
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    seen = set()

    # 1. Standard Heading-based sections (Auto News, Cars & UVs, Railways, etc.)
    for h in soup.find_all(['h2', 'h3']):
        sec_name = h.get_text(" ", strip=True)
        # Skip site headers or navigation junk
        if not sec_name or len(sec_name) < 3 or len(sec_name) > 40:
            continue
        if sec_name in ['Most Popular', 'Trending Now', 'More From', 'Top News from ET', 'Download ET App:']:
            continue

        next_h = h.find_next(['h2', 'h3'])
        sib = h.next_sibling
        while sib and sib != next_h:
            if isinstance(sib, Tag):
                for a in sib.find_all('a'):
                    txt = a.get_text(" ", strip=True)
                    href = a.get("href", "")
                    if len(txt) > 20 and not txt.startswith("More From") and txt != sec_name:
                        if ('articleshow' in href or '.cms' in href or '/industry/' in href) and txt not in seen:
                            seen.add(txt)
                            rows.append({"section": sec_name, "headline": txt})
            sib = sib.next_sibling

    # 2. Container-based sections (Solar Energy, Wind Energy, EVs on Renewables)
    for div in soup.find_all('div', class_=re.compile(r'subsec', re.I)):
        title_tag = div.find(['h2', 'h3', 'h4'])
        if not title_tag:
            continue
        sec_name = title_tag.get_text(" ", strip=True)
        if len(sec_name) > 40 or "More" in sec_name:
            continue

        for a in div.find_all('a'):
            txt = a.get_text(" ", strip=True)
            href = a.get("href", "")
            if len(txt) > 20 and not txt.startswith("More From") and txt != sec_name:
                if txt not in seen:
                    seen.add(txt)
                    rows.append({"section": sec_name, "headline": txt})

    return pd.DataFrame(rows, columns=["section", "headline"])

def et_news_scraper():
    industry_page_url = "https://m.economictimes.com/industry"
    headers = {"User-Agent": "Mozilla/5.0"}
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    response_industry = requests.get(industry_page_url, headers=headers)

    # print(f'Status Code - Industry Page : {response_industry.status_code}')

    df_ind = parse_industry_html(response_industry.text)
    
    # Sending the output to outputs/validation for validating if number of industries is consistently scraped or not
    industry_validation = get_path("outputs/validation")
    inv_file_path = industry_validation / f"eco_news_industry_list_{datetime_now}.csv"
    df_ind.to_csv(inv_file_path, index=False)


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
    file_path = output_dir / f"current_economic_news_{datetime_now}.csv"
    output_df.to_csv(file_path, index=False)

if __name__ == "__main__":
    et_news_scraper()

