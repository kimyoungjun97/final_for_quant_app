import sys
import yfinance as yf
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from tensorflow.keras.models import load_model
import pandas as pd
import pickle
import datetime


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
        self.setWindowTitle('Final for quant(LSTM)')
        self.setWindowIcon(QIcon('img/icons8-stock-64.png'))

        # 버튼에 기능을 연결하는 코드
        self.btn_futures.clicked.connect(self.btn_futures_click)
        self.btn_world_indices.clicked.connect(self.btn_world_indices_click)
        self.btn_currencies.clicked.connect(self.btn_currencies_click)
        self.cbox_list.activated[str].connect(self.list_click)
        self.btn_high.clicked.connect(self.btn_high_click)
        self.btn_low.clicked.connect(self.btn_low_click)
        self.btn_close.clicked.connect(self.btn_close_click)

        #버튼이나 GUI위에 커서를 올리면 설명해주는 툴팁 표시
        self.btn_world_indices.setToolTip('여기는 세계지수 버튼 입니다.')
        self.btn_futures.setToolTip('여기는 선물 버튼입니다.')
        self.btn_currencies.setToolTip('여기는 환율 버튼입니다.')
        self.setToolTip('예측하고자 하는 버튼을 누르고 콤보박스에 원하는 종목을 클릭 후 고가, 저가, 종가 예측 버튼을 누르세요')
        
        #출력 라벨 가운데 정렬
        self.lbl_01.setAlignment(Qt.AlignCenter)

        self.currencies_list = [('AUDUSD=X', 'AUD-USD'), ('CNY=X', 'USD-CNY'), ('EURCAD=X', 'EUR-CAD'), ('EURCHF=X', 'EUR-CHF'), ('EURGBP=X', 'EUR-GBP'),
                            ('EURHUF=X', 'EUR-HUF'), ('EURJPY=X', 'EUR-JPY'), ('EURSEK=X', 'EUR-SEK'), ('EURUSD=X', 'EUR-USD'), ('GBPJPY=X', 'GBP-JPY'),
                            ('GBPUSD=X', 'GBP-USD'), ('HKD=X', 'USD-HKD'), ('IDR=X', 'USD-IDR'), ('INR=X', 'USD-INR'), ('JPY=X', 'USD-JPY'),
                            ('MXN=X', 'USD-MXN'), ('MYR=X', 'USD-MYR'), ('NZDUSD=X', 'NZD-USD'), ('PHP=X', 'USD-PHP'), ('RUB=X', 'USD-RUB'),
                            ('SGD=X', 'USD-SGD'), ('THB=X', 'USD-THB'), ('ZAR=X', 'USD-ZAR')]

        self.futures_list = [('BZ=F', 'BRENT_OIL'), ('CC=F', 'COCOA'), ('KC=F', 'Coffee'), ('HG=F', 'COPPER'), ('ZC=F', 'CORN'),
                   ('CT=F', 'COTTON'),
                   ('CL=F', 'CRUDE_OIL'), ('YM=F', 'DOW'), ('GF=F', 'FEEDER_CATTLE'), ('GC=F', 'GOLD'),
                   ('HE=F', 'LEAN_HOGS'), ('LE=F', 'LIVE_CATTLE'),
                   ('LBS=F', 'LUMBER'), ('NQ=F', 'NASDAQ'), ('NG=F', 'NATURAL_GAS'), ('ZO=F', 'OAT'),
                   ('PA=F', 'PALLADIUM'), ('PL=F', 'PLATINUM'), ('ZR=F', 'ROUGH_RICE'),
                   ('RTY=F', 'RUSSEL2000'), ('SI=F', 'SILVER'), ('ZS=F', 'SOYBEAN'), ('ZM=F', 'SOYBEAN_MEAL'),
                   ('ZL=F', 'SOYBEAN_OIL'),
                   ('ES=F', 'SPX'), ('SB=F', 'SUGAR'), ('ZT=F', 'US2YT'), ('ZF=F', 'US5YT'), ('ZN=F', 'US10YT'),
                   ('ZB=F', 'US30YT'), ('KE=F', 'WHEAT')]

        self.world_indices_list = []

    def btn_futures_click(self):
        self.cbox_list.clear()
        self.cbox_list.setEnabled(True)
        self.section = 'futures'
        for ticker, name in self.futures_list:
            self.cbox_list.addItem(name)

    def btn_world_indices_click(self):
        self.cbox_list.clear()
        self.cbox_list.setEnabled(True)
        self.section = 'world_indices'
        for ticker, name in self.world_indices_list:
            self.cbox_list.addItem(name)

    def btn_currencies_click(self):
        self.cbox_list.clear()
        self.cbox_list.setEnabled(True)
        self.section = 'currencies'
        for ticker, name in self.currencies_list:
            self.cbox_list.addItem(name)

    def list_click(self):
        self.btn_high.setEnabled(True)
        self.btn_low.setEnabled(True)
        self.btn_close.setEnabled(True)

        self.index = str(self.cbox_list.currentIndex())
        self.int_index = int(self.index)
        print('int index', self.int_index)
        print(self.index)
        self.text = str(self.cbox_list.currentText())
        print(self.text)
        self.name = self.text

    def btn_close_click(self):
        updated_Close = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, 'Adj Close'))
        updated_Close['Date'] = pd.to_datetime(updated_Close['Date'])
        updated_Close.set_index('Date', inplace=True)

        a = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
        b = datetime.datetime.strptime('23:59:00', '%H:%M:%S').time()
        c = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
        d = datetime.datetime.strptime('05:59:00', '%H:%M:%S').time()

        currentTime = datetime.datetime.now().time()  # 현재시간만.
        Today = datetime.date.today()
        last_date_from_previous_df = pd.to_datetime(updated_Close.index[-1]).date()  # 01.25일
        one_day = datetime.timedelta(days=1)

        if a <= currentTime <= b:
            print('하루 전 데이터까지')
            print(self.index)
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제
            # date만 가져오는 코드 어떡하지?(시간제외)
            print(new_data)  # 01/26(휴무일이라 안나옴) -> 01/27, 01/28 데이터만 나옴
            print(new_data.index)
        elif c <= currentTime <= d:
            print('마지막 종가 이전거 까지')
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제-1day 데이터까지
            new_data = new_data[:-1]
            print(new_data)
        else:
            print(' 8AM에 이후로 다시 시도하시오.')

        col_list = [(updated_Close, 'Adj Close')]

        for updated_data, col in col_list:
            divided_new_data = new_data[[col]]
            final_df = pd.concat([updated_data, divided_new_data])
            final_df = final_df.drop_duplicates()
        final_df.to_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, col), index=True)

        # 마지막 30개 예측
        with open('./{}_minmaxscaler/{}_{}_minmaxscaler.pickle'.format(self.section, self.name, col), 'rb') as f:
            minmaxscaler = pickle.load(f)
        last30_df = final_df[-30:]
        scaled_last30_df = minmaxscaler.transform(last30_df)
        model = load_model('./{}_models/{}_{}_model.h5'.format(self.section, self.name, col))
        tmr_predict = model.predict(scaled_last30_df.reshape(1, 30, 1))
        print(tmr_predict)
        tmr_predicted_value = minmaxscaler.inverse_transform(tmr_predict)
        print('%s의 내일예측값$ %2f ' % (self.text, tmr_predicted_value[0][0]))
        print('{}의 내일 예측값_{}'.format(col, tmr_predicted_value))

        self.lbl_01.setText('내일 %s의 예측 종가는 %.3f$입니다.' % (self.text, tmr_predicted_value[0][0]))

    def btn_high_click(self):
        updated_High = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, 'High'))
        updated_High['Date'] = pd.to_datetime(updated_High['Date'])
        updated_High.set_index('Date', inplace=True)

        a = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
        b = datetime.datetime.strptime('23:59:00', '%H:%M:%S').time()
        c = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
        d = datetime.datetime.strptime('05:59:00', '%H:%M:%S').time()

        currentTime = datetime.datetime.now().time()  # 현재시간만.
        Today = datetime.date.today()
        last_date_from_previous_df = pd.to_datetime(updated_High.index[-1]).date()  # 01.25일
        one_day = datetime.timedelta(days=1)

        if a <= currentTime <= b:
            print('하루 전 데이터까지')
            print(self.index)
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제
            # date만 가져오는 코드 어떡하지?(시간제외)
            print(new_data)  # 01/26(휴무일이라 안나옴) -> 01/27, 01/28 데이터만 나옴
            print(new_data.index)
        elif c <= currentTime <= d:
            print('마지막 종가 이전거 까지')
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제-1day 데이터까지
            new_data = new_data[:-1]
            print(new_data)
        else:
            print(' 8AM에 이후로 다시 시도하시오.')

        col_list = [(updated_High, 'High')]

        for updated_data, col in col_list:
            divided_new_data = new_data[[col]]
            final_df = pd.concat([updated_data, divided_new_data])
            final_df = final_df.drop_duplicates()
        final_df.to_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, col), index=True)

        # 마지막 30개 예측
        with open('./{}_minmaxscaler/{}_{}_minmaxscaler.pickle'.format(self.section, self.name, col), 'rb') as f:
            minmaxscaler = pickle.load(f)
        last30_df = final_df[-30:]
        scaled_last30_df = minmaxscaler.transform(last30_df)
        model = load_model('./{}_models/{}_{}_model.h5'.format(self.section, self.name, col))
        tmr_predict = model.predict(scaled_last30_df.reshape(1, 30, 1))
        print(tmr_predict)
        tmr_predicted_value = minmaxscaler.inverse_transform(tmr_predict)
        print('%s의 내일예측값$ %2f ' % (self.text, tmr_predicted_value[0][0]))
        print('{}의 내일 예측값_{}'.format(col, tmr_predicted_value))

        self.lbl_01.setText('내일 %s의 예측 최고가는 %.3f $입니다.' % (self.text, tmr_predicted_value[0][0]))  # 버튼을 누르면 라벨글 변경

    def btn_low_click(self):
        updated_Low = pd.read_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, 'Low'))
        updated_Low['Date'] = pd.to_datetime(updated_Low['Date'])
        updated_Low.set_index('Date', inplace=True)

        a = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
        b = datetime.datetime.strptime('23:59:00', '%H:%M:%S').time()
        c = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
        d = datetime.datetime.strptime('05:59:00', '%H:%M:%S').time()

        currentTime = datetime.datetime.now().time()  # 현재시간만.
        Today = datetime.date.today()
        last_date_from_previous_df = pd.to_datetime(updated_Low.index[-1]).date()  # 01.25일
        one_day = datetime.timedelta(days=1)

        if a <= currentTime <= b:
            print('하루 전 데이터까지')
            print(self.index)
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제
            # date만 가져오는 코드 어떡하지?(시간제외)
            print(new_data)  # 01/26(휴무일이라 안나옴) -> 01/27, 01/28 데이터만 나옴
            print(new_data.index)
        elif c <= currentTime <= d:
            print('마지막 종가 이전거 까지')
            new_data = yf.download(self.currencies_list[self.int_index][0], start=last_date_from_previous_df + one_day,
                                   end=Today)  # 마지막 날짜부터 어제-1day 데이터까지
            new_data = new_data[:-1]
            print(new_data)
        else:
            print(' 8AM에 이후로 다시 시도하시오.')

        col_list = [(updated_Low, 'Low')]

        for updated_data, col in col_list:
            divided_new_data = new_data[[col]]
            final_df = pd.concat([updated_data, divided_new_data])
            final_df = final_df.drop_duplicates()
        final_df.to_csv('./{}_updated/{}_{}_updated.csv'.format(self.section, self.name, col), index=True)

        # 마지막 30개 예측
        with open('./{}_minmaxscaler/{}_{}_minmaxscaler.pickle'.format(self.section, self.name, col), 'rb') as f:
            minmaxscaler = pickle.load(f)
        last30_df = final_df[-30:]
        scaled_last30_df = minmaxscaler.transform(last30_df)
        model = load_model('./{}_models/{}_{}_model.h5'.format(self.section, self.name, col))
        tmr_predict = model.predict(scaled_last30_df.reshape(1, 30, 1))
        print(tmr_predict)
        tmr_predicted_value = minmaxscaler.inverse_transform(tmr_predict)
        print('%s의 내일예측값$ %2f ' % (self.text, tmr_predicted_value[0][0]))
        print('{}의 내일 예측값_{}'.format(col, tmr_predicted_value))

        self.lbl_01.setText('내일 %s의 예측 최저가는 %.3f원입니다.' % (self.text, tmr_predicted_value[0][0]))

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()