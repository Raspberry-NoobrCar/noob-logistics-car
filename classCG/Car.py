import RPi.GPIO as GPIO
import time

class Car:

    def __init__(self):
        # Car motor pin definitions
        self.IN1 = 20
        self.IN2 = 21
        self.IN3 = 19
        self.IN4 = 26
        self.ENA = 16
        self.ENB = 13
        # 超声波引脚定义
        self.EchoPin = 0
        self.TrigPin = 1
        # Track infrared pin definitions
        self.TrackSensorLeftPin1 = 3  # Define leftmost track infrared sensor pin as GPIO 3
        self.TrackSensorLeftPin2 = 5  # Define second left track infrared sensor pin as GPIO 5
        self.TrackSensorRightPin1 = 4  # Define rightmost track infrared sensor pin as GPIO 4
        self.TrackSensorRightPin2 = 18  # Define second right track infrared sensor pin as GPIO 18

        # Car key definition
        self.key = 8

        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)
        # Ignore warning messages
        GPIO.setwarnings(False)
    
    def initCarSetup(self):
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.key, GPIO.IN)
        GPIO.setup(self.EchoPin, GPIO.IN)
        GPIO.setup(self.TrigPin, GPIO.OUT)
        GPIO.setup(self.TrackSensorLeftPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorLeftPin2, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin2, GPIO.IN)
        # Set PWM pins and frequency to 2000Hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    def run(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Move the car backward
    def back(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Turn the car left
    def left(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Turn the car right
    def right(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Spin the car left in place
    def spin_left(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Spin the car right in place
    def spin_right(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # Stop the car
    def brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    # Key press detection
    def key_scan(self):
        while GPIO.input(self.key):
            pass
        while not GPIO.input(self.key):
            time.sleep(0.01)
            if not GPIO.input(self.key):
                time.sleep(0.01)
            while not GPIO.input(self.key):
                pass

    # 超声波函数
    def Distance(self):
        GPIO.output(self.TrigPin, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)

        t3 = time.time()

        while not GPIO.input(self.EchoPin):
            t4 = time.time()
            if (t4 - t3) > 0.03:
                return -1

        t1 = time.time()
        while GPIO.input(self.EchoPin):
            t5 = time.time()
            if (t5 - t1) > 0.03:
                return -1

        t2 = time.time()
        time.sleep(0.01)
        return ((t2 - t1) * 340 / 2) * 100

    # 超声波距离检测
    def Distance_test(self):
        num = 0
        ultrasonic = []
        while num < 5:
            distance = self.Distance()
            while int(distance) == -1:
                distance = self.Distance()
#                 print("Tdistance is %f" % distance)
            while int(distance) >= 500 or int(distance) == 0:
                distance = self.Distance()
#                 print("Edistance is %f" % distance)
            ultrasonic.append(distance)
            num = num + 1
            time.sleep(0.01)
#         print(ultrasonic)
        distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3]) / 3
#         print("distance is %f" % distance)
        return distance

    def lineWalk(self):
        while True:
            # Track infrared sensor values
            TrackSensorLeftValue1 = GPIO.input(self.TrackSensorLeftPin1)
            TrackSensorLeftValue2 = GPIO.input(self.TrackSensorLeftPin2)
            TrackSensorRightValue1 = GPIO.input(self.TrackSensorRightPin1)
            TrackSensorRightValue2 = GPIO.input(self.TrackSensorRightPin2)

            if TrackSensorLeftValue1 == False and TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False and TrackSensorRightValue2 == False:
                self.brake()
#                 print("坐标点")
                time.sleep(2)
                return True
            else: 
                # Handle sharp right and right angle turns
                if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
                    self.spin_right(10, 10)
#                     print("右直角转弯")
                    time.sleep(0.1)

                # Handle sharp left and left angle turns
                elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
                    self.spin_left(10, 10)
#                     print("左直角转弯")
                    time.sleep(0.1)

                # Handle leftmost detection
                elif TrackSensorLeftValue1 == False:
                    self.spin_left(10, 10)

                # Handle rightmost detection
                elif TrackSensorRightValue2 == False:
                    self.spin_right(10, 10)

                # Handle left curve
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                    self.left(0, 10)

                # Handle right curve
                elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                    self.right(10, 0)

                # 两侧空 中间在轨道
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                    self.run(15, 15)
#                     print("向前跑！")
                #   time.sleep(10)

    
    #     后退巡线    
    def lineWalk_BackVersion(self):
        while True:
            # Track infrared sensor values
            TrackSensorLeftValue1 = GPIO.input(self.TrackSensorLeftPin1)
            TrackSensorLeftValue2 = GPIO.input(self.TrackSensorLeftPin2)
            TrackSensorRightValue1 = GPIO.input(self.TrackSensorRightPin1)
            TrackSensorRightValue2 = GPIO.input(self.TrackSensorRightPin2)

            if TrackSensorLeftValue1 == False and TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False and TrackSensorRightValue2 == False:
                self.brake()
                print("坐标点")
                time.sleep(1.5)
                return True
            else: 
                # Handle sharp right and right angle turns
                if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
                    self.spin_right(15, 15)
#                     print("右直角转弯")
                    time.sleep(0.1)

                # Handle sharp left and left angle turns
                elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
                    self.spin_left(15, 15)
#                     print("左直角转弯")
                    time.sleep(0.1)

                # Handle leftmost detection
                elif TrackSensorLeftValue1 == False:
                    self.spin_left(10, 10)

                # Handle rightmost detection
                elif TrackSensorRightValue2 == False:
                    self.spin_right(10, 10)

                # Handle left curve
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                    self.left(0, 10)

                # Handle right curve
                elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                    self.right(10, 0)

                # 两侧空 中间在轨道
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                    self.back(9, 9)
#                     print("向前跑！")
                #   time.sleep(10)
        
    def tackleDetection(self):
        dis = self.Distance_test()
        print("距离: ", dis)
        if dis < 55 and dis > 5:
            return True
        else:
            return False
    
    #         二次检测 对向来车 后退避障 左转一格

    def secondary_Detection(self):
            dis1 = self.Distance_test()
            time.sleep(2)
            dis2 = self.Distance()
            diff = dis1 - dis2
            if diff>= 10:
                return True

                
    def back_Turnaround(self):
            self.spin_left(15,15)
            time.sleep(1)
            self.spin_right(15,15)
            time.sleep(1)
            self.brake()
            time.sleep(2)
    
    def reSetup(self):
        self.pwm_ENA.stop()
        self.pwm_ENB.stop()
        GPIO.cleanup()