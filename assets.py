import pygame
import os
from constants import *

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.base_path = os.path.dirname(__file__)
        self.assets_loaded = False
        
        # Initialize pygame mixer for sound
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error:
            print("Warning: Could not initialize audio mixer")
    
    def load_image(self, filename, size=None, fallback_color=None, fallback_size=(32, 32)):
        """Load image with fallback to colored rectangle if image not found"""
        filepath = os.path.join(self.base_path, filename)
        
        try:
            if os.path.exists(filepath):
                image = pygame.image.load(filepath)
                # Try convert_alpha first, fallback to convert if display not initialized
                try:
                    image = image.convert_alpha()
                except pygame.error:
                    try:
                        image = image.convert()
                    except pygame.error:
                        pass  # Use original image if convert fails
                if size:
                    image = pygame.transform.scale(image, size)
                return image
            else:
                # Create fallback colored surface
                surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
                if fallback_color:
                    surface.fill(fallback_color)
                return surface
        except Exception as e:
            pass  # Silently fall back to colored surface
            # Create fallback colored surface on any error
            surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
            if fallback_color:
                surface.fill(fallback_color)
            return surface
    
    def load_sound(self, filename, fallback_volume=0.3):
        """Load sound with fallback to silent sound if file not found"""
        filepath = os.path.join(self.base_path, filename)
        
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(fallback_volume)
                return sound
            else:

                return None
        except Exception as e:

            return None
    
    def load_all_assets(self):
        """Load all game assets"""
        
        # Background
        self.images['background'] = self.load_image('background.png', 
                                                   (SCREEN_WIDTH, SCREEN_HEIGHT), 
                                                   DARK_GREEN)
        
        # Castle
        self.images['castle'] = self.load_image('castle.png', (130, 130), GRAY)
        
        # Enemy sprites - using single images (no separate walk animations)
        enemy_size = (32, 32)
        self.images['goblin'] = self.load_image('goblin.png', enemy_size, GREEN)
        self.images['orc'] = self.load_image('orc.png', enemy_size, DARK_GREEN)
        self.images['troll'] = self.load_image('troll.png', (40, 40), BROWN)
        self.images['dragon'] = self.load_image('dragon.png', (50, 50), RED)
        
        # Tower sprites - single image per type, level shown via UI
        tower_size = (64, 64)
        self.images['archer_tower'] = self.load_image('archer_tower.png', tower_size, BROWN)
        self.images['magic_tower'] = self.load_image('magic_tower.png', tower_size, PURPLE)
        self.images['cannon_tower'] = self.load_image('cannon_tower.png', tower_size, GRAY)
        
        # Projectiles
        self.images['arrow'] = self.load_image('arrow.png', (16, 16), YELLOW, (8, 8))
        self.images['magic_bolt'] = self.load_image('magic_bolt.png', (16, 16), PURPLE, (8, 8))
        self.images['cannonball'] = self.load_image('cannonball.png', (16, 16), BLACK, (8, 8))
        
        # UI Elements
        self.images['button_normal'] = self.load_image('button_normal.png', (100, 30), GRAY)
        self.images['button_hover'] = self.load_image('button_hover.png', (100, 30), BLUE)
        self.images['button_pressed'] = self.load_image('button_pressed.png', (100, 30), DARK_GREEN)
        
        self.images['coin_icon'] = self.load_image('coin_icon.png', (24, 24), YELLOW, (20, 20))
        self.images['coin_pickup'] = self.load_image('coin_pickup.png', (32, 32), YELLOW, (24, 24))
        self.images['heart_icon'] = self.load_image('heart_icon.png', (24, 24), RED, (20, 20))
        self.images['wave_icon'] = self.load_image('wave_icon.png', (24, 24), BLUE, (20, 20))
        
        # Effects
        self.images['explosion_1'] = self.load_image('explosion_1.png', (32, 32), ORANGE, (20, 20))
        self.images['explosion_2'] = self.load_image('explosion_2.png', (32, 32), RED, (20, 20))
        self.images['explosion_3'] = self.load_image('explosion_3.png', (32, 32), YELLOW, (20, 20))
        self.images['explosion_4'] = self.load_image('explosion_4.png', (32, 32), WHITE, (20, 20))
        
        # Path segments
        self.images['path_straight'] = self.load_image('path_straight.png', (40, 40), BROWN, (20, 20))
        self.images['path_curve'] = self.load_image('path_curve.png', (40, 40), BROWN, (20, 20))
        
        # Portal (enemy spawn point)
        self.images['portal'] = self.load_image('portal.gif', (80, 80), PURPLE, (60, 60))
        
        # Sound effects
        self.sounds['coin_pickup'] = self.load_sound('coin_pickup.mp3', 0.4)
        self.sounds['coin_pickup_alt'] = self.load_sound('coin_pickup.wav', 0.4)  # Alternative format
        self.sounds['enemy_death'] = self.load_sound('enemy_death.mp3', 0.7)
        self.sounds['tower_shoot'] = self.load_sound('tower_shoot.mp3', 0.3)
        
        # Mark assets as loaded
        self.assets_loaded = True
    
    def get_image(self, name):
        """Get loaded image by name"""
        if not self.assets_loaded:
            self.load_all_assets()
        return self.images.get(name, None)
    
    def get_sound(self, name):
        """Get loaded sound by name"""
        if not self.assets_loaded:
            self.load_all_assets()
        return self.sounds.get(name, None)
        
    def play_sound(self, name):
        """Play a sound effect by name"""
        sound = self.get_sound(name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass  # Silently ignore sound errors
    
    def get_enemy_sprite(self, enemy_type, frame=0):
        """Get enemy sprite (frame parameter ignored, using single images)"""
        return self.get_image(enemy_type)
    
    def get_tower_sprite(self, tower_type, level):
        """Get tower sprite based on type (level ignored, shown via UI)"""
        return self.get_image(f"{tower_type}_tower")
    
    def get_projectile_sprite(self, tower_type):
        """Get projectile sprite based on tower type"""
        projectile_map = {
            'archer': 'arrow',
            'magic': 'magic_bolt', 
            'cannon': 'cannonball'
        }
        return self.get_image(projectile_map.get(tower_type, 'arrow'))

# Global asset manager instance
assets = AssetManager()
