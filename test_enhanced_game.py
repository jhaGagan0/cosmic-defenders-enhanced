## test_enhanced_game.py
python
#!/usr/bin/env python3
"""
Test Script for Cosmic Defenders Enhanced
========================================

Simple test to verify all components are working.
"""

import sys
import pygame
from pathlib import Path

def test_imports():
    """Test all game module imports."""
    print("Testing imports...")

    # Add game directory to path
    sys.path.insert(0, str(Path(__file__).parent / "game"))
    
    try:
        from settings_enhanced import SCREEN_WIDTH, SCREEN_HEIGHT, UI_PRIMARY
        print("✓ Settings module")
        
        from audio_enhanced import AudioManager
        print("✓ Audio module")
        
        from leaderboard_enhanced import LeaderboardManager
        print("✓ Leaderboard module")
        
        from level_enhanced import LevelManager
        print("✓ Level module")

        from particles_enhanced import ParticleManager
        print("✓ Particle module")
        
        from powerup_enhanced import PowerUpManager
        print("✓ Power-up module")
        
        from bullet_enhanced import BulletManager
        print("✓ Bullet module")
        
        from enemy_enhanced import EnemyManager
        print("✓ Enemy module")
        
        from player_enhanced import EnhancedPlayer
        print("✓ Player module")
        
        from ui_enhanced import UIManager
        print("✓ UI module")
        
        print("✓ All modules imported successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_pygame():
    """Test pygame functionality."""
    print("\nTesting Pygame...")
    
    try:
        pygame.init()
        
        # Test display
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Window")
        print("✓ Display initialized")

        # Test basic rendering
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (400, 300), 50)
        pygame.display.flip()
        print("✓ Basic rendering works")
        
        # Test audio
        pygame.mixer.init()
        print("✓ Audio system initialized")
        
        pygame.quit()
        print("✓ Pygame test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Pygame test failed: {e}")
        return False

def test_game_components():
    """Test individual game components."""
    print("\nTesting game components...")
    
    try:
        # Add game directory to path
        sys.path.insert(0, str(Path(__file__).parent / "game"))
        
        # Test audio manager
        from audio_enhanced import AudioManager
        audio = AudioManager()
        print("✓ Audio manager created")
        
        # Test leaderboard
        from leaderboard_enhanced import LeaderboardManager
        leaderboard = LeaderboardManager()
        leaderboard.add_score("TestPlayer", 1000, "COMMANDER")
        print("✓ Leaderboard manager working")
        
        # Test particle system
        from particles_enhanced import ParticleManager
        particles = ParticleManager()
        particles.create_explosion(100, 100, 10)
        print("✓ Particle system working")
        
        # Test level manager
        from level_enhanced import LevelManager
        levels = LevelManager()
        print(f"✓ Level manager - {len(levels.unlocked_levels)} levels unlocked")
        
        print("✓ All components tested successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Component test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("COSMIC DEFENDERS ENHANCED - COMPONENT TEST")
    print("=" * 50)
    
    # Create directories
    for directory in ["saves", "assets", "assets/images", "assets/sounds", "assets/fonts"]:
        Path(directory).mkdir(parents=True, exist_ok=True)

    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_pygame()
    success &= test_game_components()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("The game is ready to run!")
        print("\nTo start the game:")
        print("  python3 launch_enhanced_game.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Check the error messages above.")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
