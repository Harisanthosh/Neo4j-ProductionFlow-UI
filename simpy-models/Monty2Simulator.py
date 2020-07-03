import simpy
from datetime import datetime, timedelta
from dateutil import parser
import time
import pandas as pd
import random
import string
import sys
#import multiprocessing
from random import randint
import os
import json
#from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as vis_factory
import configparser
config = configparser.ConfigParser()
config.read("C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/setup.ini")

model_file_path = config['MODEL_SETTINGS']['model_file_path']
simpy_path = config['MODEL_SETTINGS']['simpy_path']

early_shift_time = config['SHIFT_TIME']['Early']
late_shift_time = config['SHIFT_TIME']['Late']
night_shift_time = config['SHIFT_TIME']['Night']


global cols_list
global resource_list
global wc_list
global ops_list
global op_choice
global processing_time
global waiting_time
global ventil_type
global iter_sfcs
global start_time
global per_choice
global oper_bk_count



#chars=string.ascii_uppercase + string.digits
def sfc_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def shift_estimator(orig_date,date_var,shifts_arr):
    #print(shifts_arr)
    diff_in_secs = date_var.timestamp() - orig_date.timestamp()
    print(diff_in_secs)
    dates_ms = []

    # date_stamp_shifts = shifts_arr.split(" ")[0]
    # time_stamp_shifts = shifts_arr.split(" ")[1]
    #t1 = datetime.strptime(shifts_arr, "%d/%m/%Y %H:%M:%S")
    pred_shift = ""
    if(date_var.hour > 6 and date_var.hour <= 14):
        pred_shift = "Early"
    elif(date_var.hour > 14 and date_var.hour <= 22):
        pred_shift = "Late"
    else:
        pred_shift = "Night"

    shift_flag = ""
    print(f"The predicted shift is at {pred_shift}")
    for key, value in shifts_arr.items():
        for item1 in value:
            print(item1['day'], '->', item1['shift'])
            date_shift = item1['day'].split(",")[1].strip()
            time_shift = early_shift_time if item1['shift'] == "Early" else late_shift_time if item1['shift'] == "Late" else night_shift_time
            full_time_shift = date_shift + " " + time_shift
            t3 = parser.parse(full_time_shift)
            print(t3)
            #Check if the date and shift is selected by the user
            if(pred_shift == item1['shift']):
                if(t3.day == date_var.day and pred_shift !="Night"):
                    shift_flag = "Yes"
                elif(t3.day == (date_var.day - 1) and pred_shift=="Night"):
                    print(f"The shift day is {t3.day} and the next day is {(date_var.day - 1)}")
                    shift_flag = "Yes"
                else:
                    continue

            #t3 = datetime.strptime(full_time_shift, "%d %B %Y %H:%M:%S")
            if(t3.timestamp() >= date_var.timestamp()):
                dates_ms.append(t3.timestamp())
            #dates_ms.append(t3.timestamp())

    #dates_ms.sort(reverse=True)
    dates_ms.sort()
    print(dates_ms)
    if(shift_flag == "Yes"):
        print(f"Predicted shift is Selected with {shift_flag}")
        return date_var.strftime('%d/%m/%Y %H:%M:%S %p')
    else:
        print(f"Shift is not selected")
        pars_date = datetime.fromtimestamp(dates_ms[0]) + timedelta(seconds=int(diff_in_secs)) if len(dates_ms) > 0 else date_var
        return pars_date.strftime('%d/%m/%Y %H:%M:%S %p')

    #return pred_shift


