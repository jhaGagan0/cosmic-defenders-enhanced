## game/level_enhanced.py
python
"""
Enhanced Level Manager - Level Progression System
===============================================

Professional level management with:
- Dynamic level generation
- Unlock system
- Level progression
- Difficulty scaling
"""

import json
import random
from typing import Dict, List, Set, Tuple
from pathlib import Path

from settings_enhanced import *

class LevelManager:
    """
    Enhanced level manager for handling level progression and unlocks.
    """
    
    def __init__(self):
        """Initialize the level manager."""
        self.unlocked_levels = {1}  # Level 1 is always unlocked
        self.current_level = 1
        self.level_data = {}
        
        # Generate level data
        self._generate_level_data()
        
        print("Level Manager initialized successfully!")
    
    def _generate_level_data(self):
        """Generate data for all levels."""
        for level in range(1, MAX_LEVELS + 1):
            self.level_data[level] = self._create_level_config(level)
    
    def _create_level_config(self, level: int) -> Dict:
        """
        Create configuration for a specific level.
        
        Args:
            level: Level number
            
        Returns:
            Level configuration dictionary
        """
        # Base configuration
        config = {
            'level': level,
            'name': f"Sector {level}",
            'description': self._get_level_description(level),
            'waves': self._calculate_waves_for_level(level),
            'enemy_types': self._get_enemy_types_for_level(level),
            'spawn_rate_multiplier': 1.0 + (level - 1) * 0.1,
            'enemy_health_multiplier': 1.0 + (level - 1) * 0.05,
            'enemy_speed_multiplier': 1.0 + (level - 1) * 0.03,
            'powerup_spawn_rate': POWERUP_SPAWN_CHANCE * (1.0 + level * 0.02),
            'background_theme': self._get_background_theme(level),
            'special_mechanics': self._get_special_mechanics(level)
        }
        
        return config

    def _get_level_description(self, level: int) -> str:
        """Get description for a level."""
        descriptions = [
            "Training grounds - Learn the basics",
            "Asteroid field - Watch for debris",
            "Enemy patrol zone - Increased resistance",
            "Nebula sector - Reduced visibility",
            "Boss stronghold - Prepare for battle!",
            "Deep space - No backup available",
            "Alien territory - Unknown threats",
            "Wormhole junction - Space distortions",
            "Mining colony - Industrial hazards",
            "Command center - Heavy defenses",
            "Black hole vicinity - Gravitational anomalies",
            "Ancient ruins - Mysterious technology",
            "Pirate hideout - Expect ambushes",
            "Research station - Experimental weapons",
            "Final approach - The ultimate test",
            "Legendary sector - For true masters",
            "Nightmare zone - Extreme difficulty",
            "Impossible realm - Beyond comprehension",
            "Cosmic apex - The final frontier",
            "Infinity gate - Transcend all limits"
        ]
        
        if level <= len(descriptions):
            return descriptions[level - 1]
        else:
            return f"Unknown sector {level} - Uncharted territory"
    
    def _calculate_waves_for_level(self, level: int) -> int:
        """Calculate number of waves for a level."""
        base_waves = 10
        additional_waves = (level - 1) * 2
        return base_waves + additional_waves
    
    def _get_enemy_types_for_level(self, level: int) -> List[str]:
        """Get enemy types available for a level."""
        all_types = ['basic', 'fast', 'heavy', 'zigzag']
        
        if level == 1:
            return ['basic']
        elif level <= 3:
            return ['basic', 'fast']
        elif level <= 6:
            return ['basic', 'fast', 'heavy']
        elif level <= 10:
            return ['basic', 'fast', 'heavy', 'zigzag']
        else:
            # Advanced levels get all types plus increased spawn rates
            return all_types
    
    def _get_background_theme(self, level: int) -> str:
        """Get background theme for a level."""
        themes = [
            'space_blue',      # 1-4
            'nebula_purple',   # 5-8
            'asteroid_gray',   # 9-12
            'alien_green',     # 13-16
            'cosmic_red'       # 17-20
        ]
        
        theme_index = min((level - 1) // 4, len(themes) - 1)
        return themes[theme_index]
    
    def _get_special_mechanics(self, level: int) -> List[str]:
        """Get special mechanics for a level."""
        mechanics = []
        
        if level >= 4:
            mechanics.append('nebula_fog')  # Reduced visibility
        if level >= 7:
            mechanics.append('asteroid_debris')  # Moving obstacles
        if level >= 10:
            mechanics.append('gravity_wells')  # Movement distortion
        if level >= 13:
            mechanics.append('energy_storms')  # Periodic damage zones
        if level >= 16:
            mechanics.append('time_distortion')  # Variable game speed
        if level >= 19:
            mechanics.append('reality_shift')  # Changing physics
        
        return mechanics
    
    def start_level(self, level: int) -> bool:
        """
        Start a specific level.
        
        Args:
            level: Level number to start
            
        Returns:
            True if level started successfully
        """
        if level not in self.unlocked_levels:
            print(f"Level {level} is not unlocked!")
            return False
        
        if level not in self.level_data:
            print(f"Level {level} data not found!")
            return False
        
        self.current_level = level
        config = self.level_data[level]

        print(f"Starting Level {level}: {config['name']}")
        print(f"Description: {config['description']}")
        print(f"Waves: {config['waves']}")
        
        return True
    
    def unlock_level(self, level: int) -> bool:
        """
        Unlock a level.
        
        Args:
            level: Level number to unlock
            
        Returns:
            True if level was newly unlocked
        """
        if level in self.unlocked_levels:
            return False

        if level < 1 or level > MAX_LEVELS:
            return False
        
        self.unlocked_levels.add(level)
        print(f"Level {level} unlocked!")
        return True
    
    def is_level_unlocked(self, level: int) -> bool:
        """Check if a level is unlocked."""
        return level in self.unlocked_levels
    
    def get_level_config(self, level: int) -> Dict:
        """Get configuration for a level."""
        return self.level_data.get(level, {})
    
    def get_unlocked_levels(self) -> Set[int]:
        """Get set of unlocked levels."""
        return self.unlocked_levels.copy()
    
    def get_next_level(self) -> int:
        """Get the next level number."""
        return self.current_level + 1 if self.current_level < MAX_LEVELS else MAX_LEVELS
    
    def is_level_complete(self, current_wave: int) -> bool:
        """
        Check if current level is complete.
        
        Args:
            current_wave: Current wave number
            
        Returns:
            True if level is complete
        """
        config = self.get_level_config(self.current_level)
        target_waves = config.get('waves', 10)
        
        return current_wave > target_waves
    
    def calculate_level_unlock_requirements(self) -> Dict[int, int]:
        """Calculate score requirements for unlocking levels."""
        requirements = {}
        
        for level in range(2, MAX_LEVELS + 1):
            # Base requirement increases exponentially
            base_score = 1000
            multiplier = 1.5 ** (level - 2)
            requirements[level] = int(base_score * multiplier)
        
        return requirements
    
    def check_level_unlocks(self, score: int) -> List[int]:
        """
        Check which levels should be unlocked based on score.
        
        Args:
            score: Player's score
            
        Returns:
            List of newly unlocked level numbers
        """
        newly_unlocked = []
        
        for level, required_score in LEVEL_REQUIREMENTS.items():
            if score >= required_score and level not in self.unlocked_levels:
                self.unlock_level(level)
                newly_unlocked.append(level)
        
        return newly_unlocked
    
    def get_level_preview(self, level: int) -> Dict:
        """
        Get preview information for a level.
        
        Args:
            level: Level number
            
        Returns:
            Preview information dictionary
        """
        if level not in self.level_data:
            return {}
        
        config = self.level_data[level]
        
        preview = {
            'name': config['name'],
            'description': config['description'],
            'waves': config['waves'],
            'difficulty_rating': self._calculate_difficulty_rating(level),
            'enemy_types': config['enemy_types'],
            'special_mechanics': config['special_mechanics'],
            'recommended_score': LEVEL_REQUIREMENTS.get(level, 0),
            'unlocked': level in self.unlocked_levels
        }
        
        return preview

    def _calculate_difficulty_rating(self, level: int) -> str:
        """Calculate difficulty rating for a level."""
        if level <= 3:
            return "Easy"
        elif level <= 7:
            return "Medium"
        elif level <= 12:
            return "Hard"
        elif level <= 17:
            return "Very Hard"
        else:
            return "Extreme"
    
    def get_level_statistics(self) -> Dict:
        """Get statistics about levels."""
        total_levels = MAX_LEVELS
        unlocked_count = len(self.unlocked_levels)
        completion_percentage = (unlocked_count / total_levels) * 100
        
        return {
            'total_levels': total_levels,
            'unlocked_levels': unlocked_count,
            'completion_percentage': completion_percentage,
            'current_level': self.current_level,
            'highest_unlocked': max(self.unlocked_levels) if self.unlocked_levels else 1
        }
    
    def save_progress(self) -> bool:
        """Save level progress to file."""
        try:
            progress_data = {
                'unlocked_levels': list(self.unlocked_levels),
                'current_level': self.current_level,
                'save_timestamp': time.time()
            }
            
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(progress_data, f, indent=2)
            
            print("Level progress saved")
            return True
            
        except Exception as e:
            print(f"Error saving level progress: {e}")
            return False

    def load_progress(self) -> bool:
        """Load level progress from file."""
        try:
            if not PROGRESS_FILE.exists():
                return False
            
            with open(PROGRESS_FILE, 'r') as f:
                progress_data = json.load(f)
            
            # Load unlocked levels
            unlocked_list = progress_data.get('unlocked_levels', [1])
            self.unlocked_levels = set(unlocked_list)
            
            # Ensure level 1 is always unlocked
            self.unlocked_levels.add(1)
            
            # Load current level
            self.current_level = progress_data.get('current_level', 1)
            
            print(f"Level progress loaded: {len(self.unlocked_levels)} levels unlocked")
            return True
            
        except Exception as e:
            print(f"Error loading level progress: {e}")
            return False
    
    def reset_progress(self) -> bool:
        """Reset all level progress."""
        try:
            self.unlocked_levels = {1}
            self.current_level = 1
            
            # Save reset progress
            self.save_progress()
            
            print("Level progress reset")
            return True
            
        except Exception as e:
            print(f"Error resetting level progress: {e}")
            return False
    
    def get_level_rewards(self, level: int) -> Dict:
        """Get rewards for completing a level."""
        base_score = 1000
        level_multiplier = level * 1.5
        
        rewards = {
            'score_bonus': int(base_score * level_multiplier),
            'unlocks': [],
            'achievements': []
        }
        
        # Special rewards for milestone levels
        if level % 5 == 0:  # Every 5th level
            rewards['achievements'].append(f'Sector {level} Master')
            rewards['score_bonus'] *= 2
        
        if level == 10:
            rewards['unlocks'].append('Advanced Difficulty')
        elif level == 15:
            rewards['unlocks'].append('Expert Mode')
        elif level == 20:
            rewards['unlocks'].append('Master Pilot Status')

        return rewards
    
    def get_level_challenges(self, level: int) -> List[Dict]:
        """Get optional challenges for a level."""
        challenges = []
        
        # Base challenges for all levels
        challenges.append({
            'name': 'Perfect Run',
            'description': 'Complete without taking damage',
            'reward': 'Score x2 multiplier'
        })

        challenges.append({
            'name': 'Speed Run',
            'description': f'Complete in under {60 + level * 10} seconds',
            'reward': 'Time bonus points'
        })
        
        # Level-specific challenges
        if level >= 5:
            challenges.append({
                'name': 'Power Collector',
                'description': 'Collect 10 power-ups',
                'reward': 'Extra life'
            })
        
        if level >= 10:
            challenges.append({
                'name': 'Boss Hunter',
                'description': 'Defeat boss without special abilities',
                'reward': 'Achievement unlock'
            })
        
        return challenges
    
    def apply_level_modifiers(self, level: int, base_stats: Dict) -> Dict:
        """Apply level-specific modifiers to game stats."""
        config = self.get_level_config(level)
        modified_stats = base_stats.copy()
        
        # Apply multipliers
        if 'enemy_health_multiplier' in config:
            modified_stats['enemy_health'] *= config['enemy_health_multiplier']
        
        if 'enemy_speed_multiplier' in config:
            modified_stats['enemy_speed'] *= config['enemy_speed_multiplier']
        
        if 'spawn_rate_multiplier' in config:
            modified_stats['spawn_rate'] *= config['spawn_rate_multiplier']
        
        # Apply special mechanics
        special_mechanics = config.get('special_mechanics', [])
        modified_stats['special_mechanics'] = special_mechanics
        
        return modified_stats
    
    def get_level_leaderboard(self, level: int) -> List[Dict]:
        """Get leaderboard for a specific level."""
        # This would integrate with the leaderboard manager
        # For now, return empty list
        return []
    
    def is_boss_level(self, level: int) -> bool:
        """Check if a level is a boss level."""
        return level % BOSS_WAVE_INTERVAL == 0
    
    def get_boss_info(self, level: int) -> Dict:
        """Get information about the boss for a boss level."""
        if not self.is_boss_level(level):
            return {}
        
        boss_names = [
            "Asteroid Guardian",
            "Nebula Destroyer", 
            "Void Leviathan",
            "Cosmic Overlord"
        ]
        
        boss_index = (level // BOSS_WAVE_INTERVAL - 1) % len(boss_names)
        
        return {
            'name': boss_names[boss_index],
            'health_multiplier': 1.0 + (level // BOSS_WAVE_INTERVAL) * 0.5,
            'attack_patterns': 3 + (level // BOSS_WAVE_INTERVAL),
            'special_abilities': self._get_boss_abilities(level)
        }
    
    def _get_boss_abilities(self, level: int) -> List[str]:
        """Get special abilities for boss at given level."""
        abilities = ['spread_shot', 'homing_missiles']
        
        if level >= 10:
            abilities.append('shield_regeneration')
        if level >= 15:
            abilities.append('teleportation')
        if level >= 20:
            abilities.append('reality_distortion')
        
        return abilities
