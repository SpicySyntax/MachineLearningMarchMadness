from scraper.scraper import Scraper

if __name__ == "__main__":
    scrape = Scraper()
    scrape.scrape(2023, 2023, skip_regular_season=True)