def create_waiting_time_simulator(config_sim):
    #print(config_sim)
    #sim_config = json.load(config_sim)
    print(f"Simulator {config_sim['name']} will be configured as per the settings chosen")
    has_ventil = config_sim['ventiltype']
    if has_ventil == "no":
        df1 = pd.read_csv('new_monty2_sfcflow_noventil.csv',sep=';')
    else:
        df1 = pd.read_csv('new_monty2_sfcflow.csv',sep=';')
    print(df1.head())
    new_df = pd.DataFrame()
    for index,row in df1.iterrows():
        current_operation = row['OPERATION_DESCRIPTION']
        if(current_operation == 'Stutzen befetten'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['stutzen_befetten_waiting_time']) * 1000
        elif(current_operation == 'Aussenmagnet montieren'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['aussenmagnet_montieren_waiting_time']) * 1000
        elif(current_operation == 'Messwerk einsetzen'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['messwerk_einsetzen_waiting_time']) * 1000
        elif(current_operation == 'Oberteil dosieren'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['oberteil_dosieren_waiting_time']) * 1000
        elif(current_operation == 'Unterteil aufsetzen'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['unterteil_aufsetzen_waiting_time']) * 1000
        elif(current_operation == 'Falz auflegen'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['falz_auflegen_waiting_time']) * 1000
        elif(current_operation == 'Zähler vorbördeln'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['zähler_vorbördeln_waiting_time']) * 1000
        elif(current_operation == 'Zähler fertigbördeln'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['zähler_fertigbördeln_waiting_time']) * 1000
        elif(current_operation == 'Zähler dichtheitsprüfen'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['zähler_dichtheitsprüfen_waiting_time']) * 1000
        elif(current_operation == 'Zähler abstapeln'):
            row['ELAPSED_QUEUE_TIME'] = int(config_sim['zähler_abstapeln_waiting_time']) * 1000
        else:
            continue
        curr_row = pd.DataFrame([row])
        new_df = new_df.append([curr_row],ignore_index=True)

    if has_ventil == "no":
        new_df.to_csv('new_monty2_sfcflow_noventil.csv', header='column_names')
    else:
        new_df.to_csv('new_monty2_sfcflow.csv', header='column_names')

def create_simulator(config_sim):
    #print(config_sim)
    #sim_config = json.load(config_sim)
    print(f"Simulator {config_sim['name']} will be configured as per the settings chosen")
    has_ventil = config_sim['ventiltype']
    if has_ventil == "no":
        df1 = pd.read_csv('monty2_sfcflow_noventil.csv',sep=';')
    else:
        df1 = pd.read_csv('monty2_sfcflow.csv',sep=';')
    print(df1.head())
    new_df = pd.DataFrame()
    for index,row in df1.iterrows():
        current_operation = row['OPERATION_DESCRIPTION']
        if(current_operation == 'Stutzen befetten'):
            row['ELAPSED_TIME'] = int(config_sim['stutzen_befetten_time']) * 1000
        elif(current_operation == 'Aussenmagnet montieren'):
            row['ELAPSED_TIME'] = int(config_sim['aussenmagnet_montieren_time']) * 1000
        elif(current_operation == 'Messwerk einsetzen'):
            row['ELAPSED_TIME'] = int(config_sim['messwerk_einsetzen_time']) * 1000
        elif(current_operation == 'Oberteil dosieren'):
            row['ELAPSED_TIME'] = int(config_sim['oberteil_dosieren_time']) * 1000
        elif(current_operation == 'Unterteil aufsetzen'):
            row['ELAPSED_TIME'] = int(config_sim['unterteil_aufsetzen_time']) * 1000
        elif(current_operation == 'Falz auflegen'):
            row['ELAPSED_TIME'] = int(config_sim['falz_auflegen_time']) * 1000
        elif(current_operation == 'Zähler vorbördeln'):
            row['ELAPSED_TIME'] = int(config_sim['zähler_vorbördeln_time']) * 1000
        elif(current_operation == 'Zähler fertigbördeln'):
            row['ELAPSED_TIME'] = int(config_sim['zähler_fertigbördeln_time']) * 1000
        elif(current_operation == 'Zähler dichtheitsprüfen'):
            row['ELAPSED_TIME'] = int(config_sim['zähler_dichtheitsprüfen_time']) * 1000
        elif(current_operation == 'Zähler abstapeln'):
            row['ELAPSED_TIME'] = int(config_sim['zähler_abstapeln_time']) * 1000
        else:
            continue
        curr_row = pd.DataFrame([row])
        new_df = new_df.append([curr_row],ignore_index=True)

    if has_ventil == "no":
        new_df.to_csv('new_monty2_sfcflow_noventil.csv', header='column_names')
    else:
        new_df.to_csv('new_monty2_sfcflow.csv', header='column_names')


