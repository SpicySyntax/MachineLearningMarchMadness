import csv
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
import re
class TeamYearRecord:
    def __init__(self):
        # record info
        self.year = 0
        self.team_link = ''
        # team info
        self.team_name = ''
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
    def __init__(self, year_str):
        self.year_string = year_str
        self.team_1_name = ''
        self.team_1_score = 0
        self.team_2_name = ''
        self.team_2_score = 0
        self.date_string = ''
    def team_1_won(self):
        if(self.team_1_score > self.team_2_score):
            return True
        return False
    def team_2_won(self):
        if(self.team_2_score > self.team_1_score):
            return True
        return False
    def populate_with_game_result_string(self, game_result_str):
        num_date_and_venue, schools_and_outcome, score = game_result_str.split(",")
        pd_index = num_date_and_venue.find('.')
        date_and_venue = num_date_and_venue[pd_index:]
        date = ''
        if('@' in date_and_venue):
            date, venue = date_and_venue.split("@")
        elif('(Neutral)' in date_and_venue):
            date, neut = date_and_venue.split('(')
        else:
            date = date_and_venue
        date = date.replace(" ", "")
        school_1_and_outcome, school_2 = schools_and_outcome.split('vs.')
        record_pattern = r"\([0-9]+-[0-9]+\)"
        matches = re.findall(record_pattern, school_1_and_outcome)
        splitter = ' '
        if(len(matches)>0):
            splitter = matches[0]
        school_1, rest = school_1_and_outcome.split(splitter)                  
        school_1_score, school_2_score = score.split('-')
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
class Scrape:
    def __init__(self):
        pass
    def scrapeYearOfData(self, year):
        url = 'https://www.sports-reference.com/cbb/seasons/' + year + '-school-stats.html'
        chrome_options = Options()  
        chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        chrome_driver_exe_path = os.path.dirname(os.path.realpath(__file__)) + '\chromedriver.exe'
        browser = webdriver.Chrome(executable_path=chrome_driver_exe_path,   chrome_options=chrome_options)
        browser.maximize_window()
        browser.get(url) #navigate to page 
        headers = browser.find_elements_by_xpath("//thead//tr//th[contains(@class, 'poptip')]")
        table = browser.find_element_by_xpath("//table[contains(@class, 'stats_table')]")
        data_rows = table.find_elements_by_xpath(".//tbody//tr")
        data_rows = [_ for _ in data_rows if 'thead' not  in _.get_attribute('class') or 't']
        school_records = []
        game_records_t1 = {}
        game_records_t2 = {}
        game_records = []
        print '---Data Rows for ' + year + '---'
        for row in data_rows:    
            th_item = row.find_element_by_tag_name("th")
            if(th_item):
                th_rk_val = th_item.text
                if(not is_number(th_rk_val)):
                    continue
                row_num = row.get_attribute("data-row")
                # If Here then it is a true data row
                #print row_num
                #print 'th: ' + th_rk_val
            td_items = row.find_elements_by_tag_name("td")
            school_record = TeamYearRecord()
            school_record.year = self.getNum(year)
            num_games = 1
            conf_wins = 0
            conf_losses = 1
            for td_item in td_items:
                txt = td_item.text
                data_stat = td_item.get_attribute('data-stat')
                # Assumes we receive column data in the following order
                if(data_stat == 'school_name'):
                    school_record.team_name = txt
                    link = td_item.find_element_by_tag_name('a').get_attribute('href')
                    school_record.team_link = link
                elif(data_stat == 'win_loss_pct'):
                    school_record.wl_pct = self.getNum(txt)
                elif(data_stat == 'g'):
                    num_games = self.getNum(txt)
                elif(data_stat == 'srs'): 
                    school_record.srs = self.getNum(txt)
                elif(data_stat == 'sos'):
                    school_record.sos = self.getNum(txt)
                elif(data_stat == 'wins_conf'):
                    conf_wins = self.getNum(txt)
                elif(data_stat == 'losses_conf'):
                    conf_losses = self.getNum(txt)  
                elif(data_stat == 'pts'):
                    school_record.pt_pg = self.getNum(txt) / num_games
                elif(data_stat == 'opp_pts'):
                    school_record.opnt_pt_pg = self.getNum(txt) / num_games
                elif(data_stat == 'fg'):
                    school_record.fg_pg = self.getNum(txt) / num_games
                elif(data_stat == 'fg_pct'):
                    school_record.fg_pct = self.getNum(txt)
                elif(data_stat == 'fg3'):
                    school_record.three_pt_pg = self.getNum(txt) / num_games
                elif(data_stat == 'fg3_pct'):
                    school_record.three_p_pct = self.getNum(txt)
                elif(data_stat == 'ft'):
                    school_record.ft_pg = self.getNum(txt) / num_games
                elif(data_stat == 'ft_pct'):
                    school_record.ft_pct = self.getNum(txt)
                elif(data_stat == 'orb'):
                    school_record.orb_pg = self.getNum(txt) / num_games
                elif(data_stat == 'trb'):
                    school_record.drb_pg = (self.getNum(txt) - school_record.orb_pg) / num_games
                elif(data_stat == 'ast'):
                    school_record.ast_pg = self.getNum(txt) / num_games
                elif(data_stat == 'stl'):
                    school_record.stl_pg = self.getNum(txt) / num_games
                elif(data_stat == 'blk'):
                    school_record.blk_pg = self.getNum(txt) / num_games
                elif(data_stat == 'tov'):
                    school_record.tov_pg = self.getNum(txt) / num_games
                elif(data_stat == 'pf'):
                    school_record.pf_pg = self.getNum(txt) / num_games
                else:
                    continue
            school_record.conf_wl_pct = conf_wins / (conf_losses + conf_wins) if conf_losses != 0 else 1
            school_records.append(school_record)

        for school_record in school_records:
            browser.get(school_record.team_link)
            timeline_results = browser.find_element_by_xpath("//div[@id='timeline_results']").find_elements_by_xpath(".//li[@class='result']")
            for result in timeline_results:
                gr = GameRecord(year)
                gr.populate_with_game_result_string(result.text)
                date = gr.date_string
                if(date + gr.team_1_name in game_records_t2):
                    continue
                else:                   
                    game_records_t2[date + gr.team_2_name] = True
                    game_records.append(gr)
        browser.close()
        return school_records, game_records
    def write_school_records_csv(self, school_records):
        if(len(school_records) == 0):
            return
        outfile = open("./school_records.csv", "wb")
        writer = csv.writer(outfile)
        writer.writerow([
            "year", "team_name","fg_pg","ft_pg","three_pt_pg",
            "orb_pg", "drb_pg", "ast_pg", "stl_pg","blk_pg", "tov_pg",
            "pf_pg", "pt_pg",  "opnt_pt_pg", "fg_pct", "three_p_pct",
            "ft_pct", "wl_pct", "conf_wl_pct", "srs", "sos"
        ])
        for school_record in school_records:       
            writer.writerow([str(school_record.year), school_record.team_name, str(school_record.fg_pg), 
                str(school_record.ft_pg), str(school_record.three_pt_pg), str(school_record.orb_pg),
                str(school_record.drb_pg), str(school_record.ast_pg), str(school_record.stl_pg),
                str(school_record.blk_pg), str(school_record.tov_pg), str(school_record.pf_pg),
                str(school_record.pt_pg), str(school_record.opnt_pt_pg), str(school_record.fg_pct),
                str(school_record.three_p_pct), str(school_record.ft_pct), str(school_record.wl_pct),
                str(school_record.conf_wl_pct), str(school_record.srs), str(school_record.sos)
                ])
    def write_game_records_csv(self, game_records):
        if(len(game_records) == 0):
            return
        outfile = open("./game_records.csv", "wb")
        writer = csv.writer(outfile)
        writer.writerow([
            "year_string"
            "team_1_name", "team_1_score", "team_2_name",
            "team_2_score", "date_string"
            ])
        for game_record in game_records:
            writer.writerow([
                game_record.year_string,
                game_record.team_1_name, str(game_record.team_1_score),
                game_record.team_2_name, str(game_record.team_2_score),
                game_record.date_string
            ])
    def getNum(self, txt):
        try:
            return float(txt)
        except:
            return -1
    def run(self):
        year = 2010
        total_school_records = []
        total_game_records = []
        while(year < 2019):
            school_records, game_records = self.scrapeYearOfData(str(year))
            year = year + 1
            total_school_records = total_school_records + school_records
            total_game_records = total_game_records + game_records
        self.write_school_records_csv(total_school_records)
        self.write_game_records_csv(total_game_records)

if __name__ == "__main__":
    scrape = Scrape()
    scrape.run()
        


