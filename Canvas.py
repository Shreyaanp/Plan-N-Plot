import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import threading
import pygame
import random
import os


canvas_width, canvas_height = 1980, 1080
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

    dot_radius = 15 # the radius of the dot mouse.

    screen_width, screen_height = screen.get_size()
    dot_pos = [random.randint(dot_radius, screen_width - dot_radius),
               random.randint(dot_radius, screen_height - dot_radius)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                distance_squared = (cursor_pos[0] - dot_pos[0]) * 2 + (cursor_pos[1] - dot_pos[1]) * 2
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

               #perform left click when thumb and index finger are close
                if thumb_x > index_x - 20 and thumb_x < index_x + 20 and thumb_y > index_y - 20 and thumb_y < index_y + 20:
                    print("Left click")
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