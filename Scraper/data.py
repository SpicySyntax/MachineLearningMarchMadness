import re

class TeamYearStats:
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
        # percentages
        self.fg_pct = 0
        self.three_p_pct = 0
        self.ft_pct = 0
        self.wl_pct = 0
        self.conf_wl_pct = 0
        # conferece/schedule
        self.srs = 0
        self.sos = 0


class Game:
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