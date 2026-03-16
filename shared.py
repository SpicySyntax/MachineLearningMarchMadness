"""
    Shared Helper Functions to be reused in notebooks
"""
import pandas as pd  # dataframes


def resolve_team_name(team_name):
    # Apply hard-coded corrections to team names
    team_name_dict = {
        "Colorado-Colorado Springs": "Colorado",
        "Colorado College": "Colorado",
        "UNC": "North Carolina",
        "UConn": "Connecticut",
        "LIU-Brooklyn": "Long Island University",
        "UTSA": "Texas-San Antonio",
        "Pitt": "Pittsburgh",
        "BYU": "Brigham Young",
        "St. Peter's": "Saint Peter's",
        "VCU": "Virginia Commonwealth",
        "Southern Miss": "Southern Mississippi",
        "Detroit": "Detroit Mercy",
        "UNLV": "Nevada-Las Vegas",
        "Ole Miss": "Mississippi",
        "St. Joseph's": "Saint Joseph's",
        "UCSB": "UC-Santa Barbara",
        "SMU": "Southern Methodist",
        "USC": "South Carolina",
        "LSU": "Louisiana State",
        "UMass": "Massachusetts",
        "ETSU": "East Tennessee State",
        "Ole Miss": "Mississippi",
        "Saint Mary's": "Saint Mary's (CA)",
        "UCSBS": "UC-Santa Barbara",
        "UNC Greensboro": "North Carolina-Greensboro",
        "LEH": "Lehigh",
        "St. John's": "St. John's (NY)",
        "Penn":"Pennsylvania",
        "Queens": "Queens (NC)",
        "UMBC": "Maryland-Baltimore County",
    }
    # TODO: for V2 add more corrections to the team_name_dict
    if team_name in team_name_dict:
        return team_name_dict[team_name]
    return team_name


def get_team_stats(df_team, year, team_name):
    return df_team[
        (df_team["year"] == year) & (df_team["team_name"] == team_name)
    ]


def get_vals(t_stats_list, key):
    ret = []
    for t_stat in t_stats_list:
        ret.append(t_stat[key].squeeze())
    return ret


def get_team_stats_dict_with_t1_win(t1_stats, t2_stats, t1_wins):
    return {
        "team_name_1": get_vals(t1_stats, "team_name"),
        "fg_pg_1": get_vals(t1_stats, "fg_pg"),
        "ft_pg_1": get_vals(t1_stats, "ft_pg"),
        "three_pt_pg_1": get_vals(t1_stats, "three_pt_pg"),
        "orb_pg_1": get_vals(t1_stats, "orb_pg"),
        "drb_pg_1": get_vals(t1_stats, "drb_pg"),
        "ast_pg_1": get_vals(t1_stats, "ast_pg"),
        "stl_pg_1": get_vals(t1_stats, "stl_pg"),
        "blk_pg_1": get_vals(t1_stats, "blk_pg"),
        "tov_pg_1": get_vals(t1_stats, "tov_pg"),
        "pf_pg_1": get_vals(t1_stats, "pf_pg"),
        "pt_pg_1": get_vals(t1_stats, "pt_pg"),
        "opnt_pt_pg_1": get_vals(t1_stats, "opnt_pt_pg"),
        "fg_pct_1": get_vals(t1_stats, "fg_pct"),
        "three_p_pct_1": get_vals(t1_stats, "three_p_pct"),
        "ft_pct_1": get_vals(t1_stats, "ft_pct"),
        "wl_pct_1": get_vals(t1_stats, "wl_pct"),
        "conf_wl_pct_1": get_vals(t1_stats, "conf_wl_pct"),
        "srs_1": get_vals(t1_stats, "srs"),
        "sos_1": get_vals(t1_stats, "sos"),
        "team_name_2": get_vals(t2_stats, "team_name"),
        "fg_pg_2": get_vals(t2_stats, "fg_pg"),
        "ft_pg_2": get_vals(t2_stats, "ft_pg"),
        "three_pt_pg_2": get_vals(t2_stats, "three_pt_pg"),
        "orb_pg_2": get_vals(t2_stats, "orb_pg"),
        "drb_pg_2": get_vals(t2_stats, "drb_pg"),
        "ast_pg_2": get_vals(t2_stats, "ast_pg"),
        "stl_pg_2": get_vals(t2_stats, "stl_pg"),
        "blk_pg_2": get_vals(t2_stats, "blk_pg"),
        "tov_pg_2": get_vals(t2_stats, "tov_pg"),
        "pf_pg_2": get_vals(t2_stats, "pf_pg"),
        "pt_pg_2": get_vals(t2_stats, "pt_pg"),
        "opnt_pt_pg_2": get_vals(t2_stats, "opnt_pt_pg"),
        "fg_pct_2": get_vals(t2_stats, "fg_pct"),
        "three_p_pct_2": get_vals(t2_stats, "three_p_pct"),
        "ft_pct_2": get_vals(t2_stats, "ft_pct"),
        "wl_pct_2": get_vals(t2_stats, "wl_pct"),
        "conf_wl_pct_2": get_vals(t2_stats, "conf_wl_pct"),
        "srs_2": get_vals(t2_stats, "srs"),
        "sos_2": get_vals(t2_stats, "sos"),
        "t1_win": t1_wins,
    }


