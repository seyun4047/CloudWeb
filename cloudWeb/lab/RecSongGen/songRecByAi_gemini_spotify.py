import os
import cv2
import requests
import sys
import google.generativeai as genai
from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

sys.path.append("../")
from ..QRGen import QRGenerator


class SongRecByAi:
    def __init__(self, path):
        self.path = path
        self.gen()

    def gen(self):
        songTitle = self.songGen()
        songUrl = self.get_video_links(songTitle)
        self.check_link_validity(songUrl)
        QRGenerator.QRGen(self.path, songUrl)

    def check_link_validity(self, url):
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.ConnectionError:
            print("error")
            return False

    def songGen(self):
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        image = cv2.imread(self.path)

        # print(image)
        def getResponseGemini():
            model = genai.GenerativeModel('gemini-pro')
            # response = model.generate_content(f"이미지의 텍스트를 주면 이에 어울리는 분위기를 파악하고 노래를 추천해줘. 노래는 k-pop 45%, j-pop 35%, global-music 20% 우선순위를 가져. 오래되지않은 노래면 좋겠어. 대답은 무조건 노래제목-가수이름 혹은 가수이름-노래제목 으로 알려줘. 예를들어 이렇게 대답해. 라일락-아이유. 다음은 이미지야. {image}")
            response = model.generate_content(f"If I give you the text of an image, it will identify the mood that matches it and recommend a song. Songs have 45% priority on k-pop, 35% on j-pop, and 20% on global-music. I hope it's a song that isn't old. Please tell me the answer as '[mv]song title-singer name' or '[mv]singer name-song title'. For example, answer like this: [mv]Lilac - IU. Next is the image. {image}")
            return response

        response = getResponseGemini()
        response = response.text
        print(response)

        return response

    def get_video_links(self, query):
        cid = os.getenv('SPOTIFY_CID')
        secret = os.getenv('SPOTIFY_SECRET')
        redirect_uri = 'http://localhost:8080/callback'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri))
        result = sp.search(query, limit=1, type='album')
        # pprint.pprint(result)
        print(result['albums']['items'][0]['external_urls']['spotify'])  # 첫번째 앨범 반환
        return result['albums']['items'][0]['external_urls']['spotify']

        # return video_link
# SongRecByAi("test2.jpeg")