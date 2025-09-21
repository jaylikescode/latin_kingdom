# 🏰 Kingdom Defender

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python recreation of the classic MSN tower defense game where you defend your castle from waves of enemies!

## 🎮 Game Preview

Defend your kingdom by strategically placing towers to stop waves of enemies from reaching your castle. Each enemy type has different strengths and weaknesses, and each tower type has unique capabilities.

## How to Play

### Objective
Defend your castle from waves of enemies by strategically placing and upgrading towers along their path. Don't let enemies reach your castle or you'll lose lives!

### Controls
- **Left Click**: Place towers, select towers, or click UI buttons
- **R**: Restart game (when game over)
- **Q**: Quit game (when game over)

### Tower Types

1. **Archer Tower** ($50)
   - Moderate damage and range
   - Fast firing rate
   - Good all-around choice

2. **Magic Tower** ($100)
   - High damage
   - Medium range and firing rate
   - Effective against stronger enemies

3. **Cannon Tower** ($150)
   - Very high damage
   - Long range but slow firing rate
   - Best for heavy enemies

### Enemy Types

- **Goblin** (Green): Fast but weak, gives $10
- **Orc** (Dark Green): Moderate health and speed, gives $20  
- **Troll** (Brown): High health but slow, gives $40
- **Dragon** (Red): Very high health, slow, gives $100

### Gameplay Tips

1. **Place towers strategically** - Position them where they can hit enemies for the longest time
2. **Upgrade your towers** - Click on a tower and then the upgrade button to increase damage and range
3. **Mix tower types** - Use different towers for different situations
4. **Manage your gold** - You earn gold by defeating enemies and completing waves
5. **Watch the path** - Enemies follow the brown path from left to right

### Wave System

- Each wave has more enemies than the last
- Later waves introduce stronger enemy types
- You get bonus gold for completing each wave
- Click "Next Wave" when ready to continue

### Game Over

You lose when enemies reduce your lives to 0. Each enemy that reaches your castle costs you 1 life.

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jaylikescode/latin_kingdom.git
   cd latin_kingdom
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install pygame directly:
   ```bash
   pip install pygame
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## 📋 Requirements

- Python 3.6+
- Pygame 2.0+

## 📁 Project Structure

```
kingdom_defender/
├── main.py              # Main entry point and game loop
├── game.py              # Main Game class with game logic
├── enemy.py             # Enemy classes and behavior
├── tower.py             # Tower classes and combat mechanics
├── projectile.py        # Projectile class for tower attacks
├── explosion.py         # Explosion effects
├── portal.py            # Enemy spawn portal
├── coin_pickup.py       # Coin collection system
├── assets.py            # Asset loading and management
├── constants.py         # Game constants and settings
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
└── assets/             # Game assets
    ├── *.png           # Sprite images
    ├── *.gif           # Animations
    ├── *.mp3           # Sound effects
    └── *.md            # Asset documentation
```

## 🎯 Features

- **Multiple Tower Types**: Archer, Magic, and Cannon towers with unique abilities
- **Diverse Enemies**: Goblins, Orcs, Trolls, and Dragons with different stats
- **Tower Upgrades**: Enhance your defenses with improved damage and range
- **Wave System**: Progressive difficulty with increasing enemy counts
- **Sound Effects**: Immersive audio feedback for actions
- **Particle Effects**: Visual explosions and animations
- **Modular Code**: Clean, organized codebase for easy modification

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Report bugs** by opening an issue
2. **Suggest features** or improvements
3. **Submit pull requests** with bug fixes or new features
4. **Improve documentation** or add comments to code

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎮 Enjoy the Game!

Defend your kingdom and have fun! If you encounter any issues or have suggestions, feel free to open an issue on GitHub.