def get_team_stats_dict(t1_stats, t2_stats):
    return {
        "team_name_1": get_vals(t1_stats, "team_name"),
        "fg_pg_1": get_vals(t1_stats, "fg_pg"),
        "ft_pg_1": get_vals(t1_stats, "ft_pg"),
        "three_pt_pg_1": get_vals(t1_stats, "three_pt_pg"),
        "orb_pg_1": get_vals(t1_stats, "orb_pg"),
        "drb_pg_1": get_vals(t1_stats, "drb_pg"),
        "ast_pg_1": get_vals(t1_stats, "ast_pg"),
        "stl_pg_1": get_vals(t1_stats, "stl_pg"),
        "blk_pg_1": get_vals(t1_stats, "blk_pg"),
        "tov_pg_1": get_vals(t1_stats, "tov_pg"),
        "pf_pg_1": get_vals(t1_stats, "pf_pg"),
        "pt_pg_1": get_vals(t1_stats, "pt_pg"),
        "opnt_pt_pg_1": get_vals(t1_stats, "opnt_pt_pg"),
        "fg_pct_1": get_vals(t1_stats, "fg_pct"),
        "three_p_pct_1": get_vals(t1_stats, "three_p_pct"),
        "ft_pct_1": get_vals(t1_stats, "ft_pct"),
        "wl_pct_1": get_vals(t1_stats, "wl_pct"),
        "conf_wl_pct_1": get_vals(t1_stats, "conf_wl_pct"),
        "srs_1": get_vals(t1_stats, "srs"),
        "sos_1": get_vals(t1_stats, "sos"),
        "team_name_2": get_vals(t2_stats, "team_name"),
        "fg_pg_2": get_vals(t2_stats, "fg_pg"),
        "ft_pg_2": get_vals(t2_stats, "ft_pg"),
        "three_pt_pg_2": get_vals(t2_stats, "three_pt_pg"),
        "orb_pg_2": get_vals(t2_stats, "orb_pg"),
        "drb_pg_2": get_vals(t2_stats, "drb_pg"),
        "ast_pg_2": get_vals(t2_stats, "ast_pg"),
        "stl_pg_2": get_vals(t2_stats, "stl_pg"),
        "blk_pg_2": get_vals(t2_stats, "blk_pg"),
        "tov_pg_2": get_vals(t2_stats, "tov_pg"),
        "pf_pg_2": get_vals(t2_stats, "pf_pg"),
        "pt_pg_2": get_vals(t2_stats, "pt_pg"),
        "opnt_pt_pg_2": get_vals(t2_stats, "opnt_pt_pg"),
        "fg_pct_2": get_vals(t2_stats, "fg_pct"),
        "three_p_pct_2": get_vals(t2_stats, "three_p_pct"),
        "ft_pct_2": get_vals(t2_stats, "ft_pct"),
        "wl_pct_2": get_vals(t2_stats, "wl_pct"),
        "conf_wl_pct_2": get_vals(t2_stats, "conf_wl_pct"),
        "srs_2": get_vals(t2_stats, "srs"),
        "sos_2": get_vals(t2_stats, "sos"),
    }


