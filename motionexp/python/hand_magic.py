import cv2
import numpy as np
import mediapipe as mp
import pygame
from pygame.locals import *
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✨ Magic Hand Stars ✨")
clock = pygame.time.Clock()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands. Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# Star class
class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_x = x
        self. target_y = y
        self.size = random.uniform(2, 6)
        self.base_size = self.size
        self. color = self.random_color()
        self.speed = random.uniform(0.02, 0.08)
        self.angle = random.uniform(0, 2 * math. pi)
        self.rotation_speed = random.uniform(0.02, 0.1)
        self.orbit_radius = random.uniform(20, 60)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.trail = []
        self.max_trail_length = 15
        self.attracted = False
        self.attraction_strength = 0
        
    def random_color(self):
        # Beautiful magical colors:  gold, cyan, magenta, white, purple
        colors = [
            (255, 215, 0),    # Gold
            (0, 255, 255),    # Cyan
            (255, 0, 255),    # Magenta
            (255, 255, 255),  # White
            (147, 112, 219),  # Purple
            (255, 182, 193),  # Pink
            (0, 255, 127),    # Spring Green
        ]
        return random.choice(colors)
    
    def update(self, hand_positions):
        # Store previous position for trail
        self.trail.append((self.x, self.y, self.size, self.color))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Find closest hand
        closest_dist = float('inf')
        closest_hand = None
        
        for hand_pos in hand_positions:
            dist = math.sqrt((hand_pos[0] - self. x) ** 2 + (hand_pos[1] - self.y) ** 2)
            if dist < closest_dist:
                closest_dist = dist
                closest_hand = hand_pos
        
        # Attraction logic
        attraction_radius = 300
        
        if closest_hand and closest_dist < attraction_radius: 
            self.attracted = True
            self. attraction_strength = 1 - (closest_dist / attraction_radius)
            
            # Move towards hand with easing
            dx = closest_hand[0] - self.x
            dy = closest_hand[1] - self.y
            
            # Add some orbit effect when close
            if closest_dist < 100:
                self.angle += self.rotation_speed
                orbit_x = math.cos(self.angle) * self.orbit_radius * (closest_dist / 100)
                orbit_y = math.sin(self.angle) * self.orbit_radius * (closest_dist / 100)
                self.target_x = closest_hand[0] + orbit_x
                self.target_y = closest_hand[1] + orbit_y
            else: 
                self.target_x = closest_hand[0]
                self.target_y = closest_hand[1]
            
            # Smooth movement with easing
            ease_factor = self.speed * (1 + self.attraction_strength * 2)
            self.x += (self.target_x - self.x) * ease_factor
            self.y += (self.target_y - self.y) * ease_factor
            
            # Increase size when attracted
            self.size = self.base_size * (1 + self.attraction_strength * 0.5)
            
            # Change color gradually when attracted
            if random.random() < 0.02: 
                self.color = self. random_color()
        else:
            self.attracted = False
            self.attraction_strength = 0
            self.size = self.base_size
            
            # Gentle floating motion when not attracted
            self.angle += 0.01
            self.x += math.sin(self.angle) * 0.5
            self.y += math. cos(self.angle * 0.7) * 0.3
        
        # Twinkle effect
        self.twinkle_phase += 0.1
        twinkle = (math.sin(self.twinkle_phase) + 1) / 2
        self.current_alpha = int(150 + 105 * twinkle)
        
        # Keep stars on screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))
    
    def draw(self, surface):
        # Draw trail
        for i, (tx, ty, tsize, tcolor) in enumerate(self.trail):
            alpha = int((i / len(self.trail)) * 100)
            trail_size = tsize * (i / len(self.trail)) * 0.7
            trail_surface = pygame.Surface((int(trail_size * 4), int(trail_size * 4)), pygame.SRCALPHA)
            pygame.draw.circle(
                trail_surface,
                (*tcolor, alpha),
                (int(trail_size * 2), int(trail_size * 2)),
                int(trail_size)
            )
            surface.blit(trail_surface, (tx - trail_size * 2, ty - trail_size * 2))
        
        # Draw glow
        glow_size = self.size * 3
        glow_surface = pygame.Surface((int(glow_size * 4), int(glow_size * 4)), pygame.SRCALPHA)
        for i in range(3):
            glow_alpha = int((self.current_alpha / 3) * (1 - i / 3))
            glow_radius = self.size * (1 + i * 0.8)
            pygame.draw.circle(
                glow_surface,
                (*self.color, glow_alpha),
                (int(glow_size * 2), int(glow_size * 2)),
                int(glow_radius)
            )
        surface.blit(glow_surface, (self.x - glow_size * 2, self.y - glow_size * 2))
        
        # Draw star core
        self.draw_star_shape(surface, self.x, self.y, self.size, self.color)
    
    def draw_star_shape(self, surface, x, y, size, color):
        # Draw a 4-pointed star
        points = []
        for i in range(8):
            angle = i * math.pi / 4 + self.angle
            if i % 2 == 0:
                r = size * 1.5
            else:
                r = size * 0.5
            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r
            points.append((px, py))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)


