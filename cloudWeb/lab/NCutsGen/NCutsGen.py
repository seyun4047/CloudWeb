import cv2
import numpy as np
import sys
sys.path.append("../")
from ..RecSongGen import SongRecByAi_gemini_spotify
sys.path.append("../")
from ..FilmGen import FilmGen3
class NCutsGen:
    def __init__(self,qrC,qrBg,pLst):
        print("this")
        # for img in
        # postedImgLst[0].image.path
        self.imgGenPath = pLst[0].image.path
        self.pLstLen = len(pLst)
        self.imgs = ["" for _ in range(4)]
        # self.imgGenPath = i1.split(".")[0] + "_gen." + i1.split(".")[1]
        #set paper
        # paper size 6:4
        self.bgH = 3000
        self.bgW = 2000
        # # bg margin
        # self.bgMarginTopH=200
        # self.bgMarginW=130
        # self.bgMarginBottomH=400
        # # cross margin
        # self.bonusMargin=150
        # 4cuts image 4:3
        if self.pLstLen==1:
            self.fgH=2080
            self.fgW=1560
            # bg margin
            self.bgMarginTopH = 290
            self.bgMarginW = 220
            self.bgMarginBottomH = 400
            # cross margin
            # self.bonusMargin = 150
        if self.pLstLen==2:
            self.fgH=1180
            self.fgW=1574
            # bg margin
            self.bgMarginTopH = 150
            self.bgMarginW = 213
            self.bgMarginBottomH = 400
            # cross margin
            self.bonusMargin = 150
        if self.pLstLen==3:
            self.fgH=1040
            self.fgW=780
            # bg margin
            self.bgMarginTopH = 200
            self.bgMarginW = 130
            self.bgMarginBottomH = 400
            # cross margin
            self.bonusMargin = 150
        if self.pLstLen==4:
            self.fgH=1040
            self.fgW=780
            # bg margin
            self.bgMarginTopH = 200
            self.bgMarginW = 130
            self.bgMarginBottomH = 400
            # cross margin
            self.bonusMargin = 150
        # create Background
        # self.createBg()

        # while True:
        for i in range(self.pLstLen):
            while True:
                try:
                    self.imgs[i] = FilmGen3.gen(pLst[i].image.path, 1, self.fgW, self.fgH)
                    break
                except Exception as e:
                    print(e)
                    continue

        if self.pLstLen==1:
            self.bg=cv2.imread("static/lab/ncuts/bg1.jpg")
            self.genedImg = self.putImage1()
        elif self.pLstLen == 2:
            self.bg=cv2.imread("static/lab/ncuts/bg2.jpg")
            self.genedImg = self.putImage2()
        elif self.pLstLen == 3:
            self.bg=cv2.imread("static/lab/ncuts/bg3.jpg")
            self.genedImg = self.putImage3()
        elif self.pLstLen == 4:
            self.bg=cv2.imread("static/lab/ncuts/bg4.jpg")
            self.genedImg = self.putImage4()

        gen = SongRecByAi_gemini_spotify.SongRecByAi(self.imgGenPath,qrC,qrBg)
        self.songUrl = gen.songUrl
    # ---------------------------
    # Create BG module
    # def createBg4(self):
    #     self.bg = np.zeros((self.bgH, self.bgW, 3), dtype=np.int64)
    #     # 1행1열
    #     self.bg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
    #     self.bgMarginW:self.bgMarginW + self.fgW] = 255
    #     # 1행2열
    #     self.bg[self.bgMarginTopH + self.bonusMargin:self.bgMarginTopH + self.bonusMargin + self.fgH, \
    #     self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = 255
    #     # 2행1열
    #     self.bg[self.bgH - self.bgMarginBottomH - self.bonusMargin - self.fgH: \
    #             self.bgH - self.bgMarginBottomH - self.bonusMargin, self.bgMarginW:self.bgMarginW + self.fgW] = 255
    #     # 2행2열
    #     self.bg[self.bgH - self.bgMarginBottomH - self.fgH:self.bgH - self.bgMarginBottomH, \
    #     self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = 255
    #
    # ---------------------------
    def putImage1(self): # get numpy array
        genedImg = self.bg.copy()
        genedImg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[0]
        cv2.imwrite(self.imgGenPath, genedImg)
        return genedImg

    def putImage2(self): # get numpy array
        genedImg = self.bg.copy()
        # 1행1열
        genedImg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[0]
        # 1행2열
        genedImg[self.bgH - self.bgMarginBottomH - self.fgH:self.bgH - self.bgMarginBottomH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.imgs[1]
        cv2.imwrite(self.imgGenPath, genedImg)
        return genedImg

    def putImage3(self): # get numpy array
        genedImg = self.bg.copy()
        # 1행1열
        genedImg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[0]
        # 1행2열
        genedImg[self.bgMarginTopH + self.bonusMargin:self.bgMarginTopH + self.bonusMargin + self.fgH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.imgs[1]
        # 2행1열
        genedImg[self.bgH - self.bgMarginBottomH - self.bonusMargin - self.fgH: \
                self.bgH - self.bgMarginBottomH - self.bonusMargin, self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[2]
        cv2.imwrite(self.imgGenPath, genedImg)
        # self.genedImg = genedImg
        return genedImg

    def putImage4(self): # get numpy array
        genedImg = self.bg.copy()
        # 1행1열
        genedImg[self.bgMarginTopH:self.bgMarginTopH + self.fgH, \
        self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[0]
        # 1행2열
        genedImg[self.bgMarginTopH + self.bonusMargin:self.bgMarginTopH + self.bonusMargin + self.fgH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.imgs[1]
        # 2행1열
        genedImg[self.bgH - self.bgMarginBottomH - self.bonusMargin - self.fgH: \
                self.bgH - self.bgMarginBottomH - self.bonusMargin, self.bgMarginW:self.bgMarginW + self.fgW] = self.imgs[2]
        # 2행2열
        genedImg[self.bgH - self.bgMarginBottomH - self.fgH:self.bgH - self.bgMarginBottomH, \
        self.bgW - self.bgMarginW - self.fgW:self.bgW - self.bgMarginW] = self.imgs[3]
        cv2.imwrite(self.imgGenPath, genedImg)
        # self.genedImg = genedImg
        return genedImg

# test = NCutsGen(255,0,"i1.jpg", "i2.jpg", "i3.jpg", "i4.jpg")
# i1=cv2.imread("i1.jpg")
# i2=cv2.imread("i2.jpg")
# i3=cv2.imread("i3.jpg")
# i4=cv2.imread("i4.jpg")