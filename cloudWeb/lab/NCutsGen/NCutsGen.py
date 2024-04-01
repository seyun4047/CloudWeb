import cv2
import numpy as np
import sys
sys.path.append("../")
from ..RecSongGen import SongRecByAi_gemini_spotify
sys.path.append("../")
from ..FilmGen import FilmGen3
class NCutsGen:
    def __init__(self,qrC,qrBg,i1,i2,i3,i4):
        print("this")
        self.imgGenPath = i1.split(".")[0] + "_gen." + i1.split(".")[1]
        #set paper
        # paper size 6:4
        self.bgH = 3000
        self.bgW = 2000
        # bg margin
        self.bgMarginTopH=200
        self.bgMarginW=130
        self.bgMarginBottomH=400
        # cross margin
        self.bonusMargin=150
        # 4cuts image 4:3
        self.fgH=1040
        self.fgW=780
        # create Background
        # self.createBg()
        self.bg=cv2.imread("static/lab/ncuts/bg2.jpg")

        while True:
            try:
                self.i1 = FilmGen3.gen(i1, 1, self.fgW, self.fgH)
                break
            except Exception as e:
                continue
        while True:
            try:
                self.i2 = FilmGen3.gen(i2, 1, self.fgW, self.fgH)
                break
            except Exception as e:
                continue
        while True:
            try:
                self.i3 = FilmGen3.gen(i3, 1, self.fgW, self.fgH)
                break
            except Exception as e:
                continue
        while True:
            try:
                self.i4 = FilmGen3.gen(i4, 1, self.fgW, self.fgH)
                break
            except Exception as e:
                continue
        self.genedImg = self.putImage()
        gen = SongRecByAi_gemini_spotify.SongRecByAi(self.imgGenPath,qrC,qrBg)
        self.songUrl = gen.songUrl
    # def getSongUrl(self):
    def createBg(self):
        self.bg = np.zeros((self.bgH, self.bgW, 3), dtype=np.int64)
        # 1행1열
        self.bg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = 255
        # 1행2열
        self.bg[self.bgMarginTopH + self.bonusMargin:self.bgMarginTopH + self.bonusMargin + self.fgH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = 255
        # 2행1열
        self.bg[self.bgH - self.bgMarginBottomH - self.bonusMargin - self.fgH: \
                self.bgH - self.bgMarginBottomH - self.bonusMargin, self.bgMarginW:self.bgMarginW + self.fgW] = 255
        # 2행2열
        self.bg[self.bgH - self.bgMarginBottomH - self.fgH:self.bgH - self.bgMarginBottomH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = 255
    def putImage(self): # get numpy array
        genedImg = self.bg.copy()
        # self.i1 = self.resizeImg(self.i1)
        # self.i2 = self.resizeImg(self.i2)
        # self.i3 = self.resizeImg(self.i3)
        # self.i4 = self.resizeImg(self.i4)
        # 1행1열
        genedImg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = self.i1
        # 1행2열
        genedImg[self.bgMarginTopH + self.bonusMargin:self.bgMarginTopH + self.bonusMargin + self.fgH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.i2
        # 2행1열
        genedImg[self.bgH - self.bgMarginBottomH - self.bonusMargin - self.fgH: \
                self.bgH - self.bgMarginBottomH - self.bonusMargin, self.bgMarginW:self.bgMarginW + self.fgW] = self.i3
        # 2행2열
        genedImg[self.bgH - self.bgMarginBottomH - self.fgH:self.bgH - self.bgMarginBottomH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.i4
        cv2.imwrite(self.imgGenPath, genedImg)
        # self.genedImg = genedImg
        return genedImg
    # FilmGen2.ColorGen2 에서 리사이즈 되게 설계됨
    # def resizeImg(self, img):
    #     img = cv2.resize(img, (self.fgW, self.fgH))
    #     return img

# test = NCutsGen(255,0,"i1.jpg", "i2.jpg", "i3.jpg", "i4.jpg")
# i1=cv2.imread("i1.jpg")
# i2=cv2.imread("i2.jpg")
# i3=cv2.imread("i3.jpg")
# i4=cv2.imread("i4.jpg")