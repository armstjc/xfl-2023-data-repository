import json
import time
from urllib.request import urlopen, urlretrieve

import pandas as pd
from tqdm import tqdm

def get_xfl_schedule(season=2023,save=False,save_photos=False):
    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    ## This gets the rosters for all teams, rather than a specific game.
    url = f"https://www.xfl.com/content/draft/draft-pick.json?season={season}"
    response = urlopen(url)
    json_data = json.loads(response.read())

    draft_year = json_data['draft']['year']

    ovr_draft_pick = 0

    for i in json_data['draft']['groups']:
        draft_section = i['number']
        draft_section_name = i['title']

        print(f'Retriving draft results from secton #{draft_section}: {draft_section_name}.')
        
        for j in tqdm(i['picks']):
            ovr_draft_pick += 1
            row_df = pd.DataFrame({'draft_year':draft_year,'draft_section':draft_section,'draft_section_name':draft_section_name},index=[0])
            row_df['overall_draft_pick'] = ovr_draft_pick
            row_df['draft_section_pick'] = j['number']
            row_df['draft_section_round'] = j['round']
            row_df['draft_team_name'] = j['team']
            player_id = j['player']['id']
            row_df['player_id'] = player_id
            row_df['player_first_name'] = j['player']['firstName']
            row_df['player_last_name'] = j['player']['lastName']
            player_photo_url = j['player']['photo']
            row_df['player_photo_url'] = player_photo_url
            row_df['player_position'] = j['player']['position']
            row_df['player_last_team'] = j['player']['lastTeam']

            main_df = pd.concat([main_df,row_df],ignore_index=True)
            
            if save_photos == True and player_photo_url != None and player_photo_url != '':
                try:
                    urlretrieve(player_photo_url,filename=f"player_info/photos/{player_id}.png")
                    time.sleep(0.5)
                except:
                    print(f'Could not retrive the photo for player #{player_id}.')
                    time.sleep(1)
            

    if (save == True):
        main_df.to_csv(f'draft/csv/{season}_xfl_draft.csv',index=False)
        main_df.to_parquet(f'draft/parquet/{season}_xfl_draft.parquet',index=False)

        with open(f"draft/json/2023_xfl_draft.json", "w+") as f:
            f.write(json.dumps(json_data,indent=2))


    return main_df

if __name__ == "__main__":
    print(get_xfl_schedule(save=True))