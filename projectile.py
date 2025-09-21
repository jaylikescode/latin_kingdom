import pygame
import math
from constants import *
from assets import assets
from explosion import VisualEffect

class Projectile:
    def __init__(self, x, y, target, damage, color, speed, tower_type="archer"):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = speed
        self.tower_type = tower_type
        self.active = True
        self.angle = 0
        
    def update(self, enemies):
        if not self.active or not self.target.alive:
            self.active = False
            return False, None
            
        # Move towards target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 5:  # Hit target
            # Create appropriate visual effect based on tower type
            effect = None
            if self.tower_type == "cannon":
                effect = VisualEffect(self.target.x, self.target.y, "explosion")
            elif self.tower_type == "magic":
                effect = VisualEffect(self.target.x, self.target.y, "sparkle")
            # archer tower gets no effect (effect stays None)
            
            if self.target.take_damage(self.damage):
                self.active = False
                return True, effect  # Enemy died
            self.active = False
            return False, effect  # Hit but enemy still alive
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            # Calculate angle for sprite rotation
            self.angle = math.degrees(math.atan2(dy, dx))
            
        return False, None
        
    def draw(self, screen):
        if self.active:
            # Try to get sprite from assets
            sprite = assets.get_projectile_sprite(self.tower_type)
            
            if sprite and sprite.get_width() > 0:  # Valid sprite loaded
                # Rotate sprite to face movement direction
                rotated_sprite = pygame.transform.rotate(sprite, -self.angle)
                sprite_rect = rotated_sprite.get_rect()
                sprite_rect.center = (int(self.x), int(self.y))
                screen.blit(rotated_sprite, sprite_rect)
            else:
                # Fallback to colored circle
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