def get_team_stats_dict_ps(t1_stats, t2_stats, t1_seeds, t2_seeds):
    return {
        "team_name_1": get_vals(t1_stats, "team_name"),
        "fg_pg_1": get_vals(t1_stats, "fg_pg"),
        "ft_pg_1": get_vals(t1_stats, "ft_pg"),
        "three_pt_pg_1": get_vals(t1_stats, "three_pt_pg"),
        "orb_pg_1": get_vals(t1_stats, "orb_pg"),
        "drb_pg_1": get_vals(t1_stats, "drb_pg"),
        "ast_pg_1": get_vals(t1_stats, "ast_pg"),
        "stl_pg_1": get_vals(t1_stats, "stl_pg"),
        "blk_pg_1": get_vals(t1_stats, "blk_pg"),
        "tov_pg_1": get_vals(t1_stats, "tov_pg"),
        "pf_pg_1": get_vals(t1_stats, "pf_pg"),
        "pt_pg_1": get_vals(t1_stats, "pt_pg"),
        "opnt_pt_pg_1": get_vals(t1_stats, "opnt_pt_pg"),
        "fg_pct_1": get_vals(t1_stats, "fg_pct"),
        "three_p_pct_1": get_vals(t1_stats, "three_p_pct"),
        "ft_pct_1": get_vals(t1_stats, "ft_pct"),
        "wl_pct_1": get_vals(t1_stats, "wl_pct"),
        "conf_wl_pct_1": get_vals(t1_stats, "conf_wl_pct"),
        "srs_1": get_vals(t1_stats, "srs"),
        "sos_1": get_vals(t1_stats, "sos"),
        "team_name_2": get_vals(t2_stats, "team_name"),
        "fg_pg_2": get_vals(t2_stats, "fg_pg"),
        "ft_pg_2": get_vals(t2_stats, "ft_pg"),
        "three_pt_pg_2": get_vals(t2_stats, "three_pt_pg"),
        "orb_pg_2": get_vals(t2_stats, "orb_pg"),
        "drb_pg_2": get_vals(t2_stats, "drb_pg"),
        "ast_pg_2": get_vals(t2_stats, "ast_pg"),
        "stl_pg_2": get_vals(t2_stats, "stl_pg"),
        "blk_pg_2": get_vals(t2_stats, "blk_pg"),
        "tov_pg_2": get_vals(t2_stats, "tov_pg"),
        "pf_pg_2": get_vals(t2_stats, "pf_pg"),
        "pt_pg_2": get_vals(t2_stats, "pt_pg"),
        "opnt_pt_pg_2": get_vals(t2_stats, "opnt_pt_pg"),
        "fg_pct_2": get_vals(t2_stats, "fg_pct"),
        "three_p_pct_2": get_vals(t2_stats, "three_p_pct"),
        "ft_pct_2": get_vals(t2_stats, "ft_pct"),
        "wl_pct_2": get_vals(t2_stats, "wl_pct"),
        "conf_wl_pct_2": get_vals(t2_stats, "conf_wl_pct"),
        "srs_2": get_vals(t2_stats, "srs"),
        "sos_2": get_vals(t2_stats, "sos"),
        "team_1_seed": t1_seeds,
        "team_2_seed": t2_seeds,
    }


def create_team_stats_df_w_t1_win(
    indeces_w_stats, t1_stats_list, t2_stats_list, t1_wins
):
    # Adds column for whether team 1 wins or not
    # Assumes all lists are of the same length
    return pd.DataFrame(
        get_team_stats_dict_with_t1_win(t1_stats_list, t2_stats_list, t1_wins),
        index=indeces_w_stats,
    )


