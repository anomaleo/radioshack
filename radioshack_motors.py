# MOTOR DRIVER
import board
import time
import pwmio
from adafruit_motor import motor

PWM_PIN_A = board.SCK
PWM_PIN_B = board.MISO
pwm_a = pwmio.PWMOut(PWM_PIN_A, frequency=1600)
pwm_b = pwmio.PWMOut(PWM_PIN_B, frequency=1600)
# motor_left = motor.DCMotor(pwm_a, pwm_b)

PWM_PIN_2A = board.TX
PWM_PIN_2B = board.RX
pwm_2a = pwmio.PWMOut(PWM_PIN_2A, frequency=1600)
pwm_2b = pwmio.PWMOut(PWM_PIN_2B, frequency=1600)
# motor_right = motor.DCMotor(pwm_2a, pwm_2b)

motors = [motor.DCMotor(pwm_a, pwm_b), motor.DCMotor(pwm_2a, pwm_2b)]

def forward(motors, adv):
	print("\nForwards")
	motors[0].throttle = adv
	motors[1].throttle = adv
	time.sleep(0.001)
	print("  throttle:", motors[0].throttle)
	time.sleep(1)
	
def stop(motors, adv):
	print("\nStop")
	motors[0].throttle = adv
	motors[1].throttle = adv
	time.sleep(0.001)
	print("  throttle:", motors[0].throttle)
	time.sleep(1)
	
def backward(motors, adv):
	print("\nBackwards")
	motors[0].throttle = -adv
	motors[1].throttle = -adv
	time.sleep(0.001)
	print("  throttle:", motors[0].throttle)
	time.sleep(1)
	
def right(motors, adv):
	print("\Right")
	motors[0].throttle = adv
	motors[1].throttle = -adv
	time.sleep(0.001)
	print("  throttle:", motors[0].throttle)
	time.sleep(1)
	
def left(motors, adv):
	print("\Left")
	motors[0].throttle = -adv
	motors[1].throttle = adv
	time.sleep(0.001)
	time.sleep(1)


# while True: 
# 	forward(motors, 0.5)
# 	time.sleep(1)
# 
# 	stop(motors, 0.0)
# 	time.sleep(1)
# 	
# 	backward(motors, -0.5)
# 	time.sleep(1)
# 
# 	stop(motors, 0.0)
# 	time.sleep(1)
# 	
# 	left(motors, 0.5)
# 	time.sleep(1)
# 	
# 	stop(motors, 0.0)
# 	time.sleep(1)
# 	
# 	right(motors, 0.5)
# 	time.sleep(1)
# 	
# 	stop(motors, 0.0)
# 	time.sleep(1)