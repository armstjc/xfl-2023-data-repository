from datetime import datetime
import json
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token


def get_xfl_standings(season=2023,week=1,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()
    
    xfl_season = season
    xfl_week = week
    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    url = f"https://api.xfl.com/scoring/v3.30/standings?access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id},index=[0])
        row_df['Rank'] = player['Rank']
        row_df['RankInConference'] = player['RankInConference']
        row_df['RankInDivision'] = player['RankInDivision']
        row_df['GamesPlayed'] = player['GamesPlayed']
        row_df['GamesBack'] = player['GamesBack']
        row_df['ScoreDiff'] = player['ScoreDiff']
        row_df['ScoreFor'] = player['ScoreFor']
        row_df['ScoreAgainst'] = player['ScoreAgainst']
        row_df['RankInWildcard'] = player['RankInWildcard']
        row_df['Streak'] = player['Streak']
        row_df['Last10'] = player['Last10']
        row_df['ClinchIndicator'] = player['ClinchIndicator']
        row_df['ConferenceScoreFor'] = player['ConferenceScoreFor']
        row_df['ConferenceScoreAgainst'] = player['ConferenceScoreAgainst']
        row_df['DivisionScoreFor'] = player['DivisionScoreFor']
        row_df['DivisionScoreAgainst'] = player['DivisionScoreAgainst']
        row_df['City'] = player['City']
        row_df['Mascot'] = player['Mascot']
        row_df['EarnedPoints'] = player['EarnedPoints']
        row_df['Wins'] = player['Wins']
        row_df['Losses'] = player['Losses']
        row_df['Ties'] = player['Ties']
        row_df['WinPct'] = player['WinPct']
        row_df['OTWins'] = player['OTWins']
        row_df['OTLosses'] = player['OTLosses']
        row_df['OTTies'] = player['OTTies']
        row_df['ShootoutWins'] = player['ShootoutWins']
        row_df['ShootoutLosses'] = player['ShootoutLosses']
        row_df['ConferenceWins'] = player['ConferenceWins']
        row_df['ConferenceLosses'] = player['ConferenceLosses']
        row_df['ConferenceTies'] = player['ConferenceTies']
        row_df['ConferenceWinPct'] = player['ConferenceWinPct']
        row_df['DivisionWins'] = player['DivisionWins']
        row_df['DivisionLosses'] = player['DivisionLosses']
        row_df['DivisionTies'] = player['DivisionTies']
        row_df['DivisionWinPct'] = str(player['DivisionWinPct'])
        row_df['RoadEarnedPoints'] = player['RoadEarnedPoints']
        row_df['RoadWins'] = player['RoadWins']
        row_df['RoadLosses'] = player['RoadLosses']
        row_df['RoadTies'] = player['RoadTies']
        row_df['RoadWinPct'] = player['RoadWinPct']
        row_df['RoadOTWins'] = player['RoadOTWins']
        row_df['RoadOTLosses'] = player['RoadOTLosses']
        row_df['RoadOTTies'] = player['RoadOTTies']
        row_df['RoadShootoutWins'] = player['RoadShootoutWins']
        row_df['RoadShootoutLosses'] = player['RoadShootoutLosses']
        row_df['RoadConferenceWins'] = player['RoadConferenceWins']
        row_df['RoadConferenceLosses'] = player['RoadConferenceLosses']
        row_df['RoadConferenceTies'] = player['RoadConferenceTies']
        row_df['RoadConferenceWinPct'] = player['RoadConferenceWinPct']
        row_df['RoadDivisionWins'] = player['RoadDivisionWins']
        row_df['RoadDivisionLosses'] = player['RoadDivisionLosses']
        row_df['RoadDivisionTies'] = player['RoadDivisionTies']
        row_df['RoadDivisionWinPct'] = str(player['RoadDivisionWinPct'])
        row_df['HomeEarnedPoints'] = player['HomeEarnedPoints']
        row_df['HomeWins'] = player['HomeWins']
        row_df['HomeLosses'] = player['HomeLosses']
        row_df['HomeTies'] = player['HomeTies']
        row_df['HomeWinPct'] = player['HomeWinPct']
        row_df['HomeOTWins'] = player['HomeOTWins']
        row_df['HomeOTLosses'] = player['HomeOTLosses']
        row_df['HomeOTTies'] = player['HomeOTTies']
        row_df['HomeShootoutWins'] = player['HomeShootoutWins']
        row_df['HomeShootoutLosses'] = player['HomeShootoutLosses']
        row_df['HomeConferenceWins'] = player['HomeConferenceWins']
        row_df['HomeConferenceLosses'] = player['HomeConferenceLosses']
        row_df['HomeConferenceTies'] = player['HomeConferenceTies']
        row_df['HomeConferenceWinPct'] = player['HomeConferenceWinPct']
        row_df['HomeDivisionWins'] = player['HomeDivisionWins']
        row_df['HomeDivisionLosses'] = player['HomeDivisionLosses']
        row_df['HomeDivisionTies'] = player['HomeDivisionTies']
        row_df['HomeDivisionWinPct'] = str(player['HomeDivisionWinPct'])
        row_df['HockeyOTAndSOLosses'] = player['HockeyOTAndSOLosses']
        row_df['HockeyRegulationAndOTWins'] = player['HockeyRegulationAndOTWins']
        row_df['HockeyRoadOTAndSOLosses'] = player['HockeyRoadOTAndSOLosses']
        row_df['HockeyHomeOTAndSOLosses'] = player['HockeyHomeOTAndSOLosses']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    if save == True:
        
        main_df.to_csv(f'standings/{xfl_season}_xfl_standings.csv',index=False)
        main_df.to_parquet(f'standings/{xfl_season}_xfl_standings.parquet',index=False)


        main_df.to_parquet(f'standings/weekly_standings/parquet/{xfl_season}_{xfl_week}_xfl_standings.parquet',index=False)
        main_df.to_csv(f'standings/weekly_standings/csv/{xfl_season}_{xfl_week}_xfl_standings.csv',index=False)
        with open(f"standings/weekly_standings/json/{xfl_season}_{xfl_week}_xfl_standings.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    return main_df

def main():
    season = 2023
    week = 9
    get_xfl_standings(season,week,True)

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_hour = now.hour
    current_minute = now.minute

    with open('timestamp.json','w+') as f:
        f.write(f"{{ \"year\":{current_year},\"month\":{current_month},\"day\":{current_day},\"hour\":{current_hour},\"minute\":{current_minute}}}")


if __name__ == "__main__":
    main()