#Allow invocation from APIs
def api_invoker(has_ventil,number_sfcs,vari_choice,oper_choice=None,bw_sfc_choice=None,nc_cases=None):
    global ventil_type
    global iter_sfcs
    global oper_bk_count
    global op_choice
    global last_date_ts
    ventil_type = has_ventil
    print(os.getcwd())
    os.chdir(simpy_path)
    #sys.path.insert(1, 'C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models/')
    if has_ventil == "no":
        df1 = pd.read_csv('monty2_sfcflow_noventil.csv',sep=';')
    elif has_ventil == "undefined":
        df1 = pd.read_csv('monty2_sfcflow_noventil.csv',sep=';')
    else:
        df1 = pd.read_csv('monty2_sfcflow.csv',sep=';')
    iter_sfcs = int(number_sfcs) if (nc_cases == None) else int(number_sfcs) + int(nc_cases)
    #print(iter_sfcs)
    oper_bk_count = randint(0,iter_sfcs) if (bw_sfc_choice == None) else int(bw_sfc_choice)
    oper_bk_count = oper_bk_count if (nc_cases == None) else oper_bk_count + int(nc_cases)
    print("Breakdown will occur at")
    print(oper_bk_count)
    global cols_list
    global resource_list
    global wc_list
    global processing_time
    global waiting_time
    global ops_list
    global start_time
    global var_choice
    global per_choice
    global nc_count
    nc_count = int(nc_cases) if (nc_cases != None) else 0
    cols_list = df1.columns
    resource_list = df1['RESRCE']
    wc_list = df1['WORK_CENTER']
    processing_time = df1['PROCESSING_TIME_SECS']
    waiting_time = df1['WAITING_TIME_SECS']
    ops_list = df1['OPERATION']
    print('Total number of Simulation runs including NonConformance is')
    print(iter_sfcs)
    #print(ops_list)
    # op_choice = input('Enter the operation id of choice to simulate bottleneck \n')
    # print(op_choice)
    # var_choice = int(input('Enter the variation of time in % \n'))
    # print(var_choice)
    op_choice = oper_choice
    var_choice = int(vari_choice)
    per_choice = 100 - random.randint(10,99)
    #for key,val in df1.iterrows():
    total_no_of_steps = 70
    start_time = time.time()
    for xt in range(iter_sfcs):
        if (xt==0):
            start_time = start_time + (xt*60)
            env = simpy.Environment(initial_time=start_time)
            env.process(startSimulator(env,df1,xt))
            env.run()
        else:
            ts_comp = time.mktime(datetime.strptime(last_date_ts, "%d-%m-%Y %H:%M:%S").timetuple())
            start_time = ts_comp - (random.randint(2,4)*60)
            # start_time = start_time + (xt*60)
            # if (ts_comp - start_time > 2400): #2400
            #     start_time = ts_comp + (random.randint(1,xt)*60)
            # elif (ts_comp - start_time < -300):
            #     start_time = ts_comp + (random.randint(1,3)*60)
            # else:
            #     start_time = start_time
            env = simpy.Environment(initial_time=start_time)
            env.process(startSimulator(env,df1,xt))
            env.run()

    return last_date_ts

#Parallel function
def sfc_simulator(env,df2,merged_sfc,tns):
    new_df = pd.DataFrame()
    #Using iloc to access can also use iat or at to access elements as matrix
    global last_date_ts
    global nc_count

    for index,row in df2.iterrows():
        #print("Index and length")
        row['SFC'] = merged_sfc
        row['case:concept:name'] = row['WORK_CENTER']
        row['concept:name'] = row['OPERATION'] + row['OPERATION_DESCRIPTION']
        row['org:resource'] = row['RESRCE']
        #row['DATE_TIME'] = f"{datetime.now():%d-%m-%Y %H:%M:%S}"
        row['DATE_TIME'] = f"{datetime.fromtimestamp(env.now):%d-%m-%Y %H:%M:%S}"
        row['time:timestamp'] = row['DATE_TIME']
        last_date_ts = row['DATE_TIME']
        et_val = row['ELAPSED_TIME']
        eqt_val = row['ELAPSED_QUEUE_TIME']
        et_lower_bound = int(et_val - (et_val / per_choice))
        et_upper_bound = int(et_val + (et_val / per_choice))
        eqt_lower_bound = int(eqt_val - (eqt_val / per_choice))
        eqt_upper_bound = int(eqt_val + (eqt_val / per_choice))
        row['ELAPSED_TIME'] = randint(et_lower_bound,et_upper_bound)
        if ((tns == (oper_bk_count-1)) and (row['OPERATION']==op_choice)):
            #row['ELAPSED_QUEUE_TIME'] = randint(eqt_lower_bound,eqt_upper_bound) * 2 * per_choice
            row['ELAPSED_QUEUE_TIME'] = randint(eqt_lower_bound,eqt_upper_bound) + var_choice
        else:
            row['ELAPSED_QUEUE_TIME'] = randint(eqt_lower_bound,eqt_upper_bound)
        # Create NC at last before operation where NC will impact the more 'i.e operation Dichtheitsprüfen'
        if (nc_count > 0 and index == len(df2)-1):
            row['QTY_NON_CONFORMED'] = 1
            row['QTY_DONE'] = 0
            nc_count -= 1
            #break

        #row['ELAPSED_QUEUE_TIME'] = randint(eqt_lower_bound,eqt_upper_bound)
        row['PROCESSING_TIME_SECS'] = row['ELAPSED_TIME'] / 1000
        row['WAITING_TIME_SECS'] = row['ELAPSED_QUEUE_TIME'] / 1000
        curr_row = pd.DataFrame([row])
        pt_time = int(row['PROCESSING_TIME_SECS'])
        wt_time = int(row['WAITING_TIME_SECS'])
        tot_time = pt_time + wt_time
        #print(tot_time)
        yield env.timeout(tot_time)
        new_df = new_df.append([curr_row],ignore_index=True)

    return new_df

