# import os
# import shutil
import time
import urllib.request

import pandas as pd
from tqdm import tqdm


def get_xfl_headshots(season:int):
    """
    
    """
    players_df = pd.read_csv(f'rosters/{season}_xfl_roster.csv')
    players_df = players_df.dropna(subset=['CloudHeadshotURL'])
    urls_arr = players_df['CloudHeadshotURL'].to_list()
    player_ids_arr = players_df['OfficialID'].to_list()

    for i in tqdm(range(0,len(urls_arr))):
        try:
            urllib.request.urlretrieve(urls_arr[i],filename=f"player_info/photos/{player_ids_arr[i]}.png")
        except:
            
            print(f'Could not retrive the photo for player #{player_ids_arr[i]}.')


        time.sleep(1)

def main():
    get_xfl_headshots(2023)

if __name__ == "__main__":
    main()