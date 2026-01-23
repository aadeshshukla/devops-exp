import cv2
import mediapipe as mp
import numpy as np
import random
import math

# Camera
cap = cv2.VideoCapture(0)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Screen
WIDTH, HEIGHT = 900, 600

# Star physics (tuned)
NUM_STARS = 100
ATTRACTION = 0.25      # stronger pull
FRICTION = 0.90        # less damping
MAX_SPEED = 8

# Stars
stars = []
for _ in range(NUM_STARS):
    stars.append({
        "x": random.uniform(0, WIDTH),
        "y": random.uniform(0, HEIGHT),
        "vx": random.uniform(-2, 2),
        "vy": random.uniform(-2, 2),
        "size": random.randint(1, 3),
        "phase": random.uniform(0, 2 * math.pi),
        "twinkle_speed": random.uniform(0.03, 0.08)
    })

# Hand smoothing
hand_x, hand_y = WIDTH // 2, HEIGHT // 2
smooth_x, smooth_y = hand_x, hand_y
alpha = 0.25  # faster response

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark[8]
        hx = int(lm.x * WIDTH)
        hy = int(lm.y * HEIGHT)

        smooth_x = int(alpha * hx + (1 - alpha) * smooth_x)
        smooth_y = int(alpha * hy + (1 - alpha) * smooth_y)

    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for star in stars:
        dx = smooth_x - star["x"]
        dy = smooth_y - star["y"]
        dist = math.sqrt(dx * dx + dy * dy) + 0.001

        # Directional attraction (normalized)
        fx = (dx / dist) * ATTRACTION
        fy = (dy / dist) * ATTRACTION

        # Apply force
        star["vx"] += fx
        star["vy"] += fy

        # Friction
        star["vx"] *= FRICTION
        star["vy"] *= FRICTION

        # Speed cap
        speed = math.sqrt(star["vx"]**2 + star["vy"]**2)
        if speed > MAX_SPEED:
            star["vx"] = (star["vx"] / speed) * MAX_SPEED
            star["vy"] = (star["vy"] / speed) * MAX_SPEED

        # Update position
        star["x"] += star["vx"]
        star["y"] += star["vy"]

        # Wrap edges
        if star["x"] < 0: star["x"] += WIDTH
        if star["x"] > WIDTH: star["x"] -= WIDTH
        if star["y"] < 0: star["y"] += HEIGHT
        if star["y"] > HEIGHT: star["y"] -= HEIGHT

        # Independent twinkle (subtle)
        star["phase"] += star["twinkle_speed"]
        brightness = int(200 + 40 * math.sin(star["phase"]))
        brightness = max(150, min(255, brightness))

        cv2.circle(
            canvas,
            (int(star["x"]), int(star["y"])),
            star["size"],
            (brightness, brightness, brightness),
            -1
        )

    cv2.imshow("Natural Star Flow", canvas)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


