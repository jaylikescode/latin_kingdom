import pygame
import math
from constants import *
from assets import assets

class Enemy:
    def __init__(self, enemy_type, path):
        self.enemy_type = enemy_type
        self.path = path
        self.path_index = 0
        self.x = path[0][0]
        self.y = path[0][1]
        self.target_x = path[1][0]
        self.target_y = path[1][1]
        
        # Enemy stats based on type
        if enemy_type == "goblin":
            self.max_health = 50
            self.speed = 2
            self.reward = 10
            self.color = GREEN
            self.size = 15
        elif enemy_type == "orc":
            self.max_health = 100
            self.speed = 1.5
            self.reward = 20
            self.color = DARK_GREEN
            self.size = 20
        elif enemy_type == "troll":
            self.max_health = 200
            self.speed = 1.6
            self.reward = 40
            self.color = BROWN
            self.size = 25
        elif enemy_type == "dragon":
            self.max_health = 500
            self.speed = 3
            self.reward = 100
            self.color = RED
            self.size = 30
            
        self.health = self.max_health
        self.alive = True
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 500  # milliseconds per frame
        
    def update(self):
        if not self.alive:
            return
            
        # Move towards target point
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 5:  # Reached target point
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.alive = False
                return "reached_end"
            else:
                self.target_x = self.path[self.path_index][0]
                self.target_y = self.path[self.path_index][1]
        else:
            # Move towards target
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        return None
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
        
    def update_animation(self):
        """Update animation frame for walking"""
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer >= self.animation_speed:
            self.animation_frame = 1 if self.animation_frame == 0 else 0
            self.animation_timer = current_time
    
    def draw(self, screen):
        if self.alive:
            # Update animation
            self.update_animation()
            
            # Try to get sprite from assets
            sprite = assets.get_enemy_sprite(self.enemy_type, self.animation_frame)
            
            if sprite and sprite.get_width() > 0:  # Valid sprite loaded
                # Draw sprite centered
                sprite_rect = sprite.get_rect()
                sprite_rect.center = (int(self.x), int(self.y))
                screen.blit(sprite, sprite_rect)
            else:
                # Fallback to colored circle
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            
            # Draw health bar
            bar_width = self.size * 2
            bar_height = 4
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, (int(self.x) - bar_width//2, int(self.y) - self.size - 15, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (int(self.x) - bar_width//2, int(self.y) - self.size - 15, bar_width * health_ratio, bar_height))
