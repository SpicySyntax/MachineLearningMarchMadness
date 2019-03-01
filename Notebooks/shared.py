'''
    Shared Helper Functions to be reused in notebooks
'''
def resolve_team_name(team_name):
    #Apply hard-coded corrections to team names
    team_name_dict = {'Colorado-Colorado Springs':'Colorado',
                     'Colorado College': 'Colorado',
                     'UNC':'North Carolina',
                     'UConn':'Connecticut',
                     'LIU-Brooklyn':'Long Island University',
                     'UTSA':'Texas-San Antonio',
                     'Pitt':'Pittsburgh',
                     'BYU':'Brigham Young',
                     "St. Peter's": "Saint Peter's",
                     'VCU':'Virginia Commonwealth',
                     'Southern Miss':'Southern Mississippi',
                     'Detroit': 'Detroit Mercy',
                     'UNLV':'Nevada-Las Vegas',
                     'Ole Miss':'Mississippi',
                     "St. Joseph's":"Saint Joseph's",
                     'UCSB':'UC-Santa Barbara',
                     'SMU': 'Southern Methodist',
                     'USC':'South Carolina',
                     'LSU':'Louisiana State',
                     'UMass':'Massachusetts',
                     'ETSU':'East Tennessee State'}
    # TODO: for V2 add more corrections to the team_name_dict
    if(team_name in team_name_dict):
        return team_name_dict[team_name]
    return team_name
def get_school_stats(year, team_name):
    return df_school[(df_school['year'] == year) & (df_school['team_name'] == team_name)]
def get_vals(t_stats_list, key):
    ret = []
    for t_stat in t_stats_list:
        ret.append(t_stat[key].squeeze())
    return ret
def get_team_stats_dict_with_t1_win(t1_stats, t2_stats, t1_wins):
    return {'team_name_1':get_vals(t1_stats,'team_name'),'fg_pg_1':get_vals(t1_stats,'fg_pg'),'ft_pg_1':get_vals(t1_stats,'ft_pg'),
            'three_pt_pg_1':get_vals(t1_stats,'three_pt_pg'),'orb_pg_1':get_vals(t1_stats,'orb_pg'),'drb_pg_1':get_vals(t1_stats,'drb_pg'),
            'ast_pg_1':get_vals(t1_stats,'ast_pg'),'stl_pg_1':get_vals(t1_stats,'stl_pg'),'blk_pg_1':get_vals(t1_stats,'blk_pg'),
            'tov_pg_1':get_vals(t1_stats,'tov_pg'),'pf_pg_1':get_vals(t1_stats,'pf_pg'), 'pt_pg_1':get_vals(t1_stats,'pt_pg'),
            'opnt_pt_pg_1':get_vals(t1_stats,'opnt_pt_pg'),'fg_pct_1':get_vals(t1_stats,'fg_pct'),'three_p_pct_1':get_vals(t1_stats,'three_p_pct'),
            'ft_pct_1':get_vals(t1_stats,'ft_pct'),'wl_pct_1':get_vals(t1_stats,'wl_pct'),'conf_wl_pct_1':get_vals(t1_stats,'conf_wl_pct'),
            'srs_1':get_vals(t1_stats,'srs'),'sos_1':get_vals(t1_stats,'sos'),
            'team_name_2':get_vals(t2_stats,'team_name'),'fg_pg_2':get_vals(t2_stats,'fg_pg'),'ft_pg_2':get_vals(t2_stats,'ft_pg'),
            'three_pt_pg_2':get_vals(t2_stats,'three_pt_pg'),'orb_pg_2':get_vals(t2_stats,'orb_pg'),'drb_pg_2':get_vals(t2_stats,'drb_pg'),
            'ast_pg_2':get_vals(t2_stats,'ast_pg'),'stl_pg_2':get_vals(t2_stats,'stl_pg'),'blk_pg_2':get_vals(t2_stats,'blk_pg'),
            'tov_pg_2':get_vals(t2_stats,'tov_pg'),'pf_pg_2':get_vals(t2_stats,'pf_pg'), 'pt_pg_2':get_vals(t2_stats,'pt_pg'),
            'opnt_pt_pg_2':get_vals(t2_stats,'opnt_pt_pg'),'fg_pct_2':get_vals(t2_stats,'fg_pct'),'three_p_pct_2':get_vals(t2_stats,'three_p_pct'),
            'ft_pct_2':get_vals(t2_stats,'ft_pct'),'wl_pct_2':get_vals(t2_stats,'wl_pct'),'conf_wl_pct_2':get_vals(t2_stats,'conf_wl_pct'),
            'srs_2':get_vals(t2_stats,'srs'),'sos_2':get_vals(t2_stats,'sos'),
            't1_win':t1_wins}
