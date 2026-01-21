"""
Web scraper for college basketball data from sports-reference.com.
Uses requests + BeautifulSoup for fast, efficient scraping with rate limiting.
"""

import csv
import logging
import os
import random
import re
import time
from dataclasses import dataclass, field
from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scraper.data import Game, TeamYearStats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def is_number(s: str) -> bool:
    """Check if a string can be converted to a number."""
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
    Scrapes team and game data from sports-reference.com and writes it to CSV.
    Uses requests + BeautifulSoup for performance instead of Selenium.
    """

    BASE_URL = "https://www.sports-reference.com"
    
    def __init__(self, delay: float = 3.5):
        """
        Initialize the scraper.
        
        Args:
            delay: Seconds to wait between requests (rate limiting).
                   Sports-Reference limits to 20 requests/minute, so 3.5s minimum.
        """
        self.delay = max(delay, 3.5)  # Enforce minimum 3.5s delay
        self.session = self._create_session()
        self.request_count = 0

    def _create_session(self) -> requests.Session:
        """Create a requests session with NO automatic retries - we handle everything manually."""
        session = requests.Session()
        
        # DISABLE all automatic retries - we handle rate limiting ourselves
        # This prevents urllib3 from sleeping on Retry-After headers
        retry_strategy = Retry(
            total=0,  # No automatic retries
            respect_retry_after_header=False  # Don't auto-sleep on Retry-After
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set headers to mimic a browser
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        
        return session

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a page with rate limiting and error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if fetch failed
        """
        # Rate limiting - Sports-Reference allows max 20 requests/minute
        # We use 3.5+ second delay to stay safely under limit
        wait_time = self.delay + random.uniform(0, 0.5)
        
        # Log what we're about to do
        short_url = url.split("/")[-1] if "/" in url else url
        print(f"[{self.request_count + 1}] Fetching: {short_url}...", end=" ", flush=True)
        
        time.sleep(wait_time)
        self.request_count += 1
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 429:
                # Rate limited - we've been "jailed". Wait for the site's timeout.
                print(f"RATE LIMITED (429)!")
                logger.error("Rate limited (429)! Waiting 60 seconds before retry...")
                logger.error("Consider increasing delay if this persists.")
                for i in range(60, 0, -10):
                    print(f"  Waiting {i}s...", flush=True)
                    time.sleep(10)
                print("Retrying...", flush=True)
                return self._fetch_page(url)  # Single retry
            
            response.raise_for_status()
            print(f"OK ({len(response.text)} bytes)", flush=True)
            
            # Log progress summary every 25 requests
            if self.request_count % 25 == 0:
                logger.info(f"  === Progress: {self.request_count} requests completed ===")
            
            return BeautifulSoup(response.text, "lxml")
            
        except requests.RequestException as e:
            print(f"FAILED: {e}", flush=True)
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def _get_num(self, txt: str) -> float:
        """Convert text to number, returning -1 if conversion fails."""
        try:
            return float(txt)
        except (ValueError, TypeError):
            return -1

    def scrape_year_of_rs_data(self, year: str) -> tuple[list[TeamYearStats], list[Game]]:
        """
        Scrape a year's worth of regular season data.
        
        Args:
            year: Year to scrape (e.g., "2024")
            
        Returns:
            Tuple of (team_yearly_stats, games)
        """
        url = f"{self.BASE_URL}/cbb/seasons/men/{year}-school-stats.html"
        logger.info(f"Scraping regular season data for {year} from {url}")
        
        soup = self._fetch_page(url)
        if not soup:
            logger.error(f"Failed to fetch school stats page for {year}")
            return [], []

        # Find the stats table
        table = soup.find("table", class_="stats_table")
        if not table:
            logger.error(f"Could not find stats table for {year}")
            return [], []

        tbody = table.find("tbody")
        if not tbody:
            logger.error(f"Could not find table body for {year}")
            return [], []

        data_rows = tbody.find_all("tr")
        team_yearly_stats = []
        
        logger.info(f"Processing {len(data_rows)} team rows for {year}")
        
        for row in data_rows:
            # Skip header rows
            if "thead" in row.get("class", []):
                continue
                
            th_item = row.find("th")
            if not th_item:
                continue
                
            th_rk_val = th_item.get_text(strip=True)
            if not is_number(th_rk_val):
                continue

            # Parse team data from row
            team_stat = self._parse_team_row(row, year)
            if team_stat:
                team_yearly_stats.append(team_stat)

        logger.info(f"Found {len(team_yearly_stats)} teams for {year}")
        
        # Scrape game data from team pages sequentially (rate limit: 20 req/min)
        logger.info(f"Scraping game data from {len(team_yearly_stats)} team pages (this will take ~{len(team_yearly_stats) * 4 // 60} minutes)...")
        
        games = self._scrape_team_games_sequential(team_yearly_stats, year)
        
        logger.info(f"Found {len(games)} games for {year}")
        return team_yearly_stats, games

    def _parse_team_row(self, row, year: str) -> Optional[TeamYearStats]:
        """Parse a team's stats from a table row."""
        team_stat = TeamYearStats()
        team_stat.year = self._get_num(year)
        
        num_games = 1
        conf_wins = 0
        conf_losses = 1
        
        td_items = row.find_all("td")
        
        for td in td_items:
            txt = td.get_text(strip=True)
            data_stat = td.get("data-stat", "")
            
            if data_stat == "school_name":
                team_stat.team_name = txt.replace("NCAA", "").strip()
                link = td.find("a")
                if link:
                    team_stat.team_link = self.BASE_URL + link.get("href", "")
            elif data_stat == "win_loss_pct":
                team_stat.wl_pct = self._get_num(txt)
            elif data_stat == "g":
                val = self._get_num(txt)
                if val == 0:
                    continue
                num_games = val
            elif data_stat == "srs":
                team_stat.srs = self._get_num(txt)
            elif data_stat == "sos":
                team_stat.sos = self._get_num(txt)
            elif data_stat == "wins_conf":
                conf_wins = self._get_num(txt)
            elif data_stat == "losses_conf":
                conf_losses = self._get_num(txt)
            elif data_stat == "pts":
                team_stat.pt_pg = self._get_num(txt) / num_games
            elif data_stat == "opp_pts":
                team_stat.opnt_pt_pg = self._get_num(txt) / num_games
            elif data_stat == "fg":
                team_stat.fg_pg = self._get_num(txt) / num_games
            elif data_stat == "fg_pct":
                team_stat.fg_pct = self._get_num(txt)
            elif data_stat == "fg3":
                team_stat.three_pt_pg = self._get_num(txt) / num_games
            elif data_stat == "fg3_pct":
                team_stat.three_p_pct = self._get_num(txt)
            elif data_stat == "ft":
                team_stat.ft_pg = self._get_num(txt) / num_games
            elif data_stat == "ft_pct":
                team_stat.ft_pct = self._get_num(txt)
            elif data_stat == "orb":
                team_stat.orb_pg = self._get_num(txt) / num_games
            elif data_stat == "trb":
                team_stat.drb_pg = (self._get_num(txt) - team_stat.orb_pg) / num_games
            elif data_stat == "ast":
                team_stat.ast_pg = self._get_num(txt) / num_games
            elif data_stat == "stl":
                team_stat.stl_pg = self._get_num(txt) / num_games
            elif data_stat == "blk":
                team_stat.blk_pg = self._get_num(txt) / num_games
            elif data_stat == "tov":
                team_stat.tov_pg = self._get_num(txt) / num_games
            elif data_stat == "pf":
                team_stat.pf_pg = self._get_num(txt) / num_games

        # Calculate conference win/loss percentage
        if conf_losses + conf_wins > 0:
            team_stat.conf_wl_pct = conf_wins / (conf_losses + conf_wins)
        else:
            team_stat.conf_wl_pct = 1
            
        return team_stat if team_stat.team_name else None

    def _scrape_team_games_sequential(self, team_stats: list[TeamYearStats], year: str) -> list[Game]:
        """Scrape game data from team pages sequentially to respect rate limits."""
        
        total_teams = len(team_stats)
        all_games = []
        seen_games = set()
        
        for i, team_stat in enumerate(team_stats):
            if not team_stat.team_link:
                continue
            
            soup = self._fetch_page(team_stat.team_link)
            if not soup:
                continue
            
            timeline = soup.find("div", id="timeline_results")
            if not timeline:
                continue
            
            results = timeline.find_all("li", class_="result")
            for result in results:
                try:
                    gr = Game(year)
                    gr.populate_with_game_result_string(result.get_text(strip=True))
                    
                    # Deduplicate games (same game appears on both team pages)
                    game_key = f"{gr.date_string}_{gr.team_1_name}"
                    reverse_key = f"{gr.date_string}_{gr.team_2_name}"
                    
                    if game_key not in seen_games and reverse_key not in seen_games:
                        seen_games.add(game_key)
                        seen_games.add(reverse_key)
                        all_games.append(gr)
                        
                except Exception as e:
                    logger.debug(f"Failed to parse game result: {e}")
                    continue
            
            # Log progress every 25 teams
            if (i + 1) % 25 == 0 or (i + 1) == total_teams:
                logger.info(f"  Team progress: {i + 1}/{total_teams}")
        
        return all_games

    def scrape_year_of_ps_data(self, year: str) -> list[Game]:
        """
        Scrape a year's worth of post-season (NCAA tournament) data.
        
        Args:
            year: Year to scrape
            
        Returns:
            List of tournament games
        """
        if year == "2020":  # No tournament in 2020 (COVID)
            return []
        
        url = f"{self.BASE_URL}/cbb/postseason/men/{year}-ncaa.html"
        logger.info(f"Scraping post-season data for {year}")
        
        soup = self._fetch_page(url)
        if not soup:
            logger.error(f"Failed to fetch post-season page for {year}")
            return []

        brackets = soup.find("div", id="brackets")
        if not brackets:
            logger.error(f"Could not find brackets div for {year}")
            return []

        all_games = []
        
        # Define region IDs to look for
        region_ids = ["east", "west", "midwest", "south", "southeast", "southwest", "national"]
        
        for region_id in region_ids:
            region_div = brackets.find("div", id=region_id)
            if not region_div:
                continue
            
            rounds = region_div.find_all("div", class_="round")
            games = self._parse_games_from_rounds(rounds, year)
            all_games.extend(games)
        
        logger.info(f"Found {len(all_games)} post-season games for {year}")
        return all_games

    def _parse_games_from_rounds(self, rounds, year: str) -> list[Game]:
        """Parse games from bracket rounds."""
        games = []
        
        for rd in rounds:
            # Find all game divs
            game_divs = rd.find_all("div", recursive=False)
            
            for game_div in game_divs:
                winner_div = game_div.find("div", class_="winner")
                loser_div = game_div.find("div", class_=lambda x: x is None or x == "")
                
                if not winner_div or not loser_div:
                    continue
                
                # Randomly assign teams to t1/t2 to avoid bias
                if random.getrandbits(1):
                    t1_data = self._parse_team_data_from_team_div(winner_div)
                    t2_data = self._parse_team_data_from_team_div(loser_div)
                else:
                    t1_data = self._parse_team_data_from_team_div(loser_div)
                    t2_data = self._parse_team_data_from_team_div(winner_div)
                
                if not t1_data or not t2_data:
                    continue
                
                t1_seed, t1_name, t1_score = t1_data
                t2_seed, t2_name, t2_score = t2_data
                
                if t1_seed < 0 or t2_seed < 0:
                    continue
                
                game = Game(year)
                game.team_1_name = t1_name
                game.team_1_score = t1_score
                game.team_1_seed = t1_seed
                game.team_2_name = t2_name
                game.team_2_score = t2_score
                game.team_2_seed = t2_seed
                
                games.append(game)
        
        return games

    def _parse_team_data_from_team_div(self, team_div) -> Optional[tuple[int, str, float]]:
        """Parse team data from a bracket team div."""
        try:
            seed_span = team_div.find("span")
            seed = self._get_num(seed_span.get_text(strip=True)) if seed_span else -1
            
            links = team_div.find_all("a")
            if len(links) < 2:
                return None
            
            team_name = links[0].get_text(strip=True)
            team_score = self._get_num(links[1].get_text(strip=True))
            
            return int(seed), team_name, team_score
        except Exception:
            return None

    def write_post_season_games_csv(self, games: list[Game]) -> None:
        """Write post-season games to CSV."""
        if not games:
            return
        
        os.makedirs("data", exist_ok=True)
        filepath = "data/post_season_games_new.csv"
        
        with open(filepath, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "year", "team_1_name", "team_1_score", "team_1_seed",
                "team_2_name", "team_2_score", "team_2_seed"
            ])
            
            for game in games:
                writer.writerow([
                    game.year_string,
                    game.team_1_name,
                    str(game.team_1_score),
                    str(game.team_1_seed),
                    game.team_2_name,
                    str(game.team_2_score),
                    str(game.team_2_seed)
                ])
        
        logger.info(f"Wrote {len(games)} post-season games to {filepath}")

    def write_team_yearly_stats_csv(self, team_yearly_stats: list[TeamYearStats]) -> None:
        """Write team yearly stats to CSV."""
        if not team_yearly_stats:
            return
        
        os.makedirs("data", exist_ok=True)
        filepath = "data/team_yearly_stats_new.csv"
        
        with open(filepath, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "year", "team_name", "fg_pg", "ft_pg", "three_pt_pg",
                "orb_pg", "drb_pg", "ast_pg", "stl_pg", "blk_pg",
                "tov_pg", "pf_pg", "pt_pg", "opnt_pt_pg", "fg_pct",
                "three_p_pct", "ft_pct", "wl_pct", "conf_wl_pct", "srs", "sos"
            ])
            
            for stat in team_yearly_stats:
                writer.writerow([
                    str(stat.year), stat.team_name,
                    str(stat.fg_pg), str(stat.ft_pg), str(stat.three_pt_pg),
                    str(stat.orb_pg), str(stat.drb_pg), str(stat.ast_pg),
                    str(stat.stl_pg), str(stat.blk_pg), str(stat.tov_pg),
                    str(stat.pf_pg), str(stat.pt_pg), str(stat.opnt_pt_pg),
                    str(stat.fg_pct), str(stat.three_p_pct), str(stat.ft_pct),
                    str(stat.wl_pct), str(stat.conf_wl_pct),
                    str(stat.srs), str(stat.sos)
                ])
        
        logger.info(f"Wrote {len(team_yearly_stats)} team stats to {filepath}")

    def write_games_csv(self, games: list[Game]) -> None:
        """Write regular season games to CSV."""
        if not games:
            return
        
        os.makedirs("data", exist_ok=True)
        filepath = "data/games_new.csv"
        
        with open(filepath, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([
                "year", "team_1_name", "team_1_score",
                "team_2_name", "team_2_score", "date_string"
            ])
            
            for game in games:
                writer.writerow([
                    game.year_string,
                    game.team_1_name,
                    str(game.team_1_score),
                    game.team_2_name,
                    str(game.team_2_score),
                    game.date_string
                ])
        
        logger.info(f"Wrote {len(games)} games to {filepath}")

    def scrape(self, start_year: int, end_year: int, skip_regular_season: bool = False) -> None:
        """
        Main entry point: scrape all data from start_year to end_year.
        
        Args:
            start_year: First year to scrape
            end_year: Last year to scrape (inclusive)
            skip_regular_season: Whether to skip regular season data (stats and games)
        """
        start_time = time.time()
        
        total_team_yearly_stats = []
        total_games = []
        total_post_season_games = []
        
        years = list(range(start_year, end_year + 1))
        logger.info(f"Starting scrape for years {start_year} to {end_year} (skip_rs={skip_regular_season})")

        for year in years:
            if not skip_regular_season:
                team_yearly_stats, games = self.scrape_year_of_rs_data(str(year))
                total_team_yearly_stats.extend(team_yearly_stats)
                total_games.extend(games)
            else:
                logger.info(f"Skipping regular season data for {year}")
            
            if year < end_year:
                post_season_games = self.scrape_year_of_ps_data(str(year))
                if post_season_games:
                    total_post_season_games.extend(post_season_games)

        if total_team_yearly_stats:
            self.write_team_yearly_stats_csv(total_team_yearly_stats)
        if total_games:
            self.write_games_csv(total_games)
        if total_post_season_games:
            self.write_post_season_games_csv(total_post_season_games)
        
        elapsed = time.time() - start_time
        logger.info(f"Scraping completed in {elapsed:.1f} seconds")
        logger.info(f"Total: {len(total_team_yearly_stats)} teams, {len(total_games)} games, {len(total_post_season_games)} post-season games")


# Default entry point
if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape(2011, 2022)
