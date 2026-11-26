from scraper.daily.et_news import et_news
from scraper.daily.legislative_bills import prs_bills_scraper
from scraper.daily.upcoming_qtr_result_lst import upcoming_qtr_result_lst

def run_all_daily_scrapers():
    print("=" * 50)
    print("🚀 Starting Daily Market Data Ingestion")
    print("=" * 50)

    print("\n[1/3] Scraping Economic News...")
    et_news()

    print("\n[2/3] Scraping Legislative Bills...")
    prs_bills_scraper()

    print("\n[3/3] Scraping Upcoming Earnings Calendar...")
    upcoming_qtr_result_lst()

    print("\n" + "=" * 50)
    print("✅ All daily dynamic data refreshed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    run_all_daily_scrapers()
