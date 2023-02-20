import pandas as pd
import json
from urllib.request import urlopen
from get_xfl_api_token import get_xfl_api_token
from tqdm import tqdm

def get_xfl_schedule(season=2023,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    ## Yes this is bad practice, but there is nothing in their JSON
    ## files to indicate what is what.
    xfl_season = season

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    ## This gets the rosters for all teams, rather than a specific game.
    url = f"https://api.xfl.com/scoring/v3.30/scoreboards?access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['EventId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'EventId':official_id},index=[0])
        row_df['NowUTC'] = player['NowUTC']
        row_df['NowLTC'] = player['NowLTC']
        row_df['VisitorScore'] = player['VisitorScore']
        row_df['HomeScore'] = player['HomeScore']
        row_df['Period'] = player['Period']
        row_df['ClockMinutes'] = player['ClockMinutes']
        row_df['ClockSeconds'] = player['ClockSeconds']
        row_df['ClockTenths'] = player['ClockTenths']
        row_df['ClockState'] = player['ClockState']
        row_df['VisitorTimeoutsRemaining'] = player['VisitorTimeoutsRemaining']
        row_df['HomeTimeoutsRemaining'] = player['HomeTimeoutsRemaining']
        row_df['VisitorChallengesRemaining'] = player['VisitorChallengesRemaining']
        row_df['HomeChallengesRemaining'] = player['HomeChallengesRemaining']
        #row_df['VisitorPeriodScores'] = player['VisitorPeriodScores']
        for j in range(0,len(player['VisitorPeriodScores'])):
            try:
                row_df[f'VisitorQuarterScore_{j+1}'] = player['VisitorPeriodScores'][j]
            except:
                row_df[f'VisitorQuarterScore_{j+1}'] = None

        for j in range(0,len(player['HomePeriodScores'])):
            try:
                row_df[f'HomeQuarterScore_{j+1}'] = player['HomePeriodScores'][j]
            except:
                row_df[f'HomeQuarterScore_{j+1}'] = None

        #row_df['HomePeriodScores'] = player['HomePeriodScores']
        row_df['EventStatusDetail'] = player['EventStatusDetail']
        row_df['VisitorShots'] = player['VisitorShots']
        row_df['HomeShots'] = player['HomeShots']
        row_df['EventStatus'] = player['EventStatus']
        row_df['OfficialCode'] = player['OfficialCode']
        row_df['PeriodSecondsRemaining'] = player['PeriodSecondsRemaining']
        row_df['PeriodSecondsElapsed'] = player['PeriodSecondsElapsed']
        row_df['PlayClock'] = player['PlayClock']
        row_df['PlayClockTenths'] = player['PlayClockTenths']
        row_df['BallOn'] = player['BallOn']
        row_df['Down'] = player['Down']
        row_df['Distance'] = player['Distance']
        row_df['PossTeam'] = player['PossTeam']
        row_df['DriveNum'] = player['DriveNum']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    if save == True:
        
        main_df.to_csv(f'schedule/{xfl_season}_xfl_schedule.csv',index=False)
        main_df.to_parquet(f'schedule/{xfl_season}_xfl_schedule.parquet',index=False)


        main_df.to_parquet(f'schedule/parquet/{xfl_season}_xfl_schedule.parquet',index=False)
        main_df.to_csv(f'schedule/csv/{xfl_season}_xfl_schedule.csv',index=False)
        with open(f"schedule/json/{xfl_season}_xfl_schedule.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    return main_df

def main():
    season = 2023
    get_xfl_schedule(season,True)

if __name__ == "__main__":
    main()