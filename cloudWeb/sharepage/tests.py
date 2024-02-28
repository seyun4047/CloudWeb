from django.test import TestCase

# Create your tests here.
import pymysql

# def insert_into_db(data):
#     # MySQL 데이터베이스 연결 설정
#     conn = pymysql.connect(
#         host="localhost",
#         user="root",
#         password="ksyun1004",
#         database="uploadPrac"
#     )
#     cursor = conn.cursor()
#
#     # 쿼리 실행
#     cursor.execute(f"INSERT INTO sharepage_post VALUES ({data})")
#
#     # 변경사항 저장
#     conn.commit()
#
#     # 연결 닫기
#     conn.close()
#
#
# # 예시 데이터
# idx = 163
# # 데이터베이스에 값 추가
# for i in range(4440, 5295, 1):
#     datains = f"{idx}, 'sharepage/images/IMG_{i}.JPG', '2024-02-28 18:17:30.511598'"
#     idx+=1
#     insert_into_db(datains)
# # INSERT INTO sharepage_post VALUES (162, sharepage/images/IMG_1.JPG, "2024-02-28 18:17:30")
#
import cv2
def resizeImg(imgSrc):
    inputImg = cv2.imread(imgSrc)
    oriH, oriW = inputImg.shape[:2]
    resizedImg = cv2.resize(inputImg, (int(oriW * 0.2), int(oriH * 0.2)), interpolation=cv2.INTER_AREA)
    new_path = imgSrc.split('.')[0]+"_t."+imgSrc.split('.')[1]
    # print("this new_path:",new_path)
    cv2.imwrite(new_path, resizedImg)

for i in range(4440, 5295, 1):
    try:
        resizeImg(f"media/sharepage/images/IMG_{i}.JPG")
    except Exception as e:
        continue