def create_team_stats_df(indeces_w_stats, t1_stats_list, t2_stats_list):
    # Assumes all lists are of the same length
    return pd.DataFrame(
        get_team_stats_dict(t1_stats_list, t2_stats_list), index=indeces_w_stats
    )


def create_team_stats_df_ps(
    indeces_w_stats, t1_stats_list, t2_stats_list, t1_seeds, t2_seeds
):
    # Only uses post season stats => inclu
    # Assumes all lists are of the same length
    return pd.DataFrame(
        get_team_stats_dict_ps(t1_stats_list, t2_stats_list, t1_seeds, t2_seeds),
        index=indeces_w_stats,
    )


def get_team_stats_df(df_team, game_df, should_print=False):
    indeces_w_stats = []
    t1_stats_list = []
    t2_stats_list = []
    t1_wins_list = []
    for index, row in game_df.iterrows():
        year = row["year"]
        team_1 = row["team_1_name"]
        team_2 = row["team_2_name"]
        team_1_score = row["team_1_score"]
        team_2_score = row["team_2_score"]
        t1_stats = get_team_stats(df_team, year, resolve_team_name(team_1))
        t2_stats = get_team_stats(df_team, year, resolve_team_name(team_2))

        if len(t1_stats) > 0 and len(t2_stats) > 0:
            indeces_w_stats.append(index)
            t1_stats_list.append(t1_stats)
            t2_stats_list.append(t2_stats)
            t1_wins_list.append(team_1_score > team_2_score)
        else:
            if should_print:
                print(year)
                if len(t1_stats) < 1:
                    print(team_1)
                if len(t2_stats) < 1:
                    print(team_2)

    team_stats_df = create_team_stats_df_w_t1_win(
        indeces_w_stats, t1_stats_list, t2_stats_list, t1_wins_list
    )
    return team_stats_df


def get_team_stats_df_vectorized(df_team, game_df):
    """
    Vectorized version of get_team_stats_df for better performance.
    """
    game_df = game_df.copy()

    # Resolve team names
    game_df["team_1_name"] = game_df["team_1_name"].apply(resolve_team_name)
    game_df["team_2_name"] = game_df["team_2_name"].apply(resolve_team_name)

    # Prepare df_team for merging
    df_team_1 = df_team.add_suffix("_1").rename(
        columns={"year_1": "year", "team_name_1": "team_1_name"}
    )
    df_team_2 = df_team.add_suffix("_2").rename(
        columns={"year_2": "year", "team_name_2": "team_2_name"}
    )

    # Merge
    merged = game_df.merge(df_team_1, on=["year", "team_1_name"], how="inner")
    merged = merged.merge(df_team_2, on=["year", "team_2_name"], how="inner")

    # Identify t1_win if scores exist
    if "team_1_score" in merged.columns and "team_2_score" in merged.columns:
        merged["t1_win"] = (merged["team_1_score"] > merged["team_2_score"]).astype(int)

    return merged


def get_matchups_stats(df_team, teams, post_season, year):
    i = 0
    t1_stats = []
    t2_stats = []
    t1_seeds = []
    t2_seeds = []
    if not is_power_of_two(len(teams)):
        print("ERROR: invalid number of team names")
        return False
    while i < len(teams):
        t1_name, t1_seed = teams[i]
        t2_name, t2_seed = teams[i + 1]
        t1_seeds.append(t1_seed)
        t2_seeds.append(t2_seed)
        t1_stats.append(get_team_stats(df_team, year, resolve_team_name(t1_name)))
        t2_stats.append(get_team_stats(df_team, year, resolve_team_name(t2_name)))
        i = i + 2
    
    # Check if all teams were found
    for idx, (t1_stat, t2_stat) in enumerate(zip(t1_stats, t2_stats)):
        if len(t1_stat) == 0:
            t1_name, _ = teams[idx * 2]
            raise ValueError(f"Team '{t1_name}' (resolved to '{resolve_team_name(t1_name)}') not found in database for year {year}")
        if len(t2_stat) == 0:
            t2_name, _ = teams[idx * 2 + 1]
            raise ValueError(f"Team '{t2_name}' (resolved to '{resolve_team_name(t2_name)}') not found in database for year {year}")
    
    if post_season:
        matchup_stats = create_team_stats_df_ps(
            range(0, int(len(teams) / 2)), t1_stats, t2_stats, t1_seeds, t2_seeds
        )
    else:
        matchup_stats = create_team_stats_df(
            range(0, int(len(teams) / 2)), t1_stats, t2_stats
        )
    return matchup_stats


