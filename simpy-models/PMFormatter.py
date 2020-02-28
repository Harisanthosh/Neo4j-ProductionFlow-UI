import simpy
from datetime import datetime
import time
import pandas as pd
import sys

prom_formatter = {}
prom_formatter['caseId'] = []
prom_formatter['Timestamp'] = []
prom_formatter['Activity'] = []

# env = simpy.RealtimeEnvironment()

def speaker(env, speaker):
    yield env.timeout(int(sys.argv[2]))
    valx = f'Speaker {speaker} finishes his speech at {env.now}'
    prom_formatter['caseId'].append(speaker)
    prom_formatter['Timestamp'].append(datetime.fromtimestamp(env.now))
    prom_formatter['Activity'].append('Finishes Speech')
    dfs = pd.DataFrame(prom_formatter)
    print(dfs)
    dfs.to_csv('processmining_template.csv',encoding='utf-8-sig',sep=';',index=False)
    yield env.timeout(1)
    return valx

def moderator(env):
    for i in range(3):
        brd = f'Speaker {i+1} gets on to the stage at {env.now}'
        prom_formatter['caseId'].append(i+1)
        prom_formatter['Timestamp'].append(datetime.fromtimestamp(env.now))
        prom_formatter['Activity'].append('Starts Speech')
        print(brd)
        val = yield env.process(speaker(env, i+1))

        print(val)

def invoker_api(time1,time2):
    env = simpy.Environment(initial_time=time.time())
    sys.argv[1] = time1
    sys.argv[2] = time2
    env.process(moderator(env))
    print(f'the time taken for each speaker is {sys.argv[1]} at an interval {sys.argv[2]}')
    env.run()

if __name__ == "__main__":
    env = simpy.RealtimeEnvironment(initial_time=time.time())
    env.process(moderator(env))
    print(f'the time taken for each speaker is {sys.argv[1]} at an interval {sys.argv[2]}')
    env.run()



