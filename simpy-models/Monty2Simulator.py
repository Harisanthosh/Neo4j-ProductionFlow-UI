import simpy
from datetime import datetime
import time
import pandas as pd
import random
import string
import sys
import multiprocessing
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
global ventil_type
global iter_sfcs
global start_time

#chars=string.ascii_uppercase + string.digits
def sfc_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Parallel function
def sfc_simulator(env,df2):
    new_df = pd.DataFrame()
    tgl = 0
    for xt in range(iter_sfcs):
        #Using iloc to access can also use iat or at to access elements as matrix
        sfc_sim = str(df2.iloc[0]['SFC'])[:3]
        sfc_act = int(sfc_sim)
        sfc_gen = int(sfc_generator())
        print(sfc_act)
        print(sfc_gen)
        merged_sfc = str(sfc_act) + str(sfc_gen)
        print(f'Starting simulation for the SFC {merged_sfc}')
        for index,row in df2.iterrows():
            #print(index, row['OPERATION'],row['PROCESSING_TIME_SECS'],row['WAITING_TIME_SECS'])
            # if index+1 > tns:
            #     break

            row['SFC'] = merged_sfc
            row['case:concept:name'] = row['WORK_CENTER']
            row['concept:name'] = row['OPERATION'] + row['OPERATION_DESCRIPTION']
            row['org:resource'] = row['RESRCE']
            #row['DATE_TIME'] = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
            row['DATE_TIME'] = f"{datetime.fromtimestamp(env.now):%d-%m-%Y %H:%M:%S}"
            row['time:timestamp'] = row['DATE_TIME']
            curr_row = pd.DataFrame([row])
            pt_time = int(row['PROCESSING_TIME_SECS'])
            wt_time = int(row['WAITING_TIME_SECS'])
            tot_time = pt_time + wt_time
            print(tot_time)
            yield env.timeout(tot_time)
            new_df = new_df.append([curr_row],ignore_index=True)

    return new_df

def startSimulator(env,df2,tns):
    #print(f'Processed at the resources {resource_list}')
    df_construct = {}
    #print(new_df)
    # pool = multiprocessing.Pool(iter_sfcs)
    # out1, out2, out3 = zip(*pool.map(calc_stuff, range(0, 10 * offset, offset)))
    res_df = yield env.process(sfc_simulator(env,df2))
    # Implementation of Petrin nets representation will be added
    if ventil_type == "no":
         res_df.to_csv('simulated_monty2_sfcflow_noventil.csv')
    else:
        res_df.to_csv('simulated_monty2_sfcflow.csv')

    log = conversion_factory.apply(res_df)
    print(log)
    net, initial_marking, final_marking = alpha_miner.apply(log)
    gviz = vis_factory.apply(net, initial_marking, final_marking)
    vis_factory.view(gviz)



if __name__ == "__main__":
    # cols_list = []
    global ventil_type
    global iter_sfcs
    ventil_type = sys.argv[1]
    print(sys.argv)
    if ventil_type == "no":
        df1 = pd.read_csv('monty2_sfcflow_noventil.csv',sep=';')
    else:
        df1 = pd.read_csv('monty2_sfcflow.csv',sep=';')
    iter_sfcs = int(sys.argv[2])
    print(iter_sfcs)
    #print(df1.head())
    global cols_list
    global resource_list
    global wc_list
    global processing_time
    global waiting_time
    global ops_list
    global start_time
    cols_list = df1.columns
    resource_list = df1['RESRCE']
    wc_list = df1['WORK_CENTER']
    processing_time = df1['PROCESSING_TIME_SECS']
    waiting_time = df1['WAITING_TIME_SECS']
    ops_list = df1['OPERATION']
    print(cols_list)
    print(len(cols_list))
    #for key,val in df1.iterrows():
    start_time = time.time()
    env = simpy.Environment(initial_time=start_time)
    total_no_of_steps = 70
    env.process(startSimulator(env,df1,total_no_of_steps))
    #startSimulator(df1,env)
    env.run()
    #print(resource_list)
    #print(wc_list)
