import time


class GestureHoldValidator:
    def __init__(self, hold_time=3.0):
        self.hold_time = hold_time
        self.current_gesture = None
        self.start_time = None
        self.confirmed_once = False

    def update(self, gesture_name):
        now = time.time()

        if gesture_name == "UNKNOWN":
            self.current_gesture = None
            self.start_time = None
            self.confirmed_once = False
            return None, 0.0

        if gesture_name != self.current_gesture:
            self.current_gesture = gesture_name
            self.start_time = now
            self.confirmed_once = False
            return None, 0.0

        held_for = now - self.start_time if self.start_time else 0.0

        if held_for >= self.hold_time and not self.confirmed_once:
            self.confirmed_once = True
            return gesture_name, held_for

        return None, held_for