class MagicParticle:
    """Small particles that spawn around hands for extra magic effect"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self. vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.uniform(1, 3)
        self.color = random.choice([
            (255, 215, 0),
            (255, 255, 255),
            (0, 255, 255),
        ])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self. vy += 0.05  # Slight gravity
        self.life -= self.decay
        return self.life > 0
    
    def draw(self, surface):
        alpha = int(self.life * 255)
        size = self.size * self.life
        if size > 0:
            particle_surface = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                (*self.color, alpha),
                (int(size * 2), int(size * 2)),
                int(size)
            )
            surface.blit(particle_surface, (self.x - size * 2, self.y - size * 2))


def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random. randint(0, HEIGHT)
        stars.append(Star(x, y))
    return stars


def get_hand_positions(frame):
    """Process frame and return hand landmark positions"""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    hand_positions = []
    finger_positions = []
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results. multi_hand_landmarks:
            # Get palm center (using wrist and middle finger base)
            wrist = hand_landmarks.landmark[0]
            middle_base = hand_landmarks.landmark[9]
            
            palm_x = int((wrist.x + middle_base.x) / 2 * WIDTH)
            palm_y = int((wrist.y + middle_base.y) / 2 * HEIGHT)
            hand_positions.append((palm_x, palm_y))
            
            # Get all fingertips
            fingertip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
            for tip_id in fingertip_ids:
                tip = hand_landmarks.landmark[tip_id]
                tip_x = int(tip.x * WIDTH)
                tip_y = int(tip. y * HEIGHT)
                finger_positions.append((tip_x, tip_y))
    
    return hand_positions, finger_positions


def main():
    stars = create_stars(150)  # Create 150 stars
    magic_particles = []
    
    # Background stars (static, for depth effect)
    bg_stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.5, 1.5)) 
                for _ in range(100)]
    
    running = True
    show_camera = True
    
    print("✨ Magic Hand Stars ✨")
    print("Controls:")
    print("  - Move your hand to attract stars")
    print("  - Press 'C' to toggle camera view")
    print("  - Press 'R' to reset stars")
    print("  - Press 'ESC' or 'Q' to quit")
    
    while running: 
        for event in pygame.event.get():
            if event. type == QUIT: 
                running = False
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE or event.key == K_q:
                    running = False
                elif event.key == K_c:
                    show_camera = not show_camera
                elif event.key == K_r:
                    stars = create_stars(150)
        
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            continue
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Get hand positions
        hand_positions, finger_positions = get_hand_positions(frame)
        all_attraction_points = hand_positions + finger_positions
        
        # Create magic particles around hands
        for pos in finger_positions:
            if random.random() < 0.3: 
                magic_particles.append(MagicParticle(pos[0], pos[1]))
        
        # Update magic particles
        magic_particles = [p for p in magic_particles if p. update()]
        
        # Clear screen with dark background
        screen.fill((5, 5, 20))
        
        # Draw background stars
        for bx, by, bs in bg_stars:
            twinkle = (math.sin(pygame.time.get_ticks() * 0.001 + bx) + 1) / 2
            alpha = int(50 + 50 * twinkle)
            star_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(star_surface, (255, 255, 255, alpha), (2, 2), int(bs))
            screen.blit(star_surface, (bx, by))
        
        # Draw camera feed if enabled (semi-transparent)
        if show_camera:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
            frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
            frame_surface.set_alpha(30)
            screen.blit(frame_surface, (0, 0))
        
        # Draw hand glow effect
        for pos in hand_positions:
            for radius in range(100, 20, -20):
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                alpha = int(30 * (1 - radius / 100))
                pygame. draw.circle(glow_surface, (100, 150, 255, alpha), (radius, radius), radius)
                screen.blit(glow_surface, (pos[0] - radius, pos[1] - radius))
        
        # Update and draw stars
        for star in stars:
            star.update(all_attraction_points)
            star.draw(screen)
        
        # Draw magic particles
        for particle in magic_particles:
            particle.draw(screen)
        
        # Draw fingertip indicators
        for pos in finger_positions:
            pygame.draw.circle(screen, (255, 255, 255, 100), pos, 8, 2)
        
        # Draw FPS
        fps = int(clock.get_fps())
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f"FPS: {fps}", True, (100, 100, 100))
        screen.blit(fps_text, (10, 10))
        
        # Draw instructions
        if not hand_positions:
            instruction_font = pygame.font.Font(None, 48)
            instruction_text = instruction_font.render("👋 Show your hand to create magic!", True, (150, 150, 150))
            text_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(instruction_text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Cleanup
    cap.release()
    hands.close()
    pygame.quit()


if __name__ == "__main__":
    main()