import glob
import json
#import time
import warnings
from urllib.request import urlopen

import pandas as pd
from tqdm import tqdm

from get_xfl_api_token import get_xfl_api_token

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def get_xfl_player_box(game_id:str,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/playerstats?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        print(f"\nPlayer #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id,'OfficialID':official_id},index=[0])

        ##############################################################################################################
        ## Game Participation
        ##############################################################################################################
        ## No longer needed.

        ## G        
        # row_df['G'] = 1

        # ## GS
        # try:
        #     row_df['GamesStarted'] = player['GamesStarted']
        # except:
        #     row_df['GamesStarted'] = 0

        ##############################################################################################################
        ## Passing
        ##############################################################################################################
        
        ## COMP
        try:
            row_df['PassAtt'] = player['PassAtt']
        except:
            row_df['PassAtt'] = None

        ## ATT
        try:
            row_df['PassComp'] = player['PassComp']
        except:
            row_df['PassComp'] = None

        ## COMP%
        try:
            row_df['PassCompPercent'] = player['PassCompPercent']
        except:
            row_df['PassCompPercent'] = None
        
        ## PASS_YDS
        try:
            row_df['PassYards'] = player['PassYards']
        except:
            row_df['PassYards'] = None


        ## PASS_TD
        try:
            row_df['PassTD'] = player['PassTD']
        except:
            row_df['PassTD'] = None

        ## PASS_INT
        try:
            row_df['PassINT'] = player['PassINT']
        except:
            row_df['PassINT'] = None

        ## 1st Downs Passing
        try:
            row_df['FirstDownsByPass'] = player['FirstDownsByPass']
        except:
            row_df['FirstDownsByPass'] = None

        ## 1st Downs Passing Percent
        try:
            row_df['FirstDownPercentOfPasses'] = player['FirstDownPercentOfPasses']
        except:
            row_df['FirstDownPercentOfPasses'] = None

        ## PASS_LONG
        try:
            row_df['PassYardsLong'] = player['PassYardsLong']
        except:
            row_df['PassYardsLong'] = None

        ## PASS_LONG_TD
        try:
            row_df['PassYardsLongTD'] = player['PassYardsLongTD']
        except:
            row_df['PassYardsLongTD'] = None

        ## PASS_YPA
        try:
            row_df['PassYardsPerAtt'] = player['PassYardsPerAtt']
        except:
            row_df['PassYardsPerAtt'] = None

        ## PASS_YPC
        try:
            row_df['PassYardsPerComp'] = player['PassYardsPerComp']
        except:
            row_df['PassYardsPerComp'] = None

        ## QBRating (Not NFL, Not CFB)
        try:
            row_df['QBRating'] = player['QBRating']
        except:
            row_df['QBRating'] = None
        
        ## Sacked
        try:
            row_df['Sacked'] = player['Sacked']
        except:
            row_df['Sacked'] = None

        ## SackedYards
        try:
            row_df['SackedYards'] = player['SackedYards']
        except:
            row_df['SackedYards'] = None

        ## SackedYardsAvg
        try:
            row_df['SackedYardsAvg'] = player['SackedYardsAvg']
        except:
            row_df['SackedYardsAvg'] = None

        ## Pass20YdPlays
        try:
            row_df['Pass20YdPlays'] = player['Pass20YdPlays']
        except:
            row_df['Pass20YdPlays'] = None

        ## Pass40YdPlays
        try:
            row_df['Pass40YdPlays'] = player['Pass40YdPlays']
        except:
            row_df['Pass40YdPlays'] = None

        ##############################################################################################################
        ## Rushing
        ##############################################################################################################
        
        ## RUSH
        try:
            row_df['RushAtt'] = player['RushAtt']
        except:
            row_df['RushAtt'] = None
        
        ## RUSH_YDS
        try:
            row_df['RushYards'] = player['RushYards']
        except:
            row_df['RushYards'] = None
        
        ## RUSH_AVG
        try:
            row_df['RushYardsAvg'] = player['RushYardsAvg']
        except:
            row_df['RushYardsAvg'] = None

        ## RUSH_TD
        try:
            row_df['RushTD'] = player['RushTD']
        except:
            row_df['RushTD'] = None
        
        ## 1st Downs Rushing
        try:
            row_df['FirstDownsByRush'] = player['FirstDownsByRush']
        except:
            row_df['FirstDownsByRush'] = None

        ## 1st Downs Rushing Percent
        try:
            row_df['FirstDownPercentOfRushes'] = player['FirstDownPercentOfRushes']
        except:
            row_df['FirstDownPercentOfRushes'] = None
        
        ## RUSH_LONG
        try:
            row_df['RushYardsLong'] = player['RushYardsLong']
        except:
            row_df['RushYardsLong'] = None

        ## RUSH_LONG_TD
        try:
            row_df['RushYardsLongTD'] = player['RushYardsLongTD']
        except:
            row_df['RushYardsLongTD'] = None

        ## Rush10YdPlays
        try:
            row_df['Rush10YdPlays'] = player['Rush10YdPlays']
        except:
            row_df['Rush10YdPlays'] = None

        ## 1st Downs Rushing Percent
        try:
            row_df['Rush20YdPlays'] = player['Rush20YdPlays']
        except:
            row_df['Rush20YdPlays'] = None

        ##############################################################################################################
        ## Reciving
        ##############################################################################################################

        ## REC_TARGET
        try:
            row_df['RecThrownAt'] = player['RecThrownAt']
        except:
            row_df['RecThrownAt'] = None

        ## REC
        try:
            row_df['Recs'] = player['Recs']
        except:
            row_df['Recs'] = None
        
        ## REC_YDS
        try:
            row_df['RecYards'] = player['RecYards']
        except:
            row_df['RecYards'] = None
        
        ## REC_AVG
        try:
            row_df['RecYardsAvg'] = player['RecYardsAvg']
        except:
            row_df['RecYardsAvg'] = None

        ## REC_TD
        try:
            row_df['RecTD'] = player['RecTD']
        except:
            row_df['RecTD'] = None

        ## 1st Downs Reciving
        try:
            row_df['FirstDownsByRec'] = player['FirstDownsByRec']
        except:
            row_df['FirstDownsByRec'] = None

        ## 1st Downs Reciving Percent
        try:
            row_df['FirstDownPercentOfRecs'] = player['FirstDownPercentOfRecs']
        except:
            row_df['FirstDownPercentOfRecs'] = None

        ## REC_LONG
        try:
            row_df['RecYardsLong'] = player['RecYardsLong']
        except:
            row_df['RecYardsLong'] = None

        ## REC_LONG_TD
        try:
            row_df['RecYardsLongTD'] = player['RecYardsLongTD']
        except:
            row_df['RecYardsLongTD'] = None
        
        ## REC_YAC
        try:
            row_df['RecYardsAfterCatch'] = player['RecYardsAfterCatch']
        except:
            row_df['RecYardsAfterCatch'] = None

        ## REC_YAC_AVG
        try:
            row_df['RecYardsAfterCatchAvg'] = player['RecYardsAfterCatchAvg']
        except:
            row_df['RecYardsAfterCatchAvg'] = None

        ## REC_DROPS
        try:
            row_df['RecDropped'] = player['RecDropped']
        except:
            row_df['RecDropped'] = None

        ## Rec20YdPlays
        try:
            row_df['Rec20YdPlays'] = player['Rec20YdPlays']
        except:
            row_df['Rec20YdPlays'] = None

        ## Rec40YdPlays
        try:
            row_df['Rec40YdPlays'] = player['Rec40YdPlays']
        except:
            row_df['Rec40YdPlays'] = None


        ##############################################################################################################
        ## Fumble Stats
        ##############################################################################################################

        ## FUMBLES
        try:
            row_df['Fumbles'] = player['Fumbles']
        except:
            row_df['Fumbles'] = None

        ## FUMBLES_LOST
        try:
            row_df['Fumbles'] = player['Fumbles']
        except:
            row_df['Fumbles'] = None

        ## OFF_TD
        try:
            row_df['OffTD'] = player['OffTD']
        except:
            row_df['OffTD'] = None

        ##############################################################################################################
        ## Misc. Offense
        ##############################################################################################################
        
        ## 1st Downs Total
        try:
            row_df['FirstDowns'] = player['FirstDowns']
        except:
            row_df['FirstDowns'] = None

        ## 1st Downs Percent
        try:
            row_df['FirstDownPercent'] = player['FirstDownPercent']
        except:
            row_df['FirstDownPercent'] = None

        ## PAT1PtAttPass
        try:
            row_df['PAT1PtAttPass'] = player['PAT1PtAttPass']
        except:
            row_df['PAT1PtAttPass'] = None

        ## PAT1PtAttRec
        try:
            row_df['PAT1PtAttRec'] = player['PAT1PtAttRec']
        except:
            row_df['PAT1PtAttRec'] = None

        ## PAT1PtAttRush
        try:
            row_df['PAT1PtAttRush'] = player['PAT1PtAttRush']
        except:
            row_df['PAT1PtAttRush'] = None

        ## PAT1PtConvRush
        try:
            row_df['PAT1PtConvRush'] = player['PAT1PtConvRush']
        except:
            row_df['PAT1PtConvRush'] = None

        ## PAT1PtPctRush
        try:
            row_df['PAT1PtPctRush'] = player['PAT1PtPctRush']
        except:
            row_df['PAT1PtPctRush'] = None
        
        ## PAT2PtAttPass
        try:
            row_df['PAT2PtAttPass'] = player['PAT2PtAttPass']
        except:
            row_df['PAT2PtAttPass'] = None

        ## PAT2PtAttRec
        try:
            row_df['PAT2PtAttRec'] = player['PAT2PtAttRec']
        except:
            row_df['PAT2PtAttRec'] = None

        ## PAT2PtAttRush
        try:
            row_df['PAT2PtAttRush'] = player['PAT2PtAttRush']
        except:
            row_df['PAT2PtAttRush'] = None

        ## PAT2PtConvRush
        try:
            row_df['PAT2PtConvRush'] = player['PAT2PtConvRush']
        except:
            row_df['PAT2PtConvRush'] = None

        ## PAT2PtPctRush
        try:
            row_df['PAT2PtPctRush'] = player['PAT2PtPctRush']
        except:
            row_df['PAT2PtPctRush'] = None
        
        ## PAT3PtAttPass
        try:
            row_df['PAT3PtAttPass'] = player['PAT3PtAttPass']
        except:
            row_df['PAT3PtAttPass'] = None

        ## PAT3PtAttRec
        try:
            row_df['PAT3PtAttRec'] = player['PAT3PtAttRec']
        except:
            row_df['PAT3PtAttRec'] = None

        ## PAT3PtAttRush
        try:
            row_df['PAT3PtAttRush'] = player['PAT3PtAttRush']
        except:
            row_df['PAT3PtAttRush'] = None

        ## PAT3PtConvRush
        try:
            row_df['PAT3PtConvRush'] = player['PAT3PtConvRush']
        except:
            row_df['PAT3PtConvRush'] = None

        ## PAT3PtPctRush
        try:
            row_df['PAT3PtPctRush'] = player['PAT3PtPctRush']
        except:
            row_df['PAT3PtPctRush'] = None
        
        ## TotalTD
        try:
            row_df['TotalTD'] = player['TotalTD']
        except:
            row_df['TotalTD'] = None

        ## TotalYards
        try:
            row_df['TotalYards'] = player['TotalYards']
        except:
            row_df['TotalYards'] = None

        ##############################################################################################################
        ## Penalty Stats
        ##############################################################################################################

        ## PAT3PtConvRush
        try:
            row_df['Penalties'] = player['Penalties']
        except:
            row_df['Penalties'] = None

        ## PAT3PtPctRush
        try:
            row_df['PenaltyYards'] = player['PenaltyYards']
        except:
            row_df['PenaltyYards'] = None

        ##############################################################################################################
        ## Defensive Stats
        ##############################################################################################################

        ## TOTAL
        try:
            row_df['DefTackles'] = player['DefTackles']
        except:
            row_df['DefTackles'] = None

        ## SOLO
        try:
            row_df['DefSoloTackles'] = player['DefSoloTackles']
        except:
            row_df['DefSoloTackles'] = None

        ## AST
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = None

        ## QB_HITS
        try:
            row_df['DefQBHits'] = player['DefQBHits']
        except:
            row_df['DefQBHits'] = None

        ## TFL
        try:
            row_df['DefTacklesForLoss'] = player['DefTacklesForLoss']
        except:
            row_df['DefTacklesForLoss'] = None

        ## SACKS
        try:
            row_df['DefSacks'] = player['DefSacks']
        except:
            row_df['DefSacks'] = None
                    
        ## SACK_YDS
        try:
            row_df['DefSackYards'] = player['DefSackYards']
        except:
            row_df['DefSackYards'] = None

        ## SACK_YDS_AVG
        try:
            row_df['DefSackYardsAvg'] = player['DefSackYardsAvg']
        except:
            row_df['DefSackYardsAvg'] = None
                                    
        ## INT
        try:
            row_df['DefINT'] = player['DefINT']
        except:
            row_df['DefINT'] = None

        ## INT_YDS
        try:
            row_df['DefINTReturnYards'] = player['DefINTReturnYards']
        except:
            row_df['DefINTReturnYards'] = None

        ## INT_AVG
        try:
            row_df['DefINTReturnYardsAvg'] = player['DefINTReturnYardsAvg']
        except:
            row_df['DefINTReturnYardsAvg'] = None
                                        
        ## INT_TD
        try:
            row_df['DefINTReturnTD'] = player['DefINTReturnTD']
        except:
            row_df['DefINTReturnTD'] = None
        
        ## INT_LONG
        try:
            row_df['DefINTReturnYardsLong'] = player['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = None
                              
        ## PD
        try:
            row_df['DefINTReturnYardsLong'] = player['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = None
                              
        ## FF
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = None
        
        ## FR
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = None

        ##############################################################################################################
        ## Field Goal Stats
        ##############################################################################################################
        
        ## FGA
        try:
            row_df['FGAtt'] = player['FGAtt']
        except:
            row_df['FGAtt'] = None

        ## FGM
        try:
            row_df['FGMade'] = player['FGMade']
        except:
            row_df['FGMade'] = None

        ## FG_LONG
        try:
            row_df['FGLong'] = player['FGLong']
        except:
            row_df['FGLong'] = None

        ## FGA_0_19
        try:
            row_df['FG0To19Att'] = player['FG0To19Att']
        except:
            row_df['FG0To19Att'] = None

        ## FGM_0_19
        try:
            row_df['FG0To19Made'] = player['FG0To19Made']
        except:
            row_df['FG0To19Made'] = None

        ## FGM_0_19
        try:
            row_df['FG0To19Made'] = player['FG0To19Made']
        except:
            row_df['FG0To19Made'] = None

        ## FGA_20_29
        try:
            row_df['FG20To29Att'] = player['FG20To29Att']
        except:
            row_df['FG20To29Att'] = None

        ## FGM_20_29
        try:
            row_df['FG20To29Made'] = player['FG20To29Made']
        except:
            row_df['FG20To29Made'] = None
        ## FGA_30_39
        try:
            row_df['FG30To39Att'] = player['FG30To39Att']
        except:
            row_df['FG30To39Att'] = None

        ## FGM_30_39
        try:
            row_df['FG30To39Made'] = player['FG30To39Made']
        except:
            row_df['FG30To39Made'] = None

        ## FGA_40_49
        try:
            row_df['FG40To49Att'] = player['FG40To49Att']
        except:
            row_df['FG40To49Att'] = None

        ## FGM_40_49
        try:
            row_df['FG40To49Made'] = player['FG40To49Made']
        except:
            row_df['FG40To49Made'] = None

        ## FGA_50_59
        try:
            row_df['FG50PlusAtt'] = player['FG50PlusAtt']
        except:
            row_df['FG50PlusAtt'] = None

        ## FGM_50_59
        try:
            row_df['FG50PlusMade'] = player['FG50PlusMade']
        except:
            row_df['FG50PlusMade'] = None

        ##############################################################################################################
        ## Punting Stats
        ##############################################################################################################

        ## PUNTS
        try:
            row_df['Punts'] = player['Punts']
        except:
            row_df['Punts'] = None

        ## GROSS_PUNT_YDS
        try:
            row_df['PuntGrossYards'] = player['PuntGrossYards']
        except:
            row_df['PuntGrossYards'] = None

        ## GROSS_PUNT_AVG
        try:
            row_df['PuntGrossYardsAvg'] = player['PuntGrossYardsAvg']
        except:
            row_df['PuntGrossYardsAvg'] = None

        ## GROSS_PUNT_LONG
        try:
            row_df['PuntGrossYardsLong'] = player['PuntGrossYardsLong']
        except:
            row_df['PuntGrossYardsLong'] = None

        ## PUNT_TB
        try:
            row_df['PuntTouchbacks'] = player['PuntTouchbacks']
        except:
            row_df['PuntTouchbacks'] = None

        ## PUNT_INSIDE_20
        try:
            row_df['PuntInside20'] = player['PuntInside20']
        except:
            row_df['PuntInside20'] = None

        ##############################################################################################################
        ## Punt Return Stats
        ##############################################################################################################
        
        ## PR
        try:
            row_df['PuntRetReturns'] = player['PuntRetReturns']
        except:
            row_df['PuntRetReturns'] = None

        ## PR_YDS
        try:
            row_df['PuntRetYards'] = player['PuntRetYards']
        except:
            row_df['PuntRetYards'] = None

        ## PR_AVG
        try:
            row_df['PuntRetYardsAvg'] = player['PuntRetYardsAvg']
        except:
            row_df['PuntRetYardsAvg'] = None

        ## PR_TD
        try:
            row_df['PuntRetTD'] = player['PuntRetTD']
        except:
            row_df['PuntRetTD'] = None

        ## PR_LONG
        try:
            row_df['PuntRetYardsLong'] = player['PuntRetYardsLong']
        except:
            row_df['PuntRetYardsLong'] = None

        ## PR_FC
        try:
            row_df['PuntRetFairCatches'] = player['PuntRetFairCatches']
        except:
            row_df['PuntRetFairCatches'] = None

        ##############################################################################################################
        ## Kick Return Stats
        ##############################################################################################################
        
        ## KR
        try:
            row_df['KickRetReturns'] = player['KickRetReturns']
        except:
            row_df['KickRetReturns'] = None

        ## KR_YDS
        try:
            row_df['KickRetYards'] = player['KickRetYards']
        except:
            row_df['KickRetYards'] = None

        ## KR_AVG
        try:
            row_df['KickRetYardsAvg'] = player['KickRetYardsAvg']
        except:
            row_df['KickRetYardsAvg'] = None

        ## KR_TD
        try:
            row_df['KickRetTD'] = player['KickRetTD']
        except:
            row_df['KickRetTD'] = None

        ## KR_LONG
        try:
            row_df['KickRetYardsLong'] = player['KickRetYardsLong']
        except:
            row_df['KickRetYardsLong'] = None


        main_df = pd.concat([main_df,row_df],ignore_index=True)

    participation_df = pd.read_parquet(f'player_info/participation_data/parquet/{game_id}.parquet')
    participation_df = participation_df.filter(items=['Season','game_id','OfficialID','VisOrHome','JerseyNum','FirstName','LastName','LastNameSuffix','Position','Participated','IsStarting','Scratch'])

    finished_df = pd.merge(participation_df,main_df,left_on=['Season','game_id','OfficialID'],right_on=['Season','game_id','OfficialID'],how='left')

    del participation_df,main_df

    #main_df = pd.DataFrame(data=json_data)
    if save == True:
        
        finished_df.to_csv(f'game_stats/player/raw/csv/{game_id}.csv',index=False)
        finished_df.to_parquet(f'game_stats/player/raw/parquet/{game_id}.parquet',index=False)

        with open(f"game_stats/player/raw/json/{game_id}.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))


    return finished_df


def get_xfl_team_box(game_id:str,save=False):
    xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/teamstats?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for team in tqdm(json_data):
        
        official_id = team['OfficialId']
        print(f"{game_id}\tTeamID #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id,'OfficialID':official_id},index=[0])

        ###############################################################################################################################################################
        ## Team Stats
        ###############################################################################################################################################################
        try:
            row_df['PlaysPerGame'] = team['PlaysPerGame']
        except:
            row_df['PlaysPerGame'] = None

        try:
            row_df['Points'] = team['Points']
        except:
            row_df['Points'] = None

        try:
            row_df['DefPointsAgainst'] = team['DefPointsAgainst']
        except:
            row_df['DefPointsAgainst'] = None

        ###############################################################################################################################################################
        try:
            row_df['YardsPerGame'] = team['YardsPerGame']
        except:
            row_df['YardsPerGame'] = None
        
        try:
            row_df['DefYardsAgainst'] = team['DefYardsAgainst']
        except:
            row_df['DefYardsAgainst'] = None
        
        try:
            row_df['PassYardsPerGame'] = team['PassYardsPerGame']
        except:
            row_df['PassYardsPerGame'] = None

        try:
            row_df['DefPassYardsAgainst'] = team['DefPassYardsAgainst']
        except:
            row_df['DefPassYardsAgainst'] = None
        try:
            row_df['RushYardsPerGame'] = team['RushYardsPerGame']
        except:
            row_df['RushYardsPerGame'] = None

        try:
            row_df['DefRushYardsAgainst'] = team['DefRushYardsAgainst']
        except:
            row_df['DefRushYardsAgainst'] = None

        ###############################################################################################################################################################
        ## This exists in the JSON files, but was blank for week 1
        try:
            row_df['DriveStartYardlineAvg'] = team['DriveStartYardlineAvg']
        except:
            row_df['DriveStartYardlineAvg'] = None

        ###############################################################################################################################################################
        
        try:
            row_df['FirstDowns'] = team['FirstDowns']
        except:
            row_df['FirstDowns'] = None

        try:
            row_df['FirstDownsByPass'] = team['FirstDownsByPass']
        except:
            row_df['FirstDownsByPass'] = None

        try:
            row_df['FirstDownsByPenalty'] = team['FirstDownsByPenalty']
        except:
            row_df['FirstDownsByPenalty'] = None

        try:
            row_df['FirstDownsByRush'] = team['FirstDownsByRush']
        except:
            row_df['FirstDownsByRush'] = None

        try:
            row_df['FirstDownPercent'] = team['FirstDownPercent']
        except:
            row_df['FirstDownPercent'] = None

        try:
            row_df['FirstDownPercentOfPasses'] = team['FirstDownPercentOfPasses']
        except:
            row_df['FirstDownPercentOfPasses'] = None

        try:
            row_df['FirstDownPercentOfRushes'] = team['FirstDownPercentOfRushes']
        except:
            row_df['FirstDownPercentOfRushes'] = None
            
        ###############################################################################################################################################################
        
        try:
            row_df['ThirdDownConv'] = team['ThirdDownConv']
        except:
            row_df['ThirdDownConv'] = None

        try:
            row_df['ThirdDownAtt'] = team['ThirdDownAtt']
        except:
            row_df['ThirdDownAtt'] = None

        try:
            row_df['ThirdDownPercent'] = team['ThirdDownPercent']
        except:
            row_df['ThirdDownPercent'] = None
        
        ###############################################################################################################################################################
        
        try:
            row_df['FourthDownConv'] = team['FourthDownConv']
        except:
            row_df['FourthDownConv'] = None

        try:
            row_df['FourthDownAtt'] = team['FourthDownAtt']
        except:
            row_df['FourthDownAtt'] = None

        try:
            row_df['FourthDownPercent'] = team['FourthDownPercent']
        except:
            row_df['FourthDownPercent'] = None

        ###############################################################################################################################################################
        try:
            row_df['Penalties'] = team['Penalties']
        except:
            row_df['Penalties'] = None

        try:
            row_df['PenaltyYards'] = team['PenaltyYards']
        except:
            row_df['PenaltyYards'] = None

        try:
            row_df['PenaltiesOffensive'] = team['PenaltiesOffensive']
        except:
            row_df['PenaltiesOffensive'] = None

        try:
            row_df['PenaltyYardsOffensive'] = team['PenaltyYardsOffensive']
        except:
            row_df['PenaltyYardsOffensive'] = None

        try:
            row_df['PenaltiesDefensive'] = team['PenaltiesDefensive']
        except:
            row_df['PenaltiesDefensive'] = None

        try:
            row_df['PenaltyYardsDefensive'] = team['PenaltyYardsDefensive']
        except:
            row_df['PenaltyYardsDefensive'] = None

        ###############################################################################################################################################################
        try:
            row_df['Turnovers'] = team['Turnovers']
        except:
            row_df['Turnovers'] = None
        
        ###############################################################################################################################################################
        try:
            row_df['TotalTD'] = team['TotalTD']
        except:
            row_df['TotalTD'] = None
        
        try:
            row_df['OffTD'] = team['OffTD']
        except:
            row_df['OffTD'] = None

        try:
            top_seconds = team['TOPSeconds']
            top_min = top_seconds // 60
            top_seconds = top_seconds - (top_min * 60)
            row_df['TOPSeconds'] = top_seconds
            row_df['TOPStrfTime'] = f"{top_min}:{top_seconds}"
            del top_seconds, top_min
        except:
            pass
        ###############################################################################################################################################################
        ## Passing Stats
        ###############################################################################################################################################################

        try:
            row_df['PassComp'] = team['PassComp']
        except:
            row_df['PassComp'] = None

        try:
            row_df['PassAtt'] = team['PassAtt']
        except:
            row_df['PassAtt'] = None

        try:
            row_df['PassCompPercent'] = team['PassCompPercent']
        except:
            row_df['PassCompPercent'] = None

        try:
            row_df['PassYards'] = team['PassYards']
        except:
            row_df['PassYards'] = None

        try:
            row_df['PassTD'] = team['PassTD']
        except:
            row_df['PassTD'] = None

        try:
            row_df['PassINT'] = team['PassINT']
        except:
            row_df['PassINT'] = None
        
        try:
            row_df['PassYardsLong'] = team['PassYardsLong']
        except:
            row_df['PassYardsLong'] = None

        try:
            row_df['PassYardsLongTD'] = team['PassYardsLongTD']
        except:
            row_df['PassYardsLongTD'] = None

        try:
            row_df['PassYardsPerAtt'] = team['PassYardsPerAtt']
        except:
            row_df['PassYardsPerAtt'] = None

        try:
            row_df['PassYardsPerComp'] = team['PassYardsPerComp']
        except:
            row_df['PassYardsPerComp'] = None

        try:
            row_df['PassYardsAfterCatch'] = team['RecYardsAfterCatch']
        except:
            row_df['PassYardsAfterCatch'] = None

        try:
            row_df['PassYardsAfterCatchAvg'] = team['RecYardsAfterCatchAvg']
        except:
            row_df['PassYardsAfterCatchAvg'] = None

        try:
            row_df['RecDropped'] = team['RecDropped']
        except:
            row_df['RecDropped'] = None
        
        try:
            row_df['Sacked'] = team['Sacked']
        except:
            row_df['Sacked'] = None
        
        try:
            row_df['SackedYards'] = team['SackedYards']
        except:
            row_df['SackedYards'] = None

        try:
            row_df['SackedYardsAvg'] = team['SackedYardsAvg']
        except:
            row_df['SackedYardsAvg'] = None

        try:
            row_df['Pass20YdPlays'] = team['Pass20YdPlays']
        except:
            row_df['Pass20YdPlays'] = None
        
        try:
            row_df['Pass40YdPlays'] = team['Pass40YdPlays']
        except:
            row_df['Pass40YdPlays'] = None

        ###############################################################################################################################################################
        ## Rushing Stats
        ###############################################################################################################################################################

        try:
            row_df['RushAtt'] = team['RushAtt']
        except:
            row_df['RushAtt'] = None

        try:
            row_df['RushTD'] = team['RushTD']
        except:
            row_df['RushTD'] = None

        try:
            row_df['RushYards'] = team['RushYards']
        except:
            row_df['RushYards'] = None

        try:
            row_df['RushYardsAvg'] = team['RushYardsAvg']
        except:
            row_df['RushYardsAvg'] = None

        try:
            row_df['RushYardsLong'] = team['RushYardsLong']
        except:
            row_df['RushYardsLong'] = None

        try:
            row_df['RushYardsLongTD'] = team['RushYardsLongTD']
        except:
            row_df['RushYardsLongTD'] = None
        
        try:
            row_df['Rush20YdPlays'] = team['Rush20YdPlays']
        except:
            row_df['Rush20YdPlays'] = None
        
        try:
            row_df['Rush40YdPlays'] = team['Rush40YdPlays']
        except:
            row_df['Rush40YdPlays'] = None

        ###############################################################################################################################################################
        ## Conversion Stats
        ###############################################################################################################################################################

        try:
            row_df['PAT1PtAtt'] = team['PAT1PtAtt']
        except:
            row_df['PAT1PtAtt'] = None
        
        try:
            row_df['PAT1PtConv'] = team['PAT1PtConv']
        except:
            row_df['PAT1PtConv'] = None
        
        try:
            row_df['PAT1PtPct'] = team['PAT1PtPct']
        except:
            row_df['PAT1PtPct'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT1PtAttPass'] = team['PAT1PtAttPass']
        except:
            row_df['PAT1PtAttPass'] = None
        
        try:
            row_df['PAT1PtConvPass'] = team['PAT1PtConvPass']
        except:
            row_df['PAT1PtConvPass'] = None
        
        try:
            row_df['PAT1PtPctPass'] = team['PAT1PtPctPass']
        except:
            row_df['PAT1PtPctPass'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT1PtAttRush'] = team['PAT1PtAttRush']
        except:
            row_df['PAT1PtAttRush'] = None
        
        try:
            row_df['PAT1PtConvRush'] = team['PAT1PtConvRush']
        except:
            row_df['PAT1PtConvRush'] = None
        
        try:
            row_df['PAT1PtPctRush'] = team['PAT1PtPctRush']
        except:
            row_df['PAT1PtPctRush'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAtt'] = team['PAT2PtAtt']
        except:
            row_df['PAT2PtAtt'] = None
        
        try:
            row_df['PAT2PtConv'] = team['PAT2PtConv']
        except:
            row_df['PAT2PtConv'] = None

        try:
            row_df['PAT2PtPct'] = team['PAT2PtPct']
        except:
            row_df['PAT2PtPct'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAttPass'] = team['PAT2PtAttPass']
        except:
            row_df['PAT2PtAttPass'] = None

        try:
            row_df['PAT2PtConvPass'] = team['PAT2PtConvPass']
        except:
            row_df['PAT2PtConvPass'] = None
        
        try:
            row_df['PAT2PtPctPass'] = team['PAT2PtPctPass']
        except:
            row_df['PAT2PtPctPass'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAttRush'] = team['PAT2PtAttRush']
        except:
            row_df['PAT2PtAttRush'] = None
        
        try:
            row_df['PAT2PtConvRush'] = team['PAT2PtConvRush']
        except:
            row_df['PAT2PtConvRush'] = None

        try:
            row_df['PAT2PtPctRush'] = team['PAT2PtPctRush']
        except:
            row_df['PAT2PtPctRush'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtAtt'] = team['PAT3PtAtt']
        except:
            row_df['PAT3PtAtt'] = None
        
        try:
            row_df['PAT3PtConv'] = team['PAT3PtConv']
        except:
            row_df['PAT3PtConv'] = None

        try:
            row_df['PAT3PtPct'] = team['PAT3PtPct']
        except:
            row_df['PAT3PtPct'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtConvPass'] = team['PAT3PtConvPass']
        except:
            row_df['PAT3PtConvPass'] = None
        
        try:
            row_df['PAT3PtAttPass'] = team['PAT3PtAttPass']
        except:
            row_df['PAT3PtAttPass'] = None

        try:
            row_df['PAT3PtPctPass'] = team['PAT3PtPctPass']
        except:
            row_df['PAT3PtPctPass'] = None

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtConvRush'] = team['PAT3PtConvRush']
        except:
            row_df['PAT3PtConvRush'] = None
        
        try:
            row_df['PAT3PtAttRush'] = team['PAT3PtAttRush']
        except:
            row_df['PAT3PtAttRush'] = None
        
        try:
            row_df['PAT3PtPctRush'] = team['PAT3PtPctRush']
        except:
            row_df['PAT3PtPctRush'] = None


        ###############################################################################################################################################################
        ## Fumble Stats
        ###############################################################################################################################################################

        try:
            row_df['Fumbles'] = team['Fumbles']
        except:
            row_df['Fumbles'] = None
        
        try:
            row_df['FumblesLost'] = team['FumblesLost']
        except:
            row_df['FumblesLost'] = None

        ###############################################################################################################################################################
        ## Defensive Stats
        ###############################################################################################################################################################

        try:
            row_df['DefTackles'] = team['DefTackles']
        except:
            row_df['DefTackles'] = None

        try:
            row_df['DefTacklesForLoss'] = team['DefTacklesForLoss']
        except:
            row_df['DefTacklesForLoss'] = None
        
        try:
            row_df['DefQBHits'] = team['DefQBHits']
        except:
            row_df['DefQBHits'] = None

        ###############################################################################################################################################################
        try:
            row_df['DefSacks'] = team['DefSacks']
        except:
            row_df['DefSacks'] = None

        try:
            row_df['DefSackYards'] = team['DefSackYards']
        except:
            row_df['DefSackYards'] = None
        
        try:
            row_df['DefSackYardsAvg'] = team['DefSackYardsAvg']
        except:
            row_df['DefSackYardsAvg'] = None

        ###############################################################################################################################################################
        try:
            row_df['DefINT'] = team['DefINT']
        except:
            row_df['DefINT'] = None
        
        try:
            row_df['DefINTReturnYards'] = team['DefINTReturnYards']
        except:
            row_df['DefINTReturnYards'] = None
        try:
            row_df['DefINTReturnYardsAvg'] = team['DefINTReturnYardsAvg']
        except:
            row_df['DefINTReturnYardsAvg'] = None
        
        try:
            row_df['DefINTReturnTD'] = team['DefINTReturnTD']
        except:
            row_df['DefINTReturnTD'] = None
        
        try:
            row_df['DefINTReturnYardsLong'] = team['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = None
        
        try:
            row_df['DefPassesDefended'] = team['DefPassesDefended']
        except:
            row_df['DefPassesDefended'] = None

        ###############################################################################################################################################################
        try:
            row_df['DefFumblesForced'] = team['DefFumblesForced']
        except:
            row_df['DefFumblesForced'] = None

        try:
            row_df['DefFumblesRecovered'] = team['DefFumblesRecovered']
        except:
            row_df['DefFumblesRecovered'] = None

        ###############################################################################################################################################################
        ## Field Goal Stats
        ###############################################################################################################################################################
        
        try:
            row_df['Punts'] = team['Punts']
        except:
            row_df['Punts'] = None
        
        try:
            row_df['PuntGrossYards'] = team['PuntGrossYards']
        except:
            row_df['PuntGrossYards'] = None
        
        try:
            row_df['PuntGrossYardsAvg'] = team['PuntGrossYardsAvg']
        except:
            row_df['PuntGrossYardsAvg'] = None

        try:
            row_df['PuntGrossYardsLong'] = team['PuntGrossYardsLong']
        except:
            row_df['PuntGrossYardsLong'] = None
        
        try:
            row_df['PuntTouchbacks'] = team['PuntTouchbacks']
        except:
            row_df['PuntTouchbacks'] = None

        try:
            row_df['PuntInside20'] = team['PuntInside20']
        except:
            row_df['PuntInside20'] = None

        ###############################################################################################################################################################
        ## Field Goal Stats
        ###############################################################################################################################################################
        try:
            row_df['FGAtt'] = team['FGAtt']
        except:
            row_df['FGAtt'] = None

        try:
            row_df['FGMade'] = team['FGMade']
        except:
            row_df['FGMade'] = None
        
        try:
            row_df['FGLong'] = team['FGLong']
        except:
            row_df['FGLong'] = None

        ###############################################################################################################################################################
        ## Kick Return Stats
        ###############################################################################################################################################################

        try:
            row_df['KickRetReturns'] = team['KickRetReturns']
        except:
            row_df['KickRetReturns'] = None
        
        try:
            row_df['KickRetYards'] = team['KickRetYards']
        except:
            row_df['KickRetYards'] = None
        
        try:
            row_df['KickRetYardsAvg'] = team['KickRetYardsAvg']
        except:
            row_df['KickRetYardsAvg'] = None
        
        try:
            row_df['KickRetTD'] = team['KickRetTD']
        except:
            row_df['KickRetTD'] = None
        
        try:
            row_df['KickRetYardsLong'] = team['KickRetYardsLong']
        except:
            row_df['KickRetYardsLong'] = None
        
        try:
            row_df['KickRetFairCatches'] = team['KickRetFairCatches']
        except:
            row_df['KickRetFairCatches'] = None

        ###############################################################################################################################################################
        ## Punt Return Stats
        ###############################################################################################################################################################
        
        try:
            row_df['PuntRetReturns'] = team['PuntRetReturns']
        except:
            row_df['PuntRetReturns'] = None
        
        try:
            row_df['PuntRetYards'] = team['PuntRetYards']
        except:
            row_df['PuntRetYards'] =  None
        
        try:
            row_df['PuntRetYardsAvg'] = team['PuntRetYardsAvg']
        except:
            row_df['PuntRetYardsAvg'] = None
        
        try:
            row_df['PuntRetTD'] = team['PuntRetTD']
        except:
            row_df['PuntRetTD'] = None

        try:
            row_df['PuntRetYardsLong'] = team['PuntRetYardsLong']
        except:
            row_df['PuntRetYardsLong'] = None

        try:
            row_df['PuntRetFairCatches'] = team['PuntRetFairCatches']
        except:
            row_df['PuntRetFairCatches'] = None

        main_df = pd.concat([main_df,row_df],ignore_index=True)
        
    if save == True:
        
        main_df.to_csv(f'game_stats/team/raw/csv/{game_id}.csv',index=False)
        main_df.to_parquet(f'game_stats/team/raw/parquet/{game_id}.parquet',index=False)

        with open(f"game_stats/team/raw/json/{game_id}.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))

    return main_df

def combine_player_box():
    main_df = pd.DataFrame()
    game_df = pd.DataFrame()
    season_df = pd.DataFrame()
    file_path = "game_stats/player/raw/csv/"

    for file in glob.iglob(file_path+"*.csv"):
        game_df = pd.read_csv(file)
        main_df = pd.concat([main_df,game_df],ignore_index=True)

    del game_df

    seasons_arr = main_df['Season'].to_list()
    seasons_arr = [*set(seasons_arr)]

    for i in seasons_arr:
        season_df = main_df[main_df['Season'] == i]
        season_df.to_csv(f"game_stats/player/csv/{i}_xfl_player_game_stats.csv",index=False)
        season_df.to_parquet(f"game_stats/player/parquet/{i}_xfl_player_game_stats.parquet",index=False)

def combine_team_box():
    main_df = pd.DataFrame()
    game_df = pd.DataFrame()
    season_df = pd.DataFrame()
    file_path = "game_stats/team/raw/csv/"

    for file in glob.iglob(file_path+"*.csv"):
        game_df = pd.read_csv(file)
        main_df = pd.concat([main_df,game_df],ignore_index=True)

    del game_df

    seasons_arr = main_df['Season'].to_list()
    seasons_arr = [*set(seasons_arr)]

    for i in seasons_arr:
        season_df = main_df[main_df['Season'] == i]
        season_df.to_csv(f"game_stats/team/csv/{i}_xfl_player_game_stats.csv",index=False)
        season_df.to_parquet(f"game_stats/team/parquet/{i}_xfl_player_game_stats.parquet",index=False)


def main():
    sched_df = pd.read_csv('schedule/2023_xfl_schedule.csv')
    event_id_arr = sched_df['EventId'].to_list()
    
    for i in event_id_arr:
        get_xfl_player_box(i,True)
        get_xfl_team_box(i,True)
        
    combine_player_box()
    #combine_team_box()

if __name__ == "__main__":
    main()
