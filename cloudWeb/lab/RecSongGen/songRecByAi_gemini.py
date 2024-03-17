from openai import OpenAI
import openai
import os
from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import requests
import sys
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

sys.path.append("../")
from QRGen import QRGenerator


class SongRecByAi:
    def __init__(self, path):
        self.path = path
        self.gen()
        # self.qrGen()

    def gen(self):
        songUrl = self.songGen()
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

        def getResponseGemini():
            model = genai.GenerativeModel('gemini-pro')
            # response = model.generate_content(f"This is the settings taken from a certain photo. Look at this and recommend a song in your own way. This is the Text: camera brand:{data[0]},camera model:{data[1]},The time taken:{data[2]},Shutter Speed:{data[3]},ExposureTime:{data[4]},ISO:{data[5]},Fnumber:{data[6]}Lens:{data[7]}. You must not say anything other than the YouTube link(can Watch). Like: https://www.youtube.com/watch?v=VdQY7BusJNU ")
            response = model.generate_content(f"This is the settings taken from a certain photo. Look at this and recommend a song in your own way. This is the Text: {image}. You must not say anything other than the YouTube link(can Watch). Like: https://www.youtube.com/watch?v=VdQY7BusJNU ")

            return response

        response = getResponseGemini()
        response = response.text
        print(response)

        return response

SongRecByAi("test.jpg")
# songUrl = gen()
# check_link_validity(songUrl)
# QRGenerator.QRGen("test.jpg",songUrl)

# print(sys.path)