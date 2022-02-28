import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pickle
import datetime
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("test.ui")[0]

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
        self.btn_01.clicked.connect(self.buttonfunction01)
        self.btn_futures.clicked.connect(self.btn_futures_click)
        self.btn_world_indices.clicked.connect(self.btn_world_indices_click)
        self.btn_currencies.clicked.connect(self.btn_currencies_click)
        self.cbox_list.activated[str].connect(self.list_click)
        #datetime ui

    def buttonfunction01(self):
        with open('./pickle/samsung_stock_minmaxscaler.pickle', 'rb') as f:
            minmaxscaler = pickle.load(f)

        X_train, X_test, Y_train, Y_test, last_test_data_X, last_test_data_Y = np.load('./datasets/samsung_preprocessing_30.npy', allow_pickle=True)

        model = load_model('./models/samsung_multivariation.h5')

        predict = model.predict(X_test)
        last_predict = model.predict(last_test_data_X)

        tomorrow_predict = model.predict(last_test_data_X[-1].reshape(1, 30, 6))

        print(tomorrow_predict)

        with open('./pickle/samsung_stock_minmaxscaler_close.pickle', 'rb') as f:
            minmaxscaler_close = pickle.load(f)

        tomorrow_predicted_value = minmaxscaler_close.inverse_transform(tomorrow_predict)
        print('%d 원' % tomorrow_predicted_value[0][0])

        self.lbl_01.setText('%d 원' % tomorrow_predicted_value[0][0]) #버튼을 누르면 라벨글 변경

    def btn_futures_click(self):
        self.cbox_list.clear()
        self.cbox_list.addItem('samsung')
        self.cbox_list.addItem('선물2')
        self.cbox_list.addItem('선물3')

    def btn_world_indices_click(self):
        self.cbox_list.clear()
        self.cbox_list.addItem('세계지수1')
        self.cbox_list.addItem('세계지수2')
        self.cbox_list.addItem('세계지수3')

    def btn_currencies_click(self):
        self.cbox_list.clear()
        self.cbox_list.addItem('환율1')
        self.cbox_list.addItem('환율2')
        self.cbox_list.addItem('환율3')
        self.cbox_list.addItem('환율4')

    def list_click(self):
        index = str(self.cbox_list.currentIndex())
        print(index)
        text = str(self.cbox_list.currentText())
        print(text)
        with open('./pickle/{}_stock_minmaxscaler.pickle'.format(text), 'rb') as f:
            minmaxscaler = pickle.load(f)
        X_train, X_test, Y_train, Y_test, last_test_data_X, last_test_data_Y = np.load('./datasets/{}_preprocessing_30.npy'.format(text), allow_pickle=True)
        model = load_model('./models/{}_multivariation.h5'.format(text))
        predict = model.predict(X_test)
        last_predict = model.predict(last_test_data_X)
        tomorrow_predict = model.predict(last_test_data_X[-1].reshape(1, 30, 6))
        print(tomorrow_predict)
        with open('./pickle/{}_stock_minmaxscaler_close.pickle'.format(text), 'rb') as f:
            minmaxscaler_close = pickle.load(f)
        tomorrow_predicted_value = minmaxscaler_close.inverse_transform(tomorrow_predict)
        print('%d 원' % tomorrow_predicted_value[0][0])

        self.lbl_01.setText('%d 원' % tomorrow_predicted_value[0][0]) #버튼을 누르면 라벨글 변경

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()