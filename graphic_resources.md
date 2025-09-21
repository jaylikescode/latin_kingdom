# Kingdom Defender - Graphics Resources

## Required PNG Files

Place these PNG files directly in the `kingdom defender` folder for the game to automatically use them.

### Background & Environment
- `background.png` - Main game background (1000x700px)
- `castle.png` - Castle sprite (60x60px)

### Enemy Sprites
- `goblin.png` - Goblin sprite (32x32px)
- `orc.png` - Orc sprite (32x32px)
- `troll.png` - Troll sprite (40x40px)
- `dragon.png` - Dragon sprite (50x50px)

### Tower Sprites (64x64px)
- `archer_tower.png` - Archer tower (all levels use same sprite)
- `magic_tower.png` - Magic tower (all levels use same sprite)
- `cannon_tower.png` - Cannon tower (all levels use same sprite)

**Note:** Tower levels are shown with a yellow number badge only when the tower is selected

### Projectile Sprites (16x16px)
- `arrow.png` - Archer tower projectile
- `magic_bolt.png` - Magic tower projectile
- `cannonball.png` - Cannon tower projectile

### UI Elements
- `button_normal.png` - Normal button state (100x30px)
- `button_hover.png` - Hover button state (100x30px)
- `button_pressed.png` - Pressed button state (100x30px)

### Icons (24x24px)
- `coin_icon.png` - Gold/money icon
- `heart_icon.png` - Lives icon
- `wave_icon.png` - Wave indicator icon

### Optional Effect Sprites
- `explosion_1.png` to `explosion_4.png` - Explosion animation frames (32x32px)
- `path_straight.png` - Straight path segment (40x40px)
- `path_curve.png` - Curved path segment (40x40px)

## How It Works

1. **Automatic Detection**: The game automatically checks for PNG files when it starts
2. **Fallback System**: If a PNG isn't found, the game uses colored shapes as fallback
3. **Hot Swapping**: Add PNG files and restart the game to see them immediately
4. **Simplified Graphics**: Each enemy and tower uses a single sprite image
5. **Rotation**: Projectiles automatically rotate to face their movement direction

## File Organization

```
kingdom defender/
├── main.py
├── game.py
├── assets.py
├── enemy.py
├── tower.py
├── projectile.py
├── constants.py
├── README.md
├── graphic_resources.md
└── [PNG FILES GO HERE]
    ├── background.png
    ├── castle.png
    ├── goblin.png
    ├── goblin_walk1.png
    ├── goblin_walk2.png
    └── [etc...]
```

## Testing

To test the graphics system:
1. Start with just one sprite (e.g., `goblin.png`)
2. Run the game to see it in action
3. Add more sprites gradually
4. Game will use sprites where available, colored shapes elsewhere
5. Click on towers to see level indicators (yellow number badge)

## Art Style Recommendations

- **Medieval Fantasy**: Stone castles, wooden towers, fantasy creatures
- **Consistent Size**: Follow the recommended pixel dimensions
- **Transparent Backgrounds**: Use PNG transparency for proper layering
- **Readable at Small Size**: Ensure sprites are clear when scaled down
- **Color Contrast**: Make sure sprites stand out against backgrounds
