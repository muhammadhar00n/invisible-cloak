import cv2
import numpy as np

# -----------------------------
# STEP 1: Capture the background
# -----------------------------
cap = cv2.VideoCapture(0)

print("Capturing background... Please move out of the frame.")
background = None

for i in range(60):  # Capture several frames for a clean background
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)

    if background is None:
        background = frame.copy()
    else:
        background = cv2.addWeighted(background, 0.9, frame, 0.1, 0)

print("Background captured! Step into the frame with your blue cloak.")

# -----------------------------
# PROCESS LIVE VIDEO
# -----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # -----------------------------
    # STEP 2: Detect cloak color (Blue) using HSV
    # -----------------------------
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Blue cloak color range
    lower_blue = np.array([80, 50, 50])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # -----------------------------
    # STEP 3: Remove that color from live video (cloak mask)
    # -----------------------------
    mask_inv = cv2.bitwise_not(mask)

    # Visible part of person (everything except cloak)
    visible_person = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # -----------------------------
    # STEP 4: Replace cloak area with background
    # -----------------------------
    invisible_area = cv2.bitwise_and(background, background, mask=mask)

    # -----------------------------
    # STEP 5: Combine both to create invisibility illusion
    # -----------------------------
    final_output = cv2.addWeighted(visible_person, 1, invisible_area, 1, 0)

    cv2.putText(final_output, "Invisible Cloak Effect - Press 'q' to quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Invisible Cloak", final_output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
