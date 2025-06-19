## game/settings_enhanced.py
python
"""
Enhanced Game Settings and Configuration
=======================================

Comprehensive configuration for Cosmic Defenders Enhanced with
professional-grade settings for performance, gameplay, and visuals.
"""

import pygame
from pathlib import Path

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
VSYNC = True

# UI Scaling for different screen sizes
UI_SCALE = 1.0
if SCREEN_WIDTH >= 1920:
    UI_SCALE = 1.5
elif SCREEN_WIDTH >= 1440:
    UI_SCALE = 1.2

# ============================================================================
# COLORS (Professional Color Palette)
# ============================================================================
# Primary Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

# UI Colors
UI_PRIMARY = (41, 128, 185)      # Professional blue
UI_SECONDARY = (52, 73, 94)      # Dark blue-gray
UI_SUCCESS = (39, 174, 96)       # Green
UI_WARNING = (241, 196, 15)      # Yellow
UI_DANGER = (231, 76, 60)        # Red
UI_INFO = (155, 89, 182)         # Purple

# Game Colors
PLAYER_COLOR = (100, 200, 255)   # Light blue
ENEMY_BASIC = (255, 100, 100)    # Red
ENEMY_FAST = (255, 255, 100)     # Yellow
ENEMY_HEAVY = (200, 100, 255)    # Purple
ENEMY_ZIGZAG = (100, 255, 100)   # Green
BOSS_COLOR = (255, 150, 50)      # Orange

# Power-up Colors
POWERUP_HEALTH = (100, 255, 100)     # Green
POWERUP_SHIELD = (100, 255, 255)     # Cyan
POWERUP_RAPID = (255, 255, 100)      # Yellow
POWERUP_MULTI = (255, 100, 255)      # Magenta
POWERUP_CLEAR = (255, 200, 100)      # Orange
POWERUP_TIME = (200, 200, 255)       # Light purple
POWERUP_HOMING = (255, 150, 150)     # Pink

# ============================================================================
# PLAYER SETTINGS
# ============================================================================
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100
PLAYER_FIRE_RATE = 10  # bullets per second
PLAYER_SIZE = (40, 40)
PLAYER_INVULNERABILITY_TIME = 2.0  # seconds

# Player abilities
SPECIAL_ABILITY_COOLDOWN = 15.0  # seconds
TIME_FREEZE_DURATION = 3.0       # seconds
HOMING_MISSILE_COUNT = 5

# ============================================================================
# ENEMY SETTINGS
# ============================================================================
# Base enemy stats (modified by difficulty)
ENEMY_SPEEDS = {
    'basic': 2,
    'fast': 4,
    'heavy': 1,
    'zigzag': 3,
    'boss': 1.5
}

ENEMY_HEALTHS = {
    'basic': 1,
    'fast': 1,
    'heavy': 5,
    'zigzag': 2,
    'boss': 50
}

ENEMY_SCORES = {
    'basic': 100,
    'fast': 150,
    'heavy': 300,
    'zigzag': 200,
    'boss': 1000
}

ENEMY_SIZES = {
    'basic': (30, 30),
    'fast': (25, 25),
    'heavy': (45, 45),
    'zigzag': (35, 35),
    'boss': (80, 80)
}

# ============================================================================
# DIFFICULTY SETTINGS
# ============================================================================
DIFFICULTIES = {
    'CADET': {
        'name': 'Cadet',
        'color': UI_SUCCESS,
        'enemy_speed_mult': 0.7,
        'enemy_health_mult': 0.8,
        'spawn_rate_mult': 0.8,
        'player_damage_mult': 1.5,
        'score_mult': 1.0,
        'description': 'Perfect for beginners'
    },
    'PILOT': {
        'name': 'Pilot',
        'color': UI_INFO,
        'enemy_speed_mult': 0.85,
        'enemy_health_mult': 0.9,
        'spawn_rate_mult': 0.9,
        'player_damage_mult': 1.2,
        'score_mult': 1.2,
        'description': 'Slightly challenging'
    },
    'COMMANDER': {
        'name': 'Commander',
        'color': UI_WARNING,
        'enemy_speed_mult': 1.0,
        'enemy_health_mult': 1.0,
        'spawn_rate_mult': 1.0,
        'player_damage_mult': 1.0,
        'score_mult': 1.5,
        'description': 'Balanced experience'
    },
    'ACE': {
        'name': 'Ace',
        'color': (255, 140, 0),  # Orange
        'enemy_speed_mult': 1.2,
        'enemy_health_mult': 1.3,
        'spawn_rate_mult': 1.2,
        'player_damage_mult': 0.8,
        'score_mult': 2.0,
        'description': 'For experienced pilots'
    },
    'LEGEND': {
        'name': 'Legend',
        'color': UI_DANGER,
        'enemy_speed_mult': 1.5,
        'enemy_health_mult': 1.5,
        'spawn_rate_mult': 1.4,
        'player_damage_mult': 0.6,
        'score_mult': 3.0,
        'description': 'Ultimate challenge'
    }
}

