import h2o
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
import random
from pandas import read_csv
from pandas import datetime
import locale
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error


model_path = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/mefi3_sfc_regressiontrees'
monty_path = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/monty2_sfc_regressiontrees_features'
monty_path_new = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/monty2_sfc_regressiontrees_features_new'
monty_so_path = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/monty2_shoporder_regressiontrees'
monty_so_path_millis = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/monty2_shoporder_regressionforest_millis'
monty2_so_daybyday = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/m2_regressiontrees_totaltime'
monty2_so_shifts = 'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/ml_models/mty2_totaltime_shifts'
#saved_model = h2o.load_model(model_path)
#Make sure h2o.init() is executed in a separate terminal
#h2o.init()
h2o.connect()
cols = ['diff_duration_secs','sfc_date_diff','PRODUCTIVITY_SFC','Hours','Unique concatenate(DESCRIPTION)','ITEM_GROUP','Unique count(WORK_CENTER)','Unique count(RESRCE)','Count(DATE_TIME)','ITEM_NO','SFC_Lineitems','Unique count(ROUTER)','Unique count(ITEM_NO)','Unique count(SHOP_ORDER_BO)']
vals = ['1227.68','2413000','37.297969332780774','0','Messwerk Karree 1, V2S Messwerke','V2S','18','25','25','25','72107433','2','2','2']
# data = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/MEFI3TrainDatasetTimeSeriesEdition.csv')

#df = pd.DataFrame([vals],columns=cols)
#hf = h2o.H2OFrame(df)

cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Max(transfer_time)','sfc_date_diff','diff_duration_secs','Mode(transfer_time)','Last(DATE_TIME)','First(DATE_TIME)','Unique count(ROUTER)','Min(transfer_time)','STUTZAB','Unique count(RESRCE)','VENTIL','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(ITEM_NO)']
#stut_val = '250,0'
stut_val = '152,4'
ventil_val = 'VE'
vals_monty = ['237580','72481','1m 35s','289000.0','21.061','13s','2019-12-06T09:26:50','2019-12-06T09:22:01','1','8s',stut_val,'10',ventil_val,'4','10','10','1']
#df1 = pd.DataFrame([vals_monty],columns=cols_monty)
#hf1 = h2o.H2OFrame(df1)
global num1
def show_entry_fields():
    global num1
    num1 = e2.get()
    print(f"Number of SFC's are {num1}")
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(model_path)
    #print(mojo_model)
    predict = mojo_model.predict(hf) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    #Since everything is processed parellely the number of quantity should be added
    full_time = predict + int(num1)
    full_val = datetime.now() + timedelta(seconds=int(full_time))
    shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')


global num2
def show_entry_fields_monty():
    global num2
    num2 = e2.get()
    print(f"Number of SFC's are {num2}")
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty_path)
    #print(mojo_model)
    df1 = pd.DataFrame([vals_monty],columns=cols_monty)
    hf1 = h2o.H2OFrame(df1)
    predict = mojo_model.predict(hf1) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    #Since everything is processed parellely the number of quantity should be added
    full_time = predict + int(num2)
    full_val = datetime.now() + timedelta(seconds=int(full_time))
    shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')

def arima_predictor():
    data1 = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/MEFI3TrainDatasetTimeSeriesEdition.csv')
    data1.head()
    uni_data = data1['Unique count(SFC)']
    uni_data.index = data1['First(DATE_TIME)']
    #uni_data.head()
    X = uni_data.values
    size = int(len(X) * 0.66)
    #print(data1.head())
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    #obs = pred_test
    #history.append(obs)
    print(yhat)
    #print('predicted=%f, expected=%f' % (yhat, obs))
    return yhat

#Method for Simulated outputs live prediction
def sim_pred_formulator():
    data2 = pd.read_csv('C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models/simulated_monty2_sfcflow_noventil.csv')
    data3 = data2.tail(10)
    #data3 = data2.head(10)
    print(data3)
    new_df = pd.DataFrame()
    overall_time_sfc = 0
    for index,row in data3.iterrows():
        row['Total_time'] = row['ELAPSED_TIME'] + row['ELAPSED_QUEUE_TIME']
        overall_time_sfc += int(row['Total_time'])
        curr_row = pd.DataFrame([row])
        new_df = new_df.append([curr_row],ignore_index=True)

    return overall_time_sfc

