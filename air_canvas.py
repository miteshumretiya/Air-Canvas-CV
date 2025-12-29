import cv2
import numpy as np
import mediapipe as mp
import math

# --- Configuration ---
draw_color = (255, 0, 255) # Default: Magenta
brush_size = 15
eraser_size = 50

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)

# --- Webcam Setup ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# --- Canvas Setup ---
img_canvas = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0

print("New UI Loaded: RED, GREEN, BLUE, YELLOW, ERASER")

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # --- 1. NEW UI HEADER LAYOUT ---
    # We now have 5 buttons. Let's space them out evenly.
    # Header Background
    cv2.rectangle(img, (0, 0), (1280, 100), (50, 50, 50), cv2.FILLED)
    
    # 1. Red Button
    cv2.rectangle(img, (40, 10), (240, 90), (0, 0, 255), cv2.FILLED)
    
    # 2. Green Button
    cv2.rectangle(img, (290, 10), (490, 90), (0, 255, 0), cv2.FILLED)
    
    # 3. Blue Button
    cv2.rectangle(img, (540, 10), (740, 90), (255, 0, 0), cv2.FILLED)
    
    # 4. NEW: Yellow Button (Yellow in BGR is 0, 255, 255)
    cv2.rectangle(img, (790, 10), (990, 90), (0, 255, 255), cv2.FILLED)
    
    # 5. Eraser Button
    cv2.rectangle(img, (1040, 10), (1240, 90), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "Eraser", (1080, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = img.shape
            
            # Key Landmarks
            x1, y1 = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h) # Index
            x2, y2 = int(hand_landmarks.landmark[12].x * w), int(hand_landmarks.landmark[12].y * h) # Middle
            x_thumb, y_thumb = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h) # Thumb

            # Finger Check
            fingers = []
            tip_ids = [8, 12, 16, 20]
            
            # Thumb check
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x: fingers.append(1)
            else: fingers.append(0)
            
            # Other 4 fingers
            for id in range(1, 5):
                if hand_landmarks.landmark[tip_ids[id-1]].y < hand_landmarks.landmark[tip_ids[id-1]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # --- PALM ERASE (All 5 Fingers) ---
            if fingers == [1, 1, 1, 1, 1]:
                img_canvas = np.zeros((720, 1280, 3), np.uint8)
                cv2.putText(img, "CLEARED", (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)

            # --- SELECTION MODE (Index + Middle) ---
            elif fingers[1] and fingers[2]:
                xp, yp = 0, 0 
                
                # --- 2. NEW SELECTION LOGIC ---
                if y1 < 100: # If hand is in the header area
                    if 40 < x1 < 240: 
                        draw_color = (0, 0, 255)   # Red
                    elif 290 < x1 < 490: 
                        draw_color = (0, 255, 0)   # Green
                    elif 540 < x1 < 740: 
                        draw_color = (255, 0, 0)   # Blue
                    elif 790 < x1 < 990: 
                        draw_color = (0, 255, 255) # Yellow (NEW)
                    elif 1040 < x1 < 1240: 
                        draw_color = (0, 0, 0)     # Eraser

                # Pinch Resize Logic
                length = math.hypot(x1 - x_thumb, y1 - y_thumb)
                brush_size = int(np.interp(length, [20, 150], [5, 50]))
                
                # Visual Indicator (Ring Color Matches Selection)
                cv2.circle(img, (x1, y1), brush_size, draw_color, 1)
                cv2.circle(img, (x1, y1), 5, draw_color, cv2.FILLED) 
                
                if draw_color == (0, 0, 0):
                    eraser_size = brush_size

            # --- DRAWING MODE (Index Only) ---
            elif fingers[1] and not fingers[2]:
                current_size = eraser_size if draw_color == (0, 0, 0) else brush_size
                
                cv2.circle(img, (x1, y1), int(current_size/2), draw_color, cv2.FILLED)
                
                if xp == 0 and yp == 0: xp, yp = x1, y1
                
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, current_size)
                xp, yp = x1, y1

    # Merge
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, img_canvas)

    cv2.imshow("Air Canvas Pro", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()