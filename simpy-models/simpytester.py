import simpy

def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)

# Process as fast as possible, in this example two events are running in the interval of 1 and 2 s till 5 seconds
env = simpy.RealtimeEnvironment()

env.process(clock(env, 'fast', 1))
env.process(clock(env, 'slow', 2))
env.run(until=5)
