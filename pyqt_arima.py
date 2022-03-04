import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
# pip install pmdarima
import pmdarima as pm
# conda install -c conda-forge ta-lib
from talib import abstract
import json
#  pip install -r requirements.txt
import talib
import numpy as np
import yfinance as yf
import datetime
from tensorflow.keras.models import load_model
import pickle

# 내일 값 예측

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("arima.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.UIClear()

    def UIClear(self):
        self.setupUi(self)
        self.setWindowTitle('Final for quant')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))

        # 버튼에 기능을 연결하는 코드
        self.cbox_list = ['brent_oil', 'Gold']
        self.cbox.addItem(self.cbox_list[0]) # brent_oil
        self.cbox.addItem(self.cbox_list[1]) # gold

        self.cbox.activated[str].connect(self.list_click)
        self.btn_predict.clicked.connect(self.btn_predict_click)  # 종가 예측 버튼

        #index 초기값 설정, 버튼 입력시 바로 동작
        self.index = 0
        self.class_name = 'brente_oil'

        self.brent_ma = 'TRIMA'
        self.gold_ma = 'WMA'
        self.brent_optimized_period = 64
        self.gold_optimized_period = 5
        self.brent_order = (2, 1, 2)
        self.gold_order = (3, 1, 3)
        self.brent_ticker = 'BZ=F'
        self.gold_ticker = 'GC=F'

    def btn_predict_click(self):
        # 기존의 ma와 이동평균 가져오기
        if self.index == 0:   # class_name == 'brent_oil'
            ma = self.brent_ma
            optimized_period = self.brent_optimized_period
            order = self.brent_order
            ticker = self.brent_ticker
        elif self.index == 1: # gold
            self.class_name = 'Gold'
            ma = self.gold_ma
            optimized_period = self.gold_optimized_period
            order = self.gold_order
            ticker = self.gold_ticker

        lstm_len = 4
        Today = datetime.date.today()

        # 적당히 6~8개월 어치 데이터 가져오기
        data = yf.download(ticker, start='2021-06-27', end=Today)
        data = data.reset_index(drop=True)

        # 우리가 예측을 위해 필요한 데이터는 (64-1) + (4-1) = 최신 101개이여야 함
        data_len = ((optimized_period - 1) + (lstm_len)) * -1
        data = data[data_len:]

        # Initialize moving averages from Ta-Lib, store functions in dictionary
        talib_moving_averages = ['SMA', 'EMA', 'WMA', 'DEMA', 'KAMA', 'MIDPOINT', 'MIDPRICE', 'T3', 'TEMA', 'TRIMA']
        functions = {}
        for ma in talib_moving_averages:
            functions[ma] = abstract.Function(ma)

        # CSV should have columns: ['date', 'open', 'high', 'low', 'close', 'volume']
        data = data.rename(columns={'Adj Close': 'close'})  # 이름을 'close' 'High', 'Low', 'close' 'change' 인덱스는 걍 순서
        data = data.rename(columns={'High': 'high'})
        data = data.rename(columns={'Low': 'low'})
        data = data.rename(columns={'Date': 'date'})
        data.drop(['Open', 'Close', 'Volume'], axis=1, inplace=True)  # drop 열 추가

        # 저변동성 / 고 변동성 시계열로 각각 나누기
        low_vol = functions[ma](data, optimized_period)  # int로 만들어줘야./ 총 1248곘지만 앞에 이평 길이-1 만큼 Nan값
        print(low_vol)  # 4개 뺴고 다 난값
        high_vol = data['close'] - low_vol
        print(high_vol)  # 4개 뺴고 다 난값

        # 모델 불러오기
        with open('./{}/{}_Arima_model.pickle'.format(self.class_name, self.class_name), 'rb') as f:
            model = pickle.load(f)

        # data = 2022-01-26 ~ 2022-02-10(가장 최신 종가데이터)를 넣어서 내일 값 예측시키기.
        predict_arima_price = low_vol[-1:]  # 마지막 1개 가져와서 예측.
        model = pm.ARIMA(order=order)
        model.fit(predict_arima_price)  # 우리는 2007년 ~ 2022-01-25까지 다 train시킨 모델을 가져온 것이기 떄문에 01-26부터 데이터만 추가시키면 되지않낭?
        arima_prediction = model.predict()[0]  # ㅁ내일 값 예측
        print('arima 내일 예측 값:', arima_prediction)  # 내일 예측 값: 79.01496184233464

        predict_lstm_price = high_vol[-4:]
        print(high_vol[-6:])
        dataset = np.reshape(predict_lstm_price.values, (lstm_len, 1))  # ( 1, lstm_len, 1) 아닌강>?
        print('dataset', dataset)
        model = load_model('./{}/{}_Lstm_model.h5'.format(self.class_name, self.class_name))
        print('-----여기까진 에러 없음-----')
        with open('./{}/{}_minmaxscaler.pickle'.format(self.class_name, self.class_name), 'rb') as f:
            minmaxscaler = pickle.load(f)
        dataset_scaled = minmaxscaler.transform(dataset)

        lstm_prediction = model.predict(np.reshape(dataset_scaled, (1, 4, 1)))  # dataset_scaled(1, 4, 1)안해줘도??
        prediction = minmaxscaler.inverse_transform(lstm_prediction)
        print('lstm 내일 예측 값 :', prediction)

        final_prediction = arima_prediction + prediction
        print('최종 내일 예측 값은?? ====> ', final_prediction)
        print(self.class_name, final_prediction)
        self.lbl.setText( '%s 종목의 예측종가는 %.2f$입니다.' % (self.class_name,  final_prediction))
        # self.lbl_01.setText('내일 %s의 예측 최고가는 %.3f원입니다.' % (text, tmr_predicted_value[0][0]))

    def list_click(self):
        self.index = str(self.cbox.currentIndex())
        self.index = int(self.index)
        print('int index', self.index)

        self.class_name = str(self.cbox.currentText())
        print(self.class_name)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()