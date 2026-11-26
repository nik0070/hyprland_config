from bs4 import BeautifulSoup, Tag
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import requests

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

