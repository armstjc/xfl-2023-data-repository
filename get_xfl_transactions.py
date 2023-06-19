# from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd
import requests


def get_xfl_transactions(season=2024, save=False):
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = f"https://www.xfl.com/xfl-transactions"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')

    table_rows = soup.find_all('tr')

    for i in range(1, len(table_rows)):
        t_rows = table_rows[i]
        t_cells = t_rows.find_all('td')
        team_logo_url = t_cells[0].find('img').get('src')
        team_id = ""

        match team_logo_url:
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-st-louis-battlehawks-500x500.png":
                team_id = "STL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-st-louis-battlehawks-500x500.png":
                team_id = "STL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-houston-roughnecks-500x500.png":
                team_id = "HOU"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-houston-roughnecks-500x500.png":
                team_id = "HOU"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "SEA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-seattle-sea-dragons-500x500.png":
                team_id = "SEA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555935/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-arlington-renegades-500x500.png":
                team_id = "ARL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-arlington-renegades-500x500.png":
                team_id = "ARL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-dc-defenders-500x500.png":
                team_id = "DC"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-dc-defenders-500x500.png":
                team_id = "DC"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-san-antonio-brahmas-500x500.png":
                team_id = "SA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-san-antonio-brahmas-500x500.png":
                team_id = "SA"
            case _:
                raise ValueError(
                    f'Unhandled Team abreviation: {team_logo_url}')

        row_df = pd.DataFrame(columns=['team_id', 'team_logo_url'], data=[
                              [team_id, team_logo_url]])
        row_df['date'] = t_cells[1].text
        row_df['player_name'] = t_cells[2].text
        row_df['player_position'] = t_cells[3].text
        row_df['transaction_type'] = t_cells[4].text
        main_df = pd.concat([main_df, row_df], ignore_index=True)

    print(main_df)
    if save == True:
        main_df.to_csv(
            f'player_info/transactions/{season}_xfl_transactions.csv', index=False)
    return main_df


if __name__ == "__main__":
    get_xfl_transactions(save=True)
