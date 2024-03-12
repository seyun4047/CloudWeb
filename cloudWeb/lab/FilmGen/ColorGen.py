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

    def getFilmImg(self, e, c, t, g, gc):
        # print(self.oriImg)
        self.img = self.oriImg.copy()
        self.downSizeImg(self.img, self.img_path)
        # cv2.imwrite("isori.jpeg", self.img)
        self.setExposure(e)
        self.setContrast(c)
        self.setTemperature(t)
        self.setGrain(g)
        self.setGreen(gc)
        self.writeImg()
        return cv2.imread(self.new_path)


    def writeImg(self):
        # cv2.imwrite(self.img_path, self.img)
        self.new_path=self.img_path.split(".")[0] + "_gen." + self.img_path.split(".")[1]
        cv2.imwrite(self.new_path,self.img)

        # cv2.imwrite(self.img_path.split(".")[0] + "_gen" + self.img_path.split(".")[1], self.img)
    # 노출: 1이 원본이고, 0~5의 값을 가지며, 0에 가까울수록 검정이고 5에가까울수록 흰색이고 소숫점으로 수치를 받아야됨.
    def setExposure(self, value):
        self.img = cv2.convertScaleAbs(self.img, alpha=value, beta=0)

    # 대비: 0이 원본이고, -10~10의 값을 가지며, -10에 가까울소록 회색이고 뿌얘지고 +10에 가까울수록 대비가 강해지며, 소숫점으로 수치를 받아야됨.
    def setContrast(self, value):
        mean_intensity = np.mean(self.img)
        contrast_factor = (float(value)) / 10.0
        self.img = np.clip((self.img - mean_intensity) * contrast_factor + mean_intensity, 0, 255).astype(np.uint8)

    # 색온도: 0이 원본이고, -100~100의 값을 가지며, 100에 가까울수록 주황색이 강조되고 -100에 가까울수록 파랑색이 강조됨
    def setTemperature(self, value):
        blue = max(value, 0)
        red = max(-value, 0)

        # RGB 값을 조절하여 이미지의 색상 변환
        blue_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float32')
        red_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float32')

        # 노란 빛 조절
        red_matrix[0][0] = 1.0
        red_matrix[1][1] = 1.0 - (0.01 * red)
        red_matrix[2][2] = 1.0 - (0.01 * red)

        # 푸른 빛 조절
        blue_matrix[0][0] = 1.0 - (0.01 * blue)
        blue_matrix[1][1] = 1.0 + (0.005 * blue)
        blue_matrix[2][2] = 1.0 + (0.01 * blue)

        # 변환 행렬 적용
        blue_adjusted = cv2.transform(self.img, blue_matrix)
        self.img = cv2.transform(blue_adjusted, red_matrix)

    # 그레인: 0-255 의값을 가지며 10에 갈수록 노이즈가 많아짐.
    # def setGrain(self, value):
    #     # 이미지 크기 가져오기
    #     height, width, channels = self.img.shape
    #
    #     # 잡음 이미지 생성
    #     grain = np.random.randint(0, 1, (height, width, channels), dtype=np.uint8)
    #
    #     # 원본 이미지와 잡음을 더하기
    #     self.img = cv2.add(self.img, grain)

    # 그레인: 0-1
    def setGrain(self, intensity=0.1):
        # 이미지 크기를 가져옵니다.
        height, width, channels = self.img.shape

        # 가우시안 잡음을 생성합니다.
        mean = 0
        sigma = 25
        gauss = np.random.normal(mean, sigma, (height, width))

        # 입력 이미지와 가우시안 잡음을 조합하여 그레인을 생성합니다.
        noisy_image = self.img.copy()
        for c in range(channels):
            noisy_image[:, :, c] = np.clip(self.img[:, :, c] + gauss * intensity, 0, 255).astype(np.uint8)

        self.img = noisy_image.copy()
        # cv2.imshow('Noisy Image', noisy_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # 초록빛: 0-1
    def setGreen(self, intensity=0.1):
        # 초록빛을 추가할 비율을 계산합니다.
        green_ratio = 1.0 + intensity

        # 이미지의 초록 채널을 강조합니다.
        green_channel = self.img[:, :, 1]  # 초록 채널 선택
        green_channel = np.clip(green_channel * green_ratio, 0, 255).astype(np.uint8)  # 강조된 초록 채널

        # 변경된 초록 채널을 이미지에 적용합니다.
        output_image = self.img.copy()
        output_image[:, :, 1] = green_channel  # 변경된 초록 채널 적용
        self.img = output_image