def monty_arima_predictor():
    data1 = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/Monty2HourlyShopOrderTrainDataset.csv')
    data1.head()
    uni_data = data1['SFC_Completed']
    uni_data.index = data1['First(DATE_TIME)']
    #uni_data.head()
    X = uni_data.values
    size = int(len(X) * 0.66)
    #print(data1.head())
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    #obs = pred_test
    #history.append(obs)
    print(yhat)
    #print('predicted=%f, expected=%f' % (yhat, obs))
    return yhat

def ts_monty2_arima_totaltime_predictor():
    data2 = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/Monty2HourlySFCTrainDataset.csv')
    data2.head()
    elapsed_time = data2['Sum(Sum(ELAPSED_TIME))']
    elapsed_queue_time = data2['Sum(Sum(ELAPSED_QUEUE_TIME))']
    total_time = (elapsed_time + elapsed_queue_time) / 1000
    uni_data = total_time
    #uni_data.index = data['First(DATE_TIME)']
    uni_data.index = data2['Unique count(SFC)']
    X = uni_data.values
    size = int(len(X) * 0.66)
    #print(data1.head())
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    #obs = pred_test
    #history.append(obs)
    print(yhat)
    #print('predicted=%f, expected=%f' % (yhat, obs))
    return yhat

def estimate_shoporder(qty):
    print(f"Number of SFC's are {qty}")
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(model_path)
    #print(mojo_model)
    predict = mojo_model.predict(hf) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    full_time = predict + int(qty)
    full_val = datetime.now() + timedelta(seconds=int(full_time))
    shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')
    return shoporder_time

def estimate_shoporder_monty(qty,casing,ventil):
    print(f"Number of SFC's are {qty} and casing is {casing} and chosen ventil is {ventil}")
    cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Max(transfer_time)','sfc_date_diff','diff_duration_secs','Mode(transfer_time)','Last(DATE_TIME)','First(DATE_TIME)','Unique count(ROUTER)','Min(transfer_time)','STUTZAB','Unique count(RESRCE)','VENTIL','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(ITEM_NO)']
    stut_val = casing
    ventil_val = ventil
    vals_monty = ['237580','72481','1m 35s','289000.0','21.061','13s','2019-12-06T09:26:50','2019-12-06T09:22:01','1','8s',stut_val,'10',ventil_val,'4','10','10','1']
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty_path)
    #print(mojo_model)
    model_prediction_val = mojo_model.predict(hf1)
    predict = model_prediction_val / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    #print(model_prediction_val)
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    # full_time = predict + int(qty)
    # full_val = datetime.now() + timedelta(seconds=int(full_time))
    # shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    # print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')
    # return shoporder_time
    return (predicted_time, int(predict) * 1000)

