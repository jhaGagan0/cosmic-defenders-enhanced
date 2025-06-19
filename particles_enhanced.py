## game/particles_enhanced.py
python
"""
Enhanced Particle Manager - Advanced Visual Effects System
========================================================

Professional particle system with:
- Multiple particle types
- Performance optimization
- Visual effects
- Background elements
"""

import pygame
import math
import random
from typing import List, Tuple, Dict, Optional
from enum import Enum

from settings_enhanced import *

class ParticleType(Enum):
    """Particle type enumeration."""
    EXPLOSION = "explosion"
    TRAIL = "trail"
    SPARK = "spark"
    STAR = "star"
    DEBRIS = "debris"
    SMOKE = "smoke"
    ENERGY = "energy"

class Particle:
    """Enhanced particle class with various effects."""
    
    def __init__(self, x: float, y: float, particle_type: ParticleType, 
                 velocity: Tuple[float, float] = (0, 0), 
                 color: Tuple[int, int, int] = WHITE,
                 size: float = 2.0, lifetime: float = 1.0):
        """Initialize a particle."""
        self.x = x
        self.y = y
        self.type = particle_type
        self.vel_x, self.vel_y = velocity
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.alpha = 255
        
        # Physics
        self.gravity = 0
        self.friction = 1.0
        self.bounce = 0
        
        # Visual effects
        self.rotation = 0
        self.rotation_speed = 0
        self.scale = 1.0
        self.fade_rate = 1.0
        
        # Apply type-specific properties
        self._apply_type_properties()
    
    def _apply_type_properties(self):
        """Apply properties based on particle type."""
        if self.type == ParticleType.EXPLOSION:
            self.gravity = 50
            self.friction = 0.95
            self.fade_rate = 2.0
            self.rotation_speed = random.uniform(-180, 180)
        
        elif self.type == ParticleType.TRAIL:
            self.friction = 0.98
            self.fade_rate = 3.0
        
        elif self.type == ParticleType.SPARK:
            self.gravity = 100
            self.friction = 0.99
            self.fade_rate = 4.0
            self.bounce = 0.3
        
        elif self.type == ParticleType.STAR:
            self.vel_y = random.uniform(10, 50)
            self.fade_rate = 0.1  # Very slow fade
            self.rotation_speed = random.uniform(-30, 30)
        
        elif self.type == ParticleType.DEBRIS:
            self.gravity = 80
            self.friction = 0.97
            self.rotation_speed = random.uniform(-90, 90)
            self.bounce = 0.2
        
        elif self.type == ParticleType.SMOKE:
            self.vel_y -= 20  # Rise upward
            self.friction = 0.99
            self.fade_rate = 1.5
            self.scale = random.uniform(0.5, 1.5)
        
        elif self.type == ParticleType.ENERGY:
            self.friction = 0.99
            self.fade_rate = 2.0
            self.rotation_speed = random.uniform(-360, 360)
    
    def update(self, dt: float):
        """Update particle state."""
        # Update lifetime
        self.lifetime -= dt * self.fade_rate
        
        # Update physics
        self.vel_y += self.gravity * dt
        self.vel_x *= self.friction
        self.vel_y *= self.friction
        
        # Update position
        self.x += self.vel_x * dt * 60
        self.y += self.vel_y * dt * 60
        
        # Handle bouncing
        if self.bounce > 0:
            if self.y > SCREEN_HEIGHT - 10 and self.vel_y > 0:
                self.vel_y *= -self.bounce
                self.y = SCREEN_HEIGHT - 10
        
        # Update visual properties
        self.rotation += self.rotation_speed * dt
        self.alpha = int(255 * max(0, self.lifetime / self.max_lifetime))
        
        # Scale changes for some particle types
        if self.type == ParticleType.EXPLOSION:
            self.scale = 1.0 + (1.0 - self.lifetime / self.max_lifetime) * 0.5
        elif self.type == ParticleType.SMOKE:
            self.scale += dt * 0.5  # Grow over time
    
    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return (self.lifetime > 0 and 
                self.x > -50 and self.x < SCREEN_WIDTH + 50 and
                self.y > -50 and self.y < SCREEN_HEIGHT + 50)
    
    def render(self, screen: pygame.Surface):
        """Render the particle."""
        if self.alpha <= 0:
            return
        
        # Calculate render properties
        render_size = max(1, int(self.size * self.scale))
        render_color = (*self.color, self.alpha)
        
        # Create particle surface
        particle_surface = pygame.Surface((render_size * 2, render_size * 2), pygame.SRCALPHA)
        
        # Draw particle based on type
        if self.type == ParticleType.STAR:
            self._render_star(particle_surface, render_size, render_color)
        elif self.type == ParticleType.DEBRIS:
            self._render_debris(particle_surface, render_size, render_color)
        elif self.type == ParticleType.ENERGY:
            self._render_energy(particle_surface, render_size, render_color)
        else:
            # Default circle
            pygame.draw.circle(particle_surface, render_color, 
                             (render_size, render_size), render_size)
        
        # Apply rotation
        if abs(self.rotation) > 0.01:
            particle_surface = pygame.transform.rotate(particle_surface, self.rotation)
        
        # Blit to screen
        rect = particle_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(particle_surface, rect)
    
    def _render_star(self, surface: pygame.Surface, size: int, color: Tuple[int, int, int, int]):
        """Render star-shaped particle."""
        center = size
        points = []
        
        for i in range(8):
            angle = i * math.pi / 4
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            
            x = center + math.cos(angle) * radius
            y = center + math.sin(angle) * radius
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
    
    def _render_debris(self, surface: pygame.Surface, size: int, color: Tuple[int, int, int, int]):
        """Render debris-shaped particle."""
        # Random polygon
        center = size
        points = []
        num_points = random.randint(3, 6)

        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            radius = random.uniform(size * 0.5, size)
            x = center + math.cos(angle) * radius
            y = center + math.sin(angle) * radius
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
    
    def _render_energy(self, surface: pygame.Surface, size: int, color: Tuple[int, int, int, int]):
        """Render energy-shaped particle."""
        center = size
        
        # Draw multiple overlapping circles with different alphas
        for i in range(3):
            alpha = color[3] // (i + 1)
            energy_color = (*color[:3], alpha)
            radius = size - i * 2
            if radius > 0:
                pygame.draw.circle(surface, energy_color, (center, center), radius)

