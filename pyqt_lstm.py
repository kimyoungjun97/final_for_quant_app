import sys
import yfinance as yf
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

        self.currencies_lists = [('AUDUSD=X', 'AUD-USD'), ('CNY=X', 'USD-CNY'), ('EURCAD=X', 'EUR-CAD'), ('EURCHF=X', 'EUR-CHF'), ('EURGBP=X', 'EUR-GBP'),
                            ('EURHUF=X', 'EUR-HUF'), ('EURJPY=X', 'EUR-JPY'), ('EURSEK=X', 'EUR-SEK'), ('EURUSD=X', 'EUR-USD'), ('GBPJPY=X', 'GBP-JPY'),
                            ('GBPUSD=X', 'GBP-USD'), ('HKD=X', 'USD-HKD'), ('IDR=X', 'USD-IDR'), ('INR=X', 'USD-INR'), ('JPY=X', 'USD-JPY'),
                            ('MXN=X', 'USD-MXN'), ('MYR=X', 'USD-MYR'), ('NZDUSD=X', 'NZD-USD'), ('PHP=X', 'USD-PHP'), ('RUB=X', 'USD-RUB'),
                            ('SGD=X', 'USD-SGD'), ('THB=X', 'USD-THB'), ('ZAR=X', 'USD-ZAR')]

        self.futures = [('BZ=F', 'BRENT_OIL'), ('CC=F', 'COCOA'), ('KC=F', 'Coffee'), ('HG=F', 'COPPER'), ('ZC=F', 'CORN'),
                   ('CT=F', 'COTTON'),
                   ('CL=F', 'CRUDE_OIL'), ('YM=F', 'DOW'), ('GF=F', 'FEEDER_CATTLE'), ('GC=F', 'GOLD'),
                   ('HE=F', 'LEAN_HOGS'), ('LE=F', 'LIVE_CATTLE'),
                   ('LBS=F', 'LUMBER'), ('NQ=F', 'NASDAQ'), ('NG=F', 'NATURAL_GAS'), ('ZO=F', 'OAT'),
                   ('PA=F', 'PALLADIUM'), ('PL=F', 'PLATINUM'), ('ZR=F', 'ROUGH_RICE'),
                   ('RTY=F', 'RUSSEL2000'), ('SI=F', 'SILVER'), ('ZS=F', 'SOYBEAN'), ('ZM=F', 'SOYBEAN_MEAL'),
                   ('ZL=F', 'SOYBEAN_OIL'),
                   ('ES=F', 'SPX'), ('SB=F', 'SUGAR'), ('ZT=F', 'US2YT'), ('ZF=F', 'US5YT'), ('ZN=F', 'US10YT'),
                   ('ZB=F', 'US30YT'), ('KE=F', 'WHEAT')]

    def buttonfunction01(self):
        with open('./pickle/samsung_stock_minmaxscaler.pickle', 'rb') as f:
            minmaxscaler = pickle.load(f)

        X_train, X_test, Y_train, Y_test, last_test_data_X, last_test_data_Y = np.load('./datasets/samsung_preprocessing_30.npy', allow_pickle=True)

        model = load_model('models/samsung_multivariation.h5')

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

    def btn_world_indices_click(self):
        self.cbox_list.clear()
        pass

    def btn_currencies_click(self):
        self.cbox_list.clear()
        # for i in range(len(self.currencies_lists)):
        #     self.cbox_list.addItem(self.currencies_lists[i][1])
        for ticker, name in self.currencies_lists:
            self.cbox_list.addItem(name)

    def list_click(self):
        index = str(self.cbox_list.currentIndex())
        int_index = int(index)
        print('int index', int_index)
        print(index)
        text = str(self.cbox_list.currentText())
        print(text)

        if text == 'samsung':
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

            self.lbl_01.setText('내일 %s의 예측 종가는 %d원입니다.' %(text, tomorrow_predicted_value[0][0])) #버튼을 누르면 라벨글 변경

        else:
            section = 'currencies_lists'
            name = text

            print(len(self.currencies_lists))
            updated_High = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, 'High'))
            updated_High['Date'] = pd.to_datetime(updated_High['Date'])
            updated_High.set_index('Date', inplace=True)
            updated_Low = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, 'Low'))
            updated_Low['Date'] = pd.to_datetime(updated_Low['Date'])
            updated_Low.set_index('Date', inplace=True)
            updated_Close = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, 'Adj Close'))
            updated_Close['Date'] = pd.to_datetime(updated_Close['Date'])
            updated_Close.set_index('Date', inplace=True)
            updated_Change = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, 'Change'))
            updated_Change['Date'] = pd.to_datetime(updated_Change['Date'])
            updated_Change.set_index('Date', inplace=True)

            a = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
            b = datetime.datetime.strptime('23:59:00', '%H:%M:%S').time()
            c = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
            d = datetime.datetime.strptime('05:59:00', '%H:%M:%S').time()

            currentTime = datetime.datetime.now().time()  # 현재시간만.
            Today = datetime.date.today()
            last_date_from_previous_df = pd.to_datetime(updated_Change.index[-1]).date()  # 01.25일
            one_day = datetime.timedelta(days=1)

            if a <= currentTime <= b:
                print('하루 전 데이터까지')
                print(index)
                print(self.currencies_lists[0][0])
                new_data = yf.download(self.currencies_lists[int_index][0], start=last_date_from_previous_df + one_day,
                                       end=Today)  # 마지막 날짜부터 어제
                # date만 가져오는 코드 어떡하지?(시간제외)
                print(new_data)  # 01/26(휴무일이라 안나옴) -> 01/27, 01/28 데이터만 나옴
                print(new_data.index)
            elif c <= currentTime <= d:
                print('마지막 종가 이전거 까지')
                new_data = yf.download(self.currencies_lists[int_index][0], start=last_date_from_previous_df + one_day,
                                       end=Today)  # 마지막 날짜부터 어제-1day 데이터까지
                new_data = new_data[:-1]
                print(new_data)
            else:
                print(' 8AM에 이후로 다시 시도하시오.')

            col_list = [(updated_High, 'High'), (updated_Low, 'Low'), (updated_Close, 'Adj Close'),
                        (updated_Change, 'Change')]
            for updated_data, col in col_list:
                if col == 'Change':
                    # change 열 전환하여 추가하는 과정
                    updated_data_Close_last_one_row = updated_Close.iloc[[-1]]  # 마지막 종가 행 하나가져오기
                    print(updated_data_Close_last_one_row)
                    new_Close = new_data[['Adj Close']]
                    updated_Close_before_Change = pd.concat([updated_data_Close_last_one_row, new_Close])
                    print(updated_Close_before_Change)
                    new_Change = (updated_Close_before_Change.pct_change(periods=1) * 100).round(2)
                    print(new_Change)
                    new_Change = new_Change[1:]
                    new_Change.rename(columns={'Adj Close': 'Change'}, inplace=True)
                    final_df = pd.concat([updated_data, new_Change])
                    print(final_df)
                else:
                    divided_new_data = new_data[[col]]
                    final_df = pd.concat([updated_data, divided_new_data])
                final_df.to_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, col), index=True)

                # 마지막 30개 예측
                with open('./{}_minmaxscaler/{}_{}_minmaxscaler.pickle'.format(section, name, col), 'rb') as f:
                    minmaxscaler = pickle.load(f)
                last30_df = final_df[-30:]
                scaled_last30_df = minmaxscaler.transform(last30_df)
                model = load_model('./{}_model/{}_{}_model.h5'.format(section, name, col))
                tmr_predict = model.predict(scaled_last30_df.reshape(1, 30, 1))
                print(tmr_predict)
                tmr_predicted_value = minmaxscaler.inverse_transform(tmr_predict)
                print('내일예측값$ %2f ' % tmr_predicted_value[0][0])
                print('{}의 내일 예측값_{}'.format(col, tmr_predicted_value))

                self.lbl_01.setText('내일 %s의 예측 종가는 %d원입니다.' % (text, tmr_predicted_value[0][0]))  # 버튼을 누르면 라벨글 변경


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()