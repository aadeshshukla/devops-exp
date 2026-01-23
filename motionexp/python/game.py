import random
import os
import time
import sys

# Game Constants
PLAYER_CHAR = "🗡️"
ENEMY_CHAR = "👹"
GOAL_CHAR = "🏆"
EMPTY_CHAR = "·"
DEAD_ENEMY = "💀"

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.attack_power = 25
        self.kills = 0
    
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self. y + dy
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def attack(self, enemies):
        """Attack all adjacent enemies"""
        killed = []
        for enemy in enemies: 
            if abs(enemy.x - self.x) <= 1 and abs(enemy.y - self.y) <= 1:
                damage = random.randint(self.attack_power - 5, self.attack_power + 10)
                enemy.health -= damage
                print(f"⚔️  You hit the enemy for {damage} damage!")
                if enemy.health <= 0:
                    killed.append(enemy)
                    self.kills += 1
                    print("💀 Enemy defeated!")
        return killed

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.attack_power = 10
    
    def move_towards_player(self, player, game_map, enemies):
        """Simple AI to move towards the player"""
        dx = 0
        dy = 0
        
        if player.x > self. x:
            dx = 1
        elif player.x < self.x:
            dx = -1
        
        if player. y > self.y:
            dy = 1
        elif player.y < self.y:
            dy = -1
        
        # Try to move (check bounds and other enemies)
        new_x = self.x + dx
        new_y = self. y + dy
        
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            # Check if another enemy is there
            for other in enemies:
                if other != self and other.x == new_x and other.y == new_y:
                    return
            self.x = new_x
            self.y = new_y
    
    def attack(self, player):
        """Attack if adjacent to player"""
        if abs(player.x - self.x) <= 1 and abs(player. y - self.y) <= 1:
            damage = random. randint(self.attack_power - 3, self.attack_power + 5)
            player.health -= damage
            print(f"👹 An enemy hits you for {damage} damage!")
            return True
        return False

class Game:
    def __init__(self, width=20, height=10, num_enemies=5):
        self.width = width
        self. height = height
        self.player = Player(1, height // 2)
        self.goal = (width - 2, height // 2)
        self.enemies = []
        self.game_over = False
        self.victory = False
        self.turn = 0
        
        # Spawn enemies randomly
        for _ in range(num_enemies):
            while True:
                ex = random.randint(3, width - 3)
                ey = random. randint(1, height - 2)
                # Make sure not on player, goal, or other enemy
                if (ex, ey) != (self.player.x, self.player.y) and (ex, ey) != self.goal:
                    if not any(e.x == ex and e.y == ey for e in self.enemies):
                        self.enemies.append(Enemy(ex, ey))
                        break
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        self.clear_screen()
        print("=" * (self.width + 10))
        print("⚔️  SWORD FIGHTER - Reach the Goal!  ⚔️")
        print("=" * (self.width + 10))
        print(f"❤️  Health: {self.player.health} | 💀 Kills: {self. player.kills} | Turn: {self.turn}")
        print("-" * (self.width + 2))
        
        # Build the map
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if x == self.player.x and y == self.player.y:
                    row += PLAYER_CHAR
                elif (x, y) == self.goal:
                    row += GOAL_CHAR
                elif any(e.x == x and e.y == y for e in self.enemies):
                    row += ENEMY_CHAR
                elif x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row += "█"
                else:
                    row += EMPTY_CHAR
            print(f"|{row}|")
        
        print("-" * (self.width + 2))
        print("\nControls:  W/A/S/D = Move | SPACE = Attack | Q = Quit")
        print("Kill enemies with your sword and reach the 🏆 goal!")
    
    def handle_input(self):
        try:
            # For cross-platform input
            if os.name == 'nt':   # Windows
                import msvcrt
                key = msvcrt.getch().decode('utf-8').lower()
            else:  # Unix/Linux/Mac
                import tty
                import termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try: 
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin. read(1).lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except: 
            key = input("\nEnter command (w/a/s/d/space/q): ").lower()
            if key == "": 
                key = " "
        
        if key == 'q':
            self.game_over = True
            print("\n👋 Thanks for playing!")
            return
        
        dx, dy = 0, 0
        if key == 'w': 
            dy = -1
        elif key == 's':
            dy = 1
        elif key == 'a':
            dx = -1
        elif key == 'd': 
            dx = 1
        elif key == ' ':
            # Attack! 
            print("\n⚔️  ATTACK!")
            killed = self.player.attack(self.enemies)
            for enemy in killed:
                self. enemies.remove(enemy)
            if not killed:
                print("No enemies in range!")
            time.sleep(0.5)
        
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, [[0] * self.width for _ in range(self.height)])
    
    def update(self):
        self.turn += 1
        
        # Check if player reached the goal
        if (self.player.x, self.player.y) == self.goal:
            self.victory = True
            self.game_over = True
            return
        
        # Check if player is dead
        if self.player. health <= 0:
            self.game_over = True
            return
        
        # Move enemies and attack
        for enemy in self.enemies:
            enemy.move_towards_player(self.player, [[0] * self.width for _ in range(self.height)], self.enemies)
            enemy.attack(self.player)
        
        # Check again if player is dead after enemy attacks
        if self.player.health <= 0:
            self. game_over = True
    
    def show_end_screen(self):
        self.clear_screen()
        print("\n" + "=" * 40)
        if self.victory:
            print("🎉🏆 VICTORY! YOU REACHED THE GOAL!  🏆🎉")
            print(f"\nYou defeated {self.player.kills} enemies!")
            print(f"Remaining health: {self.player.health}")
            print(f"Turns taken: {self.turn}")
        else:
            if self.player.health <= 0:
                print("💀 GAME OVER - You have been defeated!  💀")
                print(f"\nYou killed {self.player.kills} enemies before falling.")
            else:
                print("👋 Game ended.")
        print("=" * 40 + "\n")
    
    def run(self):
        print("\n⚔️  SWORD FIGHTER ⚔️")
        print("-" * 30)
        print("Navigate through enemies and reach the goal!")
        print("Use WASD to move, SPACE to attack nearby enemies.")
        print("\nPress any key to start...")
        
        try:
            if os.name == 'nt': 
                import msvcrt
                msvcrt.getch()
            else:
                import tty, termios
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    sys.stdin. read(1)
                finally: 
                    termios.tcsetattr(fd, termios. TCSADRAIN, old)
        except:
            input()
        
        while not self. game_over:
            self. draw()
            self.handle_input()
            if not self.game_over:
                self.update()
        
        self.show_end_screen()

def main():
    print("\n🎮 Welcome to Sword Fighter!  🎮\n")
    
    while True:
        try:
            difficulty = input("Select difficulty (1=Easy, 2=Normal, 3=Hard): ").strip()
            if difficulty == '1':
                game = Game(width=15, height=8, num_enemies=3)
            elif difficulty == '2':
                game = Game(width=20, height=10, num_enemies=5)
            elif difficulty == '3': 
                game = Game(width=25, height=12, num_enemies=8)
            else:
                game = Game()  # Default normal
            break
        except: 
            game = Game()
            break
    
    game.run()
    
    play_again = input("\nPlay again? (y/n): ").lower()
    if play_again == 'y':
        main()

if __name__ == "__main__":
    main()