import os
import cv2
import requests
import sys
import google.generativeai as genai
from googleapiclient.discovery import build
import spotipy
# from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
# import pprint

sys.path.append("../")
from ..QRGen import QRGenerator

class SongRecByAi:
    def __init__(self, path, color, background):
        self.path = path
        self.color = color
        self.background = background
        self.gen()

    def gen(self):
        songTitle = self.songGen()
        self.songUrl = self.get_video_links(songTitle)
        self.check_link_validity(self.songUrl)
        QRGenerator.QRGen(self.path, self.songUrl, self.color, self.background)

    def check_link_validity(self, url):
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                # print("checked link validity!")
                return True
            else:
                return False
        except requests.ConnectionError:
            # print("error")
            return False

    def songGen(self):
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        image = cv2.imread(self.path)

#         # print(image)
        def getResponseGemini():
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"I'm going to give the text of the image. You recommend a song by understanding the mood, emotion, environment, time, season, etc. of this text. Songs have priorities of 50% in k-pop, 25% in j-pop, and 25% in global music. Please tell me the answer as '[mv]song title-singer name' or '[mv]singer name-song title' and K-pop is in Korean like 아이유-라일락, J-pop is in Japanese, and global music is in English. For example, answer like this: Lilac - IU. Next is the image. {image}")
            return response

        response = getResponseGemini()
        response = response.text

        return response
    def get_video_links(self, query):
        cid = os.getenv('SPOTIFY_CID')
        secret = os.getenv('SPOTIFY_SECRET')
        redirect_uri = 'http://mutzin.site/lab/songqrup/callback'
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        result = sp.search(query, limit=1, type='album')
        # pprint.pprint(result)
        print(result['albums']['items'][0]['external_urls']['spotify'])  # 첫번째 앨범 반환
        return result['albums']['items'][0]['external_urls']['spotify']

        # return video_link
# SongRecByAi("test2.jpeg")