def estimate_sfc_totaltime(qty,casing,ventil,date_stamp=None):
    print(f"Number of SFC's are {qty} and casing is {casing} and chosen ventil is {ventil}")
    stut_val = casing
    ventil_val = ventil
    if (stut_val == '152,4' and ventil_val != 'VE'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [409916,98321,'A01PDR0017',ventil_val,'ATEX-Zähler für Serienaufträge, Aufträge Monti2, Rüstintervall Stutzen 1BS746',9,17,17,17,'A01PP000200, A01PP000100, A01PP000400',stut_val,1,1]
    elif (stut_val == '250,0'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [187778,72761,'A01PDR0023',ventil_val,'Rüstintervall Stutzen DN25, BK 4 V2',4,10,10,10,'A01PP000500, A00PP000500',stut_val,1,1]
    elif (stut_val == '220,0'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [183803,77224,'A01PDR0023',ventil_val,'Rüstintervall Stutzen GM3/4, BK V2S, Aufträge Monti2',4,10,10,10,'A01PP000300, A00PP000300, A01PP000100',stut_val,1,1]
    elif (stut_val == '250,'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [549271,104155,'A01PDR0019',ventil_val,'Rüstintervall Stutzen DN25, BK 4 V2 TC, ATEX-Zähler für Serienaufträge, Aufträge Monti2',7,14,14,14,'A01PP000500, A00PP000600, A01PP000200, A01PP000100',stut_val,1,1]
    elif (stut_val == '220'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [564417,88113,'A01PDR0001',ventil_val,'Rüstintervall Stutzen GM3/4, Aufträge Monti2',7,15,15,15,'A01PP000300, A01PP000100',stut_val,1,1]
    elif (stut_val == '50'):
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [0,0,'A01PDR0001',ventil_val,'Rüstintervall Stutzen GM3/4, Aufträge Monti2',7,15,15,15,'A01PP000300, A01PP000100','220',1,1]
    else:
        #Has Ventil VE (Valve)
        cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','Sum(ELAPSED_TIME)','Unique concatenate(ROUTER)','VENTIL','First(Unique concatenate(DESCRIPTION))','Unique count(WORK_CENTER)','Unique count(OPERATION)','SFC_Lineitems','Unique count(RESRCE)','First(Unique concatenate(ITEM_GROUP))','STUTZAB','Unique count(ROUTER)','Unique count(ITEM_NO)']
        vals_monty = [1547654,99070,'A01PDR0020',ventil_val,'ATEX-Zähler für Serienaufträge, Aufträge Monti2, Rüstintervall Stutzen 1BS746',8,15,15,15,'A01PP000200, A01PP000100, A01PP000400',stut_val,1,1]
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty_path_new)
    df4 = pd.DataFrame([vals_monty],columns=cols_monty)
    hf4 = h2o.H2OFrame(df4)
    #print(mojo_model)
    model_prediction_val = mojo_model.predict(hf4)
    predict = model_prediction_val / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    #print(model_prediction_val)
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict)) if date_stamp == None else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    #predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The Start time for the SFC is {orig_time}')
    print(f'The estimated time of completion for the first SFC is {predicted_time}')
    return (predicted_time, int(predict) * 1000)

def estimate_timeseries_shoporder_monty(time,sfc_released):
    print(f"Time taken for one SFC's is {time} and the total SFC released for the next hour {sfc_released}")
    cols_monty = ['Sum(ELAPSED_QUEUE_TIME)','First(DATE_TIME)','Last(DATE_TIME)','Max(transfer_time)','Sum(ELAPSED_TIME)','SFC_Released','Unique count(WORK_CENTER)','Events','Min(transfer_time)','Hour','Day of month','Day of week (name)','SFC_Completed','Mode(transfer_time)','Month (number)','Sum(QTY_SCRAPPED)','Sum(QTY_NON_CONFORMED)']
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    hour = f"{datetime.now():%H}"
    day_int = f"{datetime.now():%d}"
    day_str = datetime.today().strftime('%A')
    month_num = f"{datetime.now():%m}"
    print(day_str,day_int,month_num,hour)
    vals_monty = [time,'02.07.19 16:00:07','02.07.19 16:11:31','5m 3s',time,sfc_released,8,1458,'7s',int(hour),int(day_int),day_str,sfc_released,'8s',month_num,0,0]
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty_so_path)
    print(vals_monty)
    df2 = pd.DataFrame([vals_monty],columns=cols_monty)
    hf2 = h2o.H2OFrame(df2)
    predict = int(mojo_model.predict(hf2)) / 10000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    #predicted_val = datetime.now() + timedelta(seconds=int(predict))
    # if(day_str == 'Samstag'):
    #     predicted_val = datetime.now() + timedelta(seconds=int(predict + 172800)) if date_stamp == None else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    # elif(day_str == 'Sonntag'):
    #     predicted_val = datetime.now() + timedelta(seconds=int(predict + 86400)) if date_stamp == None else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    # else:
    #     predicted_val = datetime.now() + timedelta(seconds=int(predict)) if date_stamp == None else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    predicted_val = datetime.now() + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the entire {sfc_released} SFCs are {predicted_time}')
    # full_time = predict
    # full_val = datetime.now() + timedelta(seconds=int(full_time))
    # shoporder_time = f"{full_val:%d-%m-%Y %H:%M:%S}"
    # print(f'The estimated time of completion for the last SFC for the Shop Order is {shoporder_time}')
    return predicted_time

def timeseries_shoporder_monty_millis(time,sfc_released,sfc_factor,date_stamp=None):
    print(f"Time taken for one SFC's is {time} and the total SFC released for the next hour {sfc_released}")
    cols_monty = ['SFC_Released','SFC_Completed','TOTAL_TIME','Unique concatenate(ITEM_GROUP)','Last(DATE_TIME)','First(DATE_TIME)','Day of month','Hour','Day of week (name)','Unique count(WORK_CENTER)','Month (number)','Sum(QTY_SCRAPPED)','Sum(QTY_NON_CONFORMED)']
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    flow_state = 1
    if(date_stamp == None):
        hour = f"{datetime.now():%H}"
        day_int = f"{datetime.now():%d}"
        day_str = datetime.today().strftime('%A')
        month_num = f"{datetime.now():%m}"
    else:
        hour = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%H}"
        day_int = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%d}"
        day_str = datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S').strftime('%A')
        month_num = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%m}"
        flow_state = 0

    print(day_str,day_int,month_num,hour)
    vals_monty = [298,sfc_released,time,'A01PP000300, A01PP000100','09.09.19 12:59:58','09.09.19 12:00:00',int(day_int),int(hour),day_str,7,month_num,0,0]
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty_so_path_millis)
    print(vals_monty)
    df3 = pd.DataFrame([vals_monty],columns=cols_monty)
    hf3 = h2o.H2OFrame(df3)
    predict = int(mojo_model.predict(hf3)) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    if (sfc_factor < 1 and flow_state == 1):
        predicted_val = datetime.now() + timedelta(seconds=int(predict))
    elif(sfc_factor < 1 and flow_state == 0):
        predicted_val = datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    else:
        predict *= sfc_factor
        predicted_val = datetime.now() + timedelta(seconds=int(predict)) if flow_state == 1 else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))

    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the entire {sfc_released} SFCs are {predicted_time}')
    return predicted_time

