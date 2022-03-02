import yfinance as yf
# import FinanceDataReader as fdr
import pandas as pd
from tensorflow.keras.models import load_model
import datetime
import pickle
from tensorflow.keras.callbacks import EarlyStopping  # early_stopping 걸기
# from matplotlib.backends.backend_pdf import PdfPages
early_stopping=EarlyStopping(monitor='val_loss',patience=5) # early_stopping 걸기
pd.set_option('display.max_columns', None) # 열이 전부다 나오게

futures =       [('BZ=F','BRENT_OIL' ),('CC=F','COCOA'),('KC=F', 'Coffee'),('HG=F','COPPER'),('ZC=F','CORN'),('CT=F','COTTON'),
                ('CL=F','CRUDE_OIL' ),('YM=F', 'DOW'),('GF=F','FEEDER_CATTLE'),('GC=F','GOLD'),('HE=F','LEAN_HOGS'),('LE=F','LIVE_CATTLE'),
                ('LBS=F','LUMBER'),('NQ=F', 'NASDAQ'),('NG=F','NATURAL_GAS'),('ZO=F','OAT'),('PA=F','PALLADIUM' ),('PL=F','PLATINUM'),('ZR=F','ROUGH_RICE'),
                ('RTY=F', 'RUSSEL2000'),('SI=F','SILVER'),('ZS=F','SOYBEAN'),('ZM=F','SOYBEAN_MEAL'),('ZL=F','SOYBEAN_OIL'),
                ('ES=F', 'SPX'),('SB=F','SUGAR'),('ZT=F','US2YT'),('ZF=F', 'US5YT'),( 'ZN=F', 'US10YT'), ('ZB=F','US30YT' ), ('KE=F','WHEAT')]
currencies_lists = [('AUDUSD=X', 'AUD-USD'), ('CNY=X', 'USD-CNY'), ('EURCAD=X', 'EUR-CAD'), ('EURCHF=X', 'EUR-CHF'), ('EURGBP=X', 'EUR-GBP'),
                    ('EURHUF=X', 'EUR-HUF'), ('EURJPY=X', 'EUR-JPY'), ('EURSEK=X', 'EUR-SEK'), ('EURUSD=X', 'EUR-USD'), ('GBPJPY=X', 'GBP-JPY'),
                    ('GBPUSD=X', 'GBP-USD'), ('HKD=X', 'USD-HKD'), ('IDR=X', 'USD-IDR'), ('INR=X', 'USD-INR'), ('JPY=X', 'USD-JPY'),
                    ('MXN=X', 'USD-MXN'), ('MYR=X', 'USD-MYR'), ('NZDUSD=X', 'NZD-USD'), ('PHP=X', 'USD-PHP'), ('RUB=X', 'USD-RUB'),
                    ('SGD=X', 'USD-SGD'), ('THB=X', 'USD-THB'), ('ZAR=X', 'USD-ZAR')]
world_indices = [('^AORD', 'ALL ORDINARIES'), ('^BFX', 'BEL 20'), ('^FCHI', 'CAC 40'), ('^BUK100P', 'Cboe UK 100'), ('^GDAXI','DAX PERFORMANCE-INDEX'),
('^DJI','Dow Jones Industrial Average'),('^STOXX50E', 'ESTX 50 PR.EUR'),('^N100', 'Euronext 100 Index'),('^KLSE','FTSE Bursa Malaysia KLCI'),
 ('^FTSE', 'FTSE 100'),('^HSI','HANG SENG INDEX'),('^BVSP','IBOVESPA'), ('^MXX','IPC MEXICO'),
 ('^JKSE', 'Jakarta Composite Index'),('^KS11','KOSPI Composite Index'),('^MERV','MERVAL'),('^IXIC','NASDAQ Composite'),
 ('^N225', 'Nikkei 225'),('^XAX','NYSE AMEX COMPOSITE INDEX'),('^NYA','NYSE COMPOSITE (DJ)'),('^RUT','Russell 2000'),('^GSPC','S&P 500'),
 ('^BSESN', 'S&P BSE SENSEX'), ('399001.SZ', 'Shenzhen Component'),('000001.SS', 'SSE Composite Index'),('^STI','STI Index'),
 ('^TA125.TA', 'TA-125'),('^TWII','TSEC weighted index'),('^VIX','Vix')]

print(len(futures), len(currencies_lists), len(world_indices))  # 31 23 29