# ============================================================================
# LEVEL SETTINGS
# ============================================================================
MAX_LEVELS = 20
BOSS_WAVE_INTERVAL = 5
ENEMIES_PER_WAVE_BASE = 5
WAVE_SPAWN_DELAY = 2.0  # seconds between waves

# Level progression
LEVEL_REQUIREMENTS = {
    1: 0,      # Always unlocked
    2: 1000,   # Score required to unlock
    3: 2500,
    4: 5000,
    5: 8000,
    6: 12000,
    7: 17000,
    8: 23000,
    9: 30000,
    10: 40000,
    11: 52000,
    12: 66000,
    13: 82000,
    14: 100000,
    15: 120000,
    16: 142000,
    17: 166000,
    18: 192000,
    19: 220000,
    20: 250000
}

# ============================================================================
# POWER-UP SETTINGS
# ============================================================================
POWERUP_SPAWN_CHANCE = 0.15  # 15% chance per enemy kill
POWERUP_DURATION = 10.0      # seconds
POWERUP_SPEED = 2

POWERUP_TYPES = {
    'health': {'weight': 25, 'color': POWERUP_HEALTH},
    'shield': {'weight': 20, 'color': POWERUP_SHIELD},
    'rapid_fire': {'weight': 20, 'color': POWERUP_RAPID},
    'multi_shot': {'weight': 15, 'color': POWERUP_MULTI},
    'screen_clear': {'weight': 10, 'color': POWERUP_CLEAR},
    'time_slow': {'weight': 7, 'color': POWERUP_TIME},
    'homing': {'weight': 3, 'color': POWERUP_HOMING}
}

# ============================================================================
# BULLET SETTINGS
# ============================================================================
BULLET_SPEED = 8
BULLET_SIZE = (4, 10)
BULLET_DAMAGE = 1

# Special bullet types
HOMING_BULLET_SPEED = 6
HOMING_BULLET_TURN_RATE = 0.1

# ============================================================================
# PARTICLE SETTINGS
# ============================================================================
MAX_PARTICLES = 500
EXPLOSION_PARTICLES = 20
TRAIL_PARTICLES = 5
STAR_COUNT = 200

# ============================================================================
# AUDIO SETTINGS
# ============================================================================
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.8

# Audio file paths
AUDIO_PATHS = {
    'menu_music': 'assets/sounds/menu_music.ogg',
    'game_music': 'assets/sounds/game_music.ogg',
    'boss_music': 'assets/sounds/boss_music.ogg',
    'shoot': 'assets/sounds/shoot.wav',
    'explosion': 'assets/sounds/explosion.wav',
    'powerup': 'assets/sounds/powerup.wav',
    'menu_select': 'assets/sounds/menu_select.wav',
    'menu_hover': 'assets/sounds/menu_hover.wav',
    'game_over': 'assets/sounds/game_over.wav',
    'level_complete': 'assets/sounds/level_complete.wav',
    'boss_warning': 'assets/sounds/boss_warning.wav'
}

# ============================================================================
# UI SETTINGS
# ============================================================================
# Font sizes (scaled by UI_SCALE)
FONT_SIZES = {
    'small': int(16 * UI_SCALE),
    'medium': int(24 * UI_SCALE),
    'large': int(36 * UI_SCALE),
    'xlarge': int(48 * UI_SCALE),
    'title': int(72 * UI_SCALE)
}

