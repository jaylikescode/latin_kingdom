import pygame
import math
from assets import assets

class CoinPickup:
    """Visual effect for coin pickups when enemies are defeated"""
    
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.start_y = y
        self.value = value
        self.alive = True
        
        # Animation properties
        self.animation_time = 0
        self.duration = 1500  # 1.5 seconds
        self.float_height = 30  # How high the coin floats up
        self.fade_start = 1000  # When to start fading
        
        # Play coin pickup sound effect
        self.play_pickup_sound()
        
    def play_pickup_sound(self):
        """Play coin pickup sound effect"""
        # Try coin_pickup sound first, then fallback to alternative format
        assets.play_sound('coin_pickup')
        if not assets.get_sound('coin_pickup'):
            assets.play_sound('coin_pickup_alt')
        
    def update(self):
        """Update the coin pickup animation"""
        self.animation_time += 16  # Roughly 60 FPS
        
        if self.animation_time >= self.duration:
            self.alive = False
            return
            
        # Float upward with easing
        progress = self.animation_time / self.duration
        # Use sine wave for smooth floating motion
        float_progress = math.sin(progress * math.pi / 2)  # Ease out
        self.y = self.start_y - (float_progress * self.float_height)
        
    def draw(self, screen):
        """Draw the coin pickup effect"""
        if not self.alive:
            return
            
        # Get coin pickup sprite
        coin_sprite = assets.get_image('coin_pickup')
        
        if coin_sprite and coin_sprite.get_width() > 0:
            # Calculate alpha for fading effect
            alpha = 255
            if self.animation_time > self.fade_start:
                fade_progress = (self.animation_time - self.fade_start) / (self.duration - self.fade_start)
                alpha = int(255 * (1 - fade_progress))
                
            # Create a copy of the sprite for alpha blending
            faded_sprite = coin_sprite.copy()
            faded_sprite.set_alpha(alpha)
            
            # Center the sprite on the position
            sprite_rect = faded_sprite.get_rect()
            sprite_rect.center = (int(self.x), int(self.y))
            screen.blit(faded_sprite, sprite_rect)
            
            # Draw gold value text
            font = pygame.font.Font(None, 20)
            text_color = (255, 255, 0, alpha)  # Yellow with fade
            text = font.render(f"+${self.value}", True, (255, 255, 0))
            
            # Apply alpha to text as well
            text.set_alpha(alpha)
            text_rect = text.get_rect()
            text_rect.center = (int(self.x), int(self.y - 25))
            screen.blit(text, text_rect)
