import sys
import cv2
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui', self)
        self.img = None

        self.loadImageButton.clicked.connect(self.loadImage)
        self.takeImageButton.clicked.connect(self.takeImage)
        self.open = False

    def openCamera(self):
        self.cap = cv2.VideoCapture(1)
        while self.open:
            ret, frame = self.cap.read()
            self.img = frame
            self.displayImage(5, frame)
            keluar = cv2.waitKey(1)
            if keluar == 27:
                break
        self.cap.release()
        cv2.destroyAllWindows()
        self.displayImage(1, self.img)
        self.grayScale()
        self.sharpenImage()
        self.threshold()
        self.findContuor()

    def takeImage(self):
        self.open = not self.open
        if self.open:
            self.openCamera()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.img = cv2.imread(file_path)
            self.img = cv2.resize(self.img, (600, 600))
            self.displayImage(1, self.img)
            self.grayScale()
            self.sharpenImage()
            self.threshold()
            self.findContuor()

    def sharpenImage(self):
        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ])

        img_height = self.gray.shape[0]
        img_width = self.gray.shape[1]

        kernel_height = kernel.shape[0]
        kernel_width = kernel.shape[1]

        H = (kernel_height) // 2
        W = (kernel_width) // 2

        out = np.zeros((img_height, img_width))

        for i in np.arange(H + 1, img_height - H):
            for j in np.arange(W + 1, img_width - W):
                sum = 0
                for k in np.arange(-H, H + 1):
                    for l in np.arange(-W, W + 1):
                        a = self.gray[i + k, j + l]
                        w = kernel[H + k, W + l]
                        sum += (w * a)
                out[i, j] = sum

        sharpened_img = np.clip(out, 0, 255).astype(np.uint8)
        self.sharpenImage = sharpened_img
        self.displayImage(2, sharpened_img)


    def grayScale(self):
        H, W = self.img.shape[:2]
        gray = np.zeros((H, W), np.uint8)
        for i in range(H):
            for j in range(W):
                gray[i, j] = np.clip(0.299 * self.img[i, j, 0] +
                                    0.587 * self.img[i, j, 1] +
                                     0.114 * self.img[i, j, 2], 0, 255)
        self.gray = gray

    def threshold(self):
        threshold = 50
        H, W = self.gray.shape[:2]
        thresh = np.zeros((H, W), np.uint8)
        for i in range(H):
            for j in range(W):
                a = self.gray.item(i, j)
                if a < threshold:
                    b = 0
                else:
                    b = 255
                thresh.itemset((i, j), b)
        self.thresh = thresh
        self.displayImage(3, thresh)

    def findContuor(self):
        contours, _ = cv2.findContours(
            self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = np.zeros(self.img.shape, dtype=np.uint8)
        decoded_texts = set()

        for contour in contours:
            for i in range(len(contour)):
                current_point = contour[i][0]
                next_point = contour[(i + 1) % len(contour)][0]
                cv2.line(contour_img, tuple(current_point),
                         tuple(next_point), (0, 255, 0))

            rect = cv2.minAreaRect(contour)
            if rect[1][0] > 50 and rect[1][1] > 50:
                box = cv2.boxPoints(rect)
                box = box.astype(int)
                cv2.drawContours(contour_img, [box], 0, (0, 0, 255), 2)
                x, y, w, h = cv2.boundingRect(contour)
                roi = self.thresh[y:y+h, x:x+w]
                qrCodeDetector = cv2.QRCodeDetector()
                decodedText, points, _ = qrCodeDetector.detectAndDecode(roi)
                if points is not None and decodedText not in decoded_texts:
                    decoded_texts.add(decodedText)
                    self.lineEdit.setText(decodedText)

        self.displayImage(4, contour_img)

    def displayImage(self, window, img):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(
            img, img.shape[1], img.shape[0], img.strides[0], qformat)

        img = img.rgbSwapped()

        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label.setScaledContents(True)
        if window == 2:
            self.label_2.setPixmap(QPixmap.fromImage(img))
            self.label_2.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_2.setScaledContents(True)
        if window == 3:
            self.label_3.setPixmap(QPixmap.fromImage(img))
            self.label_3.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_3.setScaledContents(True)
        if window == 4:
            self.label_4.setPixmap(QPixmap.fromImage(img))
            self.label_4.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_4.setScaledContents(True)
        if window == 5:
            self.label_9.setPixmap(QPixmap.fromImage(img))
            self.label_9.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_9.setScaledContents(True)


app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Pertemuan 8')
window.show()
sys.exit(app.exec_())