# Animation settings
ANIMATION_SPEED = 0.1
BUTTON_HOVER_SCALE = 1.1
MENU_TRANSITION_SPEED = 0.2

# UI Layout
MENU_BUTTON_WIDTH = int(300 * UI_SCALE)
MENU_BUTTON_HEIGHT = int(60 * UI_SCALE)
MENU_BUTTON_SPACING = int(20 * UI_SCALE)

# HUD settings
HUD_MARGIN = 20
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
MINIMAP_SIZE = 150

# ============================================================================
# FILE PATHS
# ============================================================================
SAVE_DIR = Path("saves")
ASSETS_DIR = Path("assets")
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"

# Save files
LEADERBOARD_FILE = SAVE_DIR / "leaderboard.json"
SETTINGS_FILE = SAVE_DIR / "settings.json"
PROGRESS_FILE = SAVE_DIR / "progress.json"

# Ensure directories exist
SAVE_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
SOUNDS_DIR.mkdir(exist_ok=True)
FONTS_DIR.mkdir(exist_ok=True)

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================
# Optimization flags
ENABLE_VSYNC = True
ENABLE_PARTICLE_CULLING = True
ENABLE_SOUND_POOLING = True
MAX_CONCURRENT_SOUNDS = 32

# Culling distances
PARTICLE_CULL_DISTANCE = SCREEN_WIDTH + 100
ENEMY_CULL_DISTANCE = SCREEN_HEIGHT + 100

# ============================================================================
# DEBUG SETTINGS
# ============================================================================
DEBUG_MODE = False
SHOW_FPS = True
SHOW_COLLISION_BOXES = DEBUG_MODE
SHOW_PARTICLE_COUNT = DEBUG_MODE

# ============================================================================
# GAME BALANCE
# ============================================================================
# Daily missions
DAILY_MISSIONS = [
    {"type": "score", "target": 5000, "reward": "unlock_level"},
    {"type": "enemies", "target": 100, "reward": "bonus_points"},
    {"type": "survival", "target": 300, "reward": "extra_life"},
    {"type": "powerups", "target": 10, "reward": "powerup_boost"}
]

# Achievement system
ACHIEVEMENTS = {
    'first_kill': {'name': 'First Blood', 'description': 'Destroy your first enemy'},
    'score_1k': {'name': 'Rising Star', 'description': 'Score 1,000 points'},
    'score_10k': {'name': 'Space Ace', 'description': 'Score 10,000 points'},
    'score_50k': {'name': 'Cosmic Legend', 'description': 'Score 50,000 points'},
    'boss_killer': {'name': 'Boss Hunter', 'description': 'Defeat your first boss'},
    'survivor': {'name': 'Survivor', 'description': 'Survive for 5 minutes'},
    'perfectionist': {'name': 'Perfect Run', 'description': 'Complete a level without taking damage'}
}

# ============================================================================
# INPUT SETTINGS
# ============================================================================
# Key bindings (customizable)
KEY_BINDINGS = {
    'move_up': [pygame.K_w, pygame.K_UP],
    'move_down': [pygame.K_s, pygame.K_DOWN],
    'move_left': [pygame.K_a, pygame.K_LEFT],
    'move_right': [pygame.K_d, pygame.K_RIGHT],
    'shoot': [pygame.K_SPACE],
    'special_ability': [pygame.K_x, pygame.K_LSHIFT],
    'pause': [pygame.K_ESCAPE, pygame.K_p],
    'menu': [pygame.K_ESCAPE]
}

# Mouse sensitivity
MOUSE_SENSITIVITY = 1.0

# ============================================================================
# VISUAL EFFECTS
# ============================================================================
# Screen shake
SCREEN_SHAKE_INTENSITY = 5
SCREEN_SHAKE_DURATION = 0.3

# Flash effects
DAMAGE_FLASH_DURATION = 0.1
POWERUP_FLASH_DURATION = 0.2

# Parallax layers
PARALLAX_LAYERS = [
    {'speed': 0.2, 'image': 'bg_far.png'},
    {'speed': 0.5, 'image': 'bg_mid.png'},
    {'speed': 1.0, 'image': 'bg_near.png'}
]
