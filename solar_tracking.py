import RPi.GPIO as GPIO
import time

# 腳位設定
GPIO.setmode(GPIO.BOARD)

# 光敏電阻腳位
SENSORS = {
    "right": 7,
    "left": 11,
    "up": 37,
    "down": 38
}

# 伺服馬達設定
SERVO_PINS = {
    "base": 10,
    "top": 16
}

GPIO.setup(SERVO_PINS["base"], GPIO.OUT)
GPIO.setup(SERVO_PINS["top"], GPIO.OUT)

servo_base = GPIO.PWM(SERVO_PINS["base"], 50)
servo_top = GPIO.PWM(SERVO_PINS["top"], 50)

servo_base.start(0)
servo_top.start(0)

# 初始角度
angle = {
    "base_right": 0,
    "base_left": 0,
    "top_up": 0,
    "top_down": 0
}

def read_light(sensor_pin):
    count = 0
    GPIO.setup(sensor_pin, GPIO.OUT)
    GPIO.output(sensor_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(sensor_pin, GPIO.IN)
    while GPIO.input(sensor_pin) == GPIO.LOW:
        count += 1
    return count

def rotate_servo(servo, degree):
    duty = 2 + (degree / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

def move_base_right():
    if angle["base_right"] > 180:
        angle["base_right"] = 0
    rotate_servo(servo_base, angle["base_right"])
    print("底部右轉角度:", angle["base_right"])

def move_base_left():
    if angle["base_left"] > 180:
        angle["base_left"] = 0
    rotate_servo(servo_base, 180 - angle["base_left"])
    print("底部左轉角度:", angle["base_left"])

def move_top_up():
    if angle["top_up"] > 180:
        angle["top_up"] = 0
    rotate_servo(servo_top, angle["top_up"])
    print("上方上轉角度:", angle["top_up"])

def move_top_down():
    if angle["top_down"] > 180:
        angle["top_down"] = 0
    rotate_servo(servo_top, 180 - angle["top_down"])
    print("上方下轉角度:", angle["top_down"])

# 主迴圈
try:
    while True:
        light = {
            direction: read_light(pin)
            for direction, pin in SENSORS.items()
        }

        print(f"右: {light['right']}, 左: {light['left']}, 上: {light['up']}, 下: {light['down']}")
        print("-------------")
        time.sleep(0.5)

        # 左右方向調整
        diff_h = abs(light['right'] - light['left'])
        if diff_h > 30:
            if light['right'] > light['left']:
                angle["base_right"] += 10
                move_base_right()
            else:
                angle["base_left"] += 10
                move_base_left()

        # 上下方向調整
        diff_v = abs(light['up'] - light['down'])
        if diff_v > 30:
            if light['up'] > light['down']:
                angle["top_up"] += 10
                move_top_up()
            else:
                angle["top_down"] += 10
                move_top_down()

except KeyboardInterrupt:
    print("程式中斷，清理 GPIO")
    servo_base.stop()
    servo_top.stop()
    GPIO.cleanup()
