import math


def landmark_to_point(hand_landmarks, index, image_width, image_height):
    lm = hand_landmarks.landmark[index]
    return int(lm.x * image_width), int(lm.y * image_height)


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def finger_is_up(hand_landmarks, finger_tip, finger_pip):
    return hand_landmarks.landmark[finger_tip].y < hand_landmarks.landmark[finger_pip].y


def thumb_is_open(hand_landmarks, handedness_label):
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]

    if handedness_label == "Right":
        return thumb_tip.x < thumb_ip.x
    return thumb_tip.x > thumb_ip.x


def get_finger_states(hand_landmarks, handedness_label):
    thumb = thumb_is_open(hand_landmarks, handedness_label)
    index = finger_is_up(hand_landmarks, 8, 6)
    middle = finger_is_up(hand_landmarks, 12, 10)
    ring = finger_is_up(hand_landmarks, 16, 14)
    pinky = finger_is_up(hand_landmarks, 20, 18)

    return {
        "thumb": thumb,
        "index": index,
        "middle": middle,
        "ring": ring,
        "pinky": pinky
    }

def classify_gesture(hand_landmarks, handedness_label, image_width, image_height):
    fingers = get_finger_states(hand_landmarks, handedness_label)

    wrist = landmark_to_point(hand_landmarks, 0, image_width, image_height)
    thumb_tip = landmark_to_point(hand_landmarks, 4, image_width, image_height)
    index_tip = landmark_to_point(hand_landmarks, 8, image_width, image_height)
    middle_tip = landmark_to_point(hand_landmarks, 12, image_width, image_height)
    ring_tip = landmark_to_point(hand_landmarks, 16, image_width, image_height)
    pinky_tip = landmark_to_point(hand_landmarks, 20, image_width, image_height)

    index_mcp = landmark_to_point(hand_landmarks, 5, image_width, image_height)
    middle_mcp = landmark_to_point(hand_landmarks, 9, image_width, image_height)
    ring_mcp = landmark_to_point(hand_landmarks, 13, image_width, image_height)
    pinky_mcp = landmark_to_point(hand_landmarks, 17, image_width, image_height)

    palm_width = distance(index_mcp, pinky_mcp)
    if palm_width == 0:
        return "UNKNOWN"

    thumb_index_dist = distance(thumb_tip, index_tip)
    thumb_middle_dist = distance(thumb_tip, middle_tip)

    index_middle_dist = distance(index_tip, middle_tip)
    middle_ring_dist = distance(middle_tip, ring_tip)
    ring_pinky_dist = distance(ring_tip, pinky_tip)
    index_pinky_dist = distance(index_tip, pinky_tip)

    index_wrist_dist = distance(index_tip, wrist)
    middle_wrist_dist = distance(middle_tip, wrist)
    ring_wrist_dist = distance(ring_tip, wrist)
    pinky_wrist_dist = distance(pinky_tip, wrist)

    index_folded = distance(index_tip, index_mcp)
    middle_folded = distance(middle_tip, middle_mcp)
    ring_folded = distance(ring_tip, ring_mcp)
    pinky_folded = distance(pinky_tip, pinky_mcp)

    fingers_together = (
        index_middle_dist < 0.45 * palm_width and
        middle_ring_dist < 0.45 * palm_width and
        ring_pinky_dist < 0.70 * palm_width
    )

    fingers_high = (
        index_wrist_dist > 2.20 * palm_width and
        middle_wrist_dist > 2.20 * palm_width and
        ring_wrist_dist > 2.00 * palm_width and
        pinky_wrist_dist > 1.80 * palm_width
    )

    open_hand = (
        fingers["index"]
        and fingers["middle"]
        and fingers["ring"]
        and fingers["pinky"]
    )

    # B first: open hand, fingers together, thumb closed
    if (
        open_hand
        and fingers_together
        and fingers_high
        and not fingers["thumb"]
    ):
        return "B"

    # C second: thumb/index opening + curled ring or pinky
    c_opening = (
        thumb_index_dist > 0.50 * palm_width and
        thumb_middle_dist > 0.60 * palm_width
    )

    c_not_flat = index_pinky_dist < 1.50 * palm_width

    c_not_fist = (
        index_folded > 0.80 * palm_width or
        middle_folded > 0.80 * palm_width or
        ring_folded > 0.80 * palm_width or
        pinky_folded > 0.80 * palm_width
    )

    c_has_curled_fingers = (
        not fingers["ring"] or
        not fingers["pinky"]
    )

    if (
        c_opening
        and c_not_flat
        and c_not_fist
        and c_has_curled_fingers
        and not open_hand
    ):
        return "C"

    # A
    a_folded = (
        index_folded < 0.85 * palm_width and
        middle_folded < 0.85 * palm_width and
        ring_folded < 0.85 * palm_width and
        pinky_folded < 0.85 * palm_width
    )

    if (
        not fingers["index"]
        and not fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
        and fingers["thumb"]
        and a_folded
    ):
        return "A"

    # PEACE
    if (
        fingers["index"]
        and fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
        and index_middle_dist > 0.20 * palm_width
    ):
        return "PEACE"

    return "UNKNOWN"