def is_power_of_two(num):
    return (((num & (num - 1)) == 0) and num != 0) or num == 2


ps_feature_col_names = [
    "team_1_seed",
    "team_2_seed",
    "fg_pg_1",
    "ft_pg_1",
    "three_pt_pg_1",
    "orb_pg_1",
    "drb_pg_1",
    "ast_pg_1",
    "stl_pg_1",
    "blk_pg_1",
    "tov_pg_1",
    "pf_pg_1",
    "pt_pg_1",
    "opnt_pt_pg_1",
    "fg_pct_1",
    "three_p_pct_1",
    "ft_pct_1",
    "wl_pct_1",
    "conf_wl_pct_1",
    "srs_1",
    "sos_1",
    "fg_pg_2",
    "ft_pg_2",
    "three_pt_pg_2",
    "orb_pg_2",
    "drb_pg_2",
    "ast_pg_2",
    "stl_pg_2",
    "blk_pg_2",
    "tov_pg_2",
    "pf_pg_2",
    "pt_pg_2",
    "opnt_pt_pg_2",
    "fg_pct_2",
    "three_p_pct_2",
    "ft_pct_2",
    "wl_pct_2",
    "conf_wl_pct_2",
    "srs_2",
    "sos_2",
]
ps_predict_class_names = ["t1_win"]


# Setup This years bracket regions
# TODO: automate this with the data received from the scraper from https://www.sports-reference.com/cbb/postseason/2021-ncaa.html
# Note: we are ignoring some of the play in teams since 16 seeds are not frequent upset candidates
team_names_south = [
    # south region
    ("Duke", 1),
    ("Siena", 16),
    ("Ohio State", 8),
    ("TCU", 9),
    ("Wisconsin", 5),
    ("High Point", 12),
    ("Nebraska", 4),
    ("Troy", 13),
    ("Louisville", 6),
    ("South Florida", 11),
    ("Georgia", 3),
    ("Saint Louis", 14),
    ("Saint Mary's", 7),
    ("Texas A&M", 10),
    ("Houston", 2),
    ("Idaho", 15),
]
team_names_west = [
    # west region
    ("Arizona", 1),
    ("Long Island University", 16),
    ("Villanova", 8),
    ("Utah State", 9),
    ("Texas Tech", 5),
    ("Akron", 12),
    ("Alabama", 4),
    ("Hofstra", 13),
    ("Tennessee", 6),
    ("Mississippi", 11),
    ("Virginia", 3),
    ("Wright State", 14),
    ("Miami (FL)", 7),
    ("Missouri", 10),
    ("Iowa State", 2),
    ("Tennessee State", 15),
]
team_names_east = [
    # east region
    ("Florida", 1),
    ("LEH", 16),
    ("Clemson", 8),
    ("Iowa", 9),
    ("St. John's", 5),
    ("Northern Iowa", 12),
    ("Kansas", 4),
    ("California Baptist", 13),
    ("North Carolina", 6),
    ("VCU", 11),
    ("Illinois", 3),
    ("Penn", 14),
    ("UCLA", 7),
    ("UCF", 10),
    ("Purdue", 2),
    ("Queens", 15),
]
team_names_midwest = [
    # mid-west region
    ("Michigan", 1),
    ("UMBC", 16),
    ("Ohio State", 8),
    ("TCU", 9),
    ("Wisconsin", 5),
    ("High Point", 12),
    ("Nebraska", 4),
    ("Troy", 13),
    ("Louisville", 6),
    ("South Florida", 11),
    ("Gonzaga", 3),
    ("Kennesaw State", 14),
    ("Kentucky", 7),
    ("Santa Clara", 10),
    ("UConn", 2),
    ("Furman", 15),
]