'''
 예측할 종목은 각 3개 섹션(futures(31), currencies(23), world_indicies(29) 로 나뉘어져 있다.
 각각의 섹션에 대해 필요한 파일은 -> 원본.csv, minmaxscaler, model, train_test_split, updated.csv 이다.
 디렉토리를 각각 섹션에 대해 만들텐데 예시는 다음과 같음-> currencies_data, currencies_minmaxscaler, currencies_model, currencies_train_test_split, currencies_updated
 <GUI 구성>
 '선물' 이라는 버튼 누르면 콤보박스 리스트에 '선물 의 name리스트만 쫙 뜸 ( ticker 말고)
 콤보박스에서  원하는 종목 누르면, 밑에 텍스트가 뜸 '*** 종목의 내일 예측 종가는 --- 입니다 ( 하락 예측) / 상승 예측
'''

# 종목 입력시 이름 찾아준다.
section = 'currencies_lists' # 'world_indicies', 'currencies'
ticker = 'AUDUSD=X'
for currencies_list in currencies_lists:
    if currencies_list[0] == ticker:
        name = currencies_list[1]
        break




# updated 데이터 먼저 가져오기(맨처음에 마지막60개 저장한 그 csv)
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


# A. 내일의 종가 예측 (밑에 대로 해야, 주말도 감안할 수 있음) 티커입력해주면 가져와서 4개 column에 관해 전부 다 예측
# - 08:00:00 – 23:59:00 이라면 하루전까지의 데이터
# - 24:00:00 – 05:59:00 이라면 이틀전까지의 데이터(마지막 종가 이전 것 까지)
# - 06:00:00 - 07:59:00 이라면 ' 8am 부터 다시 시도하시오 '

a = datetime.datetime.strptime('08:00:00', '%H:%M:%S').time()
b = datetime.datetime.strptime('23:59:00', '%H:%M:%S').time()
c = datetime.datetime.strptime('00:00:00', '%H:%M:%S').time()
d = datetime.datetime.strptime('05:59:00', '%H:%M:%S').time()

currentTime = datetime.datetime.now().time() # 현재시간만.
Today = datetime.date.today()
last_date_from_previous_df = pd.to_datetime(updated_Change.index[-1]).date() #01.25일
one_day = datetime.timedelta(days=1)


# 현재 시간대에 따라 알아서 적합한 데이터갯수를 추가하여 데이터프레임을 업데이트시켜줌
if a <= currentTime <= b:
    print('하루 전 데이터까지')
    new_data = yf.download(world_indices[0][0], start=last_date_from_previous_df + one_day, end=Today)  # 마지막 날짜부터 어제
    # date만 가져오는 코드 어떡하지?(시간제외)
    print(new_data)  # 01/26(휴무일이라 안나옴) -> 01/27, 01/28 데이터만 나옴
    print(new_data.index)
elif c <= currentTime <= d:
    print('마지막 종가 이전거 까지')
    new_data = yf.download(world_indices[0][0], start=last_date_from_previous_df + one_day, end=Today)  # 마지막 날짜부터 어제-1day 데이터까지
    new_data = new_data[:-1]
    print(new_data)
else:
    print(' 8AM에 이후로 다시 시도하시오.')



col_list = [(updated_High, 'High'), (updated_Low, 'Low'),(updated_Close, 'Adj Close'), (updated_Change, 'Change')]
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
    final_df.to_csv('./{}_updated/{}_{}_updated.csv'.format(section, name, col), index=True )

    # 마지막 30개 예측
    with open('./{}_minmaxscaler/{}_{}_minmaxscaler.pickle'.format(section, name, col), 'rb') as f:
        minmaxscaler = pickle.load(f)
    last30_df = final_df[-30:]
    scaled_last30_df = minmaxscaler.transform(last30_df)
    model = load_model('./{}_model/{}_{}_model.h5'.format(section, name, col))
    tmr_predict = model.predict(scaled_last30_df.reshape(1, 30, 1))
    print(tmr_predict)
    tmr_predicted_value = minmaxscaler.inverse_transform(tmr_predict)
    print('내일예측값$ %2f '%tmr_predicted_value[0][0])
    print('{}의 내일 예측값_{}'.format(col, tmr_predicted_value))

#LSTM 예측
#티커로 찾기 -> 이름으로 찾기로 변경?
