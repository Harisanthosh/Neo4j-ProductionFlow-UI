import simpy
from datetime import datetime
import time
import pandas as pd
import random
import string
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as vis_factory

global cols_list
global resource_list
global wc_list
global ops_list
global processing_time
global waiting_time

#chars=string.ascii_uppercase + string.digits
def sfc_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def startSimulator(env,df2,tns):
    #Using iloc to access can also use iat or at to access elements as matrix
    sfc_sim = str(df2.iloc[0]['SFC'])[:6]
    sfc_act = int(sfc_sim)
    sfc_gen = int(sfc_generator())
    print(sfc_act)
    print(sfc_gen)
    merged_sfc = str(sfc_act) + str(sfc_gen)
    print(f'Starting simulation for the SFC {merged_sfc}')
    #print(f'Processed at the resources {resource_list}')
    df_construct = {}
    new_df = pd.DataFrame()
    #print(new_df)
    for index,row in df2.iterrows():
        #print(index, row['OPERATION'],row['PROCESSING_TIME_SECS'],row['WAITING_TIME_SECS'])
        if index+1 > tns:
            break
        row['SFC'] = merged_sfc
        row['case:concept:name'] = row['WORK_CENTER']
        row['concept:name'] = row['OPERATION']
        row['org:resource'] = row['RESRCE']
        #row['DATE_TIME'] = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
        row['DATE_TIME'] = f"{datetime.fromtimestamp(env.now):%d-%m-%Y %H:%M:%S}"
        row['time:timestamp'] = row['DATE_TIME']
        curr_row = pd.DataFrame([row])
        pt_time = int(row['PROCESSING_TIME_SECS'])
        print(pt_time)
        yield env.timeout(pt_time)
        new_df = new_df.append([curr_row],ignore_index=True)

    #print(new_df)
    # Implementation of Petrin nets representation will be added
    log = conversion_factory.apply(new_df)
    print(log)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    #gviz = vis_factory.apply(net, initial_marking, final_marking)
    #vis_factory.view(gviz)



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
    env = simpy.Environment(initial_time=time.time())
    total_no_of_steps = 70
    env.process(startSimulator(env,df1,total_no_of_steps))
    #startSimulator(df1,env)
    env.run()
    #print(resource_list)
    #print(wc_list)