def startSimulator(env,df2,tns):
    #print(f'Processed at the resources {resource_list}')
    df_construct = {}
    #print(new_df)
    # pool = multiprocessing.Pool(iter_sfcs)
    # out1, out2, out3 = zip(*pool.map(calc_stuff, range(0, 10 * offset, offset)))
    sfc_sim = str(df2.iloc[0]['SFC'])[:3]
    sfc_act = int(sfc_sim)
    sfc_gen = int(sfc_generator())
    merged_sfc = str(sfc_act) + str(sfc_gen)
    print(f'Starting simulation for the SFC {merged_sfc}')
    res_df = yield env.process(sfc_simulator(env,df2,merged_sfc,tns))
    # Implementation of Petri nets representation will be added
    if ventil_type == "no":
        # if file does not exist write header
        if not os.path.isfile('simulated_monty2_sfcflow_noventil.csv'):
           res_df.to_csv('simulated_monty2_sfcflow_noventil.csv', header='column_names')
        else: # else it exists so append without writing the header
           res_df.to_csv('simulated_monty2_sfcflow_noventil.csv', mode='a', header=False)
        #res_df.to_csv('simulated_monty2_sfcflow_noventil.csv',mode='a')
    else:
        if not os.path.isfile('simulated_monty2_sfcflow.csv'):
           res_df.to_csv('simulated_monty2_sfcflow.csv', header='column_names')
        else: # else it exists so append without writing the header
           res_df.to_csv('simulated_monty2_sfcflow.csv', mode='a', header=False)
        #res_df.to_csv('simulated_monty2_sfcflow.csv',mode='a')

    # log = conversion_factory.apply(res_df)
    # print(log)
    # net, initial_marking, final_marking = alpha_miner.apply(log)
    # gviz = vis_factory.apply(net, initial_marking, final_marking)
    # vis_factory.view(gviz)



if __name__ == "__main__":
    """
    Monty2 Line Simulator which produces Whitemeter, used to mimic the behavior of SAP ME and produces the production log
    [Note]: Enter whether to include the flow with Ventil or not and the amount of SFCS to produce as the parameters
    """
    # cols_list = []
    global ventil_type
    global iter_sfcs
    global oper_bk_count
    global op_choice
    ventil_type = sys.argv[1]
    #print(sys.argv)
    if ventil_type == "no":
        df1 = pd.read_csv('monty2_sfcflow_noventil.csv',sep=';')
    else:
        df1 = pd.read_csv('monty2_sfcflow.csv',sep=';')
    iter_sfcs = int(sys.argv[2])
    oper_bk_count = randint(0,iter_sfcs)
    print(oper_bk_count)
    #print(iter_sfcs)
    global cols_list
    global resource_list
    global wc_list
    global processing_time
    global waiting_time
    global ops_list
    global start_time
    global per_choice
    cols_list = df1.columns
    resource_list = df1['RESRCE']
    wc_list = df1['WORK_CENTER']
    processing_time = df1['PROCESSING_TIME_SECS']
    waiting_time = df1['WAITING_TIME_SECS']
    ops_list = df1['OPERATION']
    #print(cols_list)
    print(ops_list)
    op_choice = input('Enter the operation of choice to simulate bottleneck \n')
    print(op_choice)
    var_choice = int(input('Enter the variation of time in % \n'))
    print(var_choice)
    per_choice = 100 - var_choice
    #for key,val in df1.iterrows():
    total_no_of_steps = 70
    start_time = time.time()
    for xt in range(iter_sfcs):
        start_time = start_time + (xt*60)
        env = simpy.Environment(initial_time=start_time)
        env.process(startSimulator(env,df1,xt))
        env.run()

    #startSimulator(df1,env)
