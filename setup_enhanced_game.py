## setup_enhanced_game.py
python
#!/usr/bin/env python3
"""
Setup script for Cosmic Defenders Enhanced
==========================================

This script sets up the game environment, installs dependencies,
and creates necessary directories and files.
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    
    try:
        # Install pygame
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame>=2.1.0"])
        print("✓ Pygame installed successfully")
        
        # Try to install numpy (optional for better sound generation)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy>=1.21.0"])
            print("✓ NumPy installed successfully")
        except subprocess.CalledProcessError:
            print("⚠ NumPy installation failed (optional, game will still work)")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    
    return True

def create_directories():
    """Create necessary game directories."""
    print("Creating directories...")
    
    directories = [
        "saves",
        "assets",
        "assets/images",
        "assets/sounds",
        "assets/fonts",
        "game/__pycache__"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_placeholder_files():
    """Create placeholder files and documentation."""
    print("Creating placeholder files...")
    
    # Create assets README
    assets_readme = """# Assets Directory

This directory contains game assets:

## Images (assets/images/)
- player.png - Player spaceship sprite
- enemy_*.png - Enemy sprites
- bullet.png - Bullet sprite
- powerup_*.png - Power-up sprites
- background_*.png - Background images
- icon.png - Game icon

## Sounds (assets/sounds/)
- menu_music.ogg - Main menu background music
- game_music.ogg - Gameplay background music
- boss_music.ogg - Boss battle music
- shoot.wav - Shooting sound effect
- explosion.wav - Explosion sound effect
- powerup.wav - Power-up collection sound
- menu_select.wav - Menu selection sound
- menu_hover.wav - Menu hover sound
- game_over.wav - Game over sound
- level_complete.wav - Level completion sound
- boss_warning.wav - Boss warning sound

## Fonts (assets/fonts/)
- game_font.ttf - Main game font

## Notes
- The game will work without these assets using built-in placeholders
- For the best experience, add high-quality assets
- Supported image formats: PNG, JPG, BMP
- Supported audio formats: WAV, OGG, MP3
- Recommended image sizes:
  - Player: 40x40 pixels
  - Enemies: 30x30 to 80x80 pixels
  - Bullets: 4x10 pixels
  - Power-ups: 24x24 pixels
"""
    
    with open("assets/README.txt", "w") as f:
        f.write(assets_readme)
    
    print("✓ Created assets README")

def create_sample_config():
    """Create sample configuration files."""
    print("Creating sample configuration...")
    
    # Create sample settings
    sample_settings = {
        "master_volume": 0.7,
        "music_volume": 0.5,
        "sfx_volume": 0.8,
        "screen_width": 1200,
        "screen_height": 800,
        "fullscreen": False,
        "vsync": True
    }
    
    import json
    with open("saves/default_settings.json", "w") as f:
        json.dump(sample_settings, f, indent=2)
    
    print("✓ Created sample settings")

def test_installation():
    """Test if the game can be imported and run."""
    print("Testing installation...")
    
    try:
        import pygame
        pygame.init()
        pygame.quit()
        print("✓ Pygame test passed")
        
        # Test game imports
        sys.path.insert(0, "game")
        from settings_enhanced import SCREEN_WIDTH, SCREEN_HEIGHT
        print("✓ Game modules test passed")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def create_launch_scripts():
    """Create convenient launch scripts."""
    print("Creating launch scripts...")
    
    # Windows batch file
    batch_content = """@echo off
echo Starting Cosmic Defenders Enhanced...
python launch_enhanced_game.py
pause
"""
    
    with open("start_game.bat", "w") as f:
        f.write(batch_content)
    
    # Unix shell script
    shell_content = """#!/bin/bash
echo "Starting Cosmic Defenders Enhanced..."
python3 launch_enhanced_game.py
"""
    
    with open("start_game.sh", "w") as f:
        f.write(shell_content)
    
    # Make shell script executable
    try:
        os.chmod("start_game.sh", 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    print("✓ Created launch scripts")

def check_system_requirements():
    """Check system requirements."""
    print("Checking system requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Check available disk space
    try:
        import shutil
        free_space = shutil.disk_usage(".").free
        if free_space < 100 * 1024 * 1024:  # 100MB
            print("⚠ Low disk space detected")
        else:
            print("✓ Sufficient disk space available")
    except:
        print("⚠ Could not check disk space")

    return True

def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 COSMIC DEFENDERS ENHANCED - SETUP")
    print("=" * 60)
    print()
    
    # Check system requirements
    if not check_system_requirements():
        print("✗ System requirements not met")
        return 1
    
    # Install dependencies
    print("\n" + "=" * 40)
    print("📦 INSTALLING DEPENDENCIES")
    print("=" * 40)
    if not install_dependencies():
        print("✗ Failed to install dependencies")
        print("You can try installing manually:")
        print("  pip install pygame>=2.1.0")
        print("  pip install numpy>=1.21.0")
        return 1
    
    # Create directories
    print("\n" + "=" * 40)
    print("📁 CREATING DIRECTORIES")
    print("=" * 40)
    create_directories()
    
    # Create placeholder files
    print("\n" + "=" * 40)
    print("📄 CREATING FILES")
    print("=" * 40)
    create_placeholder_files()
    create_sample_config()
    create_launch_scripts()

    # Test installation
    print("\n" + "=" * 40)
    print("🧪 TESTING INSTALLATION")
    print("=" * 40)
    if not test_installation():
        print("✗ Installation test failed")
        return 1
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("🎮 TO PLAY THE GAME:")
    print("   python3 launch_enhanced_game.py")
    print("   OR")
    print("   ./start_game.sh (Linux/Mac)")
    print("   OR")
    print("   start_game.bat (Windows)")
    print()
    print("📖 TO ADD CUSTOM ASSETS:")
    print("   See assets/README.txt for details")
    print()
    print("🧪 TO TEST COMPONENTS:")
    print("   python3 test_enhanced_game.py")
    print()
    print("🚀 ENJOY THE GAME!")
    print("   Defend the galaxy and become a Cosmic Legend! 🌌")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Setup failed with error: {e}")
        sys.exit(1)
