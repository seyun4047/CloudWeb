import cv2
import numpy as np

class ColorOp:
    def __init__(self, path):
        print("this way:" + path)
        self.img_path = path
        self.oriImg = cv2.imread(self.img_path)
        self.img = self.oriImg.copy()
        # self.resizeImg()

    def resizeImg(self, image, path):
        oriH, oriW = image.shape[:2]
        image = cv2.resize(image, (int(oriW * 0.5), int(oriH * 0.5)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, image)

    def downSizeImg(self, image, path):
        oriH, oriW = image.shape[:2]
        image = cv2.resize(image, (int(oriW * 0.5), int(oriH * 0.5)), interpolation=cv2.INTER_AREA)
        image = cv2.resize(image, (int(oriW * 2), int(oriH * 2)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, image)

    def getImg(self):
        return self.img

    def getFilmImg(self, b, cr, cb, c, g):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCrCb)
        print("converted! BGR2YCrCb")
        self.setBrightness(b)
        print("set Brightness!")
        self.setTemperature(cr, cb)
        print("set Cr Cb!")
        # YCrCb2BGR
        self.img = cv2.cvtColor(self.img, cv2.COLOR_YCrCb2BGR)
        print("converted! YCrCb2BGR")
        self.setContrast(c)
        # print("set Contrast!")
        self.setGrain(g)
        print("set Grain!")
        # save & return
        self.writeImg()
        print("Saved!" + self.new_path)
        return cv2.imread(self.new_path)

    # write
    def writeImg(self):
        # cv2.imwrite(self.img_path, self.img)
        self.new_path=self.img_path.split(".")[0] + "_gen." + self.img_path.split(".")[1]
        cv2.imwrite(self.new_path,self.img)

    # 노출값 0~255 (가감 필요)
    def setBrightness(self, b):
        self.img[:, :, 0] = cv2.add(self.img[:, :, 0], b)
        # c3 = cv2.cvtColor(c2, cv2.COLOR_YCrCb2BGR)

    # -127~128의 범위를 가짐
    # Yellowish:Decrease Cb, Increase Cr.
    # Orange:Decrease Cb, Increase Cr significantly.
    # Greenish:Increase Cb, Decrease Cr.
    # Bluish: Decrease Cb significantly, Decrease Cr.
    def setTemperature(self, addcr, addcb):
        self.img[:, :, 1] = cv2.add(self.img[:, :, 1], addcr)  # cr
        self.img[:, :, 2] = cv2.add(self.img[:, :, 2], addcb)  # cb

    # 대비: 0이 원본이고, -10~10의 값을 가지며, -10에 가까울소록 회색이고 뿌얘지고 +10에 가까울수록 대비가 강해지며, 소숫점으로 수치를 받아야됨.
    def setContrast(self, value):
        mean_intensity = np.mean(self.img)
        contrast_factor = (value) / 10.0
        self.img = np.clip((self.img - mean_intensity) * contrast_factor + mean_intensity, 0, 255).astype(np.uint8)

    def setGrain(self, intensity=0.1):
        height, width, channels = self.img.shape
        mean = 0
        sigma = 25
        gauss = np.random.normal(mean, sigma, (height, width))
        noisy_image = self.img.copy()
        for c in range(channels):
            noisy_image[:, :, c] = np.clip(self.img[:, :, c] + gauss * intensity, 0, 255).astype(np.uint8)
        self.img = noisy_image.copy()

