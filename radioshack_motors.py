import board
import time
import math

# MOTOR DRIVER
import pwmio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import motor

# DEFINE PWM CONTROL FOR MOTOR LEFT AND RIGHT. 
PWM_PIN_A = board.SDA
PWM_PIN_B = board.SCL
pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=1600)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=1600)

motor1 = motor.DCMotor(pwm_a, pwm_b)

PWM_PIN_2A = board.SCK
PWM_PIN_2B = board.MISO
pwm_2a = pwmio.PWMOut(PWM_PIN_2A, frequency=50)
pwm_2b = pwmio.PWMOut(PWM_PIN_2B, frequency=50)
motor2 = motor.DCMotor(pwm_2a, pwm_2b)
# motor_l = motor.DCMotor(pwm_a, pwm_b)

motor_l_ctl_a = DigitalInOut(board.TX)
motor_l_ctl_b = DigitalInOut(board.RX)
motor_l_ctl_a.direction = Direction.OUTPUT
motor_l_ctl_b.direction = Direction.OUTPUT
# 
motor2.throttle = 0.5
# motor_l_ctl_a.value = True
# motor_l_ctl_b.value = False
# motor_r_ctl_a.value = True
# motor_r_ctl_b.value = False
# 
time.sleep(2)
# 
motor2.throttle = -0.5
# motor_l_ctl_a.value = False
# motor_l_ctl_b.value = True
# motor_r_ctl_a.value = True
# motor_r_ctl_b.value = False
# 
time.sleep(2)
# 
motor2.throttle = 0.0
# motor_l_ctl_a.value = True
# motor_l_ctl_b.value = True
# motor_r_ctl_a.value = True
# motor_r_ctl_b.value = True


# while True:
# 	pass
# 	print("***DC motor test***")
# 
# 	print("\nForwards slow")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = False
# 	motor_l.throttle = 0.5
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nStop")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = 0
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nForwards")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = False
# 	motor_l.throttle = 1.0
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nStop")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = 0
# 	print("throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nBackwards")
# 	motor_l_ctl_a.value = False
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = -1.0
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nStop")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = 0
# 	print("throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nBackwards slow")
# 	motor_l_ctl_a.value = False
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = -0.5
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nStop")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = True
# 	motor_l.throttle = 0
# 	print("  throttle:", motor_l.throttle)
# 	time.sleep(1)
# 
# 	print("\nSpin freely")
# 	motor_l_ctl_a.value = True
# 	motor_l_ctl_b.value = False
# 	motor_l.throttle = None
# 	print("  throttle:", motor_l.throttle)
# 
# 	print("\n***Motor test is complete***")