def get_team_stats_dict(t1_stats, t2_stats):
    return {'team_name_1':get_vals(t1_stats,'team_name'),'fg_pg_1':get_vals(t1_stats,'fg_pg'),'ft_pg_1':get_vals(t1_stats,'ft_pg'),
            'three_pt_pg_1':get_vals(t1_stats,'three_pt_pg'),'orb_pg_1':get_vals(t1_stats,'orb_pg'),'drb_pg_1':get_vals(t1_stats,'drb_pg'),
            'ast_pg_1':get_vals(t1_stats,'ast_pg'),'stl_pg_1':get_vals(t1_stats,'stl_pg'),'blk_pg_1':get_vals(t1_stats,'blk_pg'),
            'tov_pg_1':get_vals(t1_stats,'tov_pg'),'pf_pg_1':get_vals(t1_stats,'pf_pg'), 'pt_pg_1':get_vals(t1_stats,'pt_pg'),
            'opnt_pt_pg_1':get_vals(t1_stats,'opnt_pt_pg'),'fg_pct_1':get_vals(t1_stats,'fg_pct'),'three_p_pct_1':get_vals(t1_stats,'three_p_pct'),
            'ft_pct_1':get_vals(t1_stats,'ft_pct'),'wl_pct_1':get_vals(t1_stats,'wl_pct'),'conf_wl_pct_1':get_vals(t1_stats,'conf_wl_pct'),
            'srs_1':get_vals(t1_stats,'srs'),'sos_1':get_vals(t1_stats,'sos'),
            'team_name_2':get_vals(t2_stats,'team_name'),'fg_pg_2':get_vals(t2_stats,'fg_pg'),'ft_pg_2':get_vals(t2_stats,'ft_pg'),
            'three_pt_pg_2':get_vals(t2_stats,'three_pt_pg'),'orb_pg_2':get_vals(t2_stats,'orb_pg'),'drb_pg_2':get_vals(t2_stats,'drb_pg'),
            'ast_pg_2':get_vals(t2_stats,'ast_pg'),'stl_pg_2':get_vals(t2_stats,'stl_pg'),'blk_pg_2':get_vals(t2_stats,'blk_pg'),
            'tov_pg_2':get_vals(t2_stats,'tov_pg'),'pf_pg_2':get_vals(t2_stats,'pf_pg'), 'pt_pg_2':get_vals(t2_stats,'pt_pg'),
            'opnt_pt_pg_2':get_vals(t2_stats,'opnt_pt_pg'),'fg_pct_2':get_vals(t2_stats,'fg_pct'),'three_p_pct_2':get_vals(t2_stats,'three_p_pct'),
            'ft_pct_2':get_vals(t2_stats,'ft_pct'),'wl_pct_2':get_vals(t2_stats,'wl_pct'),'conf_wl_pct_2':get_vals(t2_stats,'conf_wl_pct'),
            'srs_2':get_vals(t2_stats,'srs'),'sos_2':get_vals(t2_stats,'sos')}
def get_team_stats_dict_ps(t1_stats, t2_stats, t1_seeds, t2_seeds):
    return {'team_name_1':get_vals(t1_stats,'team_name'),'fg_pg_1':get_vals(t1_stats,'fg_pg'),'ft_pg_1':get_vals(t1_stats,'ft_pg'),
            'three_pt_pg_1':get_vals(t1_stats,'three_pt_pg'),'orb_pg_1':get_vals(t1_stats,'orb_pg'),'drb_pg_1':get_vals(t1_stats,'drb_pg'),
            'ast_pg_1':get_vals(t1_stats,'ast_pg'),'stl_pg_1':get_vals(t1_stats,'stl_pg'),'blk_pg_1':get_vals(t1_stats,'blk_pg'),
            'tov_pg_1':get_vals(t1_stats,'tov_pg'),'pf_pg_1':get_vals(t1_stats,'pf_pg'), 'pt_pg_1':get_vals(t1_stats,'pt_pg'),
            'opnt_pt_pg_1':get_vals(t1_stats,'opnt_pt_pg'),'fg_pct_1':get_vals(t1_stats,'fg_pct'),'three_p_pct_1':get_vals(t1_stats,'three_p_pct'),
            'ft_pct_1':get_vals(t1_stats,'ft_pct'),'wl_pct_1':get_vals(t1_stats,'wl_pct'),'conf_wl_pct_1':get_vals(t1_stats,'conf_wl_pct'),
            'srs_1':get_vals(t1_stats,'srs'),'sos_1':get_vals(t1_stats,'sos'),
            'team_name_2':get_vals(t2_stats,'team_name'),'fg_pg_2':get_vals(t2_stats,'fg_pg'),'ft_pg_2':get_vals(t2_stats,'ft_pg'),
            'three_pt_pg_2':get_vals(t2_stats,'three_pt_pg'),'orb_pg_2':get_vals(t2_stats,'orb_pg'),'drb_pg_2':get_vals(t2_stats,'drb_pg'),
            'ast_pg_2':get_vals(t2_stats,'ast_pg'),'stl_pg_2':get_vals(t2_stats,'stl_pg'),'blk_pg_2':get_vals(t2_stats,'blk_pg'),
            'tov_pg_2':get_vals(t2_stats,'tov_pg'),'pf_pg_2':get_vals(t2_stats,'pf_pg'), 'pt_pg_2':get_vals(t2_stats,'pt_pg'),
            'opnt_pt_pg_2':get_vals(t2_stats,'opnt_pt_pg'),'fg_pct_2':get_vals(t2_stats,'fg_pct'),'three_p_pct_2':get_vals(t2_stats,'three_p_pct'),
            'ft_pct_2':get_vals(t2_stats,'ft_pct'),'wl_pct_2':get_vals(t2_stats,'wl_pct'),'conf_wl_pct_2':get_vals(t2_stats,'conf_wl_pct'),
            'srs_2':get_vals(t2_stats,'srs'),'sos_2':get_vals(t2_stats,'sos'), 'team_1_seed':t1_seeds,
            'team_2_seed':t2_seeds}
