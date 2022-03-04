import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# df = pd.read_csv('./datasets/futures_GOLD.csv')
# print(df)
# plt.plot(df['Date'][-30:], df['Adj_Close'][-30:], label='Close')
# plt.plot(df['Date'][-30:], df['High'][-30:], label='High')
# plt.plot(df['Date'][-30:], df['Low'][-30:], label='Low')
# plt.legend()
# plt.show()

# http://www.gisdeveloper.co.kr/?p=8343 pyqt 위젯 안에 그래프 그리기 참조

form_class = uic.loadUiType("pair_trading.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.UIClear()

    def UIClear(self):
        self.setupUi(self)
        self.setWindowTitle('Final for quant(Pair_Trading)')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.leftlayout.addWidget(self.canvas)

        data = pd.read_csv('./datasets/futures_GOLD.csv')

        ax = self.fig.add_subplot(111)
        ax.plot(data['Date'][-30:], data['Adj_Close'][-30:], label='close')
        ax.plot(data['Date'][-30:], data['High'][-30:], label='High')
        ax.set_title('title title title title')
        ax.legend()
        
        self.canvas.draw()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
