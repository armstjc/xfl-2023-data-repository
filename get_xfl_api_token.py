import json
import os
import platform


def get_xfl_api_token(key_path=""):
    try:
        key = os.environ['XFL_API_TOKEN']
        return key
    except:
        print('The XFL API token was not found in this python environment. Attempting to load the API token from a file.')

    print(platform.uname().system)
    try:
        if platform.uname().system == "Windows":
            with open('C:/XFL/xfl_api.json', 'r') as f:
                json_data = json.loads(f.read())
        elif platform.uname().system == "Darwin":
            with open('/Users/Shared/XFL/xfl_api.json', 'r') as f:
                json_data = json.loads(f.read())
        else:
            with open(key_path, 'r') as f:
                json_data = json.loads(f.read())

        return json_data['xfl_api_token']
    except:
        raise FileNotFoundError(
            'The XFL API token was not found in your computer.')


if __name__ == "__main__":
    get_xfl_api_token()
