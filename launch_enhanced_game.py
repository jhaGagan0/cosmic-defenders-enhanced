## launch_enhanced_game.py
python
#!/usr/bin/env python3
"""
Launch Script for Cosmic Defenders Enhanced
==========================================

Simple launcher that handles the environment setup and starts the game.
"""

import os
import sys
from pathlib import Path

def main():
    """Launch the enhanced game."""
    print("🚀 Launching Cosmic Defenders Enhanced...")
    
    # Ensure we're in the right directory
    game_dir = Path(__file__).parent
    os.chdir(game_dir)
    
    # Add game directory to Python path
    sys.path.insert(0, str(game_dir / "game"))
    
    # Create necessary directories
    for directory in ["saves", "assets", "assets/images", "assets/sounds", "assets/fonts"]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    try:
        # Import and run the game
        print("Loading game modules...")
        
        # Test imports first
        from settings_enhanced import SCREEN_WIDTH, SCREEN_HEIGHT
        print(f"✓ Game configured for {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Import the main game
        import pygame
        pygame.init()

        from game_manager_enhanced import EnhancedGameManager
        
        # Set up display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cosmic Defenders Enhanced")
        
        print("✓ Game initialized successfully!")
        print("\n" + "="*50)
        print("COSMIC DEFENDERS ENHANCED")
        print("="*50)
        print("Controls:")
        print("  WASD/Arrow Keys - Move")
        print("  Space - Shoot")
        print("  X/Shift - Special Ability")
        print("  ESC - Pause/Menu")
        print("="*50)
        print("Starting game...")
        
        # Create and run game
        game_manager = EnhancedGameManager(screen)
        game_manager.run()
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure all game files are present in the 'game' directory.")
        return 1
    except Exception as e:
        print(f"✗ Error starting game: {e}")
        print("Check the console output above for more details.")
        return 1
    finally:
        pygame.quit()
    
    print("Thanks for playing Cosmic Defenders Enhanced! 🌌")
    return 0

if __name__ == "__main__":
    sys.exit(main())
