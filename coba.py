from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog
import sys
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Input Gambar')
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel(self)
        self.label.setText('Belum ada gambar yang dipilih')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.button = QPushButton('Pilih Gambar', self)
        self.button.clicked.connect(self.selectImage)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def selectImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "",
                                                  "Images (*.png *.xpm *.jpg *.bmp *.jpeg);;All Files (*)", options=options)
        if fileName:
            self.displayImage(fileName)

    def displayImage(self, fileName):
        self.label.setText('Gambar dipilih: ' + fileName)
        img = cv2.imread(fileName)
        # Lakukan proses gambar sesuai kebutuhan
        # ...


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
