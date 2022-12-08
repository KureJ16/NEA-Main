import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from statsmodels.api import OLS
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import lyricsgenius as lg
from Functions import Functions
from transformers import pipeline
import math


class LearnFromData:
   def __init__(self, file_name1, file_name2, focus_emotion):
       self.focus_emotion = focus_emotion
       self.songs_from_file1 = pd.read_csv(file_name1, index_col=0)
       self.songs_from_file1[self.focus_emotion] = 1
       self.songs_from_file2 = pd.read_csv(file_name2, index_col=0)
       self.songs_from_file2[self.focus_emotion] = 0
       self.songs = pd.concat([self.songs_from_file1, self.songs_from_file2], ignore_index=True)
       self.songs["loudness"] *= -1
       self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
           self.songs.drop([self.focus_emotion], axis=1), self.songs[self.focus_emotion], test_size=0.33,
           random_state=30)

   def pairplot(self):
       sns.pairplot(self.songs, hue=self.focus_emotion)
       plt.show(block=True)

   def olsRegressionTest(self):
       ols_model = OLS(self.y_train, self.x_train)
       res = ols_model.fit()
       print(res.summary())

   def randomForestTest(self):
       rf = RandomForestRegressor(criterion='squared_error')
       rf.fit(self.x_train, self.y_train)
       trees = rf.estimators_
       feature_importances = pd.DataFrame(index=self.songs.drop([self.focus_emotion], axis=1).columns)

       for i in range(len(trees)):
           col_name = "tree_" + str(i)
           feature_importances[col_name] = trees[i].feature_importances_

       tree_names = feature_importances.columns
       feature_importances['mean_feature_importance'] = feature_importances[tree_names].mean(axis=1)

       feature_importances = feature_importances.sort_values(by=['mean_feature_importance'], ascending=False)

       feature_importances = feature_importances.drop('mean_feature_importance', axis=1)

       fig, ax = plt.subplots(1, 1, figsize=(15, 4))
       sns.barplot(
           data=feature_importances.T,
           ax=ax,
           ci="sd"
       )
       ax.set_xticklabels(rotation=90, labels=feature_importances.index);

       plt.show(block=True)

   def naiveBayesTest(self, nameFromHTML, artistFromHTML):
       test = Functions()
       feeling = ""
       while True:
           name = str(nameFromHTML)
           artist = str(artistFromHTML)
           sentiment = self.sentimentAnalysisTest(artist, name)
           print("lyric score:",sentiment)
           data = test.findSongStats(name, artist)
           try:
               data["loudness"] *= -1
               mnb = MultinomialNB()
               mnb.fit(self.x_train, self.y_train)
               #print(mnb.score(self.x_train, self.y_train))
               #print(mnb.score(self.x_test, self.y_test))
               score = (mnb.predict(data) + sentiment)/2
               print("song features score:",mnb.predict(data))
               print("overall score:",score)
               if score > 0.5:
                   print(name, "is a sad song")
                   feeling = "sad"
                   return score, feeling
               elif score < 0.5:
                   print(name, "is a happy song")
                   feeling = "happy"
                   return score, feeling
               else:
                   feeling = "undeterminable"
                   return score, feeling
               again = str(input("Would you like to enter another song (Y/N)? "))
               if again.lower() == "n":
                   break
           except TypeError:
               pass

   def sentimentAnalysisTest(self, artistToFind, songToFind):
       api_key = "r8Nw6Np7KGdBHlVwRJYWnC2CHmXj-3R9kXNaCCjJsTNg6Q4KCzK6Ukst3kjZgNJv"
       genius = lg.Genius(api_key)
       song = genius.search_song(songToFind, artistToFind)
       sentimentPipeline = pipeline("sentiment-analysis")
       if (len(song.lyrics)/500) < 2:
           sentimentScore = sentimentPipeline(song.lyrics)
       elif (len(song.lyrics)/500) < 3:
           sentimentScore1 = sentimentPipeline(song.lyrics[:int(len(song.lyrics)/2)])
           sentimentScore2 = sentimentPipeline(song.lyrics[int(len(song.lyrics)/2):])
           sentimentScore = [sentimentScore1,sentimentScore2]
       elif (len(song.lyrics)/500) < 4:
           sentimentScore1 = sentimentPipeline(song.lyrics[:int(len(song.lyrics)/3)])
           sentimentScore2 = sentimentPipeline(song.lyrics[int(len(song.lyrics)/3):2*(int(len(song.lyrics)/3))])
           sentimentScore3 = sentimentPipeline(song.lyrics[2*(int(len(song.lyrics)/3)):])
           sentimentScore = [sentimentScore1,sentimentScore2, sentimentScore3]
       sentimentScoreTotal = 0
       if len(sentimentScore)==1:
           if sentimentScore[0]["label"] == "POSITIVE":
               sentimentScoreTotal += sentimentScore[0]["score"] - 1
           elif sentimentScore[0]["label"] == "NEGATIVE":
               sentimentScoreTotal += sentimentScore[0]["score"]
       else:
           for i in sentimentScore:
               if i[0]["label"] == "POSITIVE":
                   sentimentScoreTotal += i[0]["score"]-1
               elif i[0]["label"] == "NEGATIVE":
                   sentimentScoreTotal += i[0]["score"]
       finalSentiment = sentimentScoreTotal/len(sentimentScore)
       return finalSentiment
