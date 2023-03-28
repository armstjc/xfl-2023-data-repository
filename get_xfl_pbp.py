import glob
import json
import warnings
from datetime import datetime
from urllib.request import urlopen

import numpy as np
import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token

warnings.simplefilter(action='ignore', category=DeprecationWarning)

def combine_pbp_files():
    main_df = pd.DataFrame()
    game_df = pd.DataFrame()
    season_df = pd.DataFrame()
    file_path = "pbp/single_game/csv/"

    for file in glob.iglob(file_path+"*.csv"):
        game_df = pd.read_csv(file)
        main_df = pd.concat([main_df,game_df],ignore_index=True)

    del game_df

    main_df = main_df.convert_dtypes()

    seasons_arr = main_df['season'].to_list()
    seasons_arr = [*set(seasons_arr)]

    main_df['FootballFumble_PlayerRecovered'] = main_df['FootballFumble_PlayerRecovered'].replace('TM',-1)
    main_df['FootballFumble_PlayerRecovered'] = main_df['FootballFumble_PlayerRecovered'].fillna(0)
    main_df['FootballFumble_PlayerRecovered'] = main_df['FootballFumble_PlayerRecovered'].astype('int')
    main_df['FootballFumble_PlayerRecovered'] = main_df['FootballFumble_PlayerRecovered'].replace(0,None)

    main_df['FootballPenalty_PlayerId'] = main_df['FootballPenalty_PlayerId'].replace('TM',-1)
    main_df['FootballPenalty_PlayerId'] = main_df['FootballPenalty_PlayerId'].fillna(0)
    main_df['FootballPenalty_PlayerId'] = main_df['FootballPenalty_PlayerId'].astype('int')
    main_df['FootballPenalty_PlayerId'] = main_df['FootballPenalty_PlayerId'].replace(0,None)

    main_df['FootballZone'] = main_df['FootballZone'].replace('-',None)


    for i in seasons_arr:
        season_df = main_df[main_df['season'] == i]
        season_df.to_csv(f"pbp/season/csv/{i}_xfl_pbp.csv",index=False)
        season_df.to_parquet(f"pbp/season/parquet/{i}_xfl_pbp.parquet",index=False)

