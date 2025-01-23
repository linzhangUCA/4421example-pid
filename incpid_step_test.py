from wheel_driver import WheelDriver
from time import sleep

# SETUP
# Instantiate wheel
w = WheelDriver((2, 3, 4), (20, 21))
# Constants
K_P = 8000
K_I = 100
K_D = 0
# Variables
dutycycle = 0.
err = 0.
err_sum = 0.
err_diff = 0.
prev_err = 0.
target_vel = 0.  # reference linear velocity
data = []

# LOOP
# 20Hz controller, 5 seconds
for i in range(100):
    if i==20:
        target_vel = 0.8
    actual_vel = w.lin_vel
#     print(actual_vel)
    err = target_vel - actual_vel
    err_sum += err
    err_diff = err - prev_err
    prev_err = err
#     print(err)
    delta_dc = K_P * err + K_I * err_sum + K_D * err_diff  # control signal
    dutycycle += delta_dc
#     print(dutycycle)
    if dutycycle > 0:
        if dutycycle > 65025:
            dutycycle = 65025
        w.forward(int(dutycycle))
    elif dutycycle < 0:
        if dutycycle < -65025:
            dutycycle = -65025
        w.backward(int(-dutycycle))
    else:
        w.stop()
    print("real velocity:", actual_vel, "target velocity:", target_vel)
    sleep(0.05)
    data.append((target_vel, actual_vel, err))

w.stop()
# with open(f'idata{target_vel}.csv', 'w') as file:
#     for item in data:
#         file.write(f'{item[0]},{item[1]},{item[2]}\n')
