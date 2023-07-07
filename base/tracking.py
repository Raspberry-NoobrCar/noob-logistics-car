import RPi.GPIO as GPIO
import time

# Car motor pin definitions
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

# Car key definition
key = 8

# Track infrared pin definitions
TrackSensorLeftPin1 = 3  # Define leftmost track infrared sensor pin as GPIO 3
TrackSensorLeftPin2 = 5  # Define second left track infrared sensor pin as GPIO 5
TrackSensorRightPin1 = 4  # Define rightmost track infrared sensor pin as GPIO 4
TrackSensorRightPin2 = 18  # Define second right track infrared sensor pin as GPIO 18

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Ignore warning messages
GPIO.setwarnings(False)

# Initialize motor pins as output and key pin as input
def init():
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(key, GPIO.IN)
    GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
    GPIO.setup(TrackSensorRightPin1, GPIO.IN)
    GPIO.setup(TrackSensorRightPin2, GPIO.IN)
    # Set PWM pins and frequency to 2000Hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)

# Move the car forward
def run(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Move the car backward
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Turn the car left
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Turn the car right
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Spin the car left in place
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Spin the car right in place
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

# Stop the car
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Key press detection
def key_scan():
    while GPIO.input(key):
        pass
    while not GPIO.input(key):
        time.sleep(0.01)
        if not GPIO.input(key):
            time.sleep(0.01)
        while not GPIO.input(key):
            pass

# 2-second delay
time.sleep(2)

# try/except statement to catch errors
try:
    init()
#     key_scan()
    
    while True:
        # Track infrared sensor values
        TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
        TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)

        
        print("TrackSensorLeftValue1:", TrackSensorLeftValue1, end=" ")
        print("TrackSensorLeftValue2:", TrackSensorLeftValue2, end=" ")
        print("TrackSensorRightValue1:", TrackSensorRightValue1, end=" ")
        print("TrackSensorRightValue2:", TrackSensorRightValue2)

        
        # Handle sharp right and right angle turns
        if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
            spin_right(35, 30)
            time.sleep(0.1)

        # Handle sharp left and left angle turns
        elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
            spin_left(15, 15)
            time.sleep(0.1)

        # Handle leftmost detection
        elif TrackSensorLeftValue1 == False:
            spin_left(15, 15)

        # Handle rightmost detection
        elif TrackSensorRightValue2 == False:
            spin_right(15, 15)

        # Handle left curve
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
            left(0, 15)

        # Handle right curve
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
            right(15, 0)

        # Handle straight line
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
            run(15, 15)

        # When all sensors detect, maintain the previous state

except KeyboardInterrupt:
    pass

pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()