def get_xfl_pbp(game_id:str,save=False,xfl_season = 2023):
    team_id_dict= {
        'ARL':1,
        'HOU':2,
        'SA':3,
        'ORL':4,
        'STL':5,#Only dome team in XFL 3.0
        'SEA':6,
        'VGS':7,
        'DC':8
    }
    
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()
    #timezone = pytz.timezone('US/Eastern')
    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    # print(i.split('_')[-1])
    # tms = i.split('_')[-1]
    # a,h =  tms.split('@')
    # print(f'{a}\t{h}')

    away_team_abv,home_team_abv = game_id.split('_')[-1].split('@')
    
    away_team = int(team_id_dict[away_team_abv])
    home_team = int(team_id_dict[home_team_abv])
    roof = ""
    print(f'gameID:\t{game_id}')
    
    if home_team != "STL":
        roof = 'outdoors'
    else:
        roof = 'dome'
    
    url = f"https://api.xfl.com/scoring/v3.30/markeractivity?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for play in tqdm(json_data):
              
        row_df = pd.DataFrame({'season':xfl_season,'game_id':game_id,'away_team_abv':away_team_abv,'away_team':away_team,'home_team_abv':home_team_abv,'home_team':home_team,'roof':roof},index=[0])
        row_df['MarkerId'] = play['MarkerId']
        row_df['MarkerUTC'] = play['MarkerUTC']
        
        try:
            row_df['MarkerLTC'] = play['MarkerLTC']
        except:
            row_df['MarkerLTC'] = None

        # dt = datetime.fromtimestamp(play['MarkerUTC'])
        # row_df['MarkerDateTime'] = dt
        row_df['play_date_time'] = datetime.fromtimestamp(play['MarkerUTC'])
        #row_df['MajorType'] = play['MajorType']
        row_df['play_type'] = play['MinorType']
        row_df['desc'] = play['Descriptor_']
        row_df['comments'] = play['Comments']
        row_df['IsOfficial'] = play['IsOfficial']
        row_df['qtr'] = int(play['ETime']['Period'])
        row_df['qtr'].astype('int')
        try:
            row_df['ClockMinutes'] = play['ETime']['ClockMinutes']
        except:
            ## if it doesn't exist, it means that it is 0
            row_df['ClockMinutes'] = 0

        try:
            row_df['ClockSeconds'] = play['ETime']['ClockSeconds']
        except:
            ## if it doesn't exist, it means that it is 0
            row_df['ClockSeconds'] = 0
        
        row_df['game_half'] = row_df['qtr'].map({1:'Half1',2:'Half1',3:'Half2',4:'Half2'})

        row_df['SourceType'] = play['SourceType']
        row_df['EventId'] = play['EventId']
        row_df['SituationCode'] = play['SituationCode']
        row_df['SourceId'] = play['SourceId']
        row_df['SourceNativeMarkerId'] = play['SourceNativeMarkerId']
        row_df['OfficialCode'] = play['OfficialCode']
        
        try:
            row_df['quarter_seconds_remaining'] = int(play['Properties'][0]['FootballEventContext']['TimeRemSecTotal'])
        except:
            row_df['quarter_seconds_remaining'] = 0

        row_df['half_seconds_remaining'] = row_df['game_half'].apply(lambda x: (((5-int(row_df['qtr']))*900) + (row_df['quarter_seconds_remaining']-900) - 1800) if x == 'Half1' else (((5-int(row_df['qtr']))*900) + (row_df['quarter_seconds_remaining']-900)))
        row_df['game_seconds_remaining'] = ((5-int(row_df['qtr']))*900) + (row_df['quarter_seconds_remaining']-900)

        row_df['time'] = play['Properties'][0]['FootballEventContext']['TimeRemStr']
        row_df['posteam'] = int(play['Properties'][0]['FootballEventContext']['PossTeam'])
        row_df['PossTeamAbv'] = row_df['posteam'].map(team_id_dict)
        row_df['LastPlaySummary'] = play['Properties'][0]['FootballEventContext']['LastPlaySummary']
        row_df['LastPlayStatus'] = play['Properties'][0]['FootballEventContext']['LastPlayStatus']

        # row_df['is_home_team_pos'] = row_df.apply(lambda x: 1 if x['posteam'] == x['home_team'] else 0)
        row_df.loc[row_df['posteam'] == row_df['home_team'],'home_team_has_pos'] = 1
        row_df.loc[row_df['posteam'] != row_df['home_team'],'home_team_has_pos'] = 0
        
        try:
            ## if it doesn't exist, it means that it is 0
            row_df['VisTimeouts'] = play['Properties'][0]['FootballEventContext']['VisTimeouts']
        except:
            row_df['VisTimeouts'] = 0

        try:
            ## if it doesn't exist, it means that it is 0
            row_df['HomeTimeouts'] = play['Properties'][0]['FootballEventContext']['HomeTimeouts']
        except:
            row_df['HomeTimeouts'] = 0

        row_df.loc[row_df['posteam'] == row_df['home_team'],'posteam_timeouts_remaining'] = row_df['HomeTimeouts']
        row_df.loc[row_df['posteam'] != row_df['home_team'],'posteam_timeouts_remaining'] = row_df['VisTimeouts']
        row_df.loc[row_df['posteam'] == row_df['home_team'],'defteam_timeouts_remaining'] = row_df['HomeTimeouts']
        row_df.loc[row_df['posteam'] != row_df['home_team'],'defteam_timeouts_remaining'] = row_df['VisTimeouts']

        row_df['BallOn_Side'] = play['Properties'][0]['FootballEventContext']['BallOn']['VisOrHome']
        row_df['BallOn_YardNum'] = play['Properties'][0]['FootballEventContext']['BallOn']['YardNum']

        try:
            row_df['DriveNum'] = play['Properties'][0]['FootballEventContext']['DriveNum']
        except:
            row_df['DriveNum'] = None


        row_df.loc[(row_df['BallOn_Side']=='Home')&(row_df['home_team_has_pos']==0),'yardline_100'] =  row_df['BallOn_YardNum']
        row_df.loc[(row_df['BallOn_Side']=='Home')&(row_df['home_team_has_pos']==1),'yardline_100'] =  100 - row_df['BallOn_YardNum'] 
        row_df.loc[(row_df['BallOn_Side']=='Visitor')&(row_df['home_team_has_pos']==0),'yardline_100'] = 100 - row_df['BallOn_YardNum']
        row_df.loc[(row_df['BallOn_Side']=='Visitor')&(row_df['home_team_has_pos']==1),'yardline_100'] = row_df['BallOn_YardNum']

        try:
            for i in play['Participants']:
                row_df[i['Role']] = i['OfficialId']
        except:
            pass

        try:
            row_df['VisScore'] = play['VisitorScore']
        except:
            row_df['VisScore'] = 0

        try:
            row_df['HomeScore'] = play['HomeScore']
        except:
            row_df['HomeScore'] = 0

        for i in play['Properties']:
            ########################################################################################################################################################################################
            ## Timeout info (if != Null, this is the teamID for who called a timeout on this play)
            ########################################################################################################################################################################################

            try:
                row_df['FootballTimeoutTeamId'] = i['FootballTimeoutTeamId']
            except:
                pass
            
            ########################################################################################################################################################################################
            ## Down, Distance and Score
            ########################################################################################################################################################################################

            try:
                row_df['FootballStatus'] = i['FootballStatus']
            except:
                pass

            try:
                row_df['down'] = i['FootballEventContext']['Down']
            except:
                pass
            
            try:
                row_df['ydstogo'] = i['FootballEventContext']['Distance']
            except:
                pass
            
            

            ########################################################################################################################################################################################
            ## Play Result, Zone, and Yards gained/lost
            ########################################################################################################################################################################################

            try:
                row_df['FootballPlayResult'] = i['FootballPlayResult']
            except:
                pass

            try:
                row_df['FootballZone'] = i['FootballZone']
            except:
                pass
            
            try:
                row_df['FootballYards'] = i['FootballYards']
            except:
                pass


            ########################################################################################################################################################################################
            ## Drive Summary
            ########################################################################################################################################################################################

            try:
                row_df['Drive_Start_VisOrHome'] = i['FootballDriveSummary']['DriveStart']['VisOrHome']
            except:
                pass

            try:
                row_df['Drive_Start_YardNum'] = i['FootballDriveSummary']['DriveStart']['YardNum']
            except:
                pass

            try:
                row_df['Drive_Plays'] = i['FootballDriveSummary']['Plays']
            except:
                pass

            try:
                row_df['Drive_Yards'] = i['FootballDriveSummary']['Yards']
            except:
                pass

            try:
                row_df['Drive_TOP'] = i['FootballDriveSummary']['TOP']
            except:
                pass

            try:
                row_df['Result'] = i['FootballDriveSummary']['Result']
            except:
                pass

            ########################################################################################################################################################################################
            ## Scoring (on this play specifically)
            ########################################################################################################################################################################################
            
            try:
                row_df['FootballMainScoringPlay'] = i['FootballMainScoringPlay']
            except:
                pass
            
            try:
                row_df['FootballConvAttPts'] = i['FootballConvAttPts']
            except:
                pass

            try:
                row_df['FootballMiscScore_MiscScoreType'] = i['FootballMiscScore']['MiscScoreType']
            except:
                pass

            try:
                row_df['FootballMiscScore_TeamId'] = i['FootballMiscScore']['TeamId']
            except:
                pass

            try:
                row_df['FootballMiscScore_PlayerId'] = i['FootballMiscScore']['PlayerId']
            except:
                pass

            ########################################################################################################################################################################################
            ## Special Teams Yards
            ########################################################################################################################################################################################
            try:
                row_df['FootballKickYards'] = i['FootballKickYards']
            except:
                pass

            try:
                row_df['FootballPuntYards'] = i['FootballPuntYards']
            except:
                pass
          
            try:
                row_df['FootballKickRetYards'] = i['FootballKickRetYards']
            except:
                pass

            try:
                row_df['FootballPuntRetYards'] = i['FootballPuntRetYards']
            except:
                pass

            ########################################################################################################################################################################################
            ## Penalty Info
            ########################################################################################################################################################################################

            try:
                row_df['FootballPenalty_TeamId'] = i['FootballPenalty']['TeamId']
            except:
                pass

            try:
                row_df['FootballPenalty_PlayerId'] = i['FootballPenalty']['PlayerId']
            except:
                pass

            try:
                row_df['FootballPenalty_Yards'] = i['FootballPenalty']['Yards']
            except:
                pass

            try:
                row_df['FootballPenalty_PenaltyResult'] = i['FootballPenalty']['PenaltyResult']
            except:
                pass

            try:
                row_df['FootballPenalty_Description'] = i['FootballPenalty']['Description']
            except:
                pass

            ########################################################################################################################################################################################
            ## Fumble Info
            ########################################################################################################################################################################################

            try:
                row_df['FootballFumble_TeamFumbled'] = i['FootballFumble']['TeamFumbled']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerFumbled'] = i['FootballFumble']['PlayerFumbled']
            except:
                pass

            try:
                row_df['FootballFumble_TeamRecovered'] = i['FootballFumble']['TeamRecovered']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerRecovered'] = i['FootballFumble']['PlayerRecovered']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerForcedFumble'] = i['FootballFumble']['PlayerForcedFumble']
            except:
                pass

            ########################################################################################################################################################################################
            ## Extra yards
            ########################################################################################################################################################################################

            try:
                row_df['FootballExtraYards_IndivOrTeam'] = i['FootballExtraYards']['IndivOrTeam']
            except:
                pass

            try:
                row_df['FootballExtraYards_TeamId'] = i['FootballExtraYards']['TeamId']
            except:
                pass

            try:
                row_df['FootballExtraYards_PlayerId'] = i['FootballExtraYards']['PlayerId']
            except:
                pass

            try:
                row_df['FootballExtraYards_Yards'] = i['FootballExtraYards']['Yards']
            except:
                pass

            ########################################################################################################################################################################################
            ## "Ball Set On" info (TBD on the exact purpose of this stat)
            ########################################################################################################################################################################################

            try:
                row_df['FootballSetBallOn_VisOrHome'] = i['FootballSetBallOn']['VisOrHome']
            except:
                pass

            try:
                row_df['FootballSetBallOn_YardNum'] = i['FootballSetBallOn']['YardNum']
            except:
                pass

        main_df = pd.concat([main_df,row_df],ignore_index=True)
    
    try:
        main_df = main_df.sort_values(by=['MarkerUTC'])
    except:
        print('Could not sort dataframe. This may be because [MarkerUTC] does not exist in this JSON, or the dataframe is empty.')
    
    if len(main_df)>0:
        main_df['MapRolePunter'] = main_df['MapRolePunter'].fillna(0)
        main_df['MapRolePunter'] = main_df['MapRolePunter'].astype('int')
        main_df['punt_attempt'] = main_df['MapRolePunter'].apply(lambda x: 1 if x > 0 else 0)
        main_df['MapRolePunter'] = main_df['MapRolePunter'].replace(0,None)

        main_df.loc[(main_df['play_type'] != 'EventFootballPass') | (main_df['Result'] != 'TD'),'pass_touchdown'] = 0
        main_df.loc[(main_df['play_type'] == 'EventFootballPass') & (main_df['Result'] == 'TD'),'pass_touchdown'] = 1

        main_df.loc[(main_df['play_type'] != 'EventFootballRush') | (main_df['Result'] != 'TD'),'rush_touchdown'] = 0
        main_df.loc[(main_df['play_type'] == 'EventFootballRush') & (main_df['Result'] == 'TD'),'rush_touchdown'] = 1

        main_df.loc[(main_df['FootballPlayResult'] == 'ResultKickMade') | (main_df['FootballPlayResult'] == 'ResultKickMade'),'field_goal_attempt'] = 1
        main_df.loc[(main_df['FootballPlayResult'] != 'ResultKickMade') & (main_df['FootballPlayResult'] != 'ResultKickMade'),'field_goal_attempt'] = 0

        main_df.loc[(main_df['FootballPlayResult'] == 'ResultKickMade'),'field_goal_made'] = 1
        main_df.loc[(main_df['FootballPlayResult'] != 'ResultKickMade'),'field_goal_made'] = 0

        main_df.loc[(main_df['FootballPlayResult'] == 'ResultKickMade'),'field_goal_made'] = 1
        main_df.loc[(main_df['FootballPlayResult'] != 'ResultKickMade'),'field_goal_made'] = 0

        main_df['touchdown'] = main_df['pass_touchdown'] + main_df['rush_touchdown']
        ## Being perfectly real, I have literally no idea how this league determines 
        ## when a safety is scored in this API.


        if save == True and len(main_df) >0:
            main_df.to_csv(f'pbp/single_game/csv/{game_id}.csv',index=False)
            main_df.to_parquet(f'pbp/single_game/parquet/{game_id}.parquet',index=False)
            with open(f"pbp/single_game/json/{game_id}.json", "w+") as f:
                f.write(json.dumps(json_data,indent=2))

    #print(main_df)
    return main_df

def main():
    sched_df = pd.read_csv('schedule/2023_xfl_schedule.csv')
    event_id_arr = sched_df['EventId'].to_list()
 
    for i in event_id_arr:
        get_xfl_pbp(i,True)
        
    combine_pbp_files()

if __name__ == "__main__":
    main()