def ts_shoporder_monty_forecaster(time,sfc_released,date_stamp=None):
    print(f"Time taken for one SFC's is {time} and the total SFC released for the next hour {sfc_released}")
    cols_monty = ['SINGLE_SFC_TIME','SFC_Completed','SFC_Released','LineItems','Unique concatenate(Day of week (name))','Unique concatenate(ITEM_GROUP)']
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    flow_state = 1
    if(date_stamp == None):
        hour = f"{datetime.now():%H}"
        day_int = f"{datetime.now():%d}"
        day_str = datetime.today().strftime('%A')
        month_num = f"{datetime.now():%m}"
    else:
        hour = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%H}"
        day_int = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%d}"
        day_str = datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S').strftime('%A')
        month_num = f"{datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S'):%m}"
        flow_state = 0

    print(day_str,day_int,month_num,hour)
    vals_monty = [time,int(sfc_released)-random.randint(2,int(sfc_released)),int(sfc_released),int(sfc_released)*10,day_str,'A01PP000300, A01PP000100']
    #Importing to work further, for making single shot predictions it is not needed
    mojo_model = h2o.import_mojo(monty2_so_daybyday)
    print(vals_monty)
    df3 = pd.DataFrame([vals_monty],columns=cols_monty)
    hf3 = h2o.H2OFrame(df3)
    predict = int(mojo_model.predict(hf3)) / 1000000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict)) if flow_state == 1 else datetime.strptime(date_stamp,'%Y-%m-%d %H:%M:%S') + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the entire {sfc_released} SFCs are {predicted_time}')
    return predicted_time

def monty_shift_so_forecaster(time,sfc_released,date_stamp=None):
    print(f"Time taken for one SFC's is {time} and the total SFC released for the next hour {sfc_released}")
    cols_monty = ['shifts','SFC_Completed','SFC_Released','Day of week (name)','Unique concatenate(ITEM_GROUP)','MEAN_TOTAL_TIME','Month (number)']
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    flow_state = 1
    if(date_stamp == None):
        hour = f"{datetime.now():%H}"
        day_int = f"{datetime.now():%d}"
        day_str = datetime.today().strftime('%A')
        month_num = f"{datetime.now():%m}"
    else:
        hour = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%H}"
        day_int = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%d}"
        day_str = datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S').strftime('%A')
        month_num = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%m}"
        flow_state = 0

    print(day_str,day_int,month_num,hour)
    if (int(hour) >= 6 and int(hour) < 14):
        shift_name = "Früh"
    elif(int(hour) >= 14 and int(hour) < 22):
        shift_name = "Spät"
    elif(int(hour) >= 22):
        shift_name = "Nacht"
    else:
        shift_name = "Nacht"

    vals_monty = [shift_name,int(sfc_released)-random.randint(2,int(sfc_released)),int(sfc_released),day_str,'A01PP000300, A01PP000100',time,month_num]
    mojo_model = h2o.import_mojo(monty2_so_shifts)
    print(vals_monty)
    df3 = pd.DataFrame([vals_monty],columns=cols_monty)
    hfmty3 = h2o.H2OFrame(df3)
    predict = int(mojo_model.predict(hfmty3)) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    #Take the time from the last simulated result and add it to the screen
    #Should be passed from the previous method call
    predicted_val = datetime.now() + timedelta(seconds=int(predict)) if flow_state == 1 else datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S') + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the entire {sfc_released} SFCs are {predicted_time}')
    return predicted_time

def monty_shift_so_forecaster_updated(time,sfc_released,sfc_completed,date_stamp=None):
    print(f"Time taken for one SFC's is {time} and the total SFC released for the next hour {sfc_released}")
    cols_monty = ['shifts','SFC_Completed','SFC_Released','Day of week (name)','Unique concatenate(ITEM_GROUP)','MEAN_TOTAL_TIME','Month (number)']
    locale.setlocale(locale.LC_ALL, 'deu_deu')
    flow_state = 1
    if(date_stamp == None):
        hour = f"{datetime.now():%H}"
        day_int = f"{datetime.now():%d}"
        day_str = datetime.today().strftime('%A')
        month_num = f"{datetime.now():%m}"
    else:
        hour = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%H}"
        day_int = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%d}"
        day_str = datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S').strftime('%A')
        month_num = f"{datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S'):%m}"
        flow_state = 0

    print(day_str,day_int,month_num,hour)
    if (int(hour) >= 6 and int(hour) < 14):
        shift_name = "Früh"
    elif(int(hour) >= 14 and int(hour) < 22):
        shift_name = "Spät"
    elif(int(hour) >= 22):
        shift_name = "Nacht"
    else:
        shift_name = "Nacht"

    vals_monty = [shift_name,int(sfc_completed),int(sfc_released),day_str,'A01PP000300, A01PP000100',time,month_num]
    mojo_model = h2o.import_mojo(monty2_so_shifts)
    print(vals_monty)
    df3 = pd.DataFrame([vals_monty],columns=cols_monty)
    hfmty3 = h2o.H2OFrame(df3)
    predict = int(mojo_model.predict(hfmty3)) / 1000
    orig_time = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
    print(predict)
    predicted_val = datetime.now() + timedelta(seconds=int(predict)) if flow_state == 1 else datetime.strptime(date_stamp,'%d-%m-%Y %H:%M:%S') + timedelta(seconds=int(predict))
    predicted_time = f"{predicted_val:%d-%m-%Y %H:%M:%S}"
    print(f'The estimated time of completion for the entire {sfc_released} SFCs are {predicted_time}')
    return predicted_time

if __name__ == "__main__":
    master = tk.Tk()
    # tk.Label(master,
    #          text="First Name").grid(row=0)
    tk.Label(master,
             text="Number of SFC's to Release").grid(row=1)

    e2 = tk.Entry(master)

    e2.grid(row=1, column=1)
    tk.Button(master,
              text='Show', command=show_entry_fields_monty).grid(row=3,
                                                           column=1,
                                                           sticky=tk.W,
                                                           pady=4)
    tk.mainloop()
#mojo_model.varimp_plot()
#h2o.print_mojo(model_path, format='json', tree_index=None)

#Direct model prediction
#h2o.mojo_predict_pandas(df, model_path, verbose=False, setInvNumNA=False)
#h2o.mojo_predict_pandas(df, model_path, genmodel_jar_path=None, classpath=None, java_options=None, verbose=False, setInvNumNA=False)
