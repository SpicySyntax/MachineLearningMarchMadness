import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import random
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path # this will get you the path variable
from scraper.data import TeamYearStats, Game
from joblib import Parallel, delayed

# TODO: clean up this whole file, sorry to whomever is reading this

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
        # Do nothing for now
        pass

    def get_browser(self):
        # get chrome browser selenium driver
        chrome_options = Options()

        browser = webdriver.Chrome(
            executable_path=binary_path, chrome_options=chrome_options
        )
        return browser

    def scrape_year_of_rs_data(self, year):
        """
        Scrapes a years worth of regular season data from sports-reference.com
        """
        url = (
            "https://www.sports-reference.com/cbb/seasons/"
            + year
            + "-school-stats.html"
        )
        browser = self.get_browser()
        browser.maximize_window()  # Make sure all data is displayed for dynamic web page by maximizing
        browser.get(url)  # navigate to page
        # gather the data rows from regular season school stats page
        headers = browser.find_elements_by_xpath(
            "//thead//tr//th[contains(@class, 'poptip')]"
        )
        table = browser.find_element_by_xpath(
            "//table[contains(@class, 'stats_table')]"
        )
        data_rows = table.find_elements_by_xpath(".//tbody//tr")
        data_rows = [
            _ for _ in data_rows if "thead" not in _.get_attribute("class") or "t"
        ]
        # now we will fetch all relevant data from the table and then cache the link to each team page for game data retreival later
        team_yearly_stats = []
        games_t1 = {}
        games_t2 = {}
        games = []
        print("---Data Rows for " + year + "---")
        for row in data_rows:
            th_item = row.find_element_by_tag_name("th")
            if th_item:
                th_rk_val = th_item.text
                if not is_number(th_rk_val):
                    continue
                row_num = row.get_attribute("data-row")
            # If Here then it is a true data row
            td_items = row.find_elements_by_tag_name("td")
            team_yearly_stat_record = TeamYearStats()
            team_yearly_stat_record.year = self.getNum(year)
            num_games = 1
            conf_wins = 0
            conf_losses = 1
            for td_item in td_items:
                txt = td_item.text
                data_stat = td_item.get_attribute("data-stat")
                # Assumes we receive column data in the following order
                if data_stat == "school_name":
                    team_yearly_stat_record.team_name = txt.replace("NCAA", "").strip()
                    link = td_item.find_element_by_tag_name("a").get_attribute("href")
                    team_yearly_stat_record.team_link = link
                elif data_stat == "win_loss_pct":
                    team_yearly_stat_record.wl_pct = self.getNum(txt)
                elif data_stat == "g":
                    if self.getNum(txt) == 0:
                        continue
                    else:
                        num_games = self.getNum(txt)
                elif data_stat == "srs":
                    team_yearly_stat_record.srs = self.getNum(txt)
                elif data_stat == "sos":
                    team_yearly_stat_record.sos = self.getNum(txt)
                elif data_stat == "wins_conf":
                    conf_wins = self.getNum(txt)
                elif data_stat == "losses_conf":
                    conf_losses = self.getNum(txt)
                elif data_stat == "pts":
                    team_yearly_stat_record.pt_pg = self.getNum(txt) / num_games
                elif data_stat == "opp_pts":
                    team_yearly_stat_record.opnt_pt_pg = self.getNum(txt) / num_games
                elif data_stat == "fg":
                    team_yearly_stat_record.fg_pg = self.getNum(txt) / num_games
                elif data_stat == "fg_pct":
                    team_yearly_stat_record.fg_pct = self.getNum(txt)
                elif data_stat == "fg3":
                    team_yearly_stat_record.three_pt_pg = self.getNum(txt) / num_games
                elif data_stat == "fg3_pct":
                    team_yearly_stat_record.three_p_pct = self.getNum(txt)
                elif data_stat == "ft":
                    team_yearly_stat_record.ft_pg = self.getNum(txt) / num_games
                elif data_stat == "ft_pct":
                    team_yearly_stat_record.ft_pct = self.getNum(txt)
                elif data_stat == "orb":
                    team_yearly_stat_record.orb_pg = self.getNum(txt) / num_games
                elif data_stat == "trb":
                    team_yearly_stat_record.drb_pg = (
                        self.getNum(txt) - team_yearly_stat_record.orb_pg
                    ) / num_games
                elif data_stat == "ast":
                    team_yearly_stat_record.ast_pg = self.getNum(txt) / num_games
                elif data_stat == "stl":
                    team_yearly_stat_record.stl_pg = self.getNum(txt) / num_games
                elif data_stat == "blk":
                    team_yearly_stat_record.blk_pg = self.getNum(txt) / num_games
                elif data_stat == "tov":
                    team_yearly_stat_record.tov_pg = self.getNum(txt) / num_games
                elif data_stat == "pf":
                    team_yearly_stat_record.pf_pg = self.getNum(txt) / num_games
                else:
                    continue
            team_yearly_stat_record.conf_wl_pct = (
                conf_wins / (conf_losses + conf_wins) if conf_losses != 0 else 1
            )
            team_yearly_stats.append(team_yearly_stat_record)

        for team_yearly_stat_record in team_yearly_stats:
            # TODO: add additional team record and player data here
            browser.get(team_yearly_stat_record.team_link)
            timeline_results = browser.find_element_by_xpath(
                "//div[@id='timeline_results']"
            ).find_elements_by_xpath(".//li[@class='result']")
            for result in timeline_results:
                gr = Game(year)
                gr.populate_with_game_result_string(result.text)
                date = gr.date_string
                if date + gr.team_1_name in games_t2:
                    continue
                else:
                    games_t2[date + gr.team_2_name] = True
                    games.append(gr)
        # Close browser and return school and game records for the given year
        browser.close()
        return team_yearly_stats, games

    def get_games_from_region(self, browser, region_div, region_rounds, year):
        # Manually override class so that the proper data for the given region is shown
        browser.execute_script(
            "arguments[0].setAttribute('class','current')", region_div
        )
        return self.parse_games_from_rounds(region_rounds, year)

    def scrape_year_of_ps_data(self, year: str):
        if year == "2020": # fuck covid19
            return None
        # Go to post season page for the given year
        url = "https://www.sports-reference.com/cbb/postseason/" + year + "-ncaa.html"
        browser = self.get_browser()
        browser.maximize_window()  # Make sure all data is displayed for dynamic web page by maximizing
        browser.get(url)  # navigate to page
        # All possible lists of games for post seasons
        all_postseason_games = []
        southeast_rounds = []
        southwest_rounds = []
        midwest_rounds = []
        south_rounds = []
        southeast_games = []
        southwest_games = []
        midwest_games = []
        south_games = []
        southeast = {}
        southwest = {}
        midwest = {}
        south = {}
        # Get bracket divs
        bracket = browser.find_element_by_xpath("//div[@id='brackets']")
        # (regions depend on the year of the tourney (i.e. < 2012))
        if float(year) < 2012:
            southeast = browser.find_element_by_xpath("//div[@id='southeast']")
            southwest = browser.find_element_by_xpath("//div[@id='southwest']")
            # Ignore the last div here
            southeast_rounds = southeast.find_elements_by_class_name("round")[:-1]
            southwest_rounds = southwest.find_elements_by_class_name("round")[:-1]
            southeast_games = self.get_games_from_region(
                browser, southeast, southeast_rounds, year
            )
            southwest_games = self.get_games_from_region(
                browser, southwest, southwest_rounds, year
            )
        else:
            midwest = browser.find_element_by_xpath("//div[@id='midwest']")
            south = browser.find_element_by_xpath("//div[@id='south']")
            # Ignore the last div here
            south_rounds = south.find_elements_by_class_name("round")[:-1]
            midwest_rounds = midwest.find_elements_by_class_name("round")[:-1]
            midwest_games = self.get_games_from_region(
                browser, midwest, midwest_rounds, year
            )
            south_games = self.get_games_from_region(browser, south, south_rounds, year)
        # West east and national are always there
        west = browser.find_element_by_xpath("//div[@id='west']")
        east = browser.find_element_by_xpath("//div[@id='east']")
        national = browser.find_element_by_xpath("//div[@id='national']")
        # Last round is just the winner for subbracket div -> ignore
        east_rounds = east.find_elements_by_class_name("round")[:-1]
        west_rounds = west.find_elements_by_class_name("round")[:-1]
        national_rounds = national.find_elements_by_class_name("round")[:-1]
        west_games = self.get_games_from_region(browser, west, west_rounds, year)
        east_games = self.get_games_from_region(browser, east, east_rounds, year)
        national_games = self.get_games_from_region(
            browser, national, national_rounds, year
        )
        # combine all of the games yielded from above
        all_postseason_games = [
            east_games,
            west_games,
            southeast_games,
            southwest_games,
            midwest_games,
            south_games,
            national_games,
        ]
        all_postseason_games = sum(all_postseason_games, [])
        # close browser and return the record of post season games
        browser.close()
        return all_postseason_games

    def parse_games_from_rounds(self, rounds, year):
        # Get the individual game records from each round of a bracket/sub-bracket
        games = []
        if len(rounds) < 1:
            print(" rounds were empty...")
            return []

        for rd in rounds:
            # all children divs will be picked up
            winners = rd.find_elements_by_xpath(".//div//div[@class='winner']")
            losers = rd.find_elements_by_xpath(".//div//div[not(@class)]")
            print(len(winners), len(losers))
            if len(winners) != len(losers):
                print("Error num losers != num winners for a round")
                return []
            i = 0
            for winner in winners:
                if bool(random.getrandbits(1)):
                    t1_seed, t1_name, t1_score = self.parse_team_data_from_team_div(
                        winner
                    )
                    t2_seed, t2_name, t2_score = self.parse_team_data_from_team_div(
                        losers[i]
                    )
                else:
                    t1_seed, t1_name, t1_score = self.parse_team_data_from_team_div(
                        losers[i]
                    )
                    t2_seed, t2_name, t2_score = self.parse_team_data_from_team_div(
                        winner
                    )
                if t1_seed < 0 or t2_seed < 0:
                    print(" Negative seed...")
                    continue
                gr = Game(str(year))
                gr.team_1_name = t1_name
                gr.team_1_score = t1_score
                gr.team_1_seed = t1_seed
                gr.team_2_name = t2_name
                gr.team_2_score = t2_score
                gr.team_2_seed = t2_seed

                games.append(gr)
                i = i + 1
                # TODO : add location fetching for v2 here
        return games

    def parse_team_data_from_team_div(self, team_div):
        # Get team level information for post season game-team div
        seed_str = team_div.find_element_by_xpath(".//span").text
        team_and_score = team_div.find_elements_by_tag_name("a")
        if len(team_and_score) != 2:
            print("Error parsing team for post season games")
            return False, False, False
        team_name = team_and_score[0].text
        team_score = self.getNum(team_and_score[1].text)
        seed = self.getNum(seed_str)
        return seed, team_name, team_score

    def write_post_season_games_csv(self, games):
        # TODO: replace with to_csv https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
        # Writes all of the given game records to csv (post season include seeds)
        if len(games) == 0:
            return
        outfile = open("./post_season_games.csv", "w", newline="")
        writer = csv.writer(outfile)
        writer.writerow(
            [
                "year",
                "team_1_name",
                "team_1_score",
                "team_1_seed",
                "team_2_name",
                "team_2_score",
                "team_2_seed",
            ]
        )
        for game in games:
            writer.writerow(
                [
                    game.year_string,
                    game.team_1_name,
                    str(game.team_1_score),
                    str(game.team_1_seed),
                    game.team_2_name,
                    str(game.team_2_score),
                    str(game.team_2_seed),
                ]
            )

    def write_team_yearly_stats_csv(self, team_yearly_stats):
        # TODO: replace with to_csv https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
        # Writes all school records to csv
        if len(team_yearly_stats) == 0:
            return
        outfile = open("./team_yearly_stats.csv", "w", newline="")
        writer = csv.writer(outfile)
        writer.writerow(
            [
                "year",
                "team_name",
                "fg_pg",
                "ft_pg",
                "three_pt_pg",
                "orb_pg",
                "drb_pg",
                "ast_pg",
                "stl_pg",
                "blk_pg",
                "tov_pg",
                "pf_pg",
                "pt_pg",
                "opnt_pt_pg",
                "fg_pct",
                "three_p_pct",
                "ft_pct",
                "wl_pct",
                "conf_wl_pct",
                "srs",
                "sos",
            ]
        )
        for team_yearly_stat_record in team_yearly_stats:
            writer.writerow(
                [
                    str(team_yearly_stat_record.year),
                    team_yearly_stat_record.team_name,
                    str(team_yearly_stat_record.fg_pg),
                    str(team_yearly_stat_record.ft_pg),
                    str(team_yearly_stat_record.three_pt_pg),
                    str(team_yearly_stat_record.orb_pg),
                    str(team_yearly_stat_record.drb_pg),
                    str(team_yearly_stat_record.ast_pg),
                    str(team_yearly_stat_record.stl_pg),
                    str(team_yearly_stat_record.blk_pg),
                    str(team_yearly_stat_record.tov_pg),
                    str(team_yearly_stat_record.pf_pg),
                    str(team_yearly_stat_record.pt_pg),
                    str(team_yearly_stat_record.opnt_pt_pg),
                    str(team_yearly_stat_record.fg_pct),
                    str(team_yearly_stat_record.three_p_pct),
                    str(team_yearly_stat_record.ft_pct),
                    str(team_yearly_stat_record.wl_pct),
                    str(team_yearly_stat_record.conf_wl_pct),
                    str(team_yearly_stat_record.srs),
                    str(team_yearly_stat_record.sos),
                ]
            )

    def write_games_csv(self, games):
        # TODO: replace with to_csv https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
        # Writes all regular season game records to csv
        if len(games) == 0:
            return
        outfile = open("./games.csv", "w", newline="")
        writer = csv.writer(outfile)
        writer.writerow(
            [
                "year",
                "team_1_name",
                "team_1_score",
                "team_2_name",
                "team_2_score",
                "date_string",
            ]
        )
        for game in games:
            writer.writerow(
                [
                    game.year_string,
                    game.team_1_name,
                    str(game.team_1_score),
                    game.team_2_name,
                    str(game.team_2_score),
                    game.date_string,
                ]
            )

    def getNum(self, txt):
        try:
            return float(txt)
        except:
            return -1

    def scrape(self, start_year, end_year):
        # top level method for fetching all desired team and game data from 'start_year' to 'end_year'

        total_team_yearly_stats = []
        total_games = []
        total_post_season_games = []
        years = [*range(start_year, end_year + 1)]

        for year in years: # TODO: parallelize this https://stackoverflow.com/questions/42732958/python-parallel-execution-with-selenium
            team_yearly_stats, games = self.scrape_year_of_rs_data(str(year))
            total_team_yearly_stats = total_team_yearly_stats + team_yearly_stats
            total_games = total_games + games
            if year < end_year:
                post_season_gr = self.scrape_year_of_ps_data(str(year))
                if post_season_gr:
                    total_post_season_games = (
                        total_post_season_games + post_season_gr
                    )

        self.write_team_yearly_stats_csv(total_team_yearly_stats)
        self.write_games_csv(total_games)
        self.write_post_season_games_csv(total_post_season_games)


# By Default Scrape data from 2011-2021
if __name__ == "__main__":
    scrape = Scraper()
    scrape.scrape(2011, 2021)
