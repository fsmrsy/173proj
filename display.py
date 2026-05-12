import cv2


def draw_status_panel(frame, gesture, held_time, confirmed):
    cv2.rectangle(frame, (10, 10), (420, 140), (0, 0, 0), -1)

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Held: {held_time:.2f}s",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    msg = f"Confirmed: {confirmed}" if confirmed else "Confirmed: None"
    cv2.putText(
        frame,
        msg,
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 200, 255),
        2
    )