import os
import cv2
import requests
import sys
import google.generativeai as genai
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
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
            response = model.generate_content(f"I'm going to give the text of the image. You recommend a song by understanding the mood, emotion, environment, time, season, etc. of this text. Songs have priorities of 25% in k-pop, 25% in j-pop, 15% in Taiwanese music, 5% in Hong Kong music, 5% in Chinese music, and 30% in global music. Please tell me the answer as '[mv]song title-singer name' or '[mv]singer name-song title' and K-pop is in Korean, j-pop is in Japanese, China, Taiwan and Hong Kong are in Chinese, and global music is in English. For example, answer like this: [mv]Lilac - IU. Next is the image. {image}")
            return response

        response = getResponseGemini()
        response = response.text

        return response
    def get_video_links(self, query):
        cid = os.getenv('SPOTIFY_CID')
        secret = os.getenv('SPOTIFY_SECRET')
        redirect_uri = 'http://mutzin.site/lab/songqrup/callback'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri))
        result = sp.search(query, limit=1, type='album')
        # pprint.pprint(result)
        print(result['albums']['items'][0]['external_urls']['spotify'])  # 첫번째 앨범 반환
        return result['albums']['items'][0]['external_urls']['spotify']

        # return video_link
# SongRecByAi("test2.jpeg")