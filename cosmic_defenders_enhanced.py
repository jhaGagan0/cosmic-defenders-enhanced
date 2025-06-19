## cosmic_defenders_enhanced.py
python
#!/usr/bin/env python3
"""
Cosmic Defenders Enhanced - A Professional 2D Space Shooting Game
================================================================

A fully-featured, high-performance 2D shooting game with:
- Professional UI/UX with animations
- Advanced gameplay mechanics
- Comprehensive leaderboard system
- Dynamic audio system
- Level progression and unlockables
- Save/load functionality
- Performance optimizations

Built with Python and Pygame for maximum compatibility and performance.
"""

import pygame
import sys
import os
from pathlib import Path

# Add the game directory to Python path
game_dir = Path(__file__).parent / "game"
sys.path.insert(0, str(game_dir))

# Import game modules
from game_manager_enhanced import EnhancedGameManager
from settings_enhanced import *

def main():
    """Main game entry point with error handling and initialization."""
    try:
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Set up display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cosmic Defenders Enhanced")
        
        # Set game icon if available
        try:
            icon_path = Path("assets/images/icon.png")
            if icon_path.exists():
                icon = pygame.image.load(str(icon_path))
                pygame.display.set_icon(icon)
        except:
            pass  # Continue without icon if not available
        
        # Create game manager and run
        game_manager = EnhancedGameManager(screen)
        game_manager.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        print("Make sure all dependencies are installed: pip install pygame")
        return 1
    
    finally:
        pygame.quit()
        return 0

if __name__ == "__main__":
    sys.exit(main())
