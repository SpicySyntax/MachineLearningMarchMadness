from dataclasses import dataclass, field
import re

@dataclass
class TeamYearStats:
    """
    Team Statistics for the Year
    """
    # record info
    year: int = 0
    team_link: str = ""
    # team info
    team_name: str = ""
    # per game
    fg_pg: float = 0.0
    ft_pg: float = 0.0
    three_pt_pg: float = 0.0
    orb_pg: float = 0.0
    drb_pg: float = 0.0
    ast_pg: float = 0.0
    stl_pg: float = 0.0
    blk_pg: float = 0.0
    tov_pg: float = 0.0
    pf_pg: float = 0.0
    pt_pg: float = 0.0
    opnt_pt_pg: float = 0.0
    # percentages
    fg_pct: float = 0.0
    three_p_pct: float = 0.0
    ft_pct: float = 0.0
    wl_pct: float = 0.0
    conf_wl_pct: float = 0.0
    # conferece/schedule
    srs: float = 0.0
    sos: float = 0.0


@dataclass
class Game:
    """
    Data Record for Single Game Outcome
    """
    year_string: str
    team_1_name: str = ""
    team_1_score: float = 0.0
    team_2_name: str = ""
    team_2_score: float = 0.0
    date_string: str = ""
    team_1_seed: float = 0.0
    team_2_seed: float = 0.0

    def populate_with_game_result_string(self, game_result_str):
        # Takes the game result string provided from team page regular season game
        # display and parse the game record from it
        try:
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
            
            # Helper to safely split
            parts = school_1_and_outcome.split(splitter)
            school_1 = parts[0]
            # rest = parts[1] if len(parts) > 1 else "" # Unused currently
            
            school_1_score, school_2_score = score.split("-")
            
            self.date_string = date.strip().strip(".")
            self.team_1_name = school_1.lstrip().rstrip()
            self.team_1_score = float(school_1_score.strip())
            self.team_2_name = school_2.strip()
            self.team_2_score = float(school_2_score.strip())
        except Exception as e:
            # Doing a broad catch here to avoid crashing on malformed lines, 
            # though logging would be better suited in the calling scope.
            print(f"Error parsing game result string '{game_result_str}': {e}")
