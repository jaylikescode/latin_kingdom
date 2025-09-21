import pygame
import os
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
from constants import *
from assets import assets

class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 100  # milliseconds between frames
        self.load_gif_frames()
        
    def load_gif_frames(self):
        """Load and convert GIF frames to pygame surfaces"""
        try:
            # Load the GIF using PIL (if available)
            gif_path = os.path.join(os.path.dirname(__file__), 'portal.gif')
            if PIL_AVAILABLE and os.path.exists(gif_path):
                with Image.open(gif_path) as gif:
                    # Extract all frames from the GIF
                    for frame_num in range(gif.n_frames):
                        gif.seek(frame_num)
                        # Convert to RGB mode to handle transparency properly
                        frame = gif.convert('RGBA')
                        # Resize frame
                        frame = frame.resize((80, 80), Image.Resampling.LANCZOS)
                        
                        # Convert PIL image to pygame surface
                        mode = frame.mode
                        size = frame.size
                        data = frame.tobytes()
                        
                        pygame_surface = pygame.image.fromstring(data, size, mode)
                        pygame_surface = pygame_surface.convert_alpha()
                        
                        self.frames.append(pygame_surface)
                        
            # If no frames loaded or file doesn't exist, create fallback
            if not self.frames:
                self.create_fallback_animation()
                
        except Exception as e:
            # Create fallback animation on any error
            self.create_fallback_animation()
    
    def create_fallback_animation(self):
        """Create a fallback portal animation using pygame shapes"""
        colors = [PURPLE, BLUE, DARK_BLUE, PURPLE, BLUE]
        
        for i, color in enumerate(colors):
            surface = pygame.Surface((80, 80), pygame.SRCALPHA)
            
            # Draw animated portal rings
            ring_size = 40 + (i * 5)
            pygame.draw.circle(surface, color, (40, 40), ring_size, 3)
            pygame.draw.circle(surface, (color[0]//2, color[1]//2, color[2]//2), (40, 40), ring_size - 10, 2)
            
            # Add center glow
            center_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
            pygame.draw.circle(surface, center_color, (40, 40), 15)
            
            self.frames.append(surface)
    
    def update(self):
        """Update portal animation"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = current_time
    
    def draw(self, screen):
        """Draw the current portal frame"""
        if self.frames:
            current_frame_surface = self.frames[self.current_frame]
            # Center the portal at the given position
            rect = current_frame_surface.get_rect()
            rect.center = (self.x, self.y)
            screen.blit(current_frame_surface, rect)
