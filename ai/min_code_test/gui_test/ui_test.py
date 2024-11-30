from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5 import QtGui
from ui_check_img import Ui_Form
import sys
import threading
import cv2

class UI_image_test(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)

    def img_show(self):
        self.cam = cv2.VideoCapture(0)

        width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)

        height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.ui.label_img_show.resize(int(width),int(height))

        while self.cam.isOpened():
            ret,img=self.cam.read()
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            h,w,c = img.shape
            qImg = QtGui.QImage(img, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            self.ui.label_img_show.setPixmap(pixmap)
        self.cam.release()

    def exit(self):
        self.cam.release()
        self.close()

    def next(self):
        self.thread1 =threading.Thread(target=self.img_show())
        self.thread1.start()

def main():
    app=QApplication([])
    window=UI_image_test()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()