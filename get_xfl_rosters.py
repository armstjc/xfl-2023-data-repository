import glob
import json
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token


def get_xfl_rosters(season=2023,week=1,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    ## Yes this is bad practice, but there is nothing in their JSON
    ## files to indicate what is what.
    xfl_season = season
    xfl_week = week

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    ## This gets the rosters for all teams, rather than a specific game.
    url = f"https://api.xfl.com/scoring/v3.30/players?access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        print(f"\nPlayer #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id},index=[0])
        row_df['JerseyNum'] = player['JerseyNum']
        row_df['FirstName'] = player['FirstName']
        row_df['LastName'] = player['LastName']
        row_df['LastNameSuffix'] = player['LastNameSuffix']
        row_df['Position'] = player['Position']
        row_df['PositionLongName'] = player['PositionLongName']
        row_df['NAbbrev'] = player['NAbbrev']
        row_df['Height'] = player['Height']
        row_df['DOB'] = player['DOB']
        row_df['POB'] = player['POB']
        row_df['Hometown'] = player['Hometown']
        row_df['Country'] = player['Country']
        row_df['CountryCode'] = player['CountryCode']
        row_df['Nickname'] = player['Nickname']
        row_df['InjuryStatus'] = player['InjuryStatus']
        row_df['InjuryDesc'] = player['InjuryDesc']
        row_df['Headshot'] = player['Headshot']
        row_df['Initials'] = player['Initials']
        row_df['TeamId'] = player['TeamId']
        row_df['Affiliate'] = player['Affiliate']
        row_df['CloudHeadshotURL'] = player['CloudHeadshotURL']
        row_df['SquadId'] = player['SquadId']
        row_df['College'] = player['College']
        row_df['LeagueStatus'] = player['LeagueStatus']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    if save == True:
        main_df.to_csv(f'rosters/{xfl_season}_xfl_roster.csv',index=False)
        main_df.to_parquet(f'rosters/{xfl_season}_xfl_roster.parquet',index=False)

        main_df['Week'] = xfl_week
        main_df.to_csv(f'rosters/weekly_rosters/csv/{xfl_season}_{xfl_week}_xfl_roster.csv',index=False)
        main_df.to_parquet(f'rosters/weekly_rosters/parquet/{xfl_season}_{xfl_week}_xfl_roster.parquet',index=False)
        #urlretrieve(url, filename=f"rosters/weekly_rosters/json/{xfl_season}_{xfl_week}_xfl_roster.json")
        with open(f"rosters/weekly_rosters/json/{xfl_season}_{xfl_week}_xfl_roster.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    main_df['Week'] = xfl_week
    return main_df

def combine_weekly_rosters():
    main_df = pd.DataFrame()
    game_df = pd.DataFrame()
    season_df = pd.DataFrame()
    file_path = "rosters/weekly_rosters/csv/"

    for file in glob.iglob(file_path+"*.csv"):
        game_df = pd.read_csv(file)
        main_df = pd.concat([main_df,game_df],ignore_index=True)

    del game_df

    seasons_arr = main_df['Season'].to_list()
    seasons_arr = [*set(seasons_arr)]

    for i in seasons_arr:
        season_df = main_df[main_df['Season'] == i]
        season_df.to_csv(f"rosters/weekly_rosters/{i}_weekly_xfl_roster.csv",index=False)
        season_df.to_parquet(f"rosters/weekly_rosters/{i}_weekly_xfl_roster.parquet",index=False)

def main():
    season = 2023
    week = 4
    get_xfl_rosters(season,week,True)

    combine_weekly_rosters()


if __name__ == "__main__":
    main()