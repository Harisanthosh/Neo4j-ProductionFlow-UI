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
global ops_list
global processing_time
global waiting_time

#chars=string.ascii_uppercase + string.digits
def sfc_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def startSimulator(df2):
    #Using iloc to access can also use iat or at to access elements as matrix
    sfc_sim = str(df2.iloc[0]['SFC'])[:6]
    sfc_act = int(sfc_sim)
    sfc_gen = int(sfc_generator())
    print(sfc_act)
    print(sfc_gen)
    merged_sfc = str(sfc_act) + str(sfc_gen)
    print(f'Starting simulation for the SFC {merged_sfc}')
    df_construct = {}
    new_df = pd.DataFrame(columns=cols_list)
    #print(new_df)
    for index,row in df2.iterrows():
        #print(index, row['OPERATION'],row['PROCESSING_TIME_SECS'],row['WAITING_TIME_SECS'])
        row['SFC'] = merged_sfc
        curr_row = pd.DataFrame([row],columns=cols_list)
        # print(curr_row)
        new_df = new_df.append([curr_row],ignore_index=True)
    print(new_df.head())



if __name__ == "__main__":
    # cols_list = []
    df1 = pd.read_csv('sapme_sfcflow.csv',sep=';')
    #print(df1.head())
    global cols_list
    global resource_list
    global wc_list
    global processing_time
    global waiting_time
    global ops_list
    cols_list = df1.columns
    resource_list = df1['RESRCE']
    wc_list = df1['WORK_CENTER']
    processing_time = df1['PROCESSING_TIME_SECS']
    waiting_time = df1['WAITING_TIME_SECS']
    ops_list = df1['OPERATION']
    print(cols_list)
    print(len(cols_list))
    #for key,val in df1.iterrows():

    startSimulator(df1)
    #print(resource_list)
    #print(wc_list)
