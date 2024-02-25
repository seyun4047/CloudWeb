import cv2
def resizeImg(imgSrc):
    inputImg = cv2.imread(imgSrc)
    oriH, oriW = inputImg.shape[:2]
    resizedImg = cv2.resize(inputImg, (int(oriW * 0.3), int(oriH * 0.3)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(imgSrc, resizedImg)
