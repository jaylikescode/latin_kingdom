import pygame
import math
import random
from constants import *
from enemy import Enemy
from tower import Tower
from coin_pickup import CoinPickup
from portal import Portal
from assets import assets

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("</>")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.gold = STARTING_GOLD
        self.lives = STARTING_LIVES
        self.wave = 1
        self.score = 0
        self.game_over = False
        self.wave_in_progress = False
        self.wave_complete = False
        
        # Game objects
        self.enemies = []
        self.towers = []
        self.coin_pickups = []
        self.selected_tower_type = "archer"
        self.selected_tower = None
        
        # Drag and drop system
        self.dragging_tower = False
        self.drag_tower_type = None
        self.drag_start_pos = None
        self.mouse_pos = (0, 0)
        
        # Grid settings for background (needed before path generation)
        self.grid_size = 40  # Size of each grid cell
        self.background_surface = None
        self.create_grid_background()
        
        # Generate randomized path
        self.path = self.generate_random_path()
        
        # Create portal at enemy spawn location (first point in path)
        self.portal = Portal(self.path[0][0], self.path[0][1])
        
        # Wave management
        self.wave_enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = ENEMY_SPAWN_DELAY
        self.wave_start_time = 0
        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def generate_random_path(self):
        """Generate a randomized blocky path from left to right with curves, aligned to grid"""
        path_points = []
        
        # Starting position (left side) - snap to grid
        start_x = 60
        start_y_grid = random.randint(4, 12)  # Random grid row (160px to 480px)
        start_y = start_y_grid * self.grid_size + self.grid_size // 2
        path_points.append((start_x, start_y))
        
        # Generate intermediate points with blocky curves
        current_x = start_x
        current_y = start_y
        
        # Create 8-12 segments for the path
        num_segments = random.randint(8, 12)
        segment_width = (SCREEN_WIDTH - 120) // num_segments  # Leave space for castle
        
        for i in range(1, num_segments):
            # Move right by segment width (snap to grid)
            current_x += segment_width
            current_x = (current_x // self.grid_size) * self.grid_size + self.grid_size // 2
            
            # Add vertical variation (curves) - snap to grid
            if i < num_segments // 2:
                # First half can curve up or down (in grid increments)
                vertical_change = random.choice([-2, -1, 0, 1, 2]) * self.grid_size
                current_y += vertical_change
            else:
                # Second half should generally move toward center for castle approach
                target_y_grid = (SCREEN_HEIGHT // 2) // self.grid_size
                current_y_grid = current_y // self.grid_size
                if current_y_grid > target_y_grid:
                    vertical_change = random.choice([-2, -1, 0]) * self.grid_size
                else:
                    vertical_change = random.choice([0, 1, 2]) * self.grid_size
                current_y += vertical_change
            
            # Snap to grid and keep within reasonable bounds
            current_y_grid = current_y // self.grid_size
            current_y_grid = max(3, min(SCREEN_HEIGHT // self.grid_size - 3, current_y_grid))
            current_y = current_y_grid * self.grid_size + self.grid_size // 2
            
            current_x_grid = current_x // self.grid_size
            current_x_grid = max(1, min(SCREEN_WIDTH // self.grid_size - 2, current_x_grid))
            current_x = current_x_grid * self.grid_size + self.grid_size // 2
            
            path_points.append((current_x, current_y))
        
        # Final point (castle position) - snap to grid
        castle_x_grid = (SCREEN_WIDTH - 80) // self.grid_size
        castle_x = castle_x_grid * self.grid_size + self.grid_size // 2
        
        current_y_grid = current_y // self.grid_size
        castle_y_grid = current_y_grid + random.choice([-1, 0, 1])
        castle_y_grid = max(4, min(SCREEN_HEIGHT // self.grid_size - 4, castle_y_grid))
        castle_y = castle_y_grid * self.grid_size + self.grid_size // 2
        
        path_points.append((castle_x, castle_y))
        
        return path_points
        
    def create_grid_background(self):
        """Create a grid-style background like the original MSN Kingdom Defender"""
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Base background color (dark green grass-like)
        base_color = (34, 80, 34)  # Dark forest green
        self.background_surface.fill(base_color)
        
        # Grid line colors
        light_grid_color = (45, 95, 45)    # Lighter green for main grid
        dark_grid_color = (25, 65, 25)     # Darker green for shadow effect
        
        # Draw horizontal grid lines
        for y in range(0, SCREEN_HEIGHT + self.grid_size, self.grid_size):
            # Main grid line
            pygame.draw.line(self.background_surface, light_grid_color, 
                           (0, y), (SCREEN_WIDTH, y), 1)
            # Shadow line (offset by 1 pixel)
            if y > 0:
                pygame.draw.line(self.background_surface, dark_grid_color, 
                               (0, y - 1), (SCREEN_WIDTH, y - 1), 1)
                
        # Draw vertical grid lines
        for x in range(0, SCREEN_WIDTH + self.grid_size, self.grid_size):
            # Main grid line
            pygame.draw.line(self.background_surface, light_grid_color, 
                           (x, 0), (x, SCREEN_HEIGHT), 1)
            # Shadow line (offset by 1 pixel)
            if x > 0:
                pygame.draw.line(self.background_surface, dark_grid_color, 
                               (x - 1, 0), (x - 1, SCREEN_HEIGHT), 1)
                
        # Add subtle texture variation to make it more interesting
        for y in range(0, SCREEN_HEIGHT, self.grid_size):
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                # Add slight color variation to each cell
                variation = random.randint(-5, 5)
                cell_color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                
                # Fill cell with slight variation (leaving border for grid lines)
                cell_rect = pygame.Rect(x + 1, y + 1, self.grid_size - 2, self.grid_size - 2)
                pygame.draw.rect(self.background_surface, cell_color, cell_rect)
        
    def start_wave(self):
        if not self.wave_in_progress:
            self.wave_enemies.clear()
            enemies_in_wave = 5 + self.wave * 2
            
            # Determine enemy composition based on wave
            for i in range(enemies_in_wave):
                if self.wave <= 2:
                    enemy_type = "goblin"
                elif self.wave <= 5:
                    enemy_type = random.choice(["goblin", "orc"])
                elif self.wave <= 10:
                    enemy_type = random.choice(["goblin", "orc", "troll"])
                else:
                    enemy_type = random.choice(["goblin", "orc", "troll", "dragon"])
                    
                self.wave_enemies.append(enemy_type)
                
            self.wave_in_progress = True
            self.wave_complete = False
            self.enemy_spawn_timer = pygame.time.get_ticks()
            self.wave_start_time = pygame.time.get_ticks()
            
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.enemy_spawn_timer >= self.enemy_spawn_delay and 
            len(self.wave_enemies) > 0):
            
            enemy_type = self.wave_enemies.pop(0)
            enemy = Enemy(enemy_type, self.path)
            self.enemies.append(enemy)
            self.enemy_spawn_timer = current_time
            
    def update(self):
        if self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Spawn enemies if wave is in progress
        if self.wave_in_progress:
            self.spawn_enemy()
            
        # Update enemies
        for enemy in self.enemies[:]:
            result = enemy.update()
            if result == "reached_end":
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_over = True
            elif not enemy.alive:
                # Play enemy death sound effect
                assets.play_sound('enemy_death')
                
                # Create coin pickup effect at enemy position
                coin_pickup = CoinPickup(enemy.x, enemy.y, enemy.reward)
                self.coin_pickups.append(coin_pickup)
                
                self.gold += enemy.reward
                self.score += enemy.reward
                self.enemies.remove(enemy)
                
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies, current_time)
            
        # Update coin pickups
        for coin_pickup in self.coin_pickups[:]:
            coin_pickup.update()
            if not coin_pickup.alive:
                self.coin_pickups.remove(coin_pickup)
                
        # Update portal animation
        self.portal.update()
            
        # Check if wave is complete
        if (self.wave_in_progress and len(self.wave_enemies) == 0 and 
            len(self.enemies) == 0):
            self.wave_in_progress = False
            self.wave_complete = True
            self.gold += WAVE_COMPLETION_BONUS
            
    def handle_mouse_down(self, pos):
        """Handle mouse button down for drag-and-drop"""
        x, y = pos
        
        # Check if clicking on tower buttons
        tower_types = [("archer", TOWER_COSTS["archer"]), 
                      ("magic", TOWER_COSTS["magic"]), 
                      ("cannon", TOWER_COSTS["cannon"])]
        
        for i, (tower_type, cost) in enumerate(tower_types):
            button_x = 20 + i * 120
            button_y = SCREEN_HEIGHT - 80
            
            if (button_x <= x <= button_x + 100 and 
                button_y <= y <= button_y + 30 and 
                self.gold >= cost):
                # Start dragging tower
                self.dragging_tower = True
                self.drag_tower_type = tower_type
                self.drag_start_pos = pos
                return
        
        # Check existing tower selection for upgrade
        for tower in self.towers:
            if (tower.x - 32 <= x <= tower.x + 32 and 
                tower.y - 32 <= y <= tower.y + 32):
                self.selected_tower = tower
                return
                
        # Check upgrade button
        if (self.selected_tower and self.selected_tower.level < 3 and
            520 <= x <= 620 and SCREEN_HEIGHT - 80 <= y <= SCREEN_HEIGHT - 50):
            cost = self.selected_tower.cost * self.selected_tower.level
            if self.gold >= cost:
                self.gold -= cost
                self.selected_tower.upgrade()
            return
            
        # Check next wave button
        if (self.wave_complete and 400 <= x <= 500 and 
            SCREEN_HEIGHT - 80 <= y <= SCREEN_HEIGHT - 50):
            self.wave += 1
            self.start_wave()
            self.wave_complete = False
            return
            
        # Clear tower selection if clicking elsewhere
        self.selected_tower = None
    
    def handle_mouse_up(self, pos):
        """Handle mouse button up for drag-and-drop"""
        if self.dragging_tower:
            x, y = pos
            
            # Snap to grid
            grid_x = (x // self.grid_size) * self.grid_size + self.grid_size // 2
            grid_y = (y // self.grid_size) * self.grid_size + self.grid_size // 2
            
            # Check if position is valid for tower placement
            if self.can_place_tower(grid_x, grid_y):
                cost = TOWER_COSTS[self.drag_tower_type]
                if self.gold >= cost:
                    # Place the tower
                    tower = Tower(grid_x, grid_y, self.drag_tower_type)
                    self.towers.append(tower)
                    self.gold -= cost
            
            # Reset drag state
            self.dragging_tower = False
            self.drag_tower_type = None
            self.drag_start_pos = None
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for drag-and-drop preview"""
        self.mouse_pos = pos
    

                
    def can_place_tower(self, x, y):
        # Check if too close to path
        for px, py in self.path:
            if math.sqrt((px - x)**2 + (py - y)**2) < 50:
                return False
                
        # Check if too close to other towers
        for tower in self.towers:
            if math.sqrt((tower.x - x)**2 + (tower.y - y)**2) < 50:
                return False
                
        # Check if in UI area
        if y > SCREEN_HEIGHT - 100:
            return False
            
        return True
        
    def draw(self):
        # Draw grid background (code-generated)
        if self.background_surface:
            self.screen.blit(self.background_surface, (0, 0))
        else:
            # Fallback to solid color if grid creation failed
            self.screen.fill(DARK_GREEN)
            
        # Draw portal (enemy spawn point)
        self.portal.draw(self.screen)
        
        # Draw blocky path aligned with grid
        path_color = (101, 67, 33)  # Brown color for path blocks
        path_border_color = (80, 52, 25)  # Darker brown for borders
        
        # Draw path blocks for each segment
        for i in range(len(self.path) - 1):
            start_point = self.path[i]
            end_point = self.path[i + 1]
            
            # Get grid positions
            start_grid_x = start_point[0] // self.grid_size
            start_grid_y = start_point[1] // self.grid_size
            end_grid_x = end_point[0] // self.grid_size
            end_grid_y = end_point[1] // self.grid_size
            
            # Draw path blocks between start and end points
            if start_grid_x == end_grid_x:
                # Vertical segment
                min_y = min(start_grid_y, end_grid_y)
                max_y = max(start_grid_y, end_grid_y)
                for y in range(min_y, max_y + 1):
                    grid_x = start_grid_x * self.grid_size
                    grid_y = y * self.grid_size
                    path_rect = pygame.Rect(grid_x, grid_y, self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, path_color, path_rect)
                    pygame.draw.rect(self.screen, path_border_color, path_rect, 2)
            elif start_grid_y == end_grid_y:
                # Horizontal segment
                min_x = min(start_grid_x, end_grid_x)
                max_x = max(start_grid_x, end_grid_x)
                for x in range(min_x, max_x + 1):
                    grid_x = x * self.grid_size
                    grid_y = start_grid_y * self.grid_size
                    path_rect = pygame.Rect(grid_x, grid_y, self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, path_color, path_rect)
                    pygame.draw.rect(self.screen, path_border_color, path_rect, 2)
            else:
                # Diagonal segment - draw L-shaped path
                # First horizontal part
                min_x = min(start_grid_x, end_grid_x)
                max_x = max(start_grid_x, end_grid_x)
                for x in range(min_x, max_x + 1):
                    grid_x = x * self.grid_size
                    grid_y = start_grid_y * self.grid_size
                    path_rect = pygame.Rect(grid_x, grid_y, self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, path_color, path_rect)
                    pygame.draw.rect(self.screen, path_border_color, path_rect, 2)
                
                # Then vertical part
                min_y = min(start_grid_y, end_grid_y)
                max_y = max(start_grid_y, end_grid_y)
                for y in range(min_y, max_y + 1):
                    grid_x = end_grid_x * self.grid_size
                    grid_y = y * self.grid_size
                    path_rect = pygame.Rect(grid_x, grid_y, self.grid_size, self.grid_size)
                    pygame.draw.rect(self.screen, path_color, path_rect)
                    pygame.draw.rect(self.screen, path_border_color, path_rect, 2)
        
        # Draw castle at the end of the path (what we're defending)
        castle_sprite = assets.get_image('castle')
        if castle_sprite and castle_sprite.get_width() > 0:
            castle_pos = self.path[-1]  # Last point in the path
            castle_rect = castle_sprite.get_rect()
            castle_rect.center = castle_pos
            self.screen.blit(castle_sprite, castle_rect)
        else:
            # Fallback castle drawing
            castle_x, castle_y = self.path[-1]
            pygame.draw.rect(self.screen, GRAY, (castle_x - 30, castle_y - 30, 60, 60))
            pygame.draw.polygon(self.screen, RED, [(castle_x, castle_y - 50), 
                                                 (castle_x - 20, castle_y - 30), 
                                                 (castle_x + 20, castle_y - 30)])
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen, tower == self.selected_tower)
            
        # Draw coin pickups
        for coin_pickup in self.coin_pickups:
            coin_pickup.draw(self.screen)
            
        # Draw drag preview
        if self.dragging_tower and self.drag_tower_type:
            mouse_x, mouse_y = self.mouse_pos
            
            # Snap preview to grid
            grid_x = (mouse_x // self.grid_size) * self.grid_size + self.grid_size // 2
            grid_y = (mouse_y // self.grid_size) * self.grid_size + self.grid_size // 2
            
            # Check if position is valid
            is_valid = self.can_place_tower(grid_x, grid_y)
            
            # Draw placement preview circle
            preview_color = GREEN if is_valid else RED
            pygame.draw.circle(self.screen, preview_color, (grid_x, grid_y), 30, 3)
            
            # Draw tower preview (semi-transparent)
            tower_sprite = assets.get_tower_sprite(self.drag_tower_type, 1)
            if tower_sprite and tower_sprite.get_width() > 0:
                # Create semi-transparent version
                preview_sprite = tower_sprite.copy()
                preview_sprite.set_alpha(128)  # Semi-transparent
                
                # Tint based on validity
                if not is_valid:
                    # Add red tint for invalid placement
                    red_overlay = pygame.Surface(preview_sprite.get_size())
                    red_overlay.fill(RED)
                    red_overlay.set_alpha(64)
                    preview_sprite.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_ADD)
                
                sprite_rect = preview_sprite.get_rect()
                sprite_rect.center = (grid_x, grid_y)
                self.screen.blit(preview_sprite, sprite_rect)
            else:
                # Fallback preview drawing
                preview_color = (0, 255, 0, 128) if is_valid else (255, 0, 0, 128)
                pygame.draw.circle(self.screen, preview_color[:3], (grid_x, grid_y), 25)
            
        # Draw tower ranges if selected
        if self.selected_tower:
            pygame.draw.circle(self.screen, (255, 255, 255, 50), 
                             (int(self.selected_tower.x), int(self.selected_tower.y)), 
                             self.selected_tower.range, 2)
            
        # Draw UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def draw_ui(self):
        # UI background
        pygame.draw.rect(self.screen, BLACK, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, WHITE, (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 2)
        
        # Tower selection buttons
        tower_types = [("Archer", "archer", TOWER_COSTS["archer"]), 
                      ("Magic", "magic", TOWER_COSTS["magic"]), 
                      ("Cannon", "cannon", TOWER_COSTS["cannon"])]
        for i, (name, tower_type, cost) in enumerate(tower_types):
            x = 20 + i * 120
            
            # Try to use button sprites
            if self.selected_tower_type == tower_type:
                button_sprite = assets.get_image('button_pressed')
            else:
                button_sprite = assets.get_image('button_normal')
            
            if button_sprite and button_sprite.get_width() > 0:
                self.screen.blit(button_sprite, (x, SCREEN_HEIGHT - 80))
            else:
                # Fallback button drawing
                color = BLUE if self.selected_tower_type == tower_type else GRAY
                pygame.draw.rect(self.screen, color, (x, SCREEN_HEIGHT - 80, 100, 30))
                pygame.draw.rect(self.screen, WHITE, (x, SCREEN_HEIGHT - 80, 100, 30), 2)
            
            text = self.small_font.render(f"{name} (${cost})", True, WHITE)
            self.screen.blit(text, (x + 5, SCREEN_HEIGHT - 75))
            
        # Next wave button
        if self.wave_complete:
            button_sprite = assets.get_image('button_hover')
            if button_sprite and button_sprite.get_width() > 0:
                self.screen.blit(button_sprite, (400, SCREEN_HEIGHT - 80))
            else:
                pygame.draw.rect(self.screen, GREEN, (400, SCREEN_HEIGHT - 80, 100, 30))
                pygame.draw.rect(self.screen, WHITE, (400, SCREEN_HEIGHT - 80, 100, 30), 2)
            text = self.small_font.render("Next Wave", True, WHITE)
            self.screen.blit(text, (415, SCREEN_HEIGHT - 75))
            
        # Upgrade button
        if self.selected_tower and self.selected_tower.level < 3:
            cost = self.selected_tower.cost * self.selected_tower.level
            button_sprite = assets.get_image('button_normal')
            if button_sprite and button_sprite.get_width() > 0:
                self.screen.blit(button_sprite, (520, SCREEN_HEIGHT - 80))
            else:
                pygame.draw.rect(self.screen, ORANGE, (520, SCREEN_HEIGHT - 80, 100, 30))
                pygame.draw.rect(self.screen, WHITE, (520, SCREEN_HEIGHT - 80, 100, 30), 2)
            text = self.small_font.render(f"Upgrade (${cost})", True, WHITE)
            self.screen.blit(text, (525, SCREEN_HEIGHT - 75))
            
        # Game stats with icons
        stats_data = [
            (f"${self.gold}", 'coin_icon'),
            (f"{self.lives}", 'heart_icon'),
            (f"Wave {self.wave}", 'wave_icon'),
            (f"Score: {self.score}", None)
        ]
        
        for i, (stat_text, icon_name) in enumerate(stats_data):
            y_pos = SCREEN_HEIGHT - 90 + i * 20
            x_pos = SCREEN_WIDTH - 200
            
            # Draw icon if available
            if icon_name:
                icon = assets.get_image(icon_name)
                if icon and icon.get_width() > 0:
                    self.screen.blit(icon, (x_pos - 25, y_pos - 2))
            
            text = self.small_font.render(stat_text, True, WHITE)
            self.screen.blit(text, (x_pos, y_pos))
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.small_font.render("Press R to restart or Q to quit", True, WHITE)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60))
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 20))
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 20))
        
    def restart(self):
        # Reinitialize the game with fresh grid background
        self.__init__()
