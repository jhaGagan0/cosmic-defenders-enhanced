## game/powerup_enhanced.py
python
"""
Enhanced Power-Up Manager - Advanced Power-Up System
==================================================

Professional power-up system with:
- Multiple power-up types
- Visual effects
- Balanced spawn rates
- Special abilities
"""

import pygame
import math
import random
import time
from typing import List, Tuple, Dict
from enum import Enum

from settings_enhanced import *

class PowerUpType(Enum):
    """Power-up type enumeration."""
    HEALTH = "health"
    SHIELD = "shield"
    RAPID_FIRE = "rapid_fire"
    MULTI_SHOT = "multi_shot"
    SCREEN_CLEAR = "screen_clear"
    TIME_SLOW = "time_slow"
    HOMING = "homing"

class PowerUp:
    """Enhanced power-up class with effects and animations."""
    
    def __init__(self, x: float, y: float, powerup_type: PowerUpType):
        """Initialize a power-up."""
        self.x = x
        self.y = y
        self.type = powerup_type
        self.size = (24, 24)
        
        # Movement
        self.velocity_y = POWERUP_SPEED
        self.float_amplitude = 5
        self.float_frequency = 3
        self.lifetime = 0
        
        # Visual effects
        self.color = POWERUP_TYPES[powerup_type.value]['color']
        self.glow_intensity = 1.0
        self.rotation = 0
        self.pulse_phase = random.random() * math.pi * 2
        self.particles = []
        
        # Audio
        self.collected = False
        
        print(f"Created {powerup_type.value} power-up at ({x}, {y})")
    
    def update(self, dt: float):
        """Update power-up state."""
        self.lifetime += dt
        
        # Movement with floating effect
        self.y += self.velocity_y * dt * 60
        float_offset = math.sin(self.lifetime * self.float_frequency) * self.float_amplitude
        
        # Visual effects
        self.rotation += dt * 90  # Rotate 90 degrees per second
        self.pulse_phase += dt * 4
        self.glow_intensity = 0.7 + 0.3 * math.sin(self.pulse_phase)
        
        # Update particles
        self._update_particles(dt)
        
        # Add new particles
        if len(self.particles) < 8:
            self.particles.append({
                'x': self.x + random.randint(-10, 10),
                'y': self.y + random.randint(-10, 10),
                'vel_x': random.uniform(-20, 20),
                'vel_y': random.uniform(-20, 20),
                'alpha': 1.0,
                'size': random.randint(1, 3),
                'lifetime': 0
            })
    
    def _update_particles(self, dt: float):
        """Update power-up particles."""
        for particle in self.particles[:]:
            particle['lifetime'] += dt
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            particle['alpha'] = max(0, 1.0 - particle['lifetime'] * 2)
            
            if particle['alpha'] <= 0 or particle['lifetime'] > 1.0:
                self.particles.remove(particle)
    
    def is_expired(self) -> bool:
        """Check if power-up should be removed."""
        return self.y > SCREEN_HEIGHT + 50 or self.lifetime > 15.0
