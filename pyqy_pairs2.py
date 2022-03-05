from PyQt5 import uic
from PyQt5.QtGui import QIcon
import pandas as pd
import matplotlib as mpl
idx = pd.IndexSlice
import seaborn as sns; sns.set(style="whitegrid")
pd.set_option('display.width', 600)
pd.set_option('display.max_columns', 14)
mpl.rcParams['axes.unicode_minus'] = False
pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_rows', None)
import numpy as np
from sklearn.model_selection import train_test_split
idx = pd.IndexSlice
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()
import datetime
from pandas_datareader import data as pdr
plt.rcParams["figure.figsize"] = (20, 15)
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['font.size'] = 15
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from PyQt5.QtCore import *

form_class = uic.loadUiType("pair_trading.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.UIClear()
        self.add_cbox_list()



    def UIClear(self):
        self.setupUi(self)
        self.setWindowTitle('Final for quant(Pair_Trading)')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))
        self.dateedit.setDate(QDate.currentDate())
        self.dateedit.dateChanged.connect(self.startdate_choice)
        self.cbox.activated[str].connect(self.cbox_list_click)

        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)

    #     Today = datetime.date.today()  # 설정한 날짜로 할 수 있게.
    #
    #     start = datetime.datetime(2007, 1, 1)
    #
    #     df = pdr.get_data_yahoo(['HE=F', 'ZS=F'], start, Today)['Adj Close']
    #     df.isnull().sum()
    #     df.fillna(method='ffill', inplace=True)
    #     df.isnull().sum()
    #     print(df.head())
    #
    #     # train test split ( train_close 은 80프로)
    #     train_close, test_close = train_test_split(df, test_size=0.2, shuffle=False)
    #
    #     # train데이터는 2007-01-01 ~ 2019-03-01 /
    #     len_df = len(df)
    #     len_train = len(train_close)
    #     len_test = len(test_close)
    #
    #     asset1 = 'HE=F'  # lean hog
    #     asset2 = 'ZS=F'  # soybean
    #     asset1_name = 'lean_hog'
    #     asset2_name = 'soybean'
    #
    #     print(len(df))  # 전체데이터 수 3806
    #
    #     # ratio 계산
    #     ratios = df[asset1] / df[asset2]  # 전체 데이터에 대한 ratios
    #     train_ratio = ratios[:len_train]
    #     test_ratio = ratios[len_test:]
    #
    #     """# test 데이터의 z-score"""
    #     test = pd.DataFrame()  # 데이터프레임
    #     test['asset1'] = test_close[asset1]  # asset1에 대한 train (series 타입)
    #     test['asset2'] = test_close[asset2]  # asset2에 대한 train (series 타입)
    #
    #     # 테스트 데이터의 zscore 생성
    #     self.signals = pd.DataFrame()
    #     # signals['asset1'] = test['asset1']
    #     # signals['asset2'] = test['asset2']
    #
    #     ma1 = test_ratio.rolling(window=3, center=False).mean()  # window수는 이따가 조정해서 바꾸기.
    #     ma2 = test_ratio.rolling(window=133, center=False).mean()
    #     std2 = test_ratio.rolling(window=133, center=False).std()
    #     rolled_zscore = (ma1 - ma2) / std2
    #
    #     # z-score 계산하고 uppser Threshoilds z-score, lower
    #     self.signals['z'] = rolled_zscore
    #     self.signals['z upper limit'] = np.mean(self.signals['z']) + np.std(self.signals['z'])
    #     self.signals['z lower limit'] = np.mean(self.signals['z']) - np.std(self.signals['z'])
    #
    #     self.ax.plot(self.signals['z']['2022-01-01':].index, self.signals['z']['2022-01-01':], label="z Value")
    #     self.ax.set_title("Z-score Evolution")
    #     self.ax.axhline(self.signals['z'].mean(), color="black")
    #     self.ax.axhline(self.signals['z upper limit'].mean(), color="red", label="Upper Threshold")
    #     self.ax.axhline(self.signals['z lower limit'].mean(), color="green", label="Lower Threshold")
    #     self.ax.set_ylim([-2, 1.5])
    #     self.ax.legend()
    #     z_max = self.signals['z'][-20:].max()
    #     z_min = self.signals['z'][-20:].min()
    #     if (z_min < -2) | (z_max > 1.5):
    #         self.ax.set_ylim([z_min - 0.5, z_max + 0.5])
    #     else:
    #         self.ax.set_ylim([-2, 1.5])
    #     self.canvas = FigureCanvas(self.fig)
    #     self.layout.addWidget(self.canvas)
    #     self.canvas.draw()
    #
    def startdate_choice(self):
        startdate = self.dateedit.date()
        print(startdate)
        change_date = startdate.toString(Qt.ISODate)
        print(type(change_date))
        print(change_date)

        change_date = pd.to_datetime(change_date)
        print(type(change_date))
        print(change_date)

        self.ax.cla()

        # self.fig = self.fig
        # self.fig = plt.Figure()
        # self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.signals['z'][change_date:].index, self.signals['z'][change_date:], label="z Value")
        self.ax.set_title("Z-score Evolution")
        self.ax.axhline(self.signals['z'].mean(), color="black")
        self.ax.axhline(self.signals['z upper limit'].mean(), color="red", label="Upper Threshold")
        self.ax.axhline(self.signals['z lower limit'].mean(), color="green", label="Lower Threshold")
        self.ax.set_ylim([-2, 1.5])
        self.ax.legend()
        self.canvas.draw()

    def add_cbox_list(self):
        self.cbox.addItem('soybean | lean_hog')
        self.cbox.addItem('KOSPI | UDS-JPY')

    def cbox_list_click(self):
        self.index = str(self.cbox.currentIndex())
        self.index = int(self.index)

        if self.index == 0:
            ticker1 = 'HE=F'
            ticker2 = 'ZS=F'
            print(self.index, ticker1, ticker2)
        elif self.index == 1:
            ticker1 = '^KS11'
            ticker2 = 'JPY=X'
            print(self.index, ticker1, ticker2)
        else :
            print('error')

        print(self.index, ticker1, ticker2)

        Today = datetime.date.today()  # 설정한 날짜로 할 수 있게.
        start = datetime.datetime(2007, 1, 1)
        df = pdr.get_data_yahoo([ticker1, ticker2], start, Today)['Adj Close']
        df.isnull().sum()
        df.fillna(method='ffill', inplace=True)
        df.isnull().sum()
        print(df.head())
        # train test split ( train_close 은 80프로)
        train_close, test_close = train_test_split(df, test_size=0.2, shuffle=False)

        # train데이터는 2007-01-01 ~ 2019-03-01 /
        len_df = len(df)
        len_train = len(train_close)
        len_test = len(test_close)

        asset1 = ticker1  # lean hog
        asset2 = ticker2  # soybean
        # asset1_name = 'lean_hog'
        # asset2_name = 'soybean'

        print(len(df))  # 전체데이터 수 3806

        # ratio 계산
        ratios = df[asset1] / df[asset2]  # 전체 데이터에 대한 ratios
        train_ratio = ratios[:len_train]
        test_ratio = ratios[len_test:]

        """# test 데이터의 z-score"""
        test = pd.DataFrame()  # 데이터프레임
        test['asset1'] = test_close[asset1]  # asset1에 대한 train (series 타입)
        test['asset2'] = test_close[asset2]  # asset2에 대한 train (series 타입)

        # 테스트 데이터의 zscore 생성
        self.signals = pd.DataFrame()
        self.signals['asset1'] = test['asset1']
        self.signals['asset2'] = test['asset2']

        # test 데이터의 ratio(asset1 / asset2) 를 rolling 하기
        ma1 = test_ratio.rolling(window=3, center=False).mean()  # window수는 이따가 조정해서 바꾸기.
        ma2 = test_ratio.rolling(window=133, center=False).mean()
        std2 = test_ratio.rolling(window=133, center=False).std()
        rolled_zscore = (ma1 - ma2) / std2

        # z-score 계산하고 uppser Threshoilds z-score, lower
        self.signals['z'] = rolled_zscore
        self.signals['z upper limit'] = np.mean(self.signals['z']) + np.std(self.signals['z'])
        self.signals['z lower limit'] = np.mean(self.signals['z']) - np.std(self.signals['z'])
        # signals 라는 DataFrame에는 현재까지 5개 열 존재(asset1/ asset2 / 'z' / 'z upper limit'/ 'z lower limit' )

        self.signals['signals1'] = 0  # 0으로 만들어진 series
        self.signals['signals1'] = np.select(
            [self.signals['z'] > self.signals['z upper limit'], self.signals['z'] < self.signals['z lower limit']],
            [-1, 1], default=0)

        # we take the first order difference to obtain portfolio position in that stock

        # (이전값, 현재값)이 각각 (1,0),(0,1),(0,-1),(-1,0) 인 것들만 값이 -1과 1로 나옴(차분 diff() = 현재값 - 이전값 )
        self.signals['positions1'] = self.signals['signals1'].diff()
        self.signals['signals2'] = -self.signals['signals1']
        self.signals['positions2'] = self.signals['signals2'].diff()

        #self.ax.cla()

        # self.fig = plt.Figure()
        # self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.signals['z'][-20:].index, self.signals['z'][-20:], label="z Value")
        self.ax.set_title("Z-score Evolution")
        self.ax.axhline(self.signals['z'].mean(), color="black")
        self.ax.axhline(self.signals['z upper limit'].mean(), color="red", label="Upper Threshold")
        self.ax.axhline(self.signals['z lower limit'].mean(), color="green", label="Lower Threshold")
        self.ax.legend()
        z_max = self.signals['z'][-20:].max()
        z_min = self.signals['z'][-20:].min()
        if (z_min < -2) | (z_max > 1.5):
            self.ax.set_ylim([z_min - 0.5, z_max + 0.5])
        else:
            self.ax.set_ylim([-2, 1.5])

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

    def clearLayout(layout):
        while layout.count():
            child = layout.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()