def create_team_stats_df_w_t1_win(indeces_w_stats, t1_stats_list, t2_stats_list,t1_wins):
    # Adds column for wether team 1 wins or not
    # Assumes all lists are of the same length
    return pd.DataFrame(get_team_stats_dict_with_t1_win(t1_stats_list, t2_stats_list,t1_wins), index = indeces_w_stats)
def create_team_stats_df(indeces_w_stats, t1_stats_list, t2_stats_list):
    # Assumes all lists are of the same length
    return pd.DataFrame(get_team_stats_dict(t1_stats_list, t2_stats_list), index = indeces_w_stats)
def create_team_stats_df_ps(indeces_w_stats, t1_stats_list, t2_stats_list, t1_seeds, t2_seeds):
    # Only uses post season stats => inclu
    # Assumes all lists are of the same length
    return pd.DataFrame(get_team_stats_dict_ps(t1_stats_list, t2_stats_list, t1_seeds, t2_seeds), index = indeces_w_stats)
def get_team_stats_df(game_df, should_print=False):
    indeces_w_stats = []
    t1_stats_list = []
    t2_stats_list = []
    t1_wins_list = []
    for index, row in game_df.iterrows():
        year = row['year']
        team_1 = row['team_1_name']
        team_2 = row['team_2_name']
        team_1_score = row['team_1_score']
        team_2_score = row['team_2_score']
        t1_stats = get_school_stats(year, resolve_team_name(team_1))
        t2_stats = get_school_stats(year, resolve_team_name(team_2))

        if(len(t1_stats) > 0 and len(t2_stats) > 0):  
            indeces_w_stats.append(index)
            t1_stats_list.append(t1_stats)
            t2_stats_list.append(t2_stats)
            t1_wins_list.append(team_1_score > team_2_score)
        else:         
            if(should_print):
                print(year)
                if(len(t1_stats) < 1):
                    print(team_1)
                if(len(t2_stats) < 1):
                    print(team_2)
            
    print(len(indeces_w_stats))
    team_stats_df = create_team_stats_df_w_t1_win(indeces_w_stats, t1_stats_list, t2_stats_list, t1_wins_list)
    return team_stats_df
def get_matchups_stats(schools, post_season):    
    
    i = 0 
    t1_stats = []
    t2_stats = []
    t1_seeds = []
    t2_seeds = []
    if(not is_power_of_two(len(schools))):
        print('ERROR: invalid number of school names')
        return False
    while i < len(schools):
        t1_name, t1_seed = schools[i]
        t2_name, t2_seed = schools[i + 1]
        t1_seeds.append(t1_seed)
        t2_seeds.append(t2_seed)
        #print(t1_name, t2_name
        t1_stats.append(get_school_stats(2018, t1_name))
        t2_stats.append(get_school_stats(2018, t2_name))
        i = i + 2
    if(post_season):
        matchup_stats = create_team_stats_df_ps(range(0,int(len(schools)/2)), t1_stats, t2_stats, t1_seeds, t2_seeds)
    else:
        matchup_stats = create_team_stats_df(range(0,int(len(schools)/2)), t1_stats, t2_stats)
    return matchup_stats
def is_power_of_two(num):
    return ((num & (num - 1)) == 0) and num != 0
ps_feature_col_names = ['team_1_seed', 'team_2_seed','fg_pg_1','ft_pg_1',
            'three_pt_pg_1','orb_pg_1','drb_pg_1',
            'ast_pg_1','stl_pg_1','blk_pg_1',
            'tov_pg_1','pf_pg_1', 'pt_pg_1',
            'opnt_pt_pg_1','fg_pct_1','three_p_pct_1',
            'ft_pct_1','wl_pct_1','conf_wl_pct_1',
            'srs_1','sos_1',
            'fg_pg_2','ft_pg_2',
            'three_pt_pg_2','orb_pg_2','drb_pg_2',
            'ast_pg_2','stl_pg_2','blk_pg_2',
            'tov_pg_2','pf_pg_2', 'pt_pg_2',
            'opnt_pt_pg_2','fg_pct_2','three_p_pct_2',
            'ft_pct_2','wl_pct_2','conf_wl_pct_2',
            'srs_2','sos_2'
            ]
ps_predict_class_names = ['t1_win']

