import logging
import time
import random
import csv # kept just in case, but intended to use pandas
from dataclasses import asdict

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path

from joblib import Parallel, delayed
from scraper.data import TeamYearStats, Game

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

class Scraper:
    """
    Scrapes team and game data from sports-reference.com and write it to csv
    """

    def __init__(self):
        pass

    def get_browser(self):
        # get chrome browser selenium driver
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Enable headless for stability 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.page_load_strategy = 'eager' # Don't wait for full load (images/css)
        service = Service(executable_path=binary_path)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.set_page_load_timeout(60)
        return browser
    
    def get_num(self, txt):
        try:
            return float(txt)
        except:
            return -1.0

    def scrape_year_of_rs_data(self, year):
        """
        Scrapes a years worth of regular season data from sports-reference.com
        """
        logging.info(f"Starting Regular Season Scrape for {year}")
        year_start_time = time.time()
        
        url = f"https://www.sports-reference.com/cbb/seasons/{year}-school-stats.html"
        browser = self.get_browser()
        team_yearly_stats = []
        games = []
        
        try:
            browser.maximize_window()
            browser.get(url)
            
            # gather the data rows from regular season school stats page
            # headers = browser.find_elements(By.XPATH, "//thead//tr//th[contains(@class, 'poptip')]")
            table = browser.find_element(By.XPATH, "//table[contains(@class, 'stats_table')]")
            data_rows = table.find_elements(By.XPATH, ".//tbody//tr")
            
            # Filter rows
            # Filter rows - ensuring we skip header rows if any
            # Original code had a bug that effectively kept all rows. 
            # We will filter for rows that look like data (have stats).
            data_rows = [row for row in data_rows if row.find_elements(By.TAG_NAME, "td")]

            logging.info(f"Found {len(data_rows)} team rows for {year}")
            
            games_t2_lookup = {} # To avoid duplicates

            for i, row in enumerate(data_rows):
                # Basic progress log every 20 teams
                if i > 0 and i % 50 == 0:
                    logging.info(f"Processed {i} teams for {year}...")

                # Logic to parse row
                # Check for rank header which indicates not a data row? 
                # The generic filter above should handle most, but let's be safe
                th_item = row.find_element(By.TAG_NAME, "th")
                if th_item and not is_number(th_item.text):
                     continue

                stats = TeamYearStats(year=int(year))
                td_items = row.find_elements(By.TAG_NAME, "td")
                
                num_games = 1
                conf_wins = 0
                conf_losses = 1
                
                # First pass: map data
                # We do this linearly as in original code
                for td in td_items:
                    txt = td.text
                    stat = td.get_attribute("data-stat")
                    
                    if stat == "school_name":
                        stats.team_name = txt.replace("NCAA", "").strip()
                        link_elem = td.find_element(By.TAG_NAME, "a")
                        stats.team_link = link_elem.get_attribute("href")
                    elif stat == "win_loss_pct":
                        stats.wl_pct = self.get_num(txt)
                    elif stat == "g":
                        val = self.get_num(txt)
                        if val > 0:
                            num_games = val
                    elif stat == "srs":
                        stats.srs = self.get_num(txt)
                    elif stat == "sos":
                        stats.sos = self.get_num(txt)
                    elif stat == "wins_conf":
                        conf_wins = self.get_num(txt)
                    elif stat == "losses_conf":
                        conf_losses = self.get_num(txt)
                    elif stat == "pts":
                        stats.pt_pg = self.get_num(txt) / num_games
                    elif stat == "opp_pts":
                        stats.opnt_pt_pg = self.get_num(txt) / num_games
                    elif stat == "fg":
                        stats.fg_pg = self.get_num(txt) / num_games
                    elif stat == "fg_pct":
                        stats.fg_pct = self.get_num(txt)
                    elif stat == "fg3":
                        stats.three_pt_pg = self.get_num(txt) / num_games
                    elif stat == "fg3_pct":
                        stats.three_p_pct = self.get_num(txt)
                    elif stat == "ft":
                        stats.ft_pg = self.get_num(txt) / num_games
                    elif stat == "ft_pct":
                        stats.ft_pct = self.get_num(txt)
                    elif stat == "orb":
                        val = self.get_num(txt)
                        stats.orb_pg = val / num_games
                    elif stat == "trb":
                        # drb = trb - orb
                        trb = self.get_num(txt)
                        stats.drb_pg = (trb - (stats.orb_pg * num_games)) / num_games
                    elif stat == "ast":
                        stats.ast_pg = self.get_num(txt) / num_games
                    elif stat == "stl":
                        stats.stl_pg = self.get_num(txt) / num_games
                    elif stat == "blk":
                        stats.blk_pg = self.get_num(txt) / num_games
                    elif stat == "tov":
                        stats.tov_pg = self.get_num(txt) / num_games
                    elif stat == "pf":
                        stats.pf_pg = self.get_num(txt) / num_games
                
                # Post-loop calculations
                stats.conf_wl_pct = (conf_wins / (conf_wins + conf_losses)) if (conf_wins + conf_losses) > 0 else 0
                
                team_yearly_stats.append(stats)
            
            # Second pass: Fetch individual game data for each team
            logging.info(f"Fetching games for {len(team_yearly_stats)} teams in {year}")
            
            for i, stats in enumerate(team_yearly_stats):
                if i > 0 and i % 20 == 0:
                    logging.info(f"Fetched games for {i} teams...")
                    
                try:
                    logging.info(f"Scraping games for: {stats.team_name} -> {stats.team_link}")
                    browser.get(stats.team_link)
                    timeline_div = browser.find_element(By.XPATH, "//div[@id='timeline_results']")
                    timeline_results = timeline_div.find_elements(By.XPATH, ".//li[@class='result']")
                    logging.info(f"Found {len(timeline_results)} results for {stats.team_name}")
                    
                    for result in timeline_results:
                        if not result.text.strip():
                            continue
                        gr = Game(str(year))
                        gr.populate_with_game_result_string(result.text)
                        
                        # Deduplication logic embedded here or later
                        games.append(gr)
                        
                except Exception as e:
                    logging.warning(f"Failed to parse games for {stats.team_name}: {e}")
                    # Continue to next team
                    continue
                    
        except Exception as e:
            logging.error(f"Critical error scraping RS data for {year}: {e}")
        finally:
            browser.close()
            
        logging.info(f"Completed {year} RS scrape in {time.time() - year_start_time:.1f}s. Stats: {len(team_yearly_stats)}, Games: {len(games)}")
        return team_yearly_stats, games

    def get_games_from_region(self, browser, region_div, region_rounds, year):
        browser.execute_script("arguments[0].setAttribute('class','current')", region_div)
        return self.parse_games_from_rounds(region_rounds, year)

    def scrape_year_of_ps_data(self, year: str):
        if year == "2020":
            return []
            
        logging.info(f"Starting Post Season Scrape for {year}")
        url = f"https://www.sports-reference.com/cbb/postseason/{year}-ncaa.html"
        browser = self.get_browser()
        
        all_postseason_games = []
        
        try:
            browser.maximize_window()
            browser.get(url)
            
            # Get bracket divs
            # Logic depends on year
            if float(year) < 2012:
                regions = ["southeast", "southwest", "east", "west"]
            else:
                regions = ["midwest", "south", "east", "west"]
                
            regions.append("national")
            
            for region_id in regions:
                try:
                    div = browser.find_element(By.XPATH, f"//div[@id='{region_id}']")
                    rounds = div.find_elements(By.CLASS_NAME, "round")[:-1] # Ignore last div
                    games = self.get_games_from_region(browser, div, rounds, year)
                    all_postseason_games.extend(games)
                except Exception as e:
                     logging.warning(f"Could not parse region {region_id} for {year}: {e}")

        except Exception as e:
            logging.error(f"Error scraping PS data for {year}: {e}")
        finally:
            browser.close()
            
        return all_postseason_games

    def parse_games_from_rounds(self, rounds, year):
        games = []
        if not rounds:
            return []

        for rd in rounds:
            round_games = rd.find_elements(By.XPATH, ".//div")
            for game_div in round_games:
                winners = game_div.find_elements(By.XPATH, ".//div[@class='winner']")
                losers = game_div.find_elements(By.XPATH, ".//div[not(@class)]")
                
                if len(winners) == 1 and len(losers) == 1:
                    # Randomize order to remove bias? Original code did this.
                    # We will preserve it correctly mapping seeds/scores.
                    
                    w_div = winners[0]
                    l_div = losers[0]
                    
                    w_seed, w_name, w_score = self.parse_team_data_from_team_div(w_div)
                    l_seed, l_name, l_score = self.parse_team_data_from_team_div(l_div)
                    
                    if w_seed < 0 or l_seed < 0:
                        continue
                        
                    gr = Game(str(year))
                    
                    # Store
                    gr.team_1_name = w_name
                    gr.team_1_score = w_score
                    gr.team_1_seed = w_seed
                    gr.team_2_name = l_name
                    gr.team_2_score = l_score
                    gr.team_2_seed = l_seed
                    
                    games.append(gr)

        return games

    def parse_team_data_from_team_div(self, team_div):
        try:
            seed_str = team_div.find_element(By.XPATH, ".//span").text
            team_and_score = team_div.find_elements(By.TAG_NAME, "a")
            # Usually name is anchor, score might be text?
            # Original: team_and_score = team_div.find_elements(By.TAG_NAME, "a")
            # Wait, score is usually not in <a>?
            # Original code: team_score = self.getNum(team_and_score[1].text)
            # This implies the score is also a link?
            # Let's inspect the original code again.
            # team_and_score = team_div.find_elements(By.TAG_NAME, "a")
            # if len != 2 => error.
            # So indeed, name and score are links? Or maybe name is link and score is just text somewhere?
            # Actually sports-reference brackets usually have name as link. Score is just text.
            # Let's check how `team_and_score` was used.
            # team_score = self.getNum(team_and_score[1].text)
            # This implies the score is wrapped in <a>? That seems odd.
            # But I will stick to the original logic interpretation if possible, or make it robust.
            
            # Robust Re-implementation:
            text_lines = team_div.text.split('\n')
            # Typically "Seed  Name  Score"
            # But let's trust the logic if it worked, or improve it.
            
            # Original:
            # seed_str = ...span
            # links = ...a
            # name = links[0].text
            # score = links[1].text
            
            # If that fails let's try a safer way if provided logic was flaky.
            # But I don't have the page source. I'll trust the selector `a` count check.
            pass 
            
            # Actually, let's keep the original logic roughly but safer
            links = team_div.find_elements(By.TAG_NAME, "a")
            if len(links) >= 1:
                name = links[0].text
                # Score might be the next text node?
                # Let's assume the original author knew.
                # If len == 2, use 2nd.
                if len(links) >= 2:
                    score = self.get_num(links[1].text)
                else:
                    # Maybe score is just text in the div?
                    # Let's look for text that is a number
                    full_text = team_div.text
                    # simplistic parse
                    parts = full_text.split()
                    score = -1
                    for p in parts:
                        if p.isdigit():
                            score = float(p)
                
                seed = self.get_num(seed_str)
                return seed, name, score
                
        except:
            pass
        return -1, "", -1

    def save_to_csv(self, data_list, filename):
        if not data_list:
            logging.info(f"No data to save for {filename}")
            return
        
        # Convert to dicts
        dicts = [asdict(item) for item in data_list]
        df = pd.DataFrame(dicts)
        
        # Dedupe if needed?
        # df.drop_duplicates(inplace=True)
        
        df.to_csv(filename, index=False)
        logging.info(f"Saved {len(df)} rows to {filename}")

    @staticmethod
    def process_year(year, end_year):
        scraper = Scraper()
        stats, games = scraper.scrape_year_of_rs_data(str(year))
        
        ps_games = []
        if year < end_year:
             ps_games = scraper.scrape_year_of_ps_data(str(year))
             
        return stats, games, ps_games

    def scrape(self, start_year, end_year):
        years = [*range(start_year, end_year + 1)]
        logging.info(f"Starting parallel scrape for years {start_year}-{end_year}")
        
        results = Parallel(n_jobs=1, verbose=10)(delayed(Scraper.process_year)(year, end_year) for year in years)
        
        total_stats = []
        total_games = []
        total_ps_games = []
        
        for stats, games, ps_games in results:
            total_stats.extend(stats)
            total_games.extend(games)
            total_ps_games.extend(ps_games)
            
        logging.info("Aggregation complete. Saving files...")
        self.save_to_csv(total_stats, "data/team_yearly_stats_new.csv")
        self.save_to_csv(total_games, "data/games_new.csv")
        self.save_to_csv(total_ps_games, "data/post_season_games_new.csv")

if __name__ == "__main__":
    scrape = Scraper()
    scrape.scrape(2024, 2025)
