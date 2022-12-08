from Login import AccessAccount
from Functions import Functions
import requests
import time
import pandas as pd

class GatherData(Functions):
  def __init__(self, mood1, mood2):
      get_token = AccessAccount()
      self.access_token = get_token.getAccessToken()
      self.moods = [mood1, mood2]
      self.playlists = self.listOfPlaylists()

  def getCsvFile(self):
      for c in range(len(self.moods)):
          mood = self.moods[c]
          playlist_ids = []
          for i in range(len(self.playlists)):
              if mood in self.playlists[i]["name"].lower():
                  playlist_ids.append(self.playlists[i]["id"])
          song_ids = []
          for z in range(len(playlist_ids)):
              list_of_songs_in_playlist_temp = requests.get("https://api.spotify.com/v1/playlists/" + playlist_ids[z] + "/tracks",
                                                            headers={"Authorization": "Bearer " + self.access_token})
              song_objects = list_of_songs_in_playlist_temp.json()["items"]
              for n in range(len(song_objects)):
                  song_ids.append(song_objects[n]["track"]["id"])
                  print(song_objects[n]["track"]["name"])
          for j in range(len(song_ids)):
              audio_features_get = requests.get("https://api.spotify.com/v1/audio-features?ids=" + song_ids[j],
                                                headers={"Authorization": "Bearer " + self.access_token})
              audio_features = audio_features_get.json()["audio_features"]
              audio_features_dict = audio_features[0]
              for g in range(7):
                  audio_features_dict.popitem()
              if j == 0:
                  song_stats = pd.DataFrame(data=audio_features_dict, index=[0])
              else:
                  song_stats_temp = pd.DataFrame(data=audio_features_dict, index=[0])
                  song_stats = pd.concat([song_stats, song_stats_temp], ignore_index=True)
              time.sleep(0.1)
          song_stats.to_csv(mood+"_song_stats.csv")


coolandcringe = GatherData("cool","cringe")
coolandcringe.getCsvFile()
