import sys
import pyautogui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

class prj02(QWidget):
    def __init__(self):
        super().__init__()
        self.UIClear()

    def UIClear(self):

        self.packingcount = 0
        self.clickcount = 0

        self.packing()
        self.mainimg()
        self.packingbtn()

        self.setWindowTitle('자동 포장 프로그램')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))
        self.setGeometry(800, 300, 1000, 540) #좌측상단 기준 x축으로500, y축으로 500떨어지고 창크기가 x, y축 400 400
        self.show()


    def packing(self):
        self.packinglabel = QLabel('00 마리가 포장되었습니다.', self)
        self.packinglabel.setFont(QFont('Helvetica', pointSize=15, weight=2))
        self.packinglabel.move(30, 70)

    def mainimg(self):
        self.mainimglabel = QLabel(self)
        self.mainimglabel.setPixmap(QPixmap('img/icons8-stock-64.png').scaled(35, 44))
        self.mainimglabel.move(10, 10)


    def packingbtn(self):
        self.btn_01 = QPushButton('생선준비', self)
        self.btn_01.move(30, 150)
        self.btn_01.setFixedSize(250, 40)

        self.btn_02 = QPushButton('생선 다듬기', self)
        self.btn_02.move(300, 150)
        self.btn_02.setFixedSize(250, 40)

        self.btn_03 = QPushButton('생선 포장', self)
        self.btn_03.move(30, 200)
        self.btn_03.setFixedSize(520, 40)
        self.btn_03.clicked.connect(self.countClick)

        self.btn_04 = QPushButton('포장 시작', self)
        self.btn_04.move(300, 300)
        self.btn_04.setFixedSize(250, 40)
        self.btn_04.clicked.connect(self.startClick)

        self.btn_05 = QLineEdit(self)
        self.btn_05.setPlaceholderText('클릭 간격(번)')
        self.btn_05.move(30, 300)

        self.btn_05label = QLabel('몇초 간격으로 포장할지 입력하세요', self)
        self.packinglabel.setFont(QFont('Helvetica', pointSize=7))
        self.btn_05label.move(30, 440)

        self.btn_06 = QLineEdit(self)
        self.btn_06.setPlaceholderText('클릭 횟수(번)')
        self.btn_06.move(30, 400)

        self.btn_06label = QLabel('몇초 간격으로 포장할지 입력하세요', self)
        self.packinglabel.setFont(QFont('Helvetica', pointSize=7))
        self.btn_06label.move(30, 340)



    def countClick(self):
        self.packingcount += 1
        self.packinglabel.setText(f'{str(self.packingcount)} 마리가 포장되었습니다.')

    def startClick(self):
        self.timer = QTimer()
        self.x = 550
        self.y = 510
        self.delay = int(self.간격입력창)



prj_repeat = QApplication(sys.argv) #프로그램 무한반복
ins = prj02() #실행인스턴스
prj_repeat.exec_() #프로그램무한반복 코드를 무한 반복 //이벤트확인