def add_differentials(df):
    df = df.copy()
    # Safely calculate differentials if source columns exist
    if "team_1_seed" in df.columns and "team_2_seed" in df.columns:
        df["seed_diff"] = df["team_1_seed"] - df["team_2_seed"]
    if "pt_pg_1" in df.columns and "opnt_pt_pg_1" in df.columns:
        df["pt_diff_1"] = df["pt_pg_1"] - df["opnt_pt_pg_1"]
    if "pt_pg_2" in df.columns and "opnt_pt_pg_2" in df.columns:
        df["pt_diff_2"] = df["pt_pg_2"] - df["opnt_pt_pg_2"]
    if "srs_1" in df.columns and "srs_2" in df.columns:
        df["srs_diff"] = df["srs_1"] - df["srs_2"]
    if "sos_1" in df.columns and "sos_2" in df.columns:
        df["sos_diff"] = df["sos_1"] - df["sos_2"]
    if "wl_pct_1" in df.columns and "wl_pct_2" in df.columns:
        df["win_pct_diff"] = df["wl_pct_1"] - df["wl_pct_2"]
    return df


def get_matchup_winners(matchup_stats, teams, model, post_season, features=None):
    # Ensure differentials are calculated if needed by the model
    matchup_stats = add_differentials(matchup_stats)

    if features is not None:
        feature_cols = features
    elif post_season:
        feature_cols = ps_feature_col_names
    else:
        # Fallback for non-post-season if no features specified
        feature_cols = ps_feature_col_names

    # Ensure all requested features exist in the dataframe
    for col in feature_cols:
        if col not in matchup_stats.columns:
            matchup_stats[col] = 0

    x_tourney = matchup_stats[feature_cols]

    # Use predict_proba to get probabilities instead of hard predictions
    # This allows for more realistic upset predictions
    import numpy as np
    try:
        y_proba = model.predict_proba(x_tourney)[:, 1]  # Probability team 1 wins
    except AttributeError:
        # Fallback to predict if predict_proba not available
        y_proba = model.predict(x_tourney)

    i = 0
    winners = []
    for prob in y_proba:
        t1_name, t1_seed = teams[i]
        t2_name, t2_seed = teams[i + 1]
        
        # Sample based on probability for more realistic results
        team_1_wins = np.random.random() < prob
        team_1_wins_int = int(team_1_wins)
        
        print(t1_name, t1_seed, " vs. ", t2_name, t2_seed, f"(team 1 won= {team_1_wins_int}, prob={prob:.3f})")
        if team_1_wins:
            winners.append((t1_name, t1_seed))
        else:
            winners.append((t2_name, t2_seed))
        i = i + 2
    return winners


def evaluate_winner(df_team, teams, sub_bracket_name, model, year=2023, features=None):
    print("Evaluating Winner of ", sub_bracket_name)
    remaining_teams = teams
    i = 1
    while len(remaining_teams) > 1:
        post_season_stats = True
        print("---", sub_bracket_name, " round ", i, "---")
        matchup_stats = get_matchups_stats(
            df_team, remaining_teams, post_season_stats, year
        )
        remaining_teams = get_matchup_winners(
            matchup_stats, remaining_teams, model, post_season_stats, features=features
        )
        i = i + 1
    winner = remaining_teams[0]
    print("Winner of ", sub_bracket_name, ":", winner)
    print("=================================")
    return winner


def evaluate_tournament(df_team, model, year=2026, features=None):
    # Get predicted final four
    final_four = [
        evaluate_winner(df_team, team_names_south, "South", model, year, features),
        evaluate_winner(df_team, team_names_east, "East", model, year, features),
        evaluate_winner(df_team, team_names_midwest, "MidWest", model, year, features),
        evaluate_winner(df_team, team_names_west, "West", model, year, features),
    ]
    print("================================")
    champ = evaluate_winner(df_team, final_four, "FinalFour", model, year, features)
    print("========= Bracket Winner =========")
    print(champ)
