import cv2
import numpy as np
from . import imgResizing
from django.shortcuts import render, redirect, get_object_or_404

def imgStack(files):
    try:
        img_len = len(files)
        # Get the url of three photos taken in the same place
        img_path = [files[i].image.path for i in range(img_len)]
        print("this imgstacker img_path",img_path)

    # img_path = [f"svg/img2/img{i}.JPG" for i in range(1,6,1)]

    # just resize Image
    # for i in range(5):
    #     imgResizing.resizeImg(img_path[i])

    # load the test img
        img = [0] * img_len
        for i in range(img_len):
            img[i] = cv2.imread(img_path[i])

        # cal width, height
        imgH, imgW = img[0].shape[:2]

        # set space uint16(최대 255*n의 값 수용가능한 uint16 2^16)
        reImg = np.zeros((imgH, imgW, 3), dtype=np.uint16)

        # cal each pix's avg
        for i in range(img_len):
            reImg += img[i]
        reImg = np.array(reImg/img_len).astype(np.uint8)

        # write overwrite first image and show this one.
        # cv2.imwrite(img_path[0], reImg)

        new_path = img_path[0].split('.')[0]+'_gen.'+img_path[0].split('.')[1]
        cv2.imwrite(new_path, reImg)

        return True
    except Exception as e:
        print("stacked error!!!!!")
        return False