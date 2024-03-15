from openai import OpenAI
import openai
import os
import numpy as np
import cv2
from . import ColorGen
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
    exV = [0.8,1.3]
    coV = [5,17]
    teV = [-20, 13]
    grV = [0.1,0.8]
    grcV = [0,0.1001]

    # base question
    # baseInfo = f"| 노출: 1이 원본이고, {exV[0]}~{exV[1]}의 값을 가지며, {exV[0]}에 가까울수록 검정이고 {exV[1]}에 가까울수록 흰색이고 소숫점으로 수치를 받아야됨. | 대비: 0이 원본이고, {coV[0]}~{coV[1]}의 값을 가지며, 값이 커질수록 어두운 부분의 차이가 커지는데, 수치를 낮추면 물빠진느낌을 주는 장점이있고, 수치를 높이면 뚜렷해지는 장점이있으며, 소숫점으로 수치를 받아야됨. | 색온도: 0이 원본이고, {teV[0]}~{teV[1]}의 값을 가지며, {teV[1]}에 가까울수록 주황색이 강조되고 {teV[0]}에 가까울수록 파랑색이 강조됨(너무 주황은 추천하지않음). | 그레인: {grV[0]}~{grV[1]} 의값을 가지며 {grV[1]}에 갈수록 노이즈가 많아지고 소숫점으로 받아야 됨. 보통수준의 그레인값이 들어왔으면 좋겠어.| 초록빛정도: {grcV[0]}~{grcV[1]} 의값을 가지며 {grcV[1]}에 갈수록 초록빛이 강하게 나타나"
    # answerform= f"주어지는 텍스트를 평균을 냈을때 다음 네가지의 값 <노출 대비 색온도 그레인 초록빛정도>을 변경하여 필름 카메라로 찍은 사진느낌으로 바꾸고자 한다. 지정할 값을 추천을 해줘라. 대답은 다음과 같이 말한다. '추천 : [노출,대비,색온도,그레인,초록빛정도]' 이외의 말은 하지않는다. 다음은 주어지는 텍스트다."
    # answerform2= f"<원본이미지>와 <너가 제안한 수정해야할 수치>를 통해 수정해본 <수치를 토대로 원본을 수정한 이미지> 텍스트를 보고 필름사진같은지 판단하고, 다시 지정할 값을 추천을 해줘라. 과감하게 값을 변경해도 좋아. 대답은 다음과 같이 말한다. '추천 : [노출,대비,색온도,그레인,초록빛정도]' 이외의 말은 하지않는다. 다음은 주어지는 텍스트다."
    baseInfo = f"| Exposure: 1 is the original,It has values of {exV[0]} to {exV[1]}, The closer it is to {exV[0]}, the black, and the closer it is to {exV[1]}, the whiter it is, and the value must be received as a decimal point.| Contrast: 0 is the original, and has values from {coV[0]} to {coV[1]}. As the value increases, the difference in dark areas increases. Lowering the value has the advantage of giving a washed-out feeling, and the value Increasing the value has the advantage of becoming more pronounced, and the value must be received as a decimal point.| Color temperature: 0 is the original, and has values from {teV[0]} to {teV[1]}. The closer it is to {teV[1]}, the more orange is emphasized, and the closer it is to {teV[0]}, the more blue it is. Emphasized (too orange is not recommended). | Grain: Has values from {grV[0]} to {grV[1]}. As {grV[1]} increases, noise increases and must be received as a decimal point. I hope the grain value comes in at a normal level.| Degree of greenness: Values range from {grcV[0]} to {grcV[1]}, with the green color appearing stronger as {grcV[1]} increases."
    answerform = f"When averaging the given text, we want to change the following four values <exposure contrast color temperature grain greenness> to make it look like a photo taken with a film camera. Please recommend a value to specify. The answer says: Do not say anything other than 'Recommendation: [Exposure, Contrast, Color Temperature, Grain, Greenness]'. The following is the given text."
    answerform2 = f"Look at the <original image> and the <image modified from the original based on the values> text that has been modified through <the values to be corrected as suggested by you>, determine whether it looks like a film photo, and recommend a value to re-specify. It’s okay to change the value boldly. The answer says: Do not say anything other than 'Recommendation: [Exposure, Contrast, Color Temperature, Grain, Greenness]'. The following is the given text."

    # 1차
    # img_path = "test1.jpeg"
    img_path = imgSrc
    c = ColorGen.ColorOp(img_path)
    img = c.getImg()

    def getResponseChatgpt(u_model):
        response = client.chat.completions.create(
            model=u_model,
            messages=[
                {"role": "assistant", "content": f"You are a famous film photographer. {baseInfo} {answerform2}"},
                {"role": "user", "content": f"{img}"},
            ]
        )
        return response

    def getResponseChatgpt2(u_model):
        response = client.chat.completions.create(
            model=u_model,
            messages=[
               {"role": "assistant",
                 "content": f"{baseInfo} By changing the following six values <Exposure, Contrast, Color Temperature, Grain, Greenness>, I want to change the look of a photo taken with a film camera. Previously you gave me the following recommendations:  {answerform2} "},
                {"role": "user",
                 "content": f"The values to be modified as suggested by you [exposure, contrast, color temperature, grain, greenness]: {answer1} | Original image: {img} | Image modified from the original based on the numbers = {fixed1}"},
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
                    print("openai error[2]!!!!!!")
                    return ""
        return response

    response = responseChatgpt()
    answer1 = response.choices[0].message.content
    answer1 = string_to_list(answer1)
    print(answer1)
    fixed1 = c.getFilmImg(float(answer1[0]),float(answer1[1]),int(answer1[2]),float(answer1[3]),float(answer1[4]))

    # #--------------------------------------
    # 2차

    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo-0125",
    #   messages=[
    #       # {"role": "assistant",
    #       #  "content": f"{baseInfo} 다음 다섯 가지의 값 <노출, 대비, 색온도, 그레인, 초록빛정도>을 변경하여 필름 카메라로 찍은 사진느낌으로 바꾸고자 한다. 이전에 너는 나에게 다음 추천값을 알려주엇다.  {answerform2} "},
    #       # {"role": "user",
    #       #  "content": f"| 너가 제안한 수정해야할 수치 [노출,대비,색온도,그레인,초록빛정도]:{answer1} | 원본이미지: {img}  | 수치를 토대로 원본을 수정한 이미지={fixed1}"},
    #
    #       {"role": "assistant",
    #        "content": f"{baseInfo} By changing the following six values <Exposure, Contrast, Color Temperature, Grain, Greenness>, I want to change the look of a photo taken with a film camera. Previously you gave me the following recommendations:  {answerform2} "},
    #       {"role": "user",
    #        "content": f"The values to be modified as suggested by you [exposure, contrast, color temperature, grain, greenness]: {answer1} | Original image: {img} | Image modified from the original based on the numbers = {fixed1}"},
    #
    #   ]
    # )
    response = responseChatgpt2()
    answer2 = response.choices[0].message.content
    answer2 = string_to_list(answer2)

    # 다시 c 1 원본 에 집어넣기
    print(answer2)
    fixed2 = c.getFilmImg(float(answer2[0]),float(answer2[1]),int(answer2[2]),float(answer2[3]),float(answer2[4]))

    # c.downSizeImg(fixed2, "test1_gen_size.jpeg")
    new_img_src = imgSrc+"gen_size.jpeg"
    # _________________________________________
    # # 3차
    #
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #       {"role": "assistant", "content": f"너는 디지털사진을 필름사진처럼 바꾸는 사진작가야. {baseInfo} {answerform}"},
    #
    #       {"role": "assistant",
    #        "content": f"{baseInfo} 다음 네가지의 값 <노출 대비 색온도 그레인>을 변경하여 필름 카메라로 찍은 사진느낌으로 바꾸고자 한다. 이전에 너는 나에게 다음 추천값을 알려주엇다.  {answerform2} "},
    #       {"role": "user", "content": f"| 너가 제안한 수정해야할 수치 [노출,대비,색온도,그레인]:{answer2} | 원본이미지: {img}  | 수치를 토대로 원본을 수정한 이미지={fixed2}"},
    #   ]
    # )
    # answer3 = response.choices[0].message.content
    # answer3 = string_to_list(answer3)
    #
    # # 다시 c 1 원본 에 집어넣기
    # print(answer3)
    # c.getFilmImg(float(answer3[0]),float(answer3[1]),int(answer3[2]),float(answer3[3]),float(answer3[4]))

