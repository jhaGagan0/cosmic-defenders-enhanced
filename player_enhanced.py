## game/player_enhanced.py
python
"""
Enhanced Player Class - Advanced Player Mechanics
================================================

Professional player implementation with:
- Smooth movement and controls
- Power-up system
- Special abilities
- Visual effects
- Difficulty scaling
"""

import pygame
import math
import time
from typing import Dict, List, Tuple

from settings_enhanced import *

class EnhancedPlayer:
    """
    Enhanced player class with advanced mechanics, power-ups, and abilities.
    """
    
    def __init__(self, x: float, y: float, difficulty: str):
        """Initialize the enhanced player."""
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.difficulty = difficulty
        
        # Movement
        self.speed = PLAYER_SPEED
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.friction = 0.8
        
        # Health and damage
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.invulnerable = False
        self.invulnerability_timer = 0
        
        # Shooting
        self.fire_rate = PLAYER_FIRE_RATE
        self.last_shot_time = 0
        self.bullet_damage = BULLET_DAMAGE
        
        # Special abilities
        self.special_ability_cooldown = SPECIAL_ABILITY_COOLDOWN
        self.last_special_use = 0
        self.time_freeze_active = False
        self.time_freeze_timer = 0
        
        # Power-ups
        self.active_powerups = {}
        self.powerup_timers = {}
        
        # Visual effects
        self.sprite_angle = 0
        self.trail_particles = []
        self.shield_effect = 0
        self.damage_flash = 0
        
        # Input state
        self.keys_pressed = set()
        
        # Apply difficulty modifiers
        self._apply_difficulty_modifiers()
        
        print(f"Enhanced Player created - Difficulty: {difficulty}")
    
    def _apply_difficulty_modifiers(self):
        """Apply difficulty-based modifiers to player stats."""
        diff_settings = DIFFICULTIES[self.difficulty]
        
        # Modify damage output
        self.bullet_damage *= diff_settings['player_damage_mult']
        
        # Adjust health for easier difficulties
        if self.difficulty in ['CADET', 'PILOT']:
            self.max_health = int(self.max_health * 1.2)
            self.health = self.max_health
    
    def update(self, dt: float):
        """Update player state."""
        # Handle input
        self._handle_input(dt)
        
        # Update movement
        self._update_movement(dt)
        
        # Update timers
        self._update_timers(dt)
        
        # Update power-ups
        self._update_powerups(dt)
        
        # Update visual effects
        self._update_visual_effects(dt)
        
        # Keep player on screen
        self._clamp_to_screen()
    
    def _handle_input(self, dt: float):
        """Handle player input with smooth movement."""
        keys = pygame.key.get_pressed()
        
        # Movement input
        target_vel_x = 0
        target_vel_y = 0
        
        if any(keys[key] for key in KEY_BINDINGS['move_left']):
            target_vel_x = -self.speed
        if any(keys[key] for key in KEY_BINDINGS['move_right']):
            target_vel_x = self.speed
        if any(keys[key] for key in KEY_BINDINGS['move_up']):
            target_vel_y = -self.speed
        if any(keys[key] for key in KEY_BINDINGS['move_down']):
            target_vel_y = self.speed
        
        # Diagonal movement normalization
        if target_vel_x != 0 and target_vel_y != 0:
            target_vel_x *= 0.707  # 1/sqrt(2)
            target_vel_y *= 0.707
        
        # Smooth acceleration
        self.velocity_x += (target_vel_x - self.velocity_x) * self.acceleration
        self.velocity_y += (target_vel_y - self.velocity_y) * self.acceleration
        
        # Apply friction
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Shooting
        if any(keys[key] for key in KEY_BINDINGS['shoot']):
            self.shoot()
    
    def _update_movement(self, dt: float):
        """Update player position."""
        # Apply power-up speed modifiers
        speed_mult = 1.0
        if 'rapid_fire' in self.active_powerups:
            speed_mult *= 1.2
        if 'shield' in self.active_powerups:
            speed_mult *= 0.8  # Slower when shielded
        
        self.x += self.velocity_x * speed_mult * dt * 60  # 60 FPS normalization
        self.y += self.velocity_y * speed_mult * dt * 60
    
    def _update_timers(self, dt: float):
        """Update various timers."""
        current_time = time.time()
        
        # Invulnerability timer
        if self.invulnerable:
            self.invulnerability_timer -= dt
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
        
        # Time freeze timer
        if self.time_freeze_active:
            self.time_freeze_timer -= dt
            if self.time_freeze_timer <= 0:
                self.time_freeze_active = False
        
        # Visual effect timers
        if self.damage_flash > 0:
            self.damage_flash = max(0, self.damage_flash - dt * 5)

        if self.shield_effect > 0:
            self.shield_effect = max(0, self.shield_effect - dt * 2)
    
    def _update_powerups(self, dt: float):
        """Update active power-ups."""
        expired_powerups = []
        
        for powerup_type, timer in self.powerup_timers.items():
            timer -= dt
            if timer <= 0:
                expired_powerups.append(powerup_type)
            else:
                self.powerup_timers[powerup_type] = timer
        
        # Remove expired power-ups
        for powerup_type in expired_powerups:
            if powerup_type in self.active_powerups:
                del self.active_powerups[powerup_type]
            if powerup_type in self.powerup_timers:
                del self.powerup_timers[powerup_type]
    
    def _update_visual_effects(self, dt: float):
        """Update visual effects."""
        # Sprite rotation based on movement
        if abs(self.velocity_x) > 0.1:
            target_angle = math.atan2(-self.velocity_x, 1) * 0.3  # Subtle banking
            self.sprite_angle += (target_angle - self.sprite_angle) * 0.1
        else:
            self.sprite_angle *= 0.9  # Return to center
        
        # Update trail particles
        self.trail_particles = [(x, y, alpha - dt * 2) for x, y, alpha in self.trail_particles if alpha > 0]
        
        # Add new trail particle
        if len(self.trail_particles) < 10:
            self.trail_particles.append((self.x, self.y + self.size[1] // 2, 1.0))
    
    def _clamp_to_screen(self):
        """Keep player within screen boundaries."""
        half_width = self.size[0] // 2
        half_height = self.size[1] // 2
        
        self.x = max(half_width, min(SCREEN_WIDTH - half_width, self.x))
        self.y = max(half_height, min(SCREEN_HEIGHT - half_height, self.y))
    
    def shoot(self, bullet_manager=None):
        """Shoot bullets based on current power-ups."""
        current_time = time.time()
        
        # Check fire rate
        fire_rate = self.fire_rate
        if 'rapid_fire' in self.active_powerups:
            fire_rate *= 2
        
        if current_time - self.last_shot_time < 1.0 / fire_rate:
            return []
        
        self.last_shot_time = current_time
        
        bullets = []
        
        if bullet_manager:
            # Use bullet manager if provided
            if 'multi_shot' in self.active_powerups:
                # Multi-shot: 3 bullets in a spread
                for i, angle in enumerate([-0.3, 0, 0.3]):
                    vel_x = math.sin(angle) * 20
                    vel_y = -BULLET_SPEED
                    bullet = bullet_manager.create_player_bullet(
                        self.x + vel_x, self.y - 20, vel_x, vel_y, self.bullet_damage
                    )
                    bullets.append(bullet)
            else:
                # Single bullet
                bullet = bullet_manager.create_player_bullet(
                    self.x, self.y - 20, 0, -BULLET_SPEED, self.bullet_damage
                )
                bullets.append(bullet)
        else:
            # Fallback to creating bullet objects directly
            from bullet_enhanced import Bullet
            
            if 'multi_shot' in self.active_powerups:
                # Multi-shot: 3 bullets in a spread
                for i, angle in enumerate([-0.3, 0, 0.3]):
                    bullet = Bullet(
                        self.x + math.sin(angle) * 20,
                        self.y - 20,
                        0,
                        -BULLET_SPEED,
                        self.bullet_damage,
                        'player'
                    )
                    bullets.append(bullet)
            else:
                # Single bullet
                bullet = Bullet(
                    self.x,
                    self.y - 20,
                    0,
                    -BULLET_SPEED,
                    self.bullet_damage,
                    'player'
                )
                bullets.append(bullet)
        
        return bullets
    
    def use_special_ability(self):
        """Use special ability (time freeze or homing missiles)."""
        current_time = time.time()
        
        if current_time - self.last_special_use < self.special_ability_cooldown:
            return False
        
        self.last_special_use = current_time
        
        # Time freeze ability
        self.time_freeze_active = True
        self.time_freeze_timer = TIME_FREEZE_DURATION
        
        print("Special ability activated: Time Freeze")
        return True
    
    def apply_powerup(self, powerup_type):
        """Apply a power-up effect."""
        if powerup_type.value == 'health':
            self.health = min(self.max_health, self.health + 25)
        elif powerup_type.value == 'shield':
            self.active_powerups['shield'] = True
            self.powerup_timers['shield'] = POWERUP_DURATION
            self.invulnerable = True
            self.invulnerability_timer = POWERUP_DURATION
            self.shield_effect = 1.0
        elif powerup_type.value == 'rapid_fire':
            self.active_powerups['rapid_fire'] = True
            self.powerup_timers['rapid_fire'] = POWERUP_DURATION
        elif powerup_type.value == 'multi_shot':
            self.active_powerups['multi_shot'] = True
            self.powerup_timers['multi_shot'] = POWERUP_DURATION
        elif powerup_type.value == 'screen_clear':
            # This will be handled by the game manager
            pass
        elif powerup_type.value == 'time_slow':
            self.active_powerups['time_slow'] = True
            self.powerup_timers['time_slow'] = POWERUP_DURATION
        elif powerup_type.value == 'homing':
            self.active_powerups['homing'] = True
            self.powerup_timers['homing'] = POWERUP_DURATION
        
        print(f"Power-up applied: {powerup_type.value}")
    
    def take_damage(self, damage: int):
        """Take damage with invulnerability check."""
        if self.invulnerable:
            return False
        
        self.health -= damage
        self.damage_flash = 0.5
        
        # Brief invulnerability after taking damage
        self.invulnerable = True
        self.invulnerability_timer = PLAYER_INVULNERABILITY_TIME
        
        print(f"Player took {damage} damage, health: {self.health}")
        return True
    
    def render(self, screen: pygame.Surface):
        """Render the player with all visual effects."""
        # Render trail particles
        self._render_trail(screen)
        
        # Calculate render position
        render_x = int(self.x)
        render_y = int(self.y)
        
        # Invulnerability flashing
        if self.invulnerable and int(time.time() * 10) % 2:
            alpha = 128
        else:
            alpha = 255
        
        # Damage flash effect
        if self.damage_flash > 0:
            flash_intensity = int(self.damage_flash * 255)
            color = (255, 255 - flash_intensity, 255 - flash_intensity)
        else:
            color = PLAYER_COLOR
        
        # Create player surface
        player_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        # Draw player shape (triangle pointing up)
        points = [
            (self.size[0] // 2, 0),  # Top
            (0, self.size[1]),       # Bottom left
            (self.size[0], self.size[1])  # Bottom right
        ]
        pygame.draw.polygon(player_surface, color, points)
        
        # Add details
        pygame.draw.polygon(player_surface, WHITE, [
            (self.size[0] // 2, 5),
            (self.size[0] // 2 - 3, self.size[1] - 10),
            (self.size[0] // 2 + 3, self.size[1] - 10)
        ])
        
        # Apply rotation
        if abs(self.sprite_angle) > 0.01:
            player_surface = pygame.transform.rotate(player_surface, math.degrees(self.sprite_angle))
        
        # Apply alpha
        player_surface.set_alpha(alpha)
        
        # Blit to screen
        rect = player_surface.get_rect(center=(render_x, render_y))
        screen.blit(player_surface, rect)
        
        # Render shield effect
        if self.shield_effect > 0:
            self._render_shield_effect(screen, render_x, render_y)
        
        # Render power-up indicators
        self._render_powerup_indicators(screen)
    
    def _render_trail(self, screen: pygame.Surface):
        """Render engine trail particles."""
        for x, y, alpha in self.trail_particles:
            if alpha > 0:
                color = (*UI_PRIMARY, int(alpha * 255))
                size = int(alpha * 8)
                if size > 0:
                    trail_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surface, color, (size // 2, size // 2), size // 2)
                    screen.blit(trail_surface, (int(x - size // 2), int(y - size // 2)))
    
    def _render_shield_effect(self, screen: pygame.Surface, x: int, y: int):
        """Render shield visual effect."""
        shield_radius = int(max(self.size) * 0.8 * (0.8 + 0.2 * math.sin(time.time() * 5)))
        shield_alpha = int(self.shield_effect * 100)

        # Create shield surface
        shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shield_surface, (*POWERUP_SHIELD, shield_alpha), 
                          (shield_radius, shield_radius), shield_radius, 3)
        
        screen.blit(shield_surface, (x - shield_radius, y - shield_radius))
    
    def _render_powerup_indicators(self, screen: pygame.Surface):
        """Render active power-up indicators."""
        indicator_y = 50
        indicator_x = SCREEN_WIDTH - 200
        
        for i, (powerup_type, timer) in enumerate(self.powerup_timers.items()):
            # Background
            bg_rect = pygame.Rect(indicator_x, indicator_y + i * 30, 150, 25)
            pygame.draw.rect(screen, UI_SECONDARY, bg_rect)
            pygame.draw.rect(screen, WHITE, bg_rect, 2)
            
            # Timer bar
            timer_width = int((timer / POWERUP_DURATION) * 146)
            timer_rect = pygame.Rect(indicator_x + 2, indicator_y + i * 30 + 2, timer_width, 21)
            
            # Color based on power-up type
            color = POWERUP_TYPES.get(powerup_type, {}).get('color', WHITE)
            pygame.draw.rect(screen, color, timer_rect)
            
            # Text
            font = pygame.font.Font(None, 20)
            text = font.render(powerup_type.replace('_', ' ').title(), True, WHITE)
            screen.blit(text, (indicator_x + 5, indicator_y + i * 30 + 5))
    
    def get_special_ability_cooldown_remaining(self) -> float:
        """Get remaining cooldown time for special ability."""
        current_time = time.time()
        remaining = self.special_ability_cooldown - (current_time - self.last_special_use)
        return max(0, remaining)
    
    def is_time_freeze_active(self) -> bool:
        """Check if time freeze is currently active."""
        return self.time_freeze_active
