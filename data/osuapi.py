import requests
import json

apiurl = "https://osu.ppy.sh/api/"
apikey = ""

with open("./config.json") as file:
    contents = json.loads(file.read())
    apikey = contents["osu"]["osu_api"]


def getPlayer(username):
    request = requests.get(f"{apiurl}get_user?k={apikey}&u={username}&m=0")
    if request.status_code != 200:
        print(f"Error fetching data, status code {request.status_code}")
        return None
    data = request.json()
    print(data)
    return data[0]
