from openai import OpenAI
import openai
import os
import numpy as np
import cv2
from . import ColorGen2
import re
import json
import sys
def string_to_list(input_string):
    s = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', input_string)
    return [float(num) for num in s]

def gen(imgSrc):

    openai.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()

    # value 범위 설정
    exV = [-20,20] # can -255-255
    crV = [-5,5]
    cbV = [-5,5]
    coV = [7,10]
    grV = [0.1,0.8]
    ranges = f"Brightness: {exV[0]} to {exV[1]}, Cr: {crV[0]} to {crV[1]}, Cb: {cbV[0]} to {cbV[1]}, Contrast: {coV[0]} to {coV[1]}, Grain: {grV[0]} to {grV[1]}"
    cbcrbaseInfo = "Yellowish:add Cr subtract Cb. Orange:add Cr significantly, subtract Cb. Greenish:subtract Cr, add Cb. Bluish: Decrease Cr, subtract Cb significantly. do not make it Redish. Make it yellow, orange, blue, or green."
    baseInfo = f"set Brightness, Cr, Cb based on {cbcrbaseInfo}, contrast, grain. Do not exceed the specified number range."
    answerform = f"To make it look like a photo taken with a film camera. The answer says: Do not say anything other than 'Recommendation: [Exposure, Cr, Cb, Contrast, Grain]'. The following is the given text. Do not exceed the specified number range."
    answerform2 = f"Look at the <original image> and the <image modified from the original based on the values> text that has been modified through <the values to be corrected as suggested by you>, determine whether it looks like a film photo, and recommend a value to re-specify. It’s okay to change the value boldly. The answer says: Do not say anything other than 'Recommendation: [Brightness, Cr, Cb, Contrast, Grain]'. The following is the given text.  Do not exceed the specified number range."

    # 1차
    # img_path = "test1.jpeg"
    img_path = imgSrc
    c = ColorGen2.ColorOp(img_path)
    img = c.getImg()

    # [Exposure, Cr, Cb, Contrast, Grain]
    def getResponseChatgpt(u_model):
        response = client.chat.completions.create(
            model=u_model,
            messages=[
                {"role": "assistant", "content": f"You are a famous film photographer. {ranges}{baseInfo}{answerform}"},
                {"role": "user", "content": f" Do not exceed the specified number range. especially Brightness. {img}"},
            ]
        )
        return response

    def getResponseChatgpt2(u_model):
        response = client.chat.completions.create(
            model=u_model,
            messages=[
               {"role": "assistant",
                 "content": f"{ranges}{baseInfo} By changing the following five values [Exposure, Cr, Cb, Contrast, Grain], I want to change the look of a photo taken with a film camera. Previously you gave me the following recommendations:  {answerform2} "},
                {"role": "user",
                 "content": f"The values to be modified as suggested by you [Exposure, Cr, Cb, Contrast, Grain]: {answer1} | Original image: {img} | Image modified from the original based on the numbers and  Do not exceed the specified number range. especially Brightness.= {fixed1}"},
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
                    # print("openai error[1]!!!!!!")
                    return ""
        return response

    def responseChatgpt2():
        try:
            response = getResponseChatgpt2("gpt-3.5-turbo")
        except Exception as e:
            try:
                response = getResponseChatgpt2("gpt-3.5-turbo-0125")
            except Exception as e2:
                try:
                    response = getResponseChatgpt2("gpt-3.5-turbo-0301")
                except Exception as e3:
                    # print("openai error[2]!!!!!!")
                    return ""
        return response

    response = responseChatgpt()
    answer1 = response.choices[0].message.content
    # print(answer1)
    answer1 = string_to_list(answer1)
    # print(answer1)
    fixed1 = c.getFilmImg(int(answer1[0]),int(answer1[1]),int(answer1[2]),float(answer1[3]),float(answer1[4]))

    response = responseChatgpt2()
    answer2 = response.choices[0].message.content
    answer2 = string_to_list(answer2)

    # 다시 c 1 원본 에 집어넣기
    # print(answer2)
    fixed2 = c.getFilmImg(int(answer2[0]),int(answer2[1]),int(answer2[2]),float(answer2[3]),float(answer2[4]))

    new_img_src = imgSrc+"gen_size.jpeg"

