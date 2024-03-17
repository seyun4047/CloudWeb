import os
import cv2
import requests
import sys
import textwrap
import google.generativeai as genai
from googleapiclient.discovery import build
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

sys.path.append("../")
from ..QRGen import QRGenerator


class SongRecByAi:
    def __init__(self, path):
        self.path = path
        self.gen()
        # self.qrGen()

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
            # response = model.generate_content(f"This is the settings taken from a certain photo. Look at this and recommend a song in your own way. This is the Text: camera brand:{data[0]},camera model:{data[1]},The time taken:{data[2]},Shutter Speed:{data[3]},ExposureTime:{data[4]},ISO:{data[5]},Fnumber:{data[6]}Lens:{data[7]}. You must not say anything other than the YouTube link(can Watch). Like: https://www.youtube.com/watch?v=VdQY7BusJNU ")
            # response = model.generate_content(f"This is the settings taken from a certain photo. Look at this and Please recommend a song you found on YouTube(can watch). This is the image: {image}. You must not say anything other than the YouTube link(can Watch). Like: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            response = model.generate_content(f"이미지의 텍스트를 주면 이에 어울리는 분위기를 파악하고 노래를 추천해줘. 노래는 k-pop, j-pop, global-music 우선순위를 가져. 오래되지않은 노래면 좋겠어. 대답은 무조건 제목-가수이름 으로 알려줘. 예를들어 이렇게 대답해. 라일락-아이유. 다음은 이미지야. {image}")

            return response

        response = getResponseGemini()
        response = response.text
        print(response)

        return response


    def get_video_links(self, query):
        DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
          q=query,
          order="relevance",
          part="snippet",
          maxResults=10,
          type="video"  # 비디오만 검색 결과로 받기
        ).execute()

        video_links = []
        for search_result in search_response.get('items', []):
          if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append(video_link)

        return video_links[0]
# SongRecByAi("test2.jpeg")