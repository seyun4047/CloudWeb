import qrcode
import cv2
import numpy as np
class QRGen:
    def __init__(self, path, data):
        print("hi this")
        self.img_path = path
        self.data = data
        self.oriImg = cv2.imread(self.img_path)
        self.img = self.oriImg.copy()
        self.h, self.w = self.img.shape[:2]
        self.qrGen()

    def qrGen(self):
        self.qrImgGen()
        print("QR gened")
        self.putQRonImg()
        print("QR putQronImg")
        self.writeImg()
        print("writed", self.new_path)
        return cv2.imread(self.new_path)
    def writeImg(self):
        self.new_path=self.img_path.split(".")[0] + "_qr_gen." + self.img_path.split(".")[1]
        cv2.imwrite(self.new_path,self.img)
    def qrImgGen(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        self.qrImg = qr.make_image(fill_color="black", back_color="white")

        # Pillow 이미지로 변환
        self.qrImg = self.qrImg.convert("RGBA")

        mlen = (int(max(self.h, self.w) / 6))
        print(mlen)
        self.qrImg = self.qrImg.resize((mlen, mlen))
        # 투명 배경 생성
        datas = self.qrImg.getdata()
        new_data = []
        for item in datas:
            # 흰색 픽셀을 투명하게 처리
            if item[0]==0 and item[1]==0 and item[2]==0:
                new_data.append(item)
            else:
                new_data.append((255, 255, 255, 0))

        self.qrImg.putdata(new_data)

    def putQRonImg(self):
        self.qrImg = np.array(self.qrImg)
        # img = cv2.imread('test.jpeg')

        # h, w = self.img.shape[:2]
        # resizeSize = int(max(h, w) / 7)
        # self.qrImg = cv2.resize(self.qrImg, (resizeSize, resizeSize), interpolation=cv2.INTER_AREA)

        _, mask = cv2.threshold(self.qrImg[:, :, 3], 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        qrImg = cv2.cvtColor(self.qrImg, cv2.COLOR_BGRA2BGR)
        qrh, qrw = qrImg.shape[:2]
        # roi = img[10:10+qrh, 10:10+qrw]
        roi = self.img[self.h - qrh - 10:self.h - 10, self.w - qrw - 10:self.w - 10]

        masked_qrImg = cv2.bitwise_and(qrImg, qrImg, mask=mask)
        masked_img = cv2.bitwise_and(roi, roi, mask=mask_inv)

        added = masked_qrImg + masked_img
        self.img[self.h - qrh - 10:self.h - 10, self.w - qrw - 10:self.w - 10] = added

        # 합성된 이미지 저장
        # cv2.imwrite('img_gen.jpeg', self.img)

#
# a = QRGen("test.jpg","https://mutzin.site")