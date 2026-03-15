# MOTOR DRIVER
import board
import pwmio
import time
from adafruit_motor import motor

PWM_PIN_A = board.SCK
PWM_PIN_B = board.MISO
pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=1600)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=1600)
motor1 = motor.DCMotor(pwm_a, pwm_b)

PWM_PIN_2A = board.TX
PWM_PIN_2B = board.RX
pwm_2a = pwmio.PWMOut(PWM_PIN_2A, frequency=1600)
pwm_2b = pwmio.PWMOut(PWM_PIN_2B, frequency=1600)
motor2 = motor.DCMotor(pwm_2a, pwm_2b)


while True: 
	print("\nForwards slow")
	motor1.throttle = 0.5
	motor2.throttle = 0.5
	print("  throttle:", motor1.throttle)
	time.sleep(1)

	print("\nStop")
	motor1.throttle = 0
	motor2.throttle = 0
	print("  throttle:", motor1.throttle)
	time.sleep(1)
	
	print("\nForwards slow")
	motor1.throttle = -0.5
	motor2.throttle = -0.5
	print("  throttle:", motor1.throttle)
	time.sleep(1)

	print("\nStop")
	motor1.throttle = 0
	motor2.throttle = 0
	print("  throttle:", motor1.throttle)
	time.sleep(1)