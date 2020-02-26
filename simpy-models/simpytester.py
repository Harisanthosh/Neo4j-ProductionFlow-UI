import simpy

def clock(env, name, tick):
    while True:
        print(name, env.now)
        yield env.timeout(tick)

# Process as fast as possible, in this example two events are running in the interval of 1 and 2 s till 5 seconds
env = simpy.RealtimeEnvironment()
# env.process(clock(env, 'fast', 1))
# env.process(clock(env, 'slow', 2))
# env.run(until=5)

# Creating processes from events, here three speakers take turn and speak infront of an audience
def speaker(env, speaker):
    yield env.timeout(3)
    return f'Speaker {speaker} finishes his speech'

def moderator(env):
    for i in range(3):
        val = yield env.process(speaker(env, i+1))
        print(val)

env.process(moderator(env))
env.run()