def get_description(self) -> str:
        """Get power-up description."""
        descriptions = {
            PowerUpType.HEALTH: "Restores 25 health points",
            PowerUpType.SHIELD: "Temporary invulnerability",
            PowerUpType.RAPID_FIRE: "Increased firing rate",
            PowerUpType.MULTI_SHOT: "Shoot multiple bullets",
            PowerUpType.SCREEN_CLEAR: "Destroys all enemies",
            PowerUpType.TIME_SLOW: "Slows down time",
            PowerUpType.HOMING: "Homing missiles"
        }
        return descriptions.get(self.type, "Unknown power-up")
    
    def render(self, screen: pygame.Surface):
        """Render the power-up with effects."""
        # Render particles
        for particle in self.particles:
            if particle['alpha'] > 0:
                color = (*self.color, int(particle['alpha'] * 255))
                size = int(particle['size'])
                if size > 0:
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, color, (size, size), size)
                    screen.blit(particle_surface, (int(particle['x'] - size), int(particle['y'] - size)))
        
        # Render glow effect
        glow_size = int(max(self.size) * 1.5 * self.glow_intensity)
        if glow_size > 0:
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            glow_color = (*self.color, 64)
            pygame.draw.circle(glow_surface, glow_color, (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (int(self.x - glow_size), int(self.y - glow_size)))
        
        # Create power-up surface
        powerup_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        # Draw power-up shape based on type
        self._render_powerup_shape(powerup_surface)
        
        # Apply rotation
        if abs(self.rotation) > 0.01:
            powerup_surface = pygame.transform.rotate(powerup_surface, self.rotation)
        
        # Apply pulsing scale
        scale = 0.9 + 0.1 * math.sin(self.pulse_phase)
        if scale != 1.0:
            new_size = (int(powerup_surface.get_width() * scale), 
                       int(powerup_surface.get_height() * scale))
            powerup_surface = pygame.transform.scale(powerup_surface, new_size)
        
        # Blit to screen
        rect = powerup_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(powerup_surface, rect)
    
    def _render_powerup_shape(self, surface: pygame.Surface):
        """Render power-up shape based on type."""
        center_x = self.size[0] // 2
        center_y = self.size[1] // 2
        
        if self.type == PowerUpType.HEALTH:
            # Cross shape
            pygame.draw.rect(surface, self.color, (center_x - 2, 2, 4, self.size[1] - 4))
            pygame.draw.rect(surface, self.color, (2, center_y - 2, self.size[0] - 4, 4))
            pygame.draw.rect(surface, WHITE, (center_x - 2, 2, 4, self.size[1] - 4), 1)
            pygame.draw.rect(surface, WHITE, (2, center_y - 2, self.size[0] - 4, 4), 1)
        
        elif self.type == PowerUpType.SHIELD:
            # Shield shape
            points = [
                (center_x, 2),
                (self.size[0] - 2, center_y),
                (center_x, self.size[1] - 2),
                (2, center_y)
            ]
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, WHITE, points, 2)
        
        elif self.type == PowerUpType.RAPID_FIRE:
            # Lightning bolt
            points = [
                (center_x - 4, 2),
                (center_x + 2, center_y - 2),
                (center_x - 2, center_y - 2),
                (center_x + 4, self.size[1] - 2),
                (center_x - 2, center_y + 2),
                (center_x + 2, center_y + 2)
            ]
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, WHITE, points, 1)
        
        elif self.type == PowerUpType.MULTI_SHOT:
            # Triple arrow
            for i in range(3):
                offset = (i - 1) * 6
                points = [
                    (center_x + offset, 2),
                    (center_x + offset + 3, center_y),
                    (center_x + offset, self.size[1] - 2),
                    (center_x + offset - 3, center_y)
                ]
                pygame.draw.polygon(surface, self.color, points)
                pygame.draw.polygon(surface, WHITE, points, 1)
        
        elif self.type == PowerUpType.SCREEN_CLEAR:
            # Explosion star
            points = []
            for i in range(8):
                angle = i * math.pi / 4
                if i % 2 == 0:
                    radius = self.size[0] // 2 - 2
                else:
                    radius = self.size[0] // 4
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                points.append((x, y))
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, WHITE, points, 1)
        
        elif self.type == PowerUpType.TIME_SLOW:
            # Clock/hourglass
            pygame.draw.circle(surface, self.color, (center_x, center_y), self.size[0] // 2 - 2)
            pygame.draw.circle(surface, WHITE, (center_x, center_y), self.size[0] // 2 - 2, 2)
            # Clock hands
            pygame.draw.line(surface, WHITE, (center_x, center_y), 
                           (center_x, center_y - 6), 2)
            pygame.draw.line(surface, WHITE, (center_x, center_y), 
                           (center_x + 4, center_y), 2)
        
        elif self.type == PowerUpType.HOMING:
            # Target/crosshair
            pygame.draw.circle(surface, self.color, (center_x, center_y), self.size[0] // 2 - 2, 2)
            pygame.draw.circle(surface, self.color, (center_x, center_y), self.size[0] // 4, 2)
            pygame.draw.line(surface, WHITE, (center_x - 8, center_y), (center_x + 8, center_y), 2)
            pygame.draw.line(surface, WHITE, (center_x, center_y - 8), (center_x, center_y + 8), 2)

class PowerUpManager:
    """Enhanced power-up manager for spawning and managing power-ups."""

    def __init__(self):
        """Initialize the power-up manager."""
        self.powerups = []
        self.spawn_cooldown = 0
        self.min_spawn_delay = 2.0  # Minimum seconds between spawns
        
        print("Power-Up Manager initialized successfully!")
    
    def spawn_powerup(self, x: float, y: float, powerup_type: PowerUpType = None) -> PowerUp:
        """
        Spawn a power-up at the specified location.
        
        Args:
            x, y: Spawn position
            powerup_type: Specific type to spawn, or None for random
            
        Returns:
            The spawned power-up
        """
        if powerup_type is None:
            powerup_type = self._choose_random_powerup()
        
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)
        
        return powerup
    
    def _choose_random_powerup(self) -> PowerUpType:
        """Choose a random power-up type based on weights."""
        # Create weighted list
        weighted_types = []
        for powerup_type_str, data in POWERUP_TYPES.items():
            weight = data['weight']
            powerup_type = PowerUpType(powerup_type_str)
            weighted_types.extend([powerup_type] * weight)
        
        return random.choice(weighted_types)
    
    def update(self, dt: float):
        """Update all power-ups."""
        self.spawn_cooldown = max(0, self.spawn_cooldown - dt)
        
        # Update all power-ups
        for powerup in self.powerups[:]:
            powerup.update(dt)
            
            # Remove expired power-ups
            if powerup.is_expired():
                self.powerups.remove(powerup)
    
    def render(self, screen: pygame.Surface):
        """Render all power-ups."""
        for powerup in self.powerups:
            powerup.render(screen)
    
    def clear(self):
        """Clear all power-ups."""
        self.powerups.clear()
    
    def get_powerup_count(self) -> int:
        """Get current power-up count."""
        return len(self.powerups)
    
    def get_powerups_in_area(self, x: float, y: float, radius: float) -> List[PowerUp]:
        """Get power-ups within a certain area."""
        powerups_in_area = []
        
        for powerup in self.powerups:
            distance = math.sqrt((powerup.x - x)**2 + (powerup.y - y)**2)
            if distance <= radius:
                powerups_in_area.append(powerup)
        
        return powerups_in_area
    
    def remove_powerup(self, powerup: PowerUp) -> bool:
        """Remove a specific power-up."""
        if powerup in self.powerups:
            self.powerups.remove(powerup)
            return True
        return False
    
    def spawn_random_powerup(self) -> PowerUp:
        """Spawn a random power-up at a random location."""
        if self.spawn_cooldown > 0:
            return None
        
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(-50, 0)
        
        powerup = self.spawn_powerup(x, y)
        self.spawn_cooldown = self.min_spawn_delay
        
        return powerup
    
    def get_powerup_statistics(self) -> Dict[str, int]:
        """Get statistics about current power-ups."""
        stats = {}
        
        for powerup in self.powerups:
            powerup_type = powerup.type.value
            stats[powerup_type] = stats.get(powerup_type, 0) + 1
        
        return stats
    
    def spawn_powerup_chain(self, start_x: float, start_y: float, 
                           count: int = 3, spacing: float = 50) -> List[PowerUp]:
        """Spawn a chain of power-ups."""
        powerups = []
        
        for i in range(count):
            x = start_x + (i - count // 2) * spacing
            y = start_y
            
            powerup = self.spawn_powerup(x, y)
            powerups.append(powerup)
        
        return powerups
    
    def spawn_rare_powerup(self, x: float, y: float) -> PowerUp:
        """Spawn a rare power-up (homing or time_slow)."""
        rare_types = [PowerUpType.HOMING, PowerUpType.TIME_SLOW]
        powerup_type = random.choice(rare_types)
        
        return self.spawn_powerup(x, y, powerup_type)
    
    def create_powerup_explosion(self, center_x: float, center_y: float, 
                                count: int = 5) -> List[PowerUp]:
        """Create an explosion of power-ups from a central point."""
        powerups = []
        
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            distance = random.uniform(30, 80)
            
            x = center_x + math.cos(angle) * distance
            y = center_y + math.sin(angle) * distance
            
            powerup = self.spawn_powerup(x, y)
            powerups.append(powerup)
        
        return powerups
    
    def apply_powerup_effect(self, powerup_type: PowerUpType, player, 
                           enemy_manager=None, bullet_manager=None, 
                           particle_manager=None) -> Dict:
        """Apply power-up effect and return result information."""
        result = {
            'type': powerup_type.value,
            'success': True,
            'message': '',
            'effects': []
        }
        
        if powerup_type == PowerUpType.HEALTH:
            if player:
                old_health = player.health
                player.health = min(player.max_health, player.health + 25)
                healed = player.health - old_health
                result['message'] = f"Restored {healed} health"
                result['effects'].append('health_restored')
        
        elif powerup_type == PowerUpType.SHIELD:
            if player:
                player.apply_powerup(powerup_type)
                result['message'] = "Shield activated"
                result['effects'].append('shield_activated')
        
        elif powerup_type == PowerUpType.RAPID_FIRE:
            if player:
                player.apply_powerup(powerup_type)
                result['message'] = "Rapid fire enabled"
                result['effects'].append('rapid_fire_enabled')
        
        elif powerup_type == PowerUpType.MULTI_SHOT:
            if player:
                player.apply_powerup(powerup_type)
                result['message'] = "Multi-shot enabled"
                result['effects'].append('multi_shot_enabled')
        
        elif powerup_type == PowerUpType.SCREEN_CLEAR:
            if enemy_manager and particle_manager:
                destroyed_count = len(enemy_manager.enemies)
                
                # Create explosion effects for each enemy
                for enemy in enemy_manager.enemies:
                    particle_manager.create_explosion(enemy.x, enemy.y, 15)
                
                # Clear all enemies
                enemy_manager.clear()
                
                # Create screen-wide effect
                particle_manager.create_screen_clear_effect(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                )
                
                result['message'] = f"Destroyed {destroyed_count} enemies"
                result['effects'].append('screen_cleared')
        
        elif powerup_type == PowerUpType.TIME_SLOW:
            if player:
                player.apply_powerup(powerup_type)
                result['message'] = "Time slowed"
                result['effects'].append('time_slowed')
        
        elif powerup_type == PowerUpType.HOMING:
            if player:
                player.apply_powerup(powerup_type)
                result['message'] = "Homing missiles ready"
                result['effects'].append('homing_enabled')
        
        return result
    
    def get_powerup_rarity(self, powerup_type: PowerUpType) -> str:
        """Get rarity classification of power-up."""
        weights = POWERUP_TYPES.get(powerup_type.value, {}).get('weight', 0)
        
        if weights >= 20:
            return "Common"
        elif weights >= 10:
            return "Uncommon"
        elif weights >= 5:
            return "Rare"
        else:
            return "Legendary"
    
    def create_boss_reward_powerups(self, boss_x: float, boss_y: float) -> List[PowerUp]:
        """Create special power-ups when boss is defeated."""
        powerups = []
        
        # Always spawn health and shield
        powerups.append(self.spawn_powerup(boss_x - 30, boss_y, PowerUpType.HEALTH))
        powerups.append(self.spawn_powerup(boss_x + 30, boss_y, PowerUpType.SHIELD))
        
        # 50% chance for rare power-up
        if random.random() < 0.5:
            rare_powerup = self.spawn_rare_powerup(boss_x, boss_y - 40)
            powerups.append(rare_powerup)
        
        # 25% chance for screen clear
        if random.random() < 0.25:
            screen_clear = self.spawn_powerup(boss_x, boss_y + 40, PowerUpType.SCREEN_CLEAR)
            powerups.append(screen_clear)
        
        return powerups
    
    def update_with_time_scale(self, dt: float, time_scale: float = 1.0):
        """Update power-ups with time scaling for slow motion effects."""
        scaled_dt = dt * time_scale
        self.spawn_cooldown = max(0, self.spawn_cooldown - dt)  # Real time
        
        # Update power-ups with scaled time
        for powerup in self.powerups[:]:
            # Save original values
            original_velocity = powerup.velocity_y
            original_frequency = powerup.float_frequency
            
            # Apply time scale
            powerup.velocity_y *= time_scale
            powerup.float_frequency *= time_scale
            
            # Update
            powerup.update(scaled_dt)
            
            # Restore original values
            powerup.velocity_y = original_velocity
            powerup.float_frequency = original_frequency
            
            # Remove expired power-ups
            if powerup.is_expired():
                self.powerups.remove(powerup)
