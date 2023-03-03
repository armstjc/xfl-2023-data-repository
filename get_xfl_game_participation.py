import json
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token


def get_xfl_game_participation(game_id:str,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/players?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id,'game_id':game_id},index=[0])
        row_df['VisOrHome'] = player['VisOrHome']
        row_df['JerseyNum'] = player['JerseyNum']
        row_df['FirstName'] = player['FirstName']
        row_df['LastName'] = player['LastName']
        row_df['LastNameSuffix'] = player['LastNameSuffix']
        row_df['Position'] = player['Position']
        row_df['PositionLongName'] = player['PositionLongName']
        row_df['NAbbrev'] = player['NAbbrev']
        row_df['Height'] = player['Height']
        row_df['Weight'] = player['Weight']
        row_df['DOB'] = player['DOB']
        row_df['POB'] = player['POB']
        
        try:
            row_df['Age'] = player['Age']
        except:
            row_df['Age'] = None

        row_df['Hometown'] = player['Hometown']
        row_df['Country'] = player['Country']
        row_df['CountryCode'] = player['CountryCode']
        row_df['Nickname'] = player['Nickname']
        row_df['InjuryStatus'] = player['InjuryStatus']
        row_df['InjuryDesc'] = player['InjuryDesc']
        try:
            row_df['GfxId'] = player['GfxId']
        except:
            row_df['GfxId'] = None

        row_df['Headshot'] = player['Headshot']
        
        try:
            row_df['IsStarting'] = player['IsStarting']
        except:
            row_df['IsStarting'] = None

        row_df['Initials'] = player['Initials']
        
        try:
            row_df['Scratch'] = player['Scratch']
        except:
            row_df['Scratch'] = None

        row_df['TrackingId'] = player['TrackingId']
        row_df['TeamId'] = player['TeamId']
        row_df['Affiliate'] = player['Affiliate']
        row_df['CloudHeadshotURL'] = player['CloudHeadshotURL']
        row_df['SquadId'] = player['SquadId']
        row_df['College'] = player['College']
        row_df['LeagueStatus'] = player['LeagueStatus']
        try:
            row_df['Participated'] = player['Participated']
        except:
            row_df['Participated'] = None
        main_df = pd.concat([main_df,row_df],ignore_index=True)

    ##main_df = main_df.replace({False:0,True:1},inplace=True)
    main_df.replace({False:0,True:1},inplace=True)
    if save == True:
        
        main_df.to_csv(f'player_info/participation_data/csv/{game_id}.csv',index=False)
        main_df.to_parquet(f'player_info/participation_data/parquet/{game_id}.parquet',index=False)

        with open(f"player_info/participation_data/json/{game_id}.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))


    return main_df

def main():
    sched_df = pd.read_csv('schedule/2023_xfl_schedule.csv')
    event_id_arr = sched_df['EventId'].to_list()
    
    for i in event_id_arr:
        get_xfl_game_participation(i,True)
        

if __name__ == "__main__":
    main()