import random
import time


def emit_gel(step):
    p = 50
    sign = 1
    while True:
        valve_action = yield p
        if valve_action == "slow down":
            sign = -1
        elif valve_action == "speed up":
            sign = 1
        p += sign * random.randint(0, step)


def valve(pr):
    if pr > 90 or pr < 10:
        generator.close()
        pr = 0
    elif pr > 80:
        pr = generator.send("slow down")
    elif pr < 20:
        pr = generator.send("speed up")
    else:
        pr = next(generator)
    return pr


if __name__ == "__main__":
    generator = emit_gel(20)
    pressure = next(generator)
    while pressure != 0:
        print(pressure)
        pressure = valve(pressure)
        time.sleep(0.5)
