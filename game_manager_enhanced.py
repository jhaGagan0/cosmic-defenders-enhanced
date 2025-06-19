## game/game_manager_enhanced.py
python
"""
Enhanced Game Manager - Core Game Logic and State Management
===========================================================

Professional game state management with advanced features:
- Multi-state game flow (Menu, Game, Pause, Settings, etc.)
- Save/Load system
- Performance optimization
- Advanced collision detection
- Dynamic difficulty scaling
"""

import pygame
import json
import time
import random
import math
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from settings_enhanced import *
from player_enhanced import EnhancedPlayer
from enemy_enhanced import EnemyManager
from bullet_enhanced import BulletManager
from powerup_enhanced import PowerUpManager
from particles_enhanced import ParticleManager
from ui_enhanced import UIManager
from audio_enhanced import AudioManager
from leaderboard_enhanced import LeaderboardManager
from level_enhanced import LevelManager

class GameState(Enum):
    """Game state enumeration for clean state management."""
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    NAME_INPUT = "name_input"
    DIFFICULTY_SELECT = "difficulty_select"
    LEVEL_SELECT = "level_select"
    INSTRUCTIONS = "instructions"
    SETTINGS = "settings"
    LEADERBOARD = "leaderboard"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"
    DAILY_MISSIONS = "daily_missions"

