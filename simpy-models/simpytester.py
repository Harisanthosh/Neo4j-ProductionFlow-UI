import simpy

def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)

# Process as fast as possible, in this example two events are running in the interval of 1500 and 2000 ms till 5000 ms
env = simpy.Environment()

env.process(clock(env, 'fast', 1500))
env.process(clock(env, 'slow', 2000))
env.run(until=5000)
