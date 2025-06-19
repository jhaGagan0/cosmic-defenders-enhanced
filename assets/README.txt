## assets/README.txt
txt
# Assets Directory

This directory contains game assets for Cosmic Defenders Enhanced.

## Directory Structure
assets/
├── images/     # Sprites and graphics
├── sounds/     # Audio files
└── fonts/      # Custom fonts

## Images (assets/images/)
The game supports the following image assets:

### Player & Enemies
- player.png - Player spaceship sprite (40x40 pixels)
- enemy_basic.png - Basic enemy sprite (30x30 pixels)
- enemy_fast.png - Fast enemy sprite (25x25 pixels)
- enemy_heavy.png - Heavy enemy sprite (45x45 pixels)
- enemy_zigzag.png - Zigzag enemy sprite (35x35 pixels)
- enemy_boss.png - Boss enemy sprite (80x80 pixels)

### Projectiles & Effects
- bullet_player.png - Player bullet sprite (4x10 pixels)
- bullet_enemy.png - Enemy bullet sprite (4x10 pixels)
- bullet_homing.png - Homing missile sprite (6x12 pixels)
- explosion_*.png - Explosion animation frames

### Power-ups
- powerup_health.png - Health boost icon (24x24 pixels)
- powerup_shield.png - Shield power-up icon (24x24 pixels)
- powerup_rapid.png - Rapid fire icon (24x24 pixels)
- powerup_multi.png - Multi-shot icon (24x24 pixels)
- powerup_clear.png - Screen clear icon (24x24 pixels)
- powerup_time.png - Time slow icon (24x24 pixels)
- powerup_homing.png - Homing missiles icon (24x24 pixels)

### UI Elements
- background_*.png - Background layers for parallax
- button_*.png - UI button states
- icon.png - Game icon (32x32 or 64x64 pixels)

## Sounds (assets/sounds/)
The game supports the following audio formats: WAV, OGG, MP3

### Music
- menu_music.ogg - Main menu background music
- game_music.ogg - Gameplay background music
- boss_music.ogg - Boss battle music

### Sound Effects
- shoot.wav - Player shooting sound
- explosion.wav - Explosion sound effect
- powerup.wav - Power-up collection sound
- menu_select.wav - Menu selection sound
- menu_hover.wav - Menu hover sound
- game_over.wav - Game over sound
- level_complete.wav - Level completion sound
- boss_warning.wav - Boss warning sound

## Fonts (assets/fonts/)
- game_font.ttf - Main game font (optional)

## Notes
- The game will work without these assets using built-in placeholders
- For the best experience, add high-quality assets matching the specified dimensions
- All assets should be optimized for performance
- Use consistent art style across all sprites
- Ensure proper licensing for any assets used

## Recommended Tools
- **Graphics**: GIMP, Aseprite, Photoshop
- **Audio**: Audacity, FL Studio, Logic Pro
- **Free Assets**: OpenGameArt.org, Freesound.org, Google Fonts

## Asset Guidelines
- Keep file sizes reasonable (< 1MB per asset)
- Use PNG for images with transparency
- Use OGG for music, WAV for short sound effects
- Maintain consistent color palette
- Test all assets in-game before finalizing
