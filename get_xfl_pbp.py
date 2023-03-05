import glob
import json
from datetime import datetime
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token


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

    seasons_arr = main_df['Season'].to_list()
    seasons_arr = [*set(seasons_arr)]
    try:
        main_df['FootballFumble_PlayerRecovered'] = main_df['FootballFumble_PlayerRecovered'].astype('str')
    except:
        print('[FootballFumble_PlayerRecovered] may not exist in this context.')

    for i in seasons_arr:
        season_df = main_df[main_df['Season'] == i]
        season_df.to_csv(f"pbp/season/csv/{i}_xfl_pbp.csv",index=False)
        #season_df.to_parquet(f"pbp/season/parquet/{i}_xfl_pbp.parquet",index=False)

def get_xfl_pbp(game_id:str,save=False):
    print(game_id)
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()
    #timezone = pytz.timezone('US/Eastern')
    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/markeractivity?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for play in tqdm(json_data):
        
        #official_id = player['OfficialId']
        
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id},index=[0])
        row_df['MarkerId'] = play['MarkerId']
        row_df['MarkerUTC'] = play['MarkerUTC']
        
        try:
            row_df['MarkerLTC'] = play['MarkerLTC']
        except:
            row_df['MarkerLTC'] = None

        # dt = datetime.fromtimestamp(play['MarkerUTC'])
        # row_df['MarkerDateTime'] = dt
        row_df['MarkerDateTime'] = datetime.fromtimestamp(play['MarkerUTC'])
        row_df['MajorType'] = play['MajorType']
        row_df['MinorType'] = play['MinorType']
        row_df['PlayDescriptor'] = play['Descriptor_']
        row_df['PlayComments'] = play['Comments']
        row_df['IsOfficial'] = play['IsOfficial']
        row_df['Quarter'] = play['ETime']['Period']

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
        row_df['SourceType'] = play['SourceType']
        row_df['EventId'] = play['EventId']
        row_df['SituationCode'] = play['SituationCode']
        row_df['SourceId'] = play['SourceId']
        row_df['SourceNativeMarkerId'] = play['SourceNativeMarkerId']
        row_df['OfficialCode'] = play['OfficialCode']
        
        try:
            row_df['TimeRemSecTotal'] = play['Properties'][0]['FootballEventContext']['TimeRemSecTotal']
        except:
            row_df['TimeRemSecTotal'] = None

        row_df['TimeRemStr'] = play['Properties'][0]['FootballEventContext']['TimeRemStr']
        
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
        
            row_df['BallOn_Side'] = play['Properties'][0]['FootballEventContext']['BallOn']['VisOrHome']
        row_df['BallOn_YardNum'] = play['Properties'][0]['FootballEventContext']['BallOn']['YardNum']
        row_df['DriveNum'] = play['Properties'][0]['FootballEventContext']['DriveNum']
        row_df['PossTeam'] = play['Properties'][0]['FootballEventContext']['PossTeam']
        row_df['LastPlaySummary'] = play['Properties'][0]['FootballEventContext']['LastPlaySummary']
        row_df['LastPlayStatus'] = play['Properties'][0]['FootballEventContext']['LastPlayStatus']

        try:
            for i in play['Participants']:
                row_df[i['Role']] = i['OfficialId']
        except:
            pass

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
                row_df['Down'] = i['FootballEventContext']['Down']
            except:
                pass
            
            try:
                row_df['Distance'] = i['FootballEventContext']['Distance']
            except:
                pass
            
            try:
                row_df['VisScore'] = i['FootballEventContext']['VisScore']
            except:
                pass

            try:
                row_df['HomeScore'] = i['HomeScore']
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
    
    if save == True and len(main_df) >0:
        main_df.to_csv(f'pbp/single_game/csv/{game_id}.csv',index=False)
        #main_df.to_parquet(f'pbp/single_game/parquet/{game_id}.parquet',index=False)
        with open(f"pbp/single_game/json/{game_id}.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    print(main_df)
    return main_df

def main():
    sched_df = pd.read_csv('schedule/2023_xfl_schedule.csv')
    event_id_arr = sched_df['EventId'].to_list()
    
    for i in event_id_arr:
        get_xfl_pbp(i,True)
        
    combine_pbp_files()

if __name__ == "__main__":
    main()