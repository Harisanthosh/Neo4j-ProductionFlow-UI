import simpy
from datetime import datetime
import time
import pandas as pd
import sys

global cols_list
global resource_list
global wc_list
global processing_time
global waiting_time

def startSimulator(df2):
    print(df2.head())
    #Using iloc to access can also use iat or at to access elements as matrix
    sfc_sim = df2.iloc[0]['SFC']
    print(sfc_sim)



if __name__ == "__main__":
    # cols_list = []
    df1 = pd.read_csv('sapme_sfcflow.csv',sep=';')
    #print(df1.head())
    global cols_list
    global resource_list
    global wc_list
    global processing_time
    global waiting_time
    cols_list = df1.columns
    resource_list = df1['RESRCE']
    wc_list = df1['WORK_CENTER']
    processing_time = df1['PROCESSING_TIME_SECS']
    waiting_time = df1['WAITING_TIME_SECS']
    print(cols_list)
    print(len(cols_list))
    #for key,val in df1.iterrows():



    startSimulator(df1)
    #print(resource_list)
    #print(wc_list)
