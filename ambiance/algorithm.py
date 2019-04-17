from math import sin, pi
from ambiance import hue
import datetime
import asyncio
from color_temp import rgb_to_temperature

start_time = 480  # Wakeup Time
end_time = 1320  # Sleep Time
min_temp = 500
max_temp = 163

step_amount = 256

last_measurement = None


def bound(value, low=0, high=255):
    return max(low, min(high, value))


async def ideal_temp(time):
    def r(t):
        return 1 if start_time <= t <= end_time else 0

    return (r(time) * (max_temp - min_temp) * sin(pi * (time - start_time) / (end_time - start_time))) + min_temp


async def record_change(data):
    global last_measurement
    last_measurement = data
    await correct(data)


async def correct(data):
    rgb = [data['rgb']['red'] / 256.0, data['rgb']['green'] / 256.0, data['rgb']['blue'] / 256.0]
    current_k = rgb_to_temperature(rgb)
    dt = datetime.datetime.now()
    time = (dt.hour * 60) + dt.minute
    ideal = await ideal_temp(time)
    # ideal = 200  # Set to constant for testing

    current_m = int(1000000 / current_k)
    print("%d,%d" % (current_m, ideal))

    try:
        if current_m > (ideal + step_amount) or current_m < (ideal - step_amount):
            inc = step_amount if current_m < (ideal - step_amount) else -step_amount
            await hue.increment_light(1, inc)
    except TypeError:
        pass


async def demo():
    for t in range(480, 1320, 10):
        ideal = int(await ideal_temp(t))
        print("T: " + str(ideal))
        await hue.set_light_ct(3, ideal)
        await asyncio.sleep(0.125)
