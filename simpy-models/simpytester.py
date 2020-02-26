import simpy
import paho.mqtt.publish as publish

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
    publish.single("simpy/test", payload=f'Speaker {speaker} finishes his speech', hostname="localhost",port=1883)

def moderator(env):
    for i in range(3):
        val = yield env.process(speaker(env, i+1))
        print(val)

    #     publish.single('simpy/test', payload=None, qos=0, retain=False, hostname="localhost",
    # port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
    # protocol=mqtt.MQTTv311, transport="tcp")

env.process(moderator(env))
env.run()

# Asynchronous and conditional process
"""
def speaker(env, speaker):
    try:
        yield env.timeout(speaker)
        return f'Speaker {speaker} finishes his speech'
    except simpy.Interrupt as interrupt:
        print(interrupt.cause)

def moderator(env):
    for i in range(5):
        speaker_proc = env.process(speaker(env, i+1))
        results = yield speaker_proc | env.timeout(2)
        if speaker_proc not in results:
            speaker_proc.interrupt('No time left')
        else:
            print(results)

env.process(moderator(env))
env.run()
"""


