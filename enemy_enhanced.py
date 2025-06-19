## game/enemy_enhanced.py
python
"""
Enhanced Enemy Manager - Advanced AI and Enemy System
===================================================

Professional enemy system with:
- Multiple enemy types with unique AI
- Boss battles
- Formation flying
- Dynamic difficulty scaling
"""

import pygame
import math
import random
import time
from typing import List, Tuple, Optional, Dict
from enum import Enum

from settings_enhanced import *

class EnemyType(Enum):
    """Enemy type enumeration."""
    BASIC = "basic"
    FAST = "fast"
    HEAVY = "heavy"
    ZIGZAG = "zigzag"
    BOSS = "boss"

class Enemy:
    """Enhanced enemy class with AI and behaviors."""
    
    def __init__(self, x: float, y: float, enemy_type: EnemyType, difficulty: str):
        """Initialize an enemy."""
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.difficulty = difficulty
        
        # Apply base stats
        self._apply_base_stats()
        
        # Apply difficulty modifiers
        self._apply_difficulty_modifiers()
        
        # Movement and AI
        self.velocity_x = 0
        self.velocity_y = self.speed
        self.target_x = x
        self.target_y = y
        
        # AI state
        self.ai_timer = 0
        self.ai_state = "moving"
        self.formation_offset = random.random() * math.pi * 2
        
        # Combat
        self.last_shot_time = 0
        self.fire_rate = self._get_fire_rate()
        self.bullet_damage = 1
        
        # Visual effects
        self.sprite_angle = 0
        self.damage_flash = 0
        self.engine_particles = []
        
        # Boss-specific
        self.attack_pattern = 0
        self.pattern_timer = 0
        self.is_boss = (enemy_type == EnemyType.BOSS)
        
        print(f"Created {enemy_type.value} enemy with {self.health} health")
    
    def _apply_base_stats(self):
        """Apply base stats based on enemy type."""
        self.max_health = ENEMY_HEALTHS[self.enemy_type.value]
        self.health = self.max_health
        self.speed = ENEMY_SPEEDS[self.enemy_type.value]
        self.size = ENEMY_SIZES[self.enemy_type.value]
        self.score_value = ENEMY_SCORES[self.enemy_type.value]
        self.color = self._get_enemy_color()
    
    def _apply_difficulty_modifiers(self):
        """Apply difficulty-based modifiers."""
        diff_settings = DIFFICULTIES[self.difficulty]
        
        self.health = int(self.health * diff_settings['enemy_health_mult'])
        self.max_health = self.health
        self.speed *= diff_settings['enemy_speed_mult']
        self.score_value = int(self.score_value * diff_settings['score_mult'])
    
    def _get_enemy_color(self) -> Tuple[int, int, int]:
        """Get color based on enemy type."""
        color_map = {
            EnemyType.BASIC: ENEMY_BASIC,
            EnemyType.FAST: ENEMY_FAST,
            EnemyType.HEAVY: ENEMY_HEAVY,
            EnemyType.ZIGZAG: ENEMY_ZIGZAG,
            EnemyType.BOSS: BOSS_COLOR
        }
        return color_map.get(self.enemy_type, WHITE)
    
    def _get_fire_rate(self) -> float:
        """Get fire rate based on enemy type."""
        fire_rates = {
            EnemyType.BASIC: 1.0,
            EnemyType.FAST: 1.5,
            EnemyType.HEAVY: 0.5,
            EnemyType.ZIGZAG: 0.8,
            EnemyType.BOSS: 3.0
        }
        return fire_rates.get(self.enemy_type, 1.0)
    
    def update(self, dt: float, player_x: float, player_y: float, bullet_manager):
        """Update enemy behavior."""
        self.ai_timer += dt
        
        # Update AI based on type
        if self.enemy_type == EnemyType.BASIC:
            self._update_basic_ai(dt, player_x, player_y)
        elif self.enemy_type == EnemyType.FAST:
            self._update_fast_ai(dt, player_x, player_y)
        elif self.enemy_type == EnemyType.HEAVY:
            self._update_heavy_ai(dt, player_x, player_y)
        elif self.enemy_type == EnemyType.ZIGZAG:
            self._update_zigzag_ai(dt, player_x, player_y)
        elif self.enemy_type == EnemyType.BOSS:
            self._update_boss_ai(dt, player_x, player_y)
        
        # Update position
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        # Update visual effects
        self._update_visual_effects(dt)
        
        # Handle shooting
        self._handle_shooting(dt, player_x, player_y, bullet_manager)
        
        # Keep on screen (except for vertical movement)
        self.x = max(self.size[0] // 2, min(SCREEN_WIDTH - self.size[0] // 2, self.x))
    
    def _update_basic_ai(self, dt: float, player_x: float, player_y: float):
        """Basic enemy AI - simple downward movement."""
        self.velocity_x = 0
        self.velocity_y = self.speed
        
        # Slight horizontal movement towards player
        if abs(player_x - self.x) > 50:
            self.velocity_x = 0.5 * (1 if player_x > self.x else -1)
    
    def _update_fast_ai(self, dt: float, player_x: float, player_y: float):
        """Fast enemy AI - erratic movement."""
        # Change direction randomly
        if self.ai_timer > 0.5:
            self.target_x = random.randint(50, SCREEN_WIDTH - 50)
            self.ai_timer = 0
        
        # Move towards target
        dx = self.target_x - self.x
        self.velocity_x = dx * 0.1
        self.velocity_y = self.speed
    
    def _update_heavy_ai(self, dt: float, player_x: float, player_y: float):
        """Heavy enemy AI - slow but steady."""
        self.velocity_x = 0
        self.velocity_y = self.speed * 0.8  # Slightly slower
        
        # Occasional side movement
        if int(self.ai_timer * 2) % 4 == 0:
            self.velocity_x = math.sin(self.ai_timer) * 0.5
    
    def _update_zigzag_ai(self, dt: float, player_x: float, player_y: float):
        """Zigzag enemy AI - side to side movement."""
        self.velocity_x = math.sin(self.ai_timer * 3) * 2
        self.velocity_y = self.speed
    
    def _update_boss_ai(self, dt: float, player_x: float, player_y: float):
        """Boss enemy AI - complex attack patterns."""
        self.pattern_timer += dt
        
        # Switch attack patterns every 5 seconds
        if self.pattern_timer > 5.0:
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.pattern_timer = 0
        
        if self.attack_pattern == 0:
            # Pattern 1: Side to side movement
            self.velocity_x = math.sin(self.ai_timer * 2) * 3
            self.velocity_y = 0.5
        elif self.attack_pattern == 1:
            # Pattern 2: Circle around player
            angle = self.ai_timer * 2
            center_x = SCREEN_WIDTH // 2
            center_y = 150
            radius = 100
            self.target_x = center_x + math.cos(angle) * radius
            self.target_y = center_y + math.sin(angle) * radius * 0.5
            
            self.velocity_x = (self.target_x - self.x) * 0.05
            self.velocity_y = (self.target_y - self.y) * 0.05
        else:
            # Pattern 3: Aggressive approach
            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 200:
                self.velocity_x = (dx / distance) * 2
                self.velocity_y = (dy / distance) * 2
            else:
                self.velocity_x = -dx * 0.01
                self.velocity_y = -dy * 0.01
    
    def _update_visual_effects(self, dt: float):
        """Update visual effects."""
        # Damage flash
        if self.damage_flash > 0:
            self.damage_flash = max(0, self.damage_flash - dt * 5)
        
        # Sprite rotation based on movement
        if abs(self.velocity_x) > 0.1:
            target_angle = math.atan2(self.velocity_x, -abs(self.velocity_y)) * 0.5
            self.sprite_angle += (target_angle - self.sprite_angle) * 0.1
        
        # Engine particles
        if len(self.engine_particles) < 5:
            self.engine_particles.append({
                'x': self.x + random.randint(-5, 5),
                'y': self.y + self.size[1] // 2,
                'alpha': 1.0,
                'size': random.randint(2, 4)
            })
        
        # Update particles
        for particle in self.engine_particles[:]:
            particle['alpha'] -= dt * 3
            particle['y'] += 50 * dt
            if particle['alpha'] <= 0:
                self.engine_particles.remove(particle)
    
    def _handle_shooting(self, dt: float, player_x: float, player_y: float, bullet_manager):
        """Handle enemy shooting."""
        if bullet_manager is None:
            return
            
        current_time = time.time()
        
        if current_time - self.last_shot_time < 1.0 / self.fire_rate:
            return
        
        # Don't shoot if too far from player
        distance_to_player = math.sqrt((player_x - self.x)**2 + (player_y - self.y)**2)
        if distance_to_player > 400:
            return
        
        self.last_shot_time = current_time
        
        if self.enemy_type == EnemyType.BOSS:
            self._boss_shooting_pattern(bullet_manager, player_x, player_y)
        else:
            self._basic_shooting(bullet_manager, player_x, player_y)
    
    def _basic_shooting(self, bullet_manager, player_x: float, player_y: float):
        """Basic enemy shooting."""
        # Shoot towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            speed = BULLET_SPEED * 0.8
            vel_x = (dx / distance) * speed
            vel_y = (dy / distance) * speed
            
            bullet_manager.create_enemy_bullet(
                self.x, self.y + self.size[1] // 2,
                vel_x, vel_y, self.bullet_damage
            )
    
    def _boss_shooting_pattern(self, bullet_manager, player_x: float, player_y: float):
        """Boss shooting patterns."""
        if self.attack_pattern == 0:
            # Spread shot
            bullet_manager.create_bullet_spread(
                self.x, self.y + self.size[1] // 2,
                'enemy', bullet_count=5, spread_angle=0.8,
                speed=BULLET_SPEED * 0.6, damage=self.bullet_damage
            )
        elif self.attack_pattern == 1:
            # Circular pattern
            bullet_manager.create_circular_pattern(
                self.x, self.y + self.size[1] // 2,
                'enemy', bullet_count=8,
                speed=BULLET_SPEED * 0.5, damage=self.bullet_damage
            )
        else:
            # Homing missiles
            for _ in range(2):
                bullet_manager.create_homing_missile(
                    self.x + random.randint(-20, 20),
                    self.y + self.size[1] // 2,
                    'enemy', damage=self.bullet_damage * 2
                )
              def take_damage(self, damage: int) -> bool:
        """Take damage and return True if destroyed."""
        self.health -= damage
        self.damage_flash = 0.3
        
        if self.health <= 0:
            return True
        
        return False

    def is_off_screen(self) -> bool:
        """Check if enemy is off screen."""
        return (self.y > SCREEN_HEIGHT + 50 or
                self.x < -50 or self.x > SCREEN_WIDTH + 50)
    
    def render(self, screen: pygame.Surface):
        """Render the enemy with effects."""
        # Render engine particles
        for particle in self.engine_particles:
            if particle['alpha'] > 0:
                color = (*self.color, int(particle['alpha'] * 128))
                size = int(particle['size'])
                if size > 0:
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, color, (size, size), size)
                    screen.blit(particle_surface, (int(particle['x'] - size), int(particle['y'] - size)))
        
        # Calculate render position
        render_x = int(self.x)
        render_y = int(self.y)
        
        # Damage flash effect
        if self.damage_flash > 0:
            flash_intensity = int(self.damage_flash * 255)
            color = (255, 255 - flash_intensity, 255 - flash_intensity)
        else:
            color = self.color
        
        # Create enemy surface
        enemy_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        
        # Draw enemy shape based on type
        if self.enemy_type == EnemyType.BOSS:
            self._render_boss_shape(enemy_surface, color)
        else:
            self._render_normal_shape(enemy_surface, color)
        
        # Apply rotation
        if abs(self.sprite_angle) > 0.01:
            enemy_surface = pygame.transform.rotate(enemy_surface, math.degrees(self.sprite_angle))
        
        # Blit to screen
        rect = enemy_surface.get_rect(center=(render_x, render_y))
        screen.blit(enemy_surface, rect)
        
        # Render health bar for bosses
        if self.is_boss:
            self._render_health_bar(screen, render_x, render_y)
    
    def _render_normal_shape(self, surface: pygame.Surface, color: Tuple[int, int, int]):
        """Render normal enemy shape."""
        # Draw main body (inverted triangle)
        points = [
            (self.size[0] // 2, self.size[1]),  # Bottom center
            (0, 0),                             # Top left
            (self.size[0], 0)                   # Top right
        ]
        pygame.draw.polygon(surface, color, points)
        
        # Add details based on type
        if self.enemy_type == EnemyType.HEAVY:
            # Thicker outline for heavy enemies
            pygame.draw.polygon(surface, WHITE, points, 3)
        else:
            pygame.draw.polygon(surface, WHITE, points, 1)
        
        # Add center line
        pygame.draw.line(surface, WHITE,
                        (self.size[0] // 2, 0),
                        (self.size[0] // 2, self.size[1] - 5), 2)
    
    def _render_boss_shape(self, surface: pygame.Surface, color: Tuple[int, int, int]):
        """Render boss enemy shape."""
        # Main body
        center_x = self.size[0] // 2
        center_y = self.size[1] // 2
        
        # Draw hexagon
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center_x + math.cos(angle) * (self.size[0] // 2 - 5)
            y = center_y + math.sin(angle) * (self.size[1] // 2 - 5)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, WHITE, points, 2)
        
        # Add inner details
        inner_points = []
        for i in range(6):
            angle = i * math.pi / 3
            x = center_x + math.cos(angle) * (self.size[0] // 4)
            y = center_y + math.sin(angle) * (self.size[1] // 4)
            inner_points.append((x, y))
        
        pygame.draw.polygon(surface, WHITE, inner_points, 1)
    
    def _render_health_bar(self, screen: pygame.Surface, x: int, y: int):
        """Render health bar for boss enemies."""
        bar_width = 100
        bar_height = 8
        bar_x = x - bar_width // 2
        bar_y = y - self.size[1] // 2 - 20
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, UI_SECONDARY, bg_rect)
        
        # Health fill
        health_percent = self.health / self.max_health
        fill_width = int(bar_width * health_percent)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
        
        if health_percent > 0.6:
            health_color = UI_SUCCESS
        elif health_percent > 0.3:
            health_color = UI_WARNING
        else:
            health_color = UI_DANGER
        
        pygame.draw.rect(screen, health_color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, WHITE, bg_rect, 1)

class EnemyManager:
    """Enhanced enemy manager for spawning and managing enemies."""
    
    def __init__(self):
        """Initialize the enemy manager."""
        self.enemies = []
        self.spawn_timer = 0
        self.wave_timer = 0
        self.current_wave = 1
        self.spawning = False
        self.enemies_to_spawn = 0
        self.spawn_delay = 1.0  # seconds between spawns
        
        print("Enemy Manager initialized successfully!")
    
    def start_wave(self, wave_number: int):
        """Start a new wave of enemies."""
        self.current_wave = wave_number
        self.spawning = True
        self.spawn_timer = 0
        self.wave_timer = 0
        
        # Calculate enemies to spawn
        base_enemies = ENEMIES_PER_WAVE_BASE
        additional_enemies = (wave_number - 1) * 2
        self.enemies_to_spawn = base_enemies + additional_enemies
        
        # Boss wave
        if wave_number % BOSS_WAVE_INTERVAL == 0:
            self.enemies_to_spawn = 1  # Only spawn boss
        
        print(f"Starting wave {wave_number} with {self.enemies_to_spawn} enemies")
    
    def update(self, dt: float, wave_number: int, difficulty: str, 
               player_x: float = 0, player_y: float = 0, bullet_manager = None):
        """Update enemy manager."""
        self.wave_timer += dt
        
        # Spawn enemies
        if self.spawning:
            self._handle_spawning(dt, wave_number, difficulty)
        
        # Update all enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, player_x, player_y, bullet_manager)
            
            # Remove off-screen enemies
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Check if wave is complete
        if not self.spawning and len(self.enemies) == 0:
            print(f"Wave {wave_number} complete!")
    
    def _handle_spawning(self, dt: float, wave_number: int, difficulty: str):
        """Handle enemy spawning."""
        self.spawn_timer += dt
        
        if self.spawn_timer >= self.spawn_delay and self.enemies_to_spawn > 0:
            self._spawn_enemy(wave_number, difficulty)
            self.enemies_to_spawn -= 1
            self.spawn_timer = 0
            
            if self.enemies_to_spawn <= 0:
                self.spawning = False
    
    def _spawn_enemy(self, wave_number: int, difficulty: str):
        """Spawn a single enemy."""
        # Determine enemy type
        if wave_number % BOSS_WAVE_INTERVAL == 0:
            enemy_type = EnemyType.BOSS
        else:
            enemy_type = self._choose_enemy_type(wave_number)
        
        # Spawn position
        if enemy_type == EnemyType.BOSS:
            x = SCREEN_WIDTH // 2
            y = -50
        else:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(-100, -50)
        
        # Create enemy
        enemy = Enemy(x, y, enemy_type, difficulty)
        self.enemies.append(enemy)

    def _choose_enemy_type(self, wave_number: int) -> EnemyType:
        """Choose enemy type based on wave number."""
        # Define spawn weights based on wave
        if wave_number <= 2:
            weights = {'basic': 100}
        elif wave_number <= 5:
            weights = {'basic': 70, 'fast': 30}
        elif wave_number <= 10:
            weights = {'basic': 50, 'fast': 30, 'heavy': 20}
        else:
            weights = {'basic': 40, 'fast': 30, 'heavy': 20, 'zigzag': 10}
        
        # Choose based on weights
        total_weight = sum(weights.values())
        rand_value = random.randint(1, total_weight)
        
        current_weight = 0
        for enemy_type_str, weight in weights.items():
            current_weight += weight
            if rand_value <= current_weight:
                return EnemyType(enemy_type_str)
        
        return EnemyType.BASIC  # Fallback
    
    def render(self, screen: pygame.Surface):
        """Render all enemies."""
        for enemy in self.enemies:
            enemy.render(screen)
    
    def clear(self):
        """Clear all enemies."""
        self.enemies.clear()
        self.spawning = False
        self.enemies_to_spawn = 0
    
    def get_enemy_count(self) -> int:
        """Get current enemy count."""
        return len(self.enemies)
    
    def get_enemies_in_area(self, x: float, y: float, radius: float) -> List[Enemy]:
        """Get enemies within a certain area."""
        enemies_in_area = []
        
        for enemy in self.enemies:
            distance = math.sqrt((enemy.x - x)**2 + (enemy.y - y)**2)
            if distance <= radius:
                enemies_in_area.append(enemy)
        
        return enemies_in_area
    
    def damage_enemies_in_area(self, x: float, y: float, radius: float, damage: int) -> int:
        """Damage all enemies in an area. Returns number of enemies destroyed."""
        destroyed_count = 0
        
        for enemy in self.enemies[:]:
            distance = math.sqrt((enemy.x - x)**2 + (enemy.y - y)**2)
            if distance <= radius:
                if enemy.take_damage(damage):
                    self.enemies.remove(enemy)
                    destroyed_count += 1
        
        return destroyed_count
                  
