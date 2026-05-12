import cv2
from collections import deque, Counter

from vision import HandTracker
from gestures import classify_gesture
from validator import GestureHoldValidator
from display import draw_status_panel

from comms import CommandSender
from simulator import RobotSimulator
from trajectories import get_trajectory

print("RUNNING VERSION 0.3")


def main():

    sender = CommandSender(mode="sim")
    sim = RobotSimulator()
    last_sent = None
    gesture_history = deque(maxlen=12)

    cap = cv2.VideoCapture(0)
    tracker = HandTracker(
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    # use 1.0 while tuning, switch back to 3.0 later
    validator = GestureHoldValidator(hold_time=1.0)

    while True:
        if not sim.is_running():
            break

        sim.step()

        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to read camera frame.")
                break

            frame = cv2.flip(frame, 1)
            image_height, image_width, _ = frame.shape

            results = tracker.process(frame)

            detected_gesture = "UNKNOWN"
            stable_gesture = "UNKNOWN"
            confirmed_gesture = None
            held_time = 0.0

            if results.multi_hand_landmarks and results.multi_handedness:
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness_label = results.multi_handedness[0].classification[0].label

                tracker.draw(frame, hand_landmarks)

                detected_gesture = classify_gesture(
                    hand_landmarks,
                    handedness_label,
                    image_width,
                    image_height
                )
                print("DETECTED =", detected_gesture)
                
                stable_gesture = detected_gesture
                confirmed_gesture, held_time = validator.update(stable_gesture)

            if confirmed_gesture:
                print("SIM TRIGGER:", confirmed_gesture)

                if confirmed_gesture != last_sent:
                    sender.send_command(confirmed_gesture)

                    path = get_trajectory(confirmed_gesture, scale=140, offset=(350, 220))
                    print("PATH:", path)

                    sim.load_trajectory(confirmed_gesture, path)
                    last_sent = confirmed_gesture
            # if confirmed_gesture:
            #     print(f"CONFIRMED GESTURE: {confirmed_gesture}")

            #     if confirmed_gesture != last_sent:
            #         sender.send_command(confirmed_gesture)

            #         path = get_trajectory(confirmed_gesture, scale=140, offset=(350, 220))
            #         sim.load_trajectory(confirmed_gesture, path)

            #     last_sent = confirmed_gesture

                # if confirmed_gesture:
                #     print(f"CONFIRMED GESTURE: {confirmed_gesture}")

                #     if confirmed_gesture == "A":
                #         print("TRIGGER DRAW A")

                #     elif confirmed_gesture == "B":
                #         print("TRIGGER DRAW B")

                #     elif confirmed_gesture == "PEACE":
                #         print("TRIGGER DRAW PEACE")

                #     elif confirmed_gesture == "C":
                #         print("TRIGGER DRAW C")

            else:
                gesture_history.clear()
                stable_gesture = "UNKNOWN"
                validator.update("UNKNOWN")
                last_sent = None

            draw_status_panel(frame, stable_gesture, held_time, confirmed_gesture)

            cv2.imshow("Gesture Test", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):
                break
    sender.close()
    sim.close()
    tracker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()