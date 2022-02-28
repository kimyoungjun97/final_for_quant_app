import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

class prj01(QWidget):
    def __init__(self):
        super().__init__()
        self.UIClear()

    def UIClear(self):
        self.img()
        self.btn()
        self.tt()
        self.number()

        self.setWindowTitle('대표 선출')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))
        self.setGeometry(500, 500, 400, 400) #좌측상단 기준 x축으로500, y축으로 500떨어지고 창크기가 x, y축 400 400
        self.show()

    def img(self): #이미지
        self.mainimg = QLabel(self) #label은 글자, 이미지, 영상 모두가능
        self.mainimg.setPixmap(QPixmap('img/icons8-stock-64.png').scaled(35, 44))
        self.mainimg.move(100, 10) #가로 세로 배치 이동

    def btn(self): #버튼
        self.btn_01 = QPushButton('대표 선출', self)
        self.btn_01.setFixedSize(340, 40) #버튼의 가로세로 크기
        self.btn_01.move(30, 290) #가로 세로 배치 이동
        self.btn_01.clicked.connect(self.choice)

        self.btn_02 = QPushButton('종료 버튼', self)
        self.btn_02.setFixedSize(340, 40) #버튼의 가로세로 크기
        self.btn_02.move(30, 340) #가로 세로 배치 이동
        self.btn_02.clicked.connect(self.btn_close)

    def tt(self): #툴팁
        self.btn_01.setToolTip('이 버튼을 누르면 대표를 선출합니다.')
        self.btn_02.setToolTip('이 버튼을 누르면 종료합니다.')
        self.mainimg.setToolTip('Main Image')
        self.setToolTip('이곳은 Qwidgets')


    def number(self): #대리인번호
        self.num_label = QLabel('000', self)
        self.num_label.setFont(QFont('Helvetica', pointSize=75, weight=2))
        self.num_label.move(100, 100)

    def choice(self):
        s = str(random.randint(1, 1000))
        print(s)
        self.num_label.setText(s)

    def btn_close(self):
        return QCoreApplication.instance().quit()



prj_repeat = QApplication(sys.argv) #프로그램 무한반복
ins = prj01() #실행인스턴스
prj_repeat.exec_() #프로그램무한반복 코드를 무한 반복 //이벤트확인
