import simpy
from datetime import datetime
import pandas as pd

prom_formatter = {}
prom_formatter['caseId'] = []
prom_formatter['Timestamp'] = []
prom_formatter['Activity'] = []

env = simpy.RealtimeEnvironment()

def speaker(env, speaker):
    yield env.timeout(3)
    valx = f'Speaker {speaker} finishes his speech at {env.now} interval on time {datetime.now()}'
    prom_formatter['caseId'].append(speaker)
    prom_formatter['Timestamp'].append(datetime.now())
    prom_formatter['Activity'].append('Finishes Speech')
    dfs = pd.DataFrame(prom_formatter)
    print(dfs)
    dfs.to_csv('processmining_template.csv',encoding='utf-8-sig',sep=';',index=False)
    yield env.timeout(1)
    return valx

def moderator(env):
    for i in range(3):
        brd = f'Speaker {i+1} gets on to the stage at {env.now} interval on time {datetime.now()}'
        prom_formatter['caseId'].append(i+1)
        prom_formatter['Timestamp'].append(datetime.now())
        prom_formatter['Activity'].append('Starts Speech')
        print(brd)
        val = yield env.process(speaker(env, i+1))

        print(val)

env.process(moderator(env))
env.run()


