import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import tensorflow as tf

class prj03(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UIClear()

    def UIClear(self):
        self.info_list = {
            0 : ['티셔츠', 5000],
            1 : ['트라우저 진', 30000],
            2 : ['스웨터', 15000],
            3 : ['드레스', 50000],
            4 : ['코트', 50000],
            5 : ['샌들', 10000],
            6 : ['셔츠', 15000],
            7 : ['스니커즈', 30000],
            8 : ['가방', 5000],
            9 : ['부츠', 40000]
        }

        self.storename = QLabel('무인가게', self)
        self.storename.setFont(QFont('Decorative', 20))
        self.storename.adjustSize()
        self.storename.move(180, 30)

        self.img = QLabel(self)
        self.img.move(170, 100)

        self.guide = QLabel('File을 눌러 모델 추가 후 이미지를 업로드 하세요', self)
        self.guide.move(150, 500)
        self.guide.adjustSize()

        self.account_number = QLabel('은행 999-999999-9999', self)
        self.account_number.move(200, 550)
        self.account_number.adjustSize()
        self.account_number.setHidden(True)

        self.img_upload = QPushButton('이미지 업로드', self)
        self.img_upload.move(170, 430)
        self.img_upload.setEnabled(False)
        self.img_upload.clicked.connect(self.loadImage)

        self.payment_btn = QPushButton('결제하기', self)
        self.payment_btn.move(370, 430)
        self.payment_btn.setEnabled(False)

        self.modelh5 = None

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        file_menu = menu.addMenu('File')

        menu_bar = QAction('모델 불러오기', self)
        menu_bar.setShortcut('Ctrl+L')
        menu_bar.triggered.connect(self.loadModel)
        file_menu.addAction(menu_bar)

        self.setWindowTitle('무인 상점 만들기')
        self.setGeometry(300, 300, 600, 600)
        self.show()

    def loadModel(self):
        try:
            model_file, _ = QFileDialog.getOpenFileName(self, '모델 추가', '')
            if model_file:
                self.modelh5 = tf.keras.models.load_model(model_file)
                self.guide.setText('모델 추가 완료')
        except:
            pass

    def loadImage(self):
        pass

prj_repeat = QApplication(sys.argv)  # 프로그램 무한반복
ins = prj03()  # 실행인스턴스
prj_repeat.exec_()  # 프로그램무한반복 코드를 무한 반복 //이벤트확인
