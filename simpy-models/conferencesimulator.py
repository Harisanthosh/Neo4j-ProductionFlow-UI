from random import randint
import simpy

# No of Gas meter units to be processed by each resource in the work center
WORK_UNITS = 10
# Average working time of each resource (5 Mins, rest time 1 Min)
WORKING_TIME = 300
TURN_OFF_TIME = 60
global totalUnitsProduced
totalUnitsProduced = 0

def resource(env, name, knowledge=0, wearntear=0):
    while True:
        # Parellely executing resources in workcenters
        global totalUnitsProduced
        for i in range(WORK_UNITS):
            knowledge += randint(0, 3) / (1 + wearntear)
            wearntear += randint(1, 4)
            totalUnitsProduced += 1
            yield env.timeout(WORKING_TIME)

        print(f'The machine {name} has processed {knowledge} units and has worn out {wearntear}')

        wearntear -= randint(1, 2)

        yield env.timeout(TURN_OFF_TIME)
        print(f'The machine {name} after resting has {knowledge} units and wear n tear at {wearntear}')


env = simpy.Environment()
# Creating 5 machines in the workcenter and executing them parellely for a hour
for i in range(5):
    env.process(resource(env,i+1))

# Running for 1 hour
env.run(until=3600)
print(f'The total units of gasmeters produced so far is {totalUnitsProduced}')



