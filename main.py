from scraper.scraper import Scraper

if __name__ == "__main__":
    scrape = Scraper()
    scrape.scrape(2025, 2026, skip_regular_season=False)