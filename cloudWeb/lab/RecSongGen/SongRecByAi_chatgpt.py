from openai import OpenAI
import openai
import os
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import requests
import sys
# sys.path.append("../")
from ..QRGen import QRGenerator

class SongRecByAi:
    def __init__(self, path, color):
        self.path = path
        self.color = color
        self.gen()
        # self.qrGen()
    def gen(self):
        songUrl = self.songGen()
        self.check_link_validity(songUrl)
        QRGenerator.QRGen(self.path, songUrl, self.color)

    def check_link_validity(self,url):
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

        openai.api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI()

        image = Image.open(self.path)
        info = image._getexif()
        # info = image.getexif()
        image.close()

        # print(info)
        taglabel = {}

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            taglabel[decoded] = value

        # print(taglabel)

        data = [taglabel['Make'], taglabel['Model'], taglabel['DateTime'], taglabel['ShutterSpeedValue'],
                taglabel['ExposureTime'], taglabel['ISOSpeedRatings'], taglabel['FNumber'], taglabel['LensModel']]


        def getResponseChatgpt(u_model):
            response = client.chat.completions.create(
                model=u_model,
                messages=[
                    {"role": "assistant", "content": "This is the settings taken from a certain photo. Look at this and recommend a song in your own way. You must not say anything other than the YouTube link. Like: https://www.youtube.com/watch?v=VdQY7BusJNU"},
                    {"role": "user", "content": f"camera brand:{data[0]},camera model:{data[1]},The time taken:{data[2]},Shutter Speed:{data[3]},ExposureTime:{data[4]},ISO:{data[5]},Fnumber:{data[6]}Lens:{data[7]}"},
                ]
            )
            return response

        def responseChatgpt():
            try:
                response = getResponseChatgpt("gpt-3.5-turbo")
            except Exception as e:
                try:
                    response = getResponseChatgpt("gpt-3.5-turbo-0125")
                except Exception as e2:
                    try:
                        response = getResponseChatgpt("gpt-3.5-turbo-0301")
                    except Exception as e3:
                        print("openai error[1]!!!!!!")
                        return ""
            return response


        response = responseChatgpt()
        answer1 = response.choices[0].message.content
        print(answer1)

        return answer1

# songUrl = gen()
# check_link_validity(songUrl)
# QRGenerator.QRGen("test.jpg",songUrl)

# print(sys.path)