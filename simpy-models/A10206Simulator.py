import simpy
from datetime import datetime
import time
import pandas as pd
import sys
import random
import string

global cols_list
global resource_list
global wc_list
global processing_time
global waiting_time

#chars=string.ascii_uppercase + string.digits
def sfc_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def startSimulator(df2):
    print(df2.head())
    #Using iloc to access can also use iat or at to access elements as matrix
    sfc_sim = str(df2.iloc[0]['SFC'])[:6]
    sfc_act = int(sfc_sim)
    sfc_gen = int(sfc_generator())
    print(sfc_act)
    print(sfc_gen)
    merged_sfc = str(sfc_act) + str(sfc_gen)
    print(merged_sfc)



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
