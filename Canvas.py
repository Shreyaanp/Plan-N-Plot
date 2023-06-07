import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import threading
import pygame
import random
import math

canvas_width, canvas_height = 1280, 720
canvas = 255 * np.ones((canvas_height, canvas_width, 3), dtype=np.uint8)
drawing = False
prev_point = None
brush_size = 3
brush_color = (0, 0, 255)

def game():
    pygame.init()
    size = (640, 450)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Mouse Game")

    bg_color = (255, 255, 255)

    running = True

    cursor_pos = [350, 250]

    dot_radius = 15

    screen_width, screen_height = screen.get_size()
    dot_pos = [random.randint(dot_radius, screen_width - dot_radius),
               random.randint(dot_radius, screen_height - dot_radius)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                distance_squared = (cursor_pos[0] - dot_pos[0]) ** 2 + (cursor_pos[1] - dot_pos[1]) ** 2
                if distance_squared < dot_radius ** 2:
                    dot_pos = [random.randint(dot_radius, screen_width - dot_radius),
                               random.randint(dot_radius, screen_height - dot_radius)]

        cursor_pos = pygame.mouse.get_pos()

        screen.fill(bg_color)

        pygame.draw.circle(screen, (255, 0, 0), cursor_pos, 10)
        pygame.draw.circle(screen, (0, 255, 0), dot_pos, dot_radius)

        pygame.display.flip()

    pygame.quit()

canvas_cleared = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# write the how to use on the canvas
cv2.putText(canvas, "Press 'c' to clear the canvas", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'd' to start/stop drawing", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'r' to change color to red", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'g' to change color to green", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'b' to change color to blue", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press '+' to increase brush size", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press '-' to decrease brush size", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'l' to play a game", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "Press 'q' to quit", (10, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "raise your index finger to go into drawing mode", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(canvas, "raise your middle finger to start cursor mode", (10, 330), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * canvas_width)
                index_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * canvas_height)
                middle_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * canvas_width)
                middle_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * canvas_height)
                thumb_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * canvas_width)
                thumb_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * canvas_height)
                if middle_y < index_y:
                    pyautogui.moveTo(middle_x, middle_y)
                index_y_pip = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * canvas_height)

                if drawing and prev_point is not None and index_y < index_y_pip:  # Check if finger is raised
                    cv2.line(canvas, prev_point, (index_x, index_y), brush_color, thickness=brush_size)

                prev_point = (index_x, index_y)

                #left click if the index finger tip is close to the thumb tip
                if math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) < 50:
                    pyautogui.click()


        # Display the canvas and the image
        cv2.imshow('Canvas', canvas)
        cv2.imshow('Hand Drawing', image)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas = 255 * np.ones((canvas_height, canvas_width, 3), dtype=np.uint8)
        elif key == ord('d'):
            drawing = not drawing
            if not drawing:
                prev_point = None
        elif key == ord('r'):
            brush_color = (0, 0, 255)
        elif key == ord('g'):
            brush_color = (0, 255, 0)
        elif key == ord('b'):
            brush_color = (255, 0, 0)
        elif key == ord('+'):
            brush_size += 1
        elif key == ord('-'):
            brush_size -= 1 if brush_size > 1 else 0
        elif key == ord('l'):
            threading.Thread(target=game).start()


cap.release()
cv2.destroyAllWindows()
