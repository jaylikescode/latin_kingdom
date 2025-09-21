import pygame
import math
from constants import *
from projectile import Projectile
from assets import assets

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        self.last_shot = 0
        
        if tower_type == "archer":
            self.damage = 15
            self.range = 80
            self.fire_rate = 1000  # milliseconds
            self.cost = TOWER_COSTS["archer"]
            self.color = GREEN
            self.projectile_color = YELLOW
            self.projectile_speed = 8
        elif tower_type == "magic":
            self.damage = 25
            self.range = 70
            self.fire_rate = 1500
            self.cost = TOWER_COSTS["magic"]
            self.color = BLUE
            self.projectile_color = PURPLE
            self.projectile_speed = 10
        elif tower_type == "cannon":
            self.damage = 40
            self.range = 100
            self.fire_rate = 2000
            self.cost = TOWER_COSTS["cannon"]
            self.color = RED
            self.projectile_color = BLACK
            self.projectile_speed = 6
            
        self.projectiles = []
        self.visual_effects = []
        
    def can_shoot(self, current_time):
        return current_time - self.last_shot >= self.fire_rate
        
    def find_target(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            if not enemy.alive:
                continue
                
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
                
        return closest_enemy
        
    def shoot(self, target, current_time):
        if self.can_shoot(current_time):
            # Play tower shooting sound effect
            assets.play_sound('tower_shoot')
            
            self.projectiles.append(Projectile(self.x, self.y, target, self.damage, self.projectile_color, self.projectile_speed, self.tower_type))
            self.last_shot = current_time
            
    def update(self, enemies, current_time):
        # Update projectiles
        for projectile in self.projectiles[:]:
            hit, effect = projectile.update(enemies)
            if hit or not projectile.active:
                if effect:  # Only add effect if it exists (not None for archer towers)
                    self.visual_effects.append(effect)
                self.projectiles.remove(projectile)
                
        # Update visual effects (explosions and sparkles)
        for effect in self.visual_effects[:]:
            if not effect.update():
                self.visual_effects.remove(effect)
                
        # Find and shoot at target
        target = self.find_target(enemies)
        if target:
            self.shoot(target, current_time)
            
    def upgrade(self):
        if self.level < 3:
            self.level += 1
            self.damage = int(self.damage * 1.5)
            self.range = int(self.range * 1.1)
            return self.cost * self.level
        return 0
        
    def draw(self, screen, selected=False):
        # Try to get sprite from assets
        sprite = assets.get_tower_sprite(self.tower_type, self.level)
        
        if sprite and sprite.get_width() > 0:  # Valid sprite loaded
            # Draw sprite centered
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (int(self.x), int(self.y))
            screen.blit(sprite, sprite_rect)
            
            # Draw level indicator only when selected
            if selected and self.level > 1:
                font = pygame.font.Font(None, 28)
                level_text = font.render(str(self.level), True, WHITE)
                # Draw background circle for better visibility
                pygame.draw.circle(screen, BLACK, (int(self.x + 25), int(self.y - 25)), 12)
                pygame.draw.circle(screen, YELLOW, (int(self.x + 25), int(self.y - 25)), 10)
                screen.blit(level_text, (self.x + 19, self.y - 33))
        else:
            # Fallback to colored circle
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 20)
            pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 20, 2)
            
            # Draw level indicator for fallback rendering (always shown for fallback)
            font = pygame.font.Font(None, 24)
            level_text = font.render(str(self.level), True, WHITE)
            screen.blit(level_text, (self.x - 6, self.y - 8))
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
            
        # Draw visual effects (explosions and sparkles)
        for effect in self.visual_effects:
            effect.draw(screen)
