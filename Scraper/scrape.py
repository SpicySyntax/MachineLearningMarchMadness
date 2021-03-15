import csv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
import random
from selenium.webdriver.support.ui import WebDriverWait
from chromedriver_py import binary_path # this will get you the path variable


# TODO: Cleanup up this whole file

# Data Record Classes
class TeamYearRecord:
    """
    Team Statistics for the Year
    """

    def __init__(self):
        # record info
        self.year = 0
        self.team_link = ""
        # team info
        self.team_name = ""
        # per game
        self.fg_pg = 0
        self.ft_pg = 0
        self.three_pt_pg = 0
        self.orb_pg = 0
        self.drb_pg = 0
        self.ast_pg = 0
        self.stl_pg = 0
        self.blk_pg = 0
        self.tov_pg = 0
        self.pf_pg = 0
        self.pt_pg = 0
        self.opnt_pt_pg = 0
        # percent
        self.fg_pct = 0
        self.three_p_pct = 0
        self.ft_pct = 0
        self.wl_pct = 0
        self.conf_wl_pct = 0
        # conferece/schedule
        self.srs = 0
        self.sos = 0


class GameRecord:
    """
    Data Record for Single Game Outcome
    """

    def __init__(self, year_str):
        self.year_string = year_str
        self.team_1_name = ""
        self.team_1_score = 0
        self.team_2_name = ""
        self.team_2_score = 0
        self.date_string = ""
        self.team_1_seed = 0
        self.team_2_seed = 0

    def populate_with_game_result_string(self, game_result_str):
        # Takes the game result string provided from team page regular season game
        # display and parse the game record from it
        num_date_and_venue, schools_and_outcome, score = game_result_str.split(",")
        pd_index = num_date_and_venue.find(".")
        date_and_venue = num_date_and_venue[pd_index:]
        date = ""
        if "@" in date_and_venue:
            date, venue = date_and_venue.split("@")
        elif "(Neutral)" in date_and_venue:
            date, neut = date_and_venue.split("(")
        else:
            date = date_and_venue
        date = date.replace(" ", "")
        school_1_and_outcome, school_2 = schools_and_outcome.split("vs.")
        record_pattern = r"\([0-9]+-[0-9]+\)"
        matches = re.findall(record_pattern, school_1_and_outcome)
        splitter = " "
        if len(matches) > 0:
            splitter = matches[0]
        school_1, rest = school_1_and_outcome.split(splitter)
        school_1_score, school_2_score = score.split("-")
        self.date_string = date.strip().strip(".")
        self.team_1_name = school_1.lstrip().rstrip()
        self.team_1_score = float(school_1_score.strip())
        self.team_2_name = school_2.strip()
        self.team_2_score = float(school_2_score.strip())


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
        school_records = []
        game_records_t1 = {}
        game_records_t2 = {}
        game_records = []
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
            school_record = TeamYearRecord()
            school_record.year = self.getNum(year)
            num_games = 1
            conf_wins = 0
            conf_losses = 1
            for td_item in td_items:
                txt = td_item.text
                data_stat = td_item.get_attribute("data-stat")
                # Assumes we receive column data in the following order
                if data_stat == "school_name":
                    school_record.team_name = txt.replace("NCAA", "").strip()
                    link = td_item.find_element_by_tag_name("a").get_attribute("href")
                    school_record.team_link = link
                elif data_stat == "win_loss_pct":
                    school_record.wl_pct = self.getNum(txt)
                elif data_stat == "g":
                    num_games = self.getNum(txt)
                elif data_stat == "srs":
                    school_record.srs = self.getNum(txt)
                elif data_stat == "sos":
                    school_record.sos = self.getNum(txt)
                elif data_stat == "wins_conf":
                    conf_wins = self.getNum(txt)
                elif data_stat == "losses_conf":
                    conf_losses = self.getNum(txt)
                elif data_stat == "pts":
                    school_record.pt_pg = self.getNum(txt) / num_games
                elif data_stat == "opp_pts":
                    school_record.opnt_pt_pg = self.getNum(txt) / num_games
                elif data_stat == "fg":
                    school_record.fg_pg = self.getNum(txt) / num_games
                elif data_stat == "fg_pct":
                    school_record.fg_pct = self.getNum(txt)
                elif data_stat == "fg3":
                    school_record.three_pt_pg = self.getNum(txt) / num_games
                elif data_stat == "fg3_pct":
                    school_record.three_p_pct = self.getNum(txt)
                elif data_stat == "ft":
                    school_record.ft_pg = self.getNum(txt) / num_games
                elif data_stat == "ft_pct":
                    school_record.ft_pct = self.getNum(txt)
                elif data_stat == "orb":
                    school_record.orb_pg = self.getNum(txt) / num_games
                elif data_stat == "trb":
                    school_record.drb_pg = (
                        self.getNum(txt) - school_record.orb_pg
                    ) / num_games
                elif data_stat == "ast":
                    school_record.ast_pg = self.getNum(txt) / num_games
                elif data_stat == "stl":
                    school_record.stl_pg = self.getNum(txt) / num_games
                elif data_stat == "blk":
                    school_record.blk_pg = self.getNum(txt) / num_games
                elif data_stat == "tov":
                    school_record.tov_pg = self.getNum(txt) / num_games
                elif data_stat == "pf":
                    school_record.pf_pg = self.getNum(txt) / num_games
                else:
                    continue
            school_record.conf_wl_pct = (
                conf_wins / (conf_losses + conf_wins) if conf_losses != 0 else 1
            )
            school_records.append(school_record)

        for school_record in school_records:
            # TODO: add additional team record and player data here
            browser.get(school_record.team_link)
            timeline_results = browser.find_element_by_xpath(
                "//div[@id='timeline_results']"
            ).find_elements_by_xpath(".//li[@class='result']")
            for result in timeline_results:
                gr = GameRecord(year)
                gr.populate_with_game_result_string(result.text)
                date = gr.date_string
                if date + gr.team_1_name in game_records_t2:
                    continue
                else:
                    game_records_t2[date + gr.team_2_name] = True
                    game_records.append(gr)
        # Close browser and return school and game records for the given year
        browser.close()
        return school_records, game_records

    def get_games_from_region(self, browser, region_div, region_rounds, year):
        # Manually override class so that the proper data for the given region is shown
        browser.execute_script(
            "arguments[0].setAttribute('class','current')", region_div
        )
        return self.parse_games_from_rounds(region_rounds, year)

    def scrape_year_of_ps_data(self, year):
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
                gr = GameRecord(str(year))
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

    def write_post_season_game_records_csv(self, game_records):
        # Writes all of the given game records to csv (post season include seeds)
        if len(game_records) == 0:
            return
        outfile = open("./post_season_game_records.csv", "w", newline="")
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
        for game_record in game_records:
            writer.writerow(
                [
                    game_record.year_string,
                    game_record.team_1_name,
                    str(game_record.team_1_score),
                    str(game_record.team_1_seed),
                    game_record.team_2_name,
                    str(game_record.team_2_score),
                    str(game_record.team_2_seed),
                ]
            )

    def write_school_records_csv(self, school_records):
        # Writes all school records to csv
        if len(school_records) == 0:
            return
        outfile = open("./school_records.csv", "w", newline="")
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
        for school_record in school_records:
            writer.writerow(
                [
                    str(school_record.year),
                    school_record.team_name,
                    str(school_record.fg_pg),
                    str(school_record.ft_pg),
                    str(school_record.three_pt_pg),
                    str(school_record.orb_pg),
                    str(school_record.drb_pg),
                    str(school_record.ast_pg),
                    str(school_record.stl_pg),
                    str(school_record.blk_pg),
                    str(school_record.tov_pg),
                    str(school_record.pf_pg),
                    str(school_record.pt_pg),
                    str(school_record.opnt_pt_pg),
                    str(school_record.fg_pct),
                    str(school_record.three_p_pct),
                    str(school_record.ft_pct),
                    str(school_record.wl_pct),
                    str(school_record.conf_wl_pct),
                    str(school_record.srs),
                    str(school_record.sos),
                ]
            )

    def write_game_records_csv(self, game_records):
        # Writes all regular season game records to csv
        if len(game_records) == 0:
            return
        outfile = open("./game_records.csv", "w", newline="")
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
        for game_record in game_records:
            writer.writerow(
                [
                    game_record.year_string,
                    game_record.team_1_name,
                    str(game_record.team_1_score),
                    game_record.team_2_name,
                    str(game_record.team_2_score),
                    game_record.date_string,
                ]
            )

    def getNum(self, txt):
        try:
            return float(txt)
        except:
            return -1

    def run(self, start_year, end_year):
        # top level method for fetching all desired team and game data from 'start_year' to 'end_year'
        year = start_year
        total_school_records = []
        total_game_records = []
        total_post_season_game_records = []
        while year <= end_year:
            school_records, game_records = self.scrape_year_of_rs_data(str(year))
            total_school_records = total_school_records + school_records
            total_game_records = total_game_records + game_records
            if year < end_year:
                post_season_gr = self.scrape_year_of_ps_data(str(year))
                total_post_season_game_records = (
                    total_post_season_game_records + post_season_gr
                )
            year = year + 1
        self.write_school_records_csv(total_school_records)
        self.write_game_records_csv(total_game_records)
        self.write_post_season_game_records_csv(total_post_season_game_records)


# By Default Scrape data from 2011-2019
if __name__ == "__main__":
    scrape = Scraper()
    scrape.run(2011, 2021)
