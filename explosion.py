import pygame
import math
import os
from constants import *

class VisualEffect:
    def __init__(self, x, y, effect_type="explosion"):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.current_frame = 0
        self.animation_speed = 3  # Frames to wait before advancing animation
        self.frame_counter = 0
        self.active = True
        self.frames = []
        
        # Load appropriate effect frames based on type
        if effect_type == "explosion":
            self.load_explosion_frames()
        elif effect_type == "sparkle":
            self.load_sparkle_frames()
        else:
            self.active = False  # No effect
        
    def load_explosion_frames(self):
        """Create explosion animation frames"""
        # Since PIL is not available, create a beautiful animated explosion using pygame
        self.create_animated_explosion()
            
    def create_animated_explosion(self):
        """Create beautiful animated explosion frames"""
        # Create a more sophisticated explosion animation
        explosion_data = [
            # Frame 1: Initial flash
            {'circles': [{'color': (255, 255, 255), 'size': 8, 'alpha': 255}]},
            # Frame 2: Growing fireball  
            {'circles': [{'color': (255, 255, 100), 'size': 15, 'alpha': 255},
                        {'color': (255, 200, 0), 'size': 12, 'alpha': 200}]},
            # Frame 3: Expanding explosion
            {'circles': [{'color': (255, 150, 0), 'size': 22, 'alpha': 255},
                        {'color': (255, 100, 0), 'size': 18, 'alpha': 200},
                        {'color': (255, 255, 100), 'size': 10, 'alpha': 150}]},
            # Frame 4: Peak explosion
            {'circles': [{'color': (255, 50, 0), 'size': 28, 'alpha': 255},
                        {'color': (255, 100, 0), 'size': 24, 'alpha': 200},
                        {'color': (255, 200, 50), 'size': 16, 'alpha': 180}]},
            # Frame 5: Fading
            {'circles': [{'color': (200, 50, 0), 'size': 30, 'alpha': 200},
                        {'color': (150, 75, 0), 'size': 25, 'alpha': 150},
                        {'color': (100, 50, 0), 'size': 18, 'alpha': 100}]},
            # Frame 6: Smoke
            {'circles': [{'color': (100, 100, 100), 'size': 25, 'alpha': 120},
                        {'color': (80, 80, 80), 'size': 20, 'alpha': 80}]},
            # Frame 7: Dissipating
            {'circles': [{'color': (60, 60, 60), 'size': 20, 'alpha': 60}]},
            # Frame 8: Gone
            {'circles': [{'color': (40, 40, 40), 'size': 15, 'alpha': 30}]}
        ]
        
        for frame_data in explosion_data:
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            
            for circle in frame_data['circles']:
                # Create a surface for this circle with alpha
                circle_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, circle['color'], (32, 32), circle['size'])
                circle_surface.set_alpha(circle['alpha'])
                surface.blit(circle_surface, (0, 0))
                
            self.frames.append(surface)
            
    def load_sparkle_frames(self):
        """Create purple sparkle animation frames for magic towers"""
        import random
        
        sparkle_data = [
            # Frame 1: Initial sparkle burst
            {'particles': 8, 'base_color': (255, 150, 255), 'size_range': (2, 4), 'alpha': 255},
            # Frame 2: Expanding sparkles
            {'particles': 12, 'base_color': (200, 100, 255), 'size_range': (1, 3), 'alpha': 220},
            # Frame 3: Peak sparkles
            {'particles': 16, 'base_color': (150, 50, 255), 'size_range': (1, 2), 'alpha': 200},
            # Frame 4: Sustained sparkles
            {'particles': 14, 'base_color': (140, 70, 220), 'size_range': (1, 2), 'alpha': 180},
            # Frame 5: Fading sparkles
            {'particles': 12, 'base_color': (120, 80, 200), 'size_range': (1, 2), 'alpha': 150},
            # Frame 6: More fading
            {'particles': 10, 'base_color': (110, 70, 180), 'size_range': (1, 1), 'alpha': 120},
            # Frame 7: Final sparkles
            {'particles': 8, 'base_color': (100, 60, 150), 'size_range': (1, 1), 'alpha': 100},
            # Frame 8: Dissipating
            {'particles': 6, 'base_color': (90, 50, 130), 'size_range': (1, 1), 'alpha': 70},
            # Frame 9: Last sparkles
            {'particles': 4, 'base_color': (80, 40, 120), 'size_range': (1, 1), 'alpha': 50}
        ]
        
        # Set animation speed slower for longer-lasting sparkles
        self.animation_speed = 5
        
        for frame_data in sparkle_data:
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            
            # Create random sparkle positions for this frame
            random.seed(42)  # Consistent sparkle pattern
            for _ in range(frame_data['particles']):
                # Random position around center
                angle = random.uniform(0, 6.28)  # 2 * pi
                distance = random.uniform(5, 20)
                x = 32 + int(distance * math.cos(angle))
                y = 32 + int(distance * math.sin(angle))
                
                # Ensure position is within bounds
                x = max(1, min(63, x))
                y = max(1, min(63, y))
                
                size = random.randint(*frame_data['size_range'])
                
                # Create sparkle with slight color variation
                color_var = random.randint(-30, 30)
                color = (
                    max(0, min(255, frame_data['base_color'][0] + color_var)),
                    max(0, min(255, frame_data['base_color'][1] + color_var)),
                    max(0, min(255, frame_data['base_color'][2] + color_var))
                )
                
                # Draw sparkle particle
                particle_surface = pygame.Surface((size*2+2, size*2+2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size+1, size+1), size)
                particle_surface.set_alpha(frame_data['alpha'])
                surface.blit(particle_surface, (x-size-1, y-size-1))
                
            self.frames.append(surface)
    
    def update(self):
        """Update the explosion animation"""
        if not self.active:
            return False
            
        self.frame_counter += 1
        
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame += 1
            
            # Check if animation is complete
            if self.current_frame >= len(self.frames):
                self.active = False
                return False
                
        return True
    
    def draw(self, screen):
        """Draw the current explosion frame"""
        if self.active and self.current_frame < len(self.frames):
            frame = self.frames[self.current_frame]
            # Center the explosion on the position
            rect = frame.get_rect()
            rect.center = (int(self.x), int(self.y))
            screen.blit(frame, rect)
