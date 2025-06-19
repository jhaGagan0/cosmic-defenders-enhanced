## game/bullet_enhanced.py
python
"""
Enhanced Bullet Manager - Advanced Projectile System
==================================================

Professional bullet system with:
- Multiple bullet types
- Homing missiles
- Particle trails
- Performance optimization
"""

import pygame
import math
import random
from typing import List, Tuple, Optional

from settings_enhanced import *

class Bullet:
    """Enhanced bullet class with various types and effects."""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, 
                 damage: int, owner: str, bullet_type: str = 'normal'):
        """
        Initialize a bullet.
        
        Args:
            x, y: Starting position
            vel_x, vel_y: Velocity components
            damage: Damage dealt by bullet
            owner: 'player' or 'enemy'
            bullet_type: Type of bullet ('normal', 'homing', 'explosive')
        """
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.owner = owner
        self.bullet_type = bullet_type
        self.size = BULLET_SIZE
        
        # Visual properties
        self.color = self._get_bullet_color()
        self.trail_particles = []
        self.lifetime = 0
        self.max_lifetime = 5.0  # seconds
        
        # Homing properties
        self.target = None
        self.turn_rate = HOMING_BULLET_TURN_RATE
        self.homing_range = 200
        
        # Special effects
        self.glow_intensity = 1.0
        self.pulse_phase = random.random() * math.pi * 2
    
    def _get_bullet_color(self) -> Tuple[int, int, int]:
        """Get color based on bullet type and owner."""
        if self.owner == 'player':
            if self.bullet_type == 'homing':
                return POWERUP_HOMING
            elif self.bullet_type == 'explosive':
                return UI_WARNING
            else:
                return UI_PRIMARY
        else:  # enemy
            if self.bullet_type == 'homing':
                return UI_DANGER
            else:
                return (255, 100, 100)
    
    def update(self, dt: float, enemies: List = None, player = None):
        """Update bullet position and behavior."""
        self.lifetime += dt
        
        # Handle homing behavior
        if self.bullet_type == 'homing':
            self._update_homing(dt, enemies if self.owner == 'player' else [player] if player else [])
        
        # Update position
        self.x += self.vel_x * dt * 60  # 60 FPS normalization
        self.y += self.vel_y * dt * 60
        
        # Update trail particles
        self._update_trail(dt)
        
        # Update visual effects
        self.pulse_phase += dt * 5
        self.glow_intensity = 0.8 + 0.2 * math.sin(self.pulse_phase)
    
    def _update_homing(self, dt: float, targets: List):
        """Update homing behavior."""
        if not targets:
            return

        # Find closest target if we don't have one
        if not self.target or not hasattr(self.target, 'x'):
            closest_target = None
            closest_distance = float('inf')
            
            for target in targets:
                if hasattr(target, 'x') and hasattr(target, 'y'):
                    distance = math.sqrt((target.x - self.x)**2 + (target.y - self.y)**2)
                    if distance < closest_distance and distance < self.homing_range:
                        closest_distance = distance
                        closest_target = target
            
            self.target = closest_target
        
        # Home in on target
        if self.target and hasattr(self.target, 'x'):
            # Calculate angle to target
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            target_angle = math.atan2(dy, dx)
            
            # Current velocity angle
            current_angle = math.atan2(self.vel_y, self.vel_x)
            
            # Calculate angle difference
            angle_diff = target_angle - current_angle
            
            # Normalize angle difference to [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # Apply turning
            max_turn = self.turn_rate * dt * 60
            turn_amount = max(-max_turn, min(max_turn, angle_diff))
            new_angle = current_angle + turn_amount
            
            # Update velocity
            speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
            self.vel_x = math.cos(new_angle) * speed
            self.vel_y = math.sin(new_angle) * speed
    
    def _update_trail(self, dt: float):
        """Update trail particles."""
        # Add new trail particle
        if len(self.trail_particles) < 8:
            self.trail_particles.append({
                'x': self.x,
                'y': self.y,
                'alpha': 1.0,
                'size': 3
            })
        
        # Update existing particles
        for particle in self.trail_particles[:]:
            particle['alpha'] -= dt * 3
            particle['size'] *= 0.98
            
            if particle['alpha'] <= 0:
                self.trail_particles.remove(particle)
    
    def is_expired(self) -> bool:
        """Check if bullet should be removed."""
        return (self.lifetime > self.max_lifetime or
                self.x < -50 or self.x > SCREEN_WIDTH + 50 or
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
    
    def render(self, screen: pygame.Surface):
        """Render the bullet with effects."""
        # Render trail
        for particle in self.trail_particles:
            if particle['alpha'] > 0 and particle['size'] > 0:
                trail_color = (*self.color, int(particle['alpha'] * 128))
                trail_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, trail_color, 
                                 (particle['size'], particle['size']), int(particle['size']))
                screen.blit(trail_surface, (int(particle['x'] - particle['size']), 
                                          int(particle['y'] - particle['size'])))
        
        # Render bullet glow
        glow_size = int(max(self.size) * 1.5 * self.glow_intensity)
        if glow_size > 0:
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (*self.color, 64)
            pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (int(self.x - glow_size), int(self.y - glow_size)))
        
        # Render main bullet
        bullet_rect = pygame.Rect(
            int(self.x - self.size[0] // 2),
            int(self.y - self.size[1] // 2),
            self.size[0],
            self.size[1]
        )
        
        if self.bullet_type == 'homing':
            # Draw diamond shape for homing bullets
            points = [
                (int(self.x), int(self.y - self.size[1] // 2)),
                (int(self.x + self.size[0] // 2), int(self.y)),
                (int(self.x), int(self.y + self.size[1] // 2)),
                (int(self.x - self.size[0] // 2), int(self.y))
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, WHITE, points, 1)
        else:
            # Draw regular bullet
            pygame.draw.ellipse(screen, self.color, bullet_rect)
            pygame.draw.ellipse(screen, WHITE, bullet_rect, 1)

class BulletManager:
    """Enhanced bullet manager for handling all projectiles."""
    
    def __init__(self):
        """Initialize the bullet manager."""
        self.player_bullets = []
        self.enemy_bullets = []
        self.max_bullets = 200  # Performance limit
        
        print("Bullet Manager initialized successfully!")
    
    def add_bullet(self, bullet: Bullet):
        """Add a bullet to the appropriate list."""
        if bullet.owner == 'player':
            self.player_bullets.append(bullet)
            # Limit player bullets for performance
            if len(self.player_bullets) > self.max_bullets // 2:
                self.player_bullets.pop(0)
        else:
            self.enemy_bullets.append(bullet)
            # Limit enemy bullets for performance
            if len(self.enemy_bullets) > self.max_bullets // 2:
                self.enemy_bullets.pop(0)
    
    def create_player_bullet(self, x: float, y: float, vel_x: float, vel_y: float, 
                           damage: int, bullet_type: str = 'normal') -> Bullet:
        """Create and add a player bullet."""
        bullet = Bullet(x, y, vel_x, vel_y, damage, 'player', bullet_type)
        self.add_bullet(bullet)
        return bullet
    
    def create_enemy_bullet(self, x: float, y: float, vel_x: float, vel_y: float, 
                          damage: int, bullet_type: str = 'normal') -> Bullet:
        """Create and add an enemy bullet."""
        bullet = Bullet(x, y, vel_x, vel_y, damage, 'enemy', bullet_type)
        self.add_bullet(bullet)
        return bullet
    
    def create_homing_missile(self, x: float, y: float, owner: str, damage: int = 2) -> Bullet:
        """Create a homing missile."""
        # Initial velocity towards center of screen
        if owner == 'player':
            vel_x = 0
            vel_y = -HOMING_BULLET_SPEED
        else:
            vel_x = 0
            vel_y = HOMING_BULLET_SPEED
        
        bullet = Bullet(x, y, vel_x, vel_y, damage, owner, 'homing')
        self.add_bullet(bullet)
        return bullet

    def update(self, dt: float, enemies: List = None, player = None):
        """Update all bullets."""
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet.update(dt, enemies, None)
            if bullet.is_expired():
                self.player_bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update(dt, None, player)
            if bullet.is_expired():
                self.enemy_bullets.remove(bullet)
    
    def render(self, screen: pygame.Surface):
        """Render all bullets."""
        # Render player bullets
        for bullet in self.player_bullets:
            bullet.render(screen)
        
        # Render enemy bullets
        for bullet in self.enemy_bullets:
            bullet.render(screen)
    
    def clear(self):
        """Clear all bullets."""
        self.player_bullets.clear()
        self.enemy_bullets.clear()
    
    def clear_player_bullets(self):
        """Clear only player bullets."""
        self.player_bullets.clear()
    
    def clear_enemy_bullets(self):
        """Clear only enemy bullets."""
        self.enemy_bullets.clear()
    
    def get_bullet_count(self) -> Tuple[int, int]:
        """Get count of player and enemy bullets."""
        return len(self.player_bullets), len(self.enemy_bullets)
    
    def create_bullet_spread(self, x: float, y: float, owner: str, 
                           bullet_count: int = 3, spread_angle: float = 0.5, 
                           speed: float = BULLET_SPEED, damage: int = 1):
        """Create a spread of bullets."""
        bullets = []
        
        for i in range(bullet_count):
            # Calculate angle for this bullet
            if bullet_count == 1:
                angle = 0
            else:
                angle = -spread_angle + (2 * spread_angle * i / (bullet_count - 1))
            
            # Calculate velocity
            if owner == 'player':
                base_vel_x = 0
                base_vel_y = -speed
            else:
                base_vel_x = 0
                base_vel_y = speed
            
            # Apply angle
            vel_x = base_vel_x * math.cos(angle) - base_vel_y * math.sin(angle)
            vel_y = base_vel_x * math.sin(angle) + base_vel_y * math.cos(angle)
            
            # Create bullet
            if owner == 'player':
                bullet = self.create_player_bullet(x, y, vel_x, vel_y, damage)
            else:
                bullet = self.create_enemy_bullet(x, y, vel_x, vel_y, damage)
            
            bullets.append(bullet)
        
        return bullets
    
    def create_circular_pattern(self, x: float, y: float, owner: str, 
                              bullet_count: int = 8, speed: float = BULLET_SPEED, 
                              damage: int = 1):
        """Create bullets in a circular pattern."""
        bullets = []
        angle_step = 2 * math.pi / bullet_count
        
        for i in range(bullet_count):
            angle = i * angle_step
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            if owner == 'player':
                bullet = self.create_player_bullet(x, y, vel_x, vel_y, damage)
            else:
                bullet = self.create_enemy_bullet(x, y, vel_x, vel_y, damage)
            
            bullets.append(bullet)
        
        return bullets
    
    def get_bullets_in_area(self, x: float, y: float, radius: float, 
                           owner: str = None) -> List[Bullet]:
        """Get bullets within a certain area."""
        bullets_in_area = []
        
        bullet_lists = []
        if owner == 'player' or owner is None:
            bullet_lists.append(self.player_bullets)
        if owner == 'enemy' or owner is None:
            bullet_lists.append(self.enemy_bullets)
        
        for bullet_list in bullet_lists:
            for bullet in bullet_list:
                distance = math.sqrt((bullet.x - x)**2 + (bullet.y - y)**2)
                if distance <= radius:
                    bullets_in_area.append(bullet)
        
        return bullets_in_area
    
    def remove_bullets_in_area(self, x: float, y: float, radius: float, 
                             owner: str = None) -> int:
        """Remove bullets within a certain area. Returns count removed."""
        removed_count = 0
        
        if owner == 'player' or owner is None:
            for bullet in self.player_bullets[:]:
                distance = math.sqrt((bullet.x - x)**2 + (bullet.y - y)**2)
                if distance <= radius:
                    self.player_bullets.remove(bullet)
                    removed_count += 1
        
        if owner == 'enemy' or owner is None:
            for bullet in self.enemy_bullets[:]:
                distance = math.sqrt((bullet.x - x)**2 + (bullet.y - y)**2)
                if distance <= radius:
                    self.enemy_bullets.remove(bullet)
                    removed_count += 1
        
        return removed_count
    
    def create_laser_beam(self, x: float, y: float, owner: str, 
                         length: int = 200, damage: int = 3):
        """Create a laser beam effect."""
        # Create multiple bullets in a line for laser effect
        bullets = []
        bullet_spacing = 10
        bullet_count = length // bullet_spacing
        
        for i in range(bullet_count):
            if owner == 'player':
                bullet_y = y - (i * bullet_spacing)
                bullet = self.create_player_bullet(x, bullet_y, 0, -BULLET_SPEED * 2, damage)
            else:
                bullet_y = y + (i * bullet_spacing)
                bullet = self.create_enemy_bullet(x, bullet_y, 0, BULLET_SPEED * 2, damage)
            
            bullets.append(bullet)
        
        return bullets

    def create_wave_pattern(self, x: float, y: float, owner: str,
                           wave_amplitude: float = 50, wave_frequency: float = 0.1,
                           bullet_count: int = 10, speed: float = BULLET_SPEED):
        """Create a wave pattern of bullets."""
        bullets = []
        
        for i in range(bullet_count):
            # Calculate wave offset
            wave_offset = math.sin(i * wave_frequency) * wave_amplitude
            
            if owner == 'player':
                vel_x = wave_offset * 0.1
                vel_y = -speed
            else:
                vel_x = wave_offset * 0.1
                vel_y = speed
            
            bullet_x = x + wave_offset
            
            if owner == 'player':
                bullet = self.create_player_bullet(bullet_x, y, vel_x, vel_y, 1)
            else:
                bullet = self.create_enemy_bullet(bullet_x, y, vel_x, vel_y, 1)
            
            bullets.append(bullet)
        
        return bullets
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics."""
        return {
            'player_bullets': len(self.player_bullets),
            'enemy_bullets': len(self.enemy_bullets),
            'total_bullets': len(self.player_bullets) + len(self.enemy_bullets),
            'max_bullets': self.max_bullets,
            'performance_ratio': (len(self.player_bullets) + len(self.enemy_bullets)) / self.max_bullets
        }
