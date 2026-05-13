from adafruit_servokit import ServoKit
from time import sleep


class ServoRobot:
    def __init__(self):
        # PCA9685 has 16 channels
        self.kit = ServoKit(channels=16)

        # Channel assignments
        self.WHEEL_1 = 0
        self.WHEEL_2 = 1
        self.WHEEL_3 = 2
        self.WHEEL_4 = 3

        self.PEN_SERVO = 5

        self.wheel_channels = [
            self.WHEEL_1,
            self.WHEEL_2,
            self.WHEEL_3,
            self.WHEEL_4,
        ]

        # Direction correction for each wheel.
        # Change individual values to -1 if a wheel spins opposite of expected.
        self.wheel_direction = {
            self.WHEEL_1: 1,
            self.WHEEL_2: 1,
            self.WHEEL_3: 1,
            self.WHEEL_4: 1,
        }

        # FS90R continuous servo pulse range.
        # You may tune this later.
        for ch in self.wheel_channels:
            self.kit.continuous_servo[ch].set_pulse_width_range(1000, 2000)

        # Pen servo pulse range.
        # This assumes the pen servo is a normal positional servo, not FS90R.
        self.kit.servo[self.PEN_SERVO].set_pulse_width_range(500, 2500)

        # Tune these for your mechanism
        self.pen_up_angle = 80
        self.pen_down_angle = 20

        self.stop_all()
        self.pen_up()

    def clamp(self, value, low=-1.0, high=1.0):
        return max(low, min(high, value))

    def set_wheel(self, channel, speed):
        """
        speed range:
            -1.0 = full reverse
             0.0 = stop
             1.0 = full forward
        """

        speed = self.clamp(speed)
        corrected_speed = speed * self.wheel_direction[channel]

        self.kit.continuous_servo[channel].throttle = corrected_speed

    def set_all_wheels(self, speeds):
        """
        speeds should be a list of 5 values:
        [wheel1, wheel2, wheel3, wheel4, wheel5]
        """

        if len(speeds) != 4:
            raise ValueError("Expected exactly 5 wheel speed values.")

        for channel, speed in zip(self.wheel_channels, speeds):
            self.set_wheel(channel, speed)

    def stop_all(self):
        for ch in self.wheel_channels:
            self.kit.continuous_servo[ch].throttle = 0

    def pen_up(self):
        self.kit.servo[self.PEN_SERVO].angle = self.pen_up_angle
        sleep(0.25)

    def pen_down(self):
        self.kit.servo[self.PEN_SERVO].angle = self.pen_down_angle
        sleep(0.25)

    # Basic movement presets.
    # You will likely tune these depending on wheel layout.

    def forward(self, speed=0.4):
        self.set_all_wheels([
            speed,
            speed,
            speed,
            speed,
        ])

    def backward(self, speed=0.4):
        self.set_all_wheels([
            -speed,
            -speed,
            -speed,
            -speed,
        ])

    def turn_left(self, speed=0.35):
        self.set_all_wheels([
            -speed,
             speed,
            -speed,
             speed,
             0,
        ])

    def turn_right(self, speed=0.35):
        self.set_all_wheels([
             speed,
            -speed,
             speed,
            -speed,
             0,
        ])

    def move_for_time(self, movement_function, seconds, speed=0.4):
        movement_function(speed)
        sleep(seconds)
        self.stop_all()
        sleep(0.1)


if __name__ == "__main__":
    robot = ServoRobot()

    try:
        print("Testing pen")
        robot.pen_up()
        sleep(1)
        robot.pen_down()
        sleep(1)
        robot.pen_up()

        print("Testing forward")
        robot.forward(0.3)
        sleep(1)
        robot.stop_all()

        print("Testing backward")
        robot.backward(0.3)
        sleep(1)
        robot.stop_all()

        print("Testing left turn")
        robot.turn_left(0.3)
        sleep(1)
        robot.stop_all()

        print("Testing right turn")
        robot.turn_right(0.3)
        sleep(1)
        robot.stop_all()

    except KeyboardInterrupt:
        print("Stopping")

    finally:
        robot.pen_up()
        robot.stop_all()