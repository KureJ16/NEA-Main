import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd


class AccessAccount:
  def __init__(self):
      self.path = "C:\Program Files (x86)\chromedriver.exe"
      self.client_data = "52627528c9534874add600fcbc20e20f:6b39cb1b336c4b05ab1ff328f12a56b9"
      self.client_data_base64 = "NTI2Mjc1MjhjOTUzNDg3NGFkZDYwMGZjYmMyMGUyMGY6NmIzOWNiMWIzMzZjNGIwNWFiMWZmMzI4ZjEyYTU2Yjk="
      self.url = "https://accounts.spotify.com"
      self.driver = None
      self.access_token = ""
      self.refresh_token = ""
      self.refresh_time = 45

  def initialiseDriver(self):
      self.driver = webdriver.Chrome(service=Service(self.path))

  def getAuthCode(self):
      self.initialiseDriver()
      self.driver.get(
          "https://accounts.spotify.com/en/authorize?client_id=52627528c9534874add600fcbc20e20f&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=playlist-modify-private,user-library-read,playlist-read-private")
      while True:
          try:
              self.driver.find_element(By.ID, 'reload-button').click()
              break
          except:
              pass
      return self.driver.current_url[37:]

  def getAccessToken(self):
      auth_code = self.getAuthCode()

      payload = {"grant_type": "authorization_code",
                 "code": auth_code,
                 "redirect_uri": "https://localhost:8888/callback"}
      headers = {"Authorization": "Basic " + self.client_data_base64}
      postr = requests.post(self.url + "/api/token", data=payload, headers=headers)
      self.access_token = postr.json()["access_token"]
      self.refresh_token = postr.json()["refresh_token"]
      return self.access_token

      self.driver.close()

  def refresh(self):
      payload = {"grant_type": "refresh_token",
                 "refresh_token": self.refresh_token}
      headers = {"Authorization": "Basic "+self.client_data_base64}
      postr = requests.post(self.url + "/api/token", data=payload, headers=headers)
      self.access_token = postr.json()["access_token"]
