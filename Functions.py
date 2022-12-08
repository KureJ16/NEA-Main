
import requests
import pandas as pd
from Login import AccessAccount


class Functions(AccessAccount):
   def __init__(self):
       self.user_id = ""
       get_token = AccessAccount()
       self.access_token = get_token.getAccessToken()

   def getUserID(self):
       openr = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": "Bearer " + self.access_token})
       self.user_id = openr.json()["id"]

   def addPlaylist(self, name, public_status, description):
       self.getUserID()
       playlistr = requests.post("https://api.spotify.com/v1/users/" + self.user_id + "/playlists",
                                 headers={"Authorization": "Bearer " + self.access_token},
                                 json={"name": name, "public": public_status, "description": description})

   def findSongStats(self, song_name, song_artist):
       song_id = ""
       song_json = requests.get("https://api.spotify.com/v1/search?q=" + song_name.lower() + "&type=track",
                                headers={"Authorization": "Bearer " + self.access_token})
       for n in range(len(song_json.json()["tracks"]["items"])):
           if (song_json.json()["tracks"]["items"][n]["name"].lower() == song_name.lower()) and (
                   song_json.json()["tracks"]["items"][n]["album"]["artists"][0][
                       "name"].lower() == song_artist.lower()):
               song_id = song_json.json()["tracks"]["items"][n]["id"]
               break
       try:
           audio_features_retreived = requests.get("https://api.spotify.com/v1/audio-features?ids=" + song_id,
                                                   headers={"Authorization": "Bearer " + self.access_token})
           audio_features_for_song = audio_features_retreived.json()["audio_features"][0]
           for g in range(7):
               audio_features_for_song.popitem()
           test_song_data = pd.DataFrame(data=audio_features_for_song, index=[0])
           return test_song_data
       except AttributeError:
           print("Song not found")
           return

   def listOfPlaylists(self):
       self.getUserID()
       list_of_playlists = requests.get("https://api.spotify.com/v1/users/" + self.user_id + "/playlists",
                                        headers={"Authorization": "Bearer " + self.access_token})
       return list_of_playlists.json()["items"]