class EnhancedGameManager:
    """
    Main game manager handling all game states, logic, and coordination
    between different game systems.
    """
    
    def __init__(self, screen: pygame.Surface):
        """Initialize the enhanced game manager."""
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.SPLASH
        self.previous_state = None
        
        # Game data
        self.player_name = ""
        self.current_difficulty = "COMMANDER"
        self.current_level = 1
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.wave = 1
        self.game_time = 0
        self.level_time = 0
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.last_fps_update = time.time()
        
        # Screen effects
        self.screen_shake = 0
        self.screen_flash = 0
        self.screen_flash_color = WHITE
        
        # Initialize managers
        self._initialize_managers()
        
        # Load game data
        self._load_game_data()
        
        # State transition timer
        self.state_timer = 0
        self.transition_alpha = 0
        self.transitioning = False

        print("Enhanced Game Manager initialized successfully!")
    
    def _initialize_managers(self):
        """Initialize all game subsystem managers."""
        try:
            # Core managers
            self.ui_manager = UIManager(self.screen)
            self.audio_manager = AudioManager()
            self.leaderboard_manager = LeaderboardManager()
            self.level_manager = LevelManager()
            
            # Game object managers
            self.player = None  # Created when game starts
            self.enemy_manager = EnemyManager()
            self.bullet_manager = BulletManager()
            self.powerup_manager = PowerUpManager()
            self.particle_manager = ParticleManager()
            
            print("All managers initialized successfully!")

        except Exception as e:
            print(f"Error initializing managers: {e}")
            # Continue with basic functionality

    def _load_game_data(self):
        """Load saved game data and settings."""
        try:
            # Load settings
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.audio_manager.set_master_volume(settings.get('master_volume', MASTER_VOLUME))
                    self.audio_manager.set_music_volume(settings.get('music_volume', MUSIC_VOLUME))
                    self.audio_manager.set_sfx_volume(settings.get('sfx_volume', SFX_VOLUME))
            
            # Load progress
            if PROGRESS_FILE.exists():
                with open(PROGRESS_FILE, 'r') as f:
                    progress = json.load(f)
                    self.level_manager.unlocked_levels = set(progress.get('unlocked_levels', [1]))
                    self.high_score = progress.get('high_score', 0)
            
            # Load leaderboard
            self.leaderboard_manager.load_leaderboard()
            
        except Exception as e:
            print(f"Error loading game data: {e}")
    
    def _save_game_data(self):
        """Save current game data and settings."""
        try:
            # Save settings
            settings = {
                'master_volume': self.audio_manager.master_volume,
                'music_volume': self.audio_manager.music_volume,
                'sfx_volume': self.audio_manager.sfx_volume
            }
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
            
            # Save progress
            progress = {
                'unlocked_levels': list(self.level_manager.unlocked_levels),
                'high_score': self.high_score
            }
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(progress, f, indent=2)
            
            # Save leaderboard
            self.leaderboard_manager.save_leaderboard()
            
        except Exception as e:
            print(f"Error saving game data: {e}")
    
    def run(self):
        """Main game loop with state management."""
        self.audio_manager.play_music('menu_music')
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            self._update_fps()
            
            # Handle events
            self._handle_events()
            
            # Update current state
            self._update_state(dt)
            
            # Render current state
            self._render_state()
            
            # Apply screen effects
            self._apply_screen_effects()

            pygame.display.flip()
        
        # Save data before quitting
        self._save_game_data()
    
    def _handle_events(self):
        """Handle pygame events for all game states."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Pass events to appropriate handlers based on state
            if self.state == GameState.SPLASH:
                self._handle_splash_events(event)
            elif self.state == GameState.MAIN_MENU:
                self._handle_main_menu_events(event)
            elif self.state == GameState.NAME_INPUT:
                self._handle_name_input_events(event)
            elif self.state == GameState.DIFFICULTY_SELECT:
                self._handle_difficulty_select_events(event)
            elif self.state == GameState.LEVEL_SELECT:
                self._handle_level_select_events(event)
            elif self.state == GameState.INSTRUCTIONS:
                self._handle_instructions_events(event)
            elif self.state == GameState.SETTINGS:
                self._handle_settings_events(event)
elif self.state == GameState.LEADERBOARD:
                self._handle_leaderboard_events(event)
            elif self.state == GameState.PLAYING:
                self._handle_playing_events(event)
            elif self.state == GameState.PAUSED:
                self._handle_paused_events(event)
            elif self.state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif self.state == GameState.LEVEL_COMPLETE:
                self._handle_level_complete_events(event)
            elif self.state == GameState.DAILY_MISSIONS:
                self._handle_daily_missions_events(event)
    
    def _update_state(self, dt: float):
        """Update logic for current game state."""
        self.state_timer += dt
        
        # Update screen effects
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - dt * 10)
        
        if self.screen_flash > 0:
            self.screen_flash = max(0, self.screen_flash - dt * 5)
        
        # State-specific updates
        if self.state == GameState.SPLASH:
            self._update_splash(dt)
        elif self.state == GameState.PLAYING:
            self._update_playing(dt)
        elif self.state == GameState.PAUSED:
            self._update_paused(dt)
        
        # Always update particle manager for visual effects
        self.particle_manager.update(dt)

    def _render_state(self):
        """Render current game state."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Render background particles (stars)
        self.particle_manager.render_background(self.screen)
        
        # State-specific rendering
        if self.state == GameState.SPLASH:
            self._render_splash()
        elif self.state == GameState.MAIN_MENU:
            self._render_main_menu()
        elif self.state == GameState.NAME_INPUT:
            self._render_name_input()
        elif self.state == GameState.DIFFICULTY_SELECT:
            self._render_difficulty_select()
        elif self.state == GameState.LEVEL_SELECT:
            self._render_level_select()
        elif self.state == GameState.INSTRUCTIONS:
            self._render_instructions()
        elif self.state == GameState.SETTINGS:
            self._render_settings()
        elif self.state == GameState.LEADERBOARD:
            self._render_leaderboard()
        elif self.state == GameState.PLAYING:
            self._render_playing()
        elif self.state == GameState.PAUSED:
            self._render_paused()
        elif self.state == GameState.GAME_OVER:
            self._render_game_over()
        elif self.state == GameState.LEVEL_COMPLETE:
            self._render_level_complete()
        elif self.state == GameState.DAILY_MISSIONS:
            self._render_daily_missions()
        
        # Render foreground particles
        self.particle_manager.render_foreground(self.screen)
        
        # Debug information
        if SHOW_FPS:
            self._render_debug_info()
    
    def _apply_screen_effects(self):
        """Apply screen shake and flash effects."""
        # Screen shake
        if self.screen_shake > 0:
            shake_x = random.randint(-int(self.screen_shake), int(self.screen_shake))
            shake_y = random.randint(-int(self.screen_shake), int(self.screen_shake))
            # Note: In a real implementation, you'd offset the camera/viewport
        
        # Screen flash
        if self.screen_flash > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill(self.screen_flash_color)
            flash_surface.set_alpha(int(self.screen_flash * 255))
            self.screen.blit(flash_surface, (0, 0))
    
    def _update_fps(self):
        """Update FPS counter."""
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_update = current_time
    
    def _render_debug_info(self):
        """Render debug information."""
        debug_info = [
            f"FPS: {self.fps}",
            f"State: {self.state.value}",
            f"Particles: {len(self.particle_manager.particles)}"
        ]
        
        if self.state == GameState.PLAYING and self.player:
            debug_info.extend([
                f"Score: {self.score}",
                f"Wave: {self.wave}",
                f"Enemies: {len(self.enemy_manager.enemies)}"
            ])
        
        y_offset = 10
        for info in debug_info:
            text_surface = self.ui_manager.fonts['small'].render(info, True, WHITE)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
    
    # ========================================================================
    # STATE TRANSITION METHODS
    # ========================================================================
    
    def change_state(self, new_state: GameState):
        """Change game state with transition effect."""
        self.previous_state = self.state
        self.state = new_state
        self.state_timer = 0
        
        # State-specific initialization
        if new_state == GameState.PLAYING:
            self._initialize_game()
        elif new_state == GameState.MAIN_MENU:
            self.audio_manager.play_music('menu_music')
    
    def _initialize_game(self):
        """Initialize a new game session."""
        # Create player
        self.player = EnhancedPlayer(
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT - 100,
            self.current_difficulty
        )

        # Reset game state
        self.score = 0
        self.wave = 1
        self.game_time = 0
        self.level_time = 0
        
        # Clear all managers
        self.enemy_manager.clear()
        self.bullet_manager.clear()
        self.powerup_manager.clear()
        self.particle_manager.clear_game_particles()
        
        # Start level
        self.level_manager.start_level(self.current_level)
        
        # Play game music
        self.audio_manager.play_music('game_music')
        
        print(f"Game initialized - Level: {self.current_level}, Difficulty: {self.current_difficulty}")
    
    # ========================================================================
    # SPLASH SCREEN
    # ========================================================================
    
    def _handle_splash_events(self, event):
        """Handle splash screen events."""
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            self.change_state(GameState.MAIN_MENU)
    
    def _update_splash(self, dt):
        """Update splash screen."""
        # Auto-transition after 3 seconds
        if self.state_timer > 3.0:
            self.change_state(GameState.MAIN_MENU)
    
    def _render_splash(self):
        """Render splash screen."""
        # Animated title
        title_alpha = min(255, self.state_timer * 128)
        title_scale = min(1.0, self.state_timer * 0.5)

        self.ui_manager.render_animated_title(
            "COSMIC DEFENDERS",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            alpha=title_alpha,
            scale=title_scale
        )
        
        # Subtitle
        if self.state_timer > 1.5:
            subtitle_alpha = min(255, (self.state_timer - 1.5) * 255)
            subtitle = self.ui_manager.fonts['medium'].render("Enhanced Edition", True, UI_PRIMARY)
            subtitle.set_alpha(subtitle_alpha)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(subtitle, subtitle_rect)
        
        # Continue prompt
        if self.state_timer > 2.5:
            prompt_alpha = int(128 + 127 * math.sin(self.state_timer * 4))
            prompt = self.ui_manager.fonts['small'].render("Press any key to continue", True, WHITE)
            prompt.set_alpha(prompt_alpha)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(prompt, prompt_rect)
    
    # ========================================================================
    # MAIN MENU
    # ========================================================================
    
    def _handle_main_menu_events(self, event):
        """Handle main menu events."""
        result = self.ui_manager.handle_main_menu_events(event)
        
        if result == "start_game":
            if not self.player_name:
                self.change_state(GameState.NAME_INPUT)
            else:
                self.change_state(GameState.DIFFICULTY_SELECT)
        elif result == "instructions":
            self.change_state(GameState.INSTRUCTIONS)
        elif result == "level_select":
            self.change_state(GameState.LEVEL_SELECT)
        elif result == "leaderboard":
            self.change_state(GameState.LEADERBOARD)
        elif result == "settings":
            self.change_state(GameState.SETTINGS)
        elif result == "daily_missions":
            self.change_state(GameState.DAILY_MISSIONS)
        elif result == "quit":
            self.running = False

    def _render_main_menu(self):
        """Render main menu."""
        self.ui_manager.render_main_menu(self.state_timer)
    
    # ========================================================================
    # NAME INPUT
    # ========================================================================
    
    def _handle_name_input_events(self, event):
        """Handle name input events."""
        result = self.ui_manager.handle_name_input_events(event)
        
        if isinstance(result, str):
            self.player_name = result
            self.change_state(GameState.DIFFICULTY_SELECT)
        elif result == "back":
            self.change_state(GameState.MAIN_MENU)
    
    def _render_name_input(self):
        """Render name input screen."""
        self.ui_manager.render_name_input()
    
    # ========================================================================
    # DIFFICULTY SELECT
    # ========================================================================
    
    def _handle_difficulty_select_events(self, event):
        """Handle difficulty selection events."""
        result = self.ui_manager.handle_difficulty_select_events(event)
        
        if result in DIFFICULTIES:
            self.current_difficulty = result
            self.change_state(GameState.LEVEL_SELECT)
        elif result == "back":
            self.change_state(GameState.MAIN_MENU)
    
    def _render_difficulty_select(self):
        """Render difficulty selection screen."""
        self.ui_manager.render_difficulty_select()
    
    # ========================================================================
    # LEVEL SELECT
    # ========================================================================
    
    def _handle_level_select_events(self, event):
        """Handle level selection events."""
        result = self.ui_manager.handle_level_select_events(
            event, 
            self.level_manager.unlocked_levels
        )
        
        if isinstance(result, int):
            self.current_level = result
            self.change_state(GameState.PLAYING)
        elif result == "back":
            self.change_state(GameState.DIFFICULTY_SELECT)
    
    def _render_level_select(self):
        """Render level selection screen."""
        self.ui_manager.render_level_select(self.level_manager.unlocked_levels)
    
    # ========================================================================
    # PLAYING STATE
    # ========================================================================

    def _handle_playing_events(self, event):
        """Handle playing state events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.change_state(GameState.PAUSED)
            elif event.key == pygame.K_x or event.key == pygame.K_LSHIFT:
                if self.player:
                    self.player.use_special_ability()
        
        # Handle continuous input for shooting
        keys = pygame.key.get_pressed()
        if any(keys[key] for key in KEY_BINDINGS['shoot']):
            if self.player:
                bullets = self.player.shoot(self.bullet_manager)
                if bullets:
                    self.audio_manager.play_sound('shoot')
    
    def _update_playing(self, dt: float):
        """Update playing state."""
        if not self.player:
            return
        
        self.game_time += dt
        self.level_time += dt
        
        # Update player
        self.player.update(dt)
        
        # Update managers
        self.enemy_manager.update(dt, self.wave, self.current_difficulty, 
                                 self.player.x if self.player else 0, 
                                 self.player.y if self.player else 0, 
                                 self.bullet_manager)
        self.bullet_manager.update(dt, self.enemy_manager.enemies, self.player)
        self.powerup_manager.update(dt)
        
        # Handle collisions
        self._handle_collisions()
        
        # Check wave progression
        self._check_wave_progression()
        
        # Check game over
        if self.player.health <= 0:
            self._game_over()
        
        # Check level completion
        if self.level_manager.is_level_complete(self.wave):
            self._level_complete()

    def _handle_collisions(self):
        """Handle all collision detection."""
        if not self.player:
            return
        
        # Player bullets vs enemies
        for bullet in self.bullet_manager.player_bullets[:]:
            for enemy in self.enemy_manager.enemies[:]:
                if self._check_collision(bullet, enemy):
                    # Damage enemy
                    enemy.take_damage(bullet.damage)
                    self.bullet_manager.player_bullets.remove(bullet)
    
                    # Create explosion effect
                    self.particle_manager.create_explosion(enemy.x, enemy.y, 10)
                    self.audio_manager.play_sound('explosion')
                    
                    # Check if enemy is destroyed
                    if enemy.health <= 0:
                        self.enemy_manager.enemies.remove(enemy)
                        self.score += enemy.score_value
                        
                        # Chance to spawn power-up
                        if random.random() < POWERUP_SPAWN_CHANCE:
                            self.powerup_manager.spawn_powerup(enemy.x, enemy.y)
                    
                    break
        
        # Enemy bullets vs player
        for bullet in self.bullet_manager.enemy_bullets[:]:
            if self._check_collision(bullet, self.player):
                if not self.player.invulnerable:
                    self.player.take_damage(bullet.damage)
                    self.bullet_manager.enemy_bullets.remove(bullet)
                    
                    # Screen effects
                    self.screen_shake = SCREEN_SHAKE_INTENSITY
                    self.screen_flash = DAMAGE_FLASH_DURATION
                    self.screen_flash_color = UI_DANGER
        
        # Player vs enemies
        for enemy in self.enemy_manager.enemies[:]:
            if self._check_collision(self.player, enemy):
                if not self.player.invulnerable:
                    self.player.take_damage(10)
                    enemy.take_damage(999)  # Destroy enemy
                    
                    # Effects
                    self.screen_shake = SCREEN_SHAKE_INTENSITY * 2
                    self.particle_manager.create_explosion(enemy.x, enemy.y, 15)

        # Player vs power-ups
        for powerup in self.powerup_manager.powerups[:]:
            if self._check_collision(self.player, powerup):
                self.player.apply_powerup(powerup.type)
                self.powerup_manager.powerups.remove(powerup)
                self.audio_manager.play_sound('powerup')
                
                # Flash effect
                self.screen_flash = POWERUP_FLASH_DURATION
                self.screen_flash_color = powerup.color
    
    def _check_collision(self, obj1, obj2) -> bool:
        """Check collision between two objects."""
        return (abs(obj1.x - obj2.x) < (obj1.size[0] + obj2.size[0]) / 2 and
                abs(obj1.y - obj2.y) < (obj1.size[1] + obj2.size[1]) / 2)
    
    def _check_wave_progression(self):
        """Check if wave should progress."""
        if len(self.enemy_manager.enemies) == 0 and not self.enemy_manager.spawning:
            self.wave += 1
            self.enemy_manager.start_wave(self.wave)
            
            # Boss wave music
            if self.wave % BOSS_WAVE_INTERVAL == 0:
                self.audio_manager.play_music('boss_music')
                self.audio_manager.play_sound('boss_warning')
    
    def _game_over(self):
        """Handle game over."""
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
        
        # Add to leaderboard
        self.leaderboard_manager.add_score(self.player_name, self.score, self.current_difficulty)
        
        # Unlock levels based on score
        for level, required_score in LEVEL_REQUIREMENTS.items():
            if self.score >= required_score:
                self.level_manager.unlock_level(level)
        
        self.change_state(GameState.GAME_OVER)
        self.audio_manager.play_sound('game_over')

    def _level_complete(self):
        """Handle level completion."""
        self.change_state(GameState.LEVEL_COMPLETE)
        self.audio_manager.play_sound('level_complete')
    
    def _render_playing(self):
        """Render playing state."""
        # Render game objects
        if self.player:
            self.player.render(self.screen)
        
        self.enemy_manager.render(self.screen)
        self.bullet_manager.render(self.screen)
        self.powerup_manager.render(self.screen)
        
        # Render HUD
        self.ui_manager.render_hud(
            self.player.health if self.player else 0,
            PLAYER_MAX_HEALTH,
            self.score,
            self.wave,
            self.player.active_powerups if self.player else {}
        )
    
    # ========================================================================
    # PAUSED STATE
    # ========================================================================
    
    def _handle_paused_events(self, event):
        """Handle paused state events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.change_state(GameState.PLAYING)
        
        result = self.ui_manager.handle_pause_menu_events(event)
        if result == "resume":
            self.change_state(GameState.PLAYING)
        elif result == "main_menu":
            self.change_state(GameState.MAIN_MENU)
        elif result == "quit":
            self.running = False
    
    def _update_paused(self, dt):
        """Update paused state (minimal updates)."""
        pass
    
    def _render_paused(self):
        """Render paused state."""
        # Render game state with overlay
        self._render_playing()
        
        # Render pause overlay
        self.ui_manager.render_pause_menu()
    
    # ========================================================================
    # OTHER STATES (Simplified implementations)
    # ========================================================================
    
    def _handle_instructions_events(self, event):
        """Handle instructions events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state(GameState.MAIN_MENU)
    
    def _render_instructions(self):
        """Render instructions screen."""
        self.ui_manager.render_instructions()
    
    def _handle_settings_events(self, event):
        """Handle settings events."""
        result = self.ui_manager.handle_settings_events(event)
        if result == "back":
            self.change_state(GameState.MAIN_MENU)
    
    def _render_settings(self):
        """Render settings screen."""
        self.ui_manager.render_settings(self.audio_manager)
    
    def _handle_leaderboard_events(self, event):
        """Handle leaderboard events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state(GameState.MAIN_MENU)
    
    def _render_leaderboard(self):
        """Render leaderboard screen."""
        self.ui_manager.render_leaderboard(self.leaderboard_manager.get_leaderboard())
    
    def _handle_game_over_events(self, event):
        """Handle game over events."""
        result = self.ui_manager.handle_game_over_events(event)
        if result == "restart":
            self.change_state(GameState.PLAYING)
        elif result == "main_menu":
            self.change_state(GameState.MAIN_MENU)
    
    def _render_game_over(self):
        """Render game over screen."""
        self.ui_manager.render_game_over(self.score, self.high_score)
    
    def _handle_level_complete_events(self, event):
        """Handle level complete events."""
        result = self.ui_manager.handle_level_complete_events(event)
        if result == "next_level":
            self.current_level += 1
            self.change_state(GameState.PLAYING)
        elif result == "main_menu":
            self.change_state(GameState.MAIN_MENU)
    
    def _render_level_complete(self):
        """Render level complete screen."""
        self.ui_manager.render_level_complete(self.current_level, self.score)

    def _handle_daily_missions_events(self, event):
        """Handle daily missions events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.change_state(GameState.MAIN_MENU)
    
    def _render_daily_missions(self):
        """Render daily missions screen."""
        self.ui_manager.render_daily_missions(DAILY_MISSIONS)
