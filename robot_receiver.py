import socket
from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

RF = 0
RB = 1
LF = 2
LB = 3

PORT = 5005


def wheels_off():
    for ch in [RF, RB, LF, LB]:
        kit.servo[ch].angle = None


def forward():
    kit.servo[RF].angle = 90
    kit.servo[RB].angle = 90
    kit.servo[LF].angle = 180
    kit.servo[LB].angle = 180


def backward():
    kit.servo[RF].angle = 180
    kit.servo[RB].angle = 180
    kit.servo[LF].angle = 90
    kit.servo[LB].angle = 90


def turn_left():
    kit.servo[RF].angle = 90
    kit.servo[RB].angle = 90
    kit.servo[LF].angle = 90
    kit.servo[LB].angle = 90


def turn_right():
    kit.servo[RF].angle = 180
    kit.servo[RB].angle = 180
    kit.servo[LF].angle = 180
    kit.servo[LB].angle = 180


def move(action, seconds):
    action()
    sleep(seconds)
    wheels_off()
    sleep(0.15)


def draw_A_motion_only():
    print("Moving in A pattern")
#line1 OK
    move(turn_left, 0.75)
    move(forward, 1)
#line2
    move(turn_left,4.5)
    move(forward, 1)
#go to center
    move(backward, 0.50)
    move(turn_left, 5)
#line3
    move(forward,0.50)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("Ready for A motion only")

try:
    wheels_off()

    while True:
        data, addr = sock.recvfrom(1024)
        cmd = data.decode().strip().upper()

        print("Received:", cmd)

        if cmd == "A":
            draw_A_motion_only()

        elif cmd == "STOP":
            wheels_off()

except KeyboardInterrupt:
    print("Stopping")

finally:
    wheels_off()