class ParticleManager:
    """Enhanced particle manager for all visual effects."""
    
    def __init__(self):
        """Initialize the particle manager."""
        self.particles = []
        self.background_stars = []
        self.max_particles = MAX_PARTICLES
        
        # Performance tracking
        self.particle_count_by_type = {}
        
        # Initialize background
        self._create_background_stars()
        
        print("Particle Manager initialized successfully!")
    
    def _create_background_stars(self):
        """Create background star field."""
        for _ in range(STAR_COUNT):
            star = Particle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                ParticleType.STAR,
                velocity=(0, random.uniform(10, 50)),
                color=(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)),
                size=random.uniform(1, 3),
                lifetime=float('inf')  # Stars don't fade
            )
            self.background_stars.append(star)
    
    def create_explosion(self, x: float, y: float, particle_count: int = 20, 
                        color: Tuple[int, int, int] = (255, 200, 100)):
        """Create an explosion effect."""
        for _ in range(particle_count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            # Vary particle properties
            particle_color = (
                color[0] + random.randint(-50, 50),
                color[1] + random.randint(-50, 50),
                color[2] + random.randint(-50, 50)
            )
            particle_color = tuple(max(0, min(255, c)) for c in particle_color)
            
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                ParticleType.EXPLOSION,
                velocity=(vel_x, vel_y),
                color=particle_color,
                size=random.uniform(2, 6),
                lifetime=random.uniform(0.5, 1.5)
            )
            
            self.add_particle(particle)
    
    def create_trail(self, x: float, y: float, velocity: Tuple[float, float],
                    color: Tuple[int, int, int] = UI_PRIMARY, count: int = 3):
        """Create a trail effect."""
        for i in range(count):
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            # Trail particles move opposite to the object
            trail_vel_x = -velocity[0] * 0.3 + random.uniform(-20, 20)
            trail_vel_y = -velocity[1] * 0.3 + random.uniform(-20, 20)
            
            particle = Particle(
                x + offset_x,
                y + offset_y,
                ParticleType.TRAIL,
                velocity=(trail_vel_x, trail_vel_y),
                color=color,
                size=random.uniform(1, 3),
                lifetime=random.uniform(0.3, 0.8)
            )
            
            self.add_particle(particle)
    
    def create_sparks(self, x: float, y: float, count: int = 10,
                     color: Tuple[int, int, int] = (255, 255, 100)):
        """Create spark effects."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 100)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x,
                y,
                ParticleType.SPARK,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(1, 2),
                lifetime=random.uniform(0.2, 0.6)
            )
            
            self.add_particle(particle)
    
    def create_debris(self, x: float, y: float, count: int = 8,
                     color: Tuple[int, int, int] = (150, 150, 150)):
        """Create debris effects."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 80)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x,
                y,
                ParticleType.DEBRIS,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(2, 5),
                lifetime=random.uniform(1.0, 3.0)
            )
            
            self.add_particle(particle)
    
    def create_energy_burst(self, x: float, y: float, count: int = 15,
                           color: Tuple[int, int, int] = (100, 200, 255)):
        """Create energy burst effect."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(40, 120)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x,
                y,
                ParticleType.ENERGY,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(3, 8),
                lifetime=random.uniform(0.8, 1.5)
            )
            
            self.add_particle(particle)
    
    def create_smoke_trail(self, x: float, y: float, count: int = 5,
                          color: Tuple[int, int, int] = (128, 128, 128)):
        """Create smoke trail effect."""
        for _ in range(count):
            vel_x = random.uniform(-10, 10)
            vel_y = random.uniform(-30, -10)  # Upward movement
            
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                ParticleType.SMOKE,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(3, 8),
                lifetime=random.uniform(2.0, 4.0)
            )
            
            self.add_particle(particle)
    
    def create_warp_effect(self, x: float, y: float, count: int = 30):
        """Create warp/teleport effect."""
        for _ in range(count):
            # Create expanding ring pattern
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 150)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            # Bright energy colors
            colors = [(0, 255, 255), (255, 0, 255), (255, 255, 0)]
            color = random.choice(colors)
            
            particle = Particle(
                x,
                y,
                ParticleType.ENERGY,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(2, 6),
                lifetime=random.uniform(0.5, 1.0)
            )
            
            self.add_particle(particle)
    
    def create_shield_impact(self, x: float, y: float, count: int = 15):
        """Create shield impact effect."""
        for _ in range(count):
            # Particles spread outward from impact point
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x + random.uniform(-10, 10),
                y + random.uniform(-10, 10),
                ParticleType.SPARK,
                velocity=(vel_x, vel_y),
                color=POWERUP_SHIELD,
                size=random.uniform(1, 4),
                lifetime=random.uniform(0.3, 0.8)
            )
            
            self.add_particle(particle)
    
    def create_power_up_aura(self, x: float, y: float, powerup_color: Tuple[int, int, int]):
        """Create continuous aura effect around power-ups."""
        for _ in range(3):
            # Gentle floating particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(10, 30)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - 20  # Slight upward drift
            
            particle = Particle(
                x + random.uniform(-15, 15),
                y + random.uniform(-15, 15),
                ParticleType.ENERGY,
                velocity=(vel_x, vel_y),
                color=powerup_color,
                size=random.uniform(1, 3),
                lifetime=random.uniform(1.0, 2.0)
            )
            
            self.add_particle(particle)
    
    def create_engine_exhaust(self, x: float, y: float, velocity: Tuple[float, float]):
        """Create engine exhaust trail."""
        for _ in range(2):
            # Exhaust particles move opposite to ship direction
            exhaust_vel_x = -velocity[0] * 0.5 + random.uniform(-20, 20)
            exhaust_vel_y = -velocity[1] * 0.5 + random.uniform(20, 60)
            
            # Engine colors (blue to white)
            colors = [(100, 150, 255), (150, 200, 255), (200, 220, 255)]
            color = random.choice(colors)
            
            particle = Particle(
                x + random.uniform(-3, 3),
                y + 15,  # Behind the ship
                ParticleType.TRAIL,
                velocity=(exhaust_vel_x, exhaust_vel_y),
                color=color,
                size=random.uniform(1, 3),
                lifetime=random.uniform(0.2, 0.5)
            )
            
            self.add_particle(particle)
    
    def create_bullet_impact(self, x: float, y: float, bullet_color: Tuple[int, int, int]):
        """Create bullet impact effect."""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x,
                y,
                ParticleType.SPARK,
                velocity=(vel_x, vel_y),
                color=bullet_color,
                size=random.uniform(1, 2),
                lifetime=random.uniform(0.1, 0.4)
            )
            
            self.add_particle(particle)
    
    def create_level_transition(self, center_x: float, center_y: float):
        """Create level transition effect."""
        # Create expanding wave of particles
        for radius in range(0, 300, 15):
            particle_count = max(8, radius // 10)
            
            for i in range(particle_count):
                angle = (i / particle_count) * 2 * math.pi
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                
                # Skip if outside screen
                if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
                    continue
                
                # Gradient colors from center
                distance_factor = radius / 300.0
                color = (
                    int(255 * (1 - distance_factor)),
                    int(255 * distance_factor),
                    255
                )
                
                particle = Particle(
                    x, y,
                    ParticleType.ENERGY,
                    velocity=(0, 0),
                    color=color,
                    size=3,
                    lifetime=1.0 - distance_factor * 0.5
                )
                
                self.add_particle(particle)
    
    def add_particle(self, particle: Particle):
        """Add a particle to the system."""
        if len(self.particles) >= self.max_particles:
            # Remove oldest particle
            self.particles.pop(0)
        
        self.particles.append(particle)
        
        # Update count tracking
        particle_type = particle.type.value
        self.particle_count_by_type[particle_type] = \
            self.particle_count_by_type.get(particle_type, 0) + 1
    
    def update(self, dt: float):
        """Update all particles."""
        # Update background stars
        for star in self.background_stars[:]:
            star.update(dt)
            
            # Wrap stars around screen
            if star.y > SCREEN_HEIGHT + 10:
                star.y = -10
                star.x = random.randint(0, SCREEN_WIDTH)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update(dt)
            
            if not particle.is_alive():
                self.particles.remove(particle)
                
                # Update count tracking
                particle_type = particle.type.value
                if particle_type in self.particle_count_by_type:
                    self.particle_count_by_type[particle_type] -= 1
                    if self.particle_count_by_type[particle_type] <= 0:
                        del self.particle_count_by_type[particle_type]
    
    def render_background(self, screen: pygame.Surface):
        """Render background particles (stars)."""
        for star in self.background_stars:
            star.render(screen)
    
    def render_foreground(self, screen: pygame.Surface):
        """Render foreground particles (effects)."""
        for particle in self.particles:
            particle.render(screen)
    
    def clear(self):
        """Clear all particles except background."""
        self.particles.clear()
        self.particle_count_by_type.clear()
    
    def clear_game_particles(self):
        """Clear only game-related particles, keep background."""
        self.clear()
    
    def clear_all(self):
        """Clear all particles including background."""
        self.particles.clear()
        self.background_stars.clear()
        self.particle_count_by_type.clear()
        self._create_background_stars()
    
    def get_particle_count(self) -> int:
        """Get total particle count."""
        return len(self.particles) + len(self.background_stars)
    
    def get_particle_statistics(self) -> Dict[str, int]:
        """Get particle statistics by type."""
        stats = self.particle_count_by_type.copy()
        stats['background_stars'] = len(self.background_stars)
        stats['total'] = self.get_particle_count()
        return stats
    
    def set_max_particles(self, max_particles: int):
        """Set maximum particle count for performance."""
        self.max_particles = max_particles
        
        # Remove excess particles if needed
        while len(self.particles) > self.max_particles:
            self.particles.pop(0)
    
    def create_screen_clear_effect(self, center_x: float, center_y: float):
        """Create a screen-clearing wave effect."""
        # Create expanding ring of particles
        for radius in range(0, 400, 20):
            circumference = 2 * math.pi * radius
            particle_count = max(8, int(circumference / 10))
            
            for i in range(particle_count):
                angle = (i / particle_count) * 2 * math.pi
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
                
                # Skip if outside screen
                if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
                    continue
                
                particle = Particle(
                    x, y,
                    ParticleType.ENERGY,
                    velocity=(0, 0),
                    color=(255, 255, 255),
                    size=3,
                    lifetime=0.5
                )
                
                self.add_particle(particle)
    
    def create_power_up_effect(self, x: float, y: float, 
                              color: Tuple[int, int, int] = UI_SUCCESS):
        """Create power-up collection effect."""
        # Upward burst
        for _ in range(12):
            angle = random.uniform(-math.pi/3, -2*math.pi/3)  # Upward cone
            speed = random.uniform(60, 120)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                ParticleType.ENERGY,
                velocity=(vel_x, vel_y),
                color=color,
                size=random.uniform(2, 5),
                lifetime=random.uniform(0.8, 1.2)
            )
            
            self.add_particle(particle)
    
    def create_boss_entrance(self, x: float, y: float):
        """Create dramatic boss entrance effect."""
        # Multiple explosion rings
        for ring in range(3):
            ring_radius = (ring + 1) * 50
            particle_count = 16 + ring * 8
            
            for i in range(particle_count):
                angle = (i / particle_count) * 2 * math.pi
                vel_x = math.cos(angle) * ring_radius
                vel_y = math.sin(angle) * ring_radius
                
                # Boss colors (orange/red)
                colors = [(255, 100, 0), (255, 150, 50), (255, 200, 100)]
                color = colors[ring % len(colors)]
                
                particle = Particle(
                    x, y,
                    ParticleType.EXPLOSION,
                    velocity=(vel_x, vel_y),
                    color=color,
                    size=random.uniform(4, 8),
                    lifetime=random.uniform(1.0, 2.0)
                )
                
                self.add_particle(particle)
    
    def create_victory_celebration(self, center_x: float, center_y: float):
        """Create victory celebration effect."""
        # Fireworks-like effect
        for _ in range(50):
            # Random explosion points around center
            explosion_x = center_x + random.uniform(-200, 200)
            explosion_y = center_y + random.uniform(-150, 150)
            
            # Create small explosion at each point
            for _ in range(8):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(30, 80)
                vel_x = math.cos(angle) * speed
                vel_y = math.sin(angle) * speed
                
                # Victory colors (gold, white, cyan)
                colors = [(255, 215, 0), (255, 255, 255), (0, 255, 255)]
                color = random.choice(colors)
                
                particle = Particle(
                    explosion_x, explosion_y,
                    ParticleType.SPARK,
                    velocity=(vel_x, vel_y),
                    color=color,
                    size=random.uniform(2, 4),
                    lifetime=random.uniform(1.0, 2.5)
                )
                
                self.add_particle(particle)
    
    def update_with_time_scale(self, dt: float, time_scale: float = 1.0):
        """Update particles with time scaling (for slow motion effects)."""
        scaled_dt = dt * time_scale
        
        # Update background stars (not affected by time scale)
        for star in self.background_stars[:]:
            star.update(dt)
            
            if star.y > SCREEN_HEIGHT + 10:
                star.y = -10
                star.x = random.randint(0, SCREEN_WIDTH)
        
        # Update particles with time scale
        for particle in self.particles[:]:
            particle.update(scaled_dt)
            
            if not particle.is_alive():
                self.particles.remove(particle)
                
                # Update count tracking
                particle_type = particle.type.value
                if particle_type in self.particle_count_by_type:
                    self.particle_count_by_type[particle_type] -= 1
                    if self.particle_count_by_type[particle_type] <= 0:
                        del self.particle_count_by_type[particle_type]
