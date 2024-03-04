import cv2
def resizeImg(imgSrc):
    inputImg = cv2.imread(imgSrc)
    oriH, oriW = inputImg.shape[:2]
    resizedImg = cv2.resize(inputImg, (int(oriW * 0.2), int(oriH * 0.2)), interpolation=cv2.INTER_AREA)
    new_path = imgSrc.split('.')[0]+"_t."+imgSrc.split('.')[1]
    # print("this new_path:",new_path)
    cv2.imwrite(new_path, resizedImg)

def resizeOURImg(imgSrc):
    inputImg = cv2.imread(imgSrc)
    oriH, oriW = inputImg.shape[:2]
    resizedImg = cv2.resize(inputImg, (int(oriW * 0.8), int(oriH * 0.8)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(imgSrc, resizedImg)