import pandas as pd
import json
from datetime import datetime
from urllib.request import urlopen
from tqdm import tqdm
from get_xfl_api_token import get_xfl_api_token
#import pytz

def get_xfl_player_box(game_id:str,save=False):
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
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        # row_df['Confidence'] = play['Confidence']
        main_df = pd.concat([main_df,row_df],ignore_index=True)

    if save == True:
        main_df.to_csv(f'pbp/single_game/csv/{game_id}.csv')
        main_df.to_parquet(f'pbp/single_game/parquet/{game_id}.parquet')
        with open(f"pbp/single_game/json/{game_id}.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    print(main_df)
    return main_df

def main():
    sched_df = pd.read_csv('schedule/2023_xfl_schedule.csv')
    event_id_arr = sched_df['EventId'].to_list()
    
    for i in event_id_arr:
        get_xfl_player_box(i,True)
        

if __name__ == "__main__":
    main()