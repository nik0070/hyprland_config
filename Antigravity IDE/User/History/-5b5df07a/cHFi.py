import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import time
from utils.helper_functions import get_path

BASE_URL = "https://zerodha.com"

async def get_sector_links(page):
    await page.goto(f"{BASE_URL}/markets/sector/", timeout=60000)
    await page.wait_for_selector("a[href*='/markets/sector/']", timeout=30000)
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/markets/sector/") and href != "/markets/sector/":
            links.add(BASE_URL + href)
    return list(links)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        links = await get_sector_links(page)
        await browser.close()
        return links


def run():
    sector_links = asyncio.run(main())
    print(f"Found {len(sector_links)} sector links.")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    all_dfs = []  # We keep DataFrames in memory instead of saving loose CSV files

    for link in tqdm(sector_links):
        driver.get(link)
        time.sleep(5)

        data = []
        sector_name = link.split("/")[-2]

        i = 1
        while True:
            try:
                company_xpath = f"/html/body/main/div/div[4]/div[2]/a[{i}]/div/div[1]/div"
                market_cap_xpath = f"/html/body/main/div/div[4]/div[2]/a[{i}]/div/div[2]/div[1]"
                pe_xpath = f"/html/body/main/div/div[4]/div[2]/a[{i}]/div/div[2]/div[2]"

                company = driver.find_element(By.XPATH, company_xpath).text.strip()
                market_cap = driver.find_element(By.XPATH, market_cap_xpath).text.strip()
                pe = driver.find_element(By.XPATH, pe_xpath).text.strip()

                data.append([sector_name, company, market_cap, pe])
                i += 1
            except:
                break

        if data:
            df = pd.DataFrame(data, columns=["sector", "company", "market_cap", "PE"])
            all_dfs.append(df)

    driver.quit()

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        save_path = get_path("src/data/static/stock_sectors.csv")
        final_df.to_csv(save_path, index=False)
        print(f"Saved {len(final_df)} rows to {save_path}")

if __name__ == "__main__":
    run()
