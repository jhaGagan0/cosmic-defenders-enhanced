## game/leaderboard_enhanced.py
python
"""
Enhanced Leaderboard Manager - Score Tracking System
==================================================

Professional leaderboard system with:
- Persistent score storage
- Multiple difficulty tracking
- Data validation
- Backup and recovery
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from settings_enhanced import *

class LeaderboardManager:
    """
    Enhanced leaderboard manager for tracking high scores.
    """
    
    def __init__(self):
        """Initialize the leaderboard manager."""
        self.leaderboard_data = []
        self.max_entries = 100  # Keep top 100 scores
        self.backup_count = 5   # Number of backup files to keep
        
        # Load existing leaderboard
        self.load_leaderboard()
        
        print("Leaderboard Manager initialized successfully!")

    def add_score(self, player_name: str, score: int, difficulty: str, 
                  level: int = 1, waves_survived: int = 0) -> bool:
        """
        Add a new score to the leaderboard.
        
        Args:
            player_name: Name of the player
            score: Final score achieved
            difficulty: Difficulty level played
            level: Level reached
            waves_survived: Number of waves survived
            
        Returns:
            True if score was added to top 10, False otherwise
        """
        # Validate input
        if not player_name or not player_name.strip():
            player_name = "Anonymous"
        
        player_name = player_name.strip()[:20]  # Limit name length
        score = max(0, score)
        
        # Create score entry
        score_entry = {
            'name': player_name,
            'score': score,
            'difficulty': difficulty,
            'level': level,
            'waves_survived': waves_survived,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Add to leaderboard
        self.leaderboard_data.append(score_entry)
        
        # Sort by score (descending)
        self.leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top entries
        self.leaderboard_data = self.leaderboard_data[:self.max_entries]
        
        # Save leaderboard
        self.save_leaderboard()
        
        # Check if score made it to top 10
        top_10_scores = [entry['score'] for entry in self.leaderboard_data[:10]]
        is_top_10 = score in top_10_scores
        
        if is_top_10:
            print(f"New high score! {player_name}: {score:,} points")
        
        return is_top_10
    
    def get_leaderboard(self, count: int = 10) -> List[Dict]:
        """
        Get top scores from leaderboard.
        
        Args:
            count: Number of entries to return
            
        Returns:
            List of score entries
        """
        return self.leaderboard_data[:count]
    
    def load_leaderboard(self) -> bool:
        """
        Load leaderboard from file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if LEADERBOARD_FILE.exists():
                with open(LEADERBOARD_FILE, 'r') as f:
                    data = json.load(f)
                    
                # Validate and clean data
                self.leaderboard_data = self._validate_leaderboard_data(data)
                
                print(f"Loaded {len(self.leaderboard_data)} leaderboard entries")
                return True
            else:
                print("No existing leaderboard file found")
                self.leaderboard_data = []
                return False
                
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            
            # Initialize empty leaderboard
            self.leaderboard_data = []
            return False
    
    def save_leaderboard(self) -> bool:
        """
        Save leaderboard to file with backup.
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Create backup before saving
            self._create_backup()
            
            # Save current leaderboard
            with open(LEADERBOARD_FILE, 'w') as f:
                json.dump(self.leaderboard_data, f, indent=2)
            
            print(f"Saved leaderboard with {len(self.leaderboard_data)} entries")
            return True
            
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            return False
    
    def _validate_leaderboard_data(self, data: List[Dict]) -> List[Dict]:
        """
        Validate and clean leaderboard data.
        
        Args:
            data: Raw leaderboard data
            
        Returns:
            Cleaned and validated data
        """
        validated_data = []

        for entry in data:
            try:
                # Required fields
                if 'name' not in entry or 'score' not in entry:
                    continue
                
                # Clean and validate entry
                clean_entry = {
                    'name': str(entry['name'])[:20],  # Limit name length
                    'score': max(0, int(entry['score'])),  # Ensure positive score
                    'difficulty': entry.get('difficulty', 'COMMANDER'),
                    'level': max(1, int(entry.get('level', 1))),
                    'waves_survived': max(0, int(entry.get('waves_survived', 0))),
                    'timestamp': entry.get('timestamp', datetime.now().isoformat()),
                    'date': entry.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))
                }
                
                # Validate difficulty
                if clean_entry['difficulty'] not in DIFFICULTIES:
                    clean_entry['difficulty'] = 'COMMANDER'

                validated_data.append(clean_entry)
                
            except (ValueError, TypeError) as e:
                print(f"Skipping invalid leaderboard entry: {e}")
                continue
        
        # Sort by score
        validated_data.sort(key=lambda x: x['score'], reverse=True)
        
        return validated_data[:self.max_entries]
    
    def _create_backup(self):
        """Create a backup of the current leaderboard."""
        try:
            if LEADERBOARD_FILE.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = SAVE_DIR / f"leaderboard_backup_{timestamp}.json"
                
                # Copy current file to backup
                import shutil
                shutil.copy2(LEADERBOARD_FILE, backup_file)
                
                # Clean up old backups
                self._cleanup_old_backups()
                
        except Exception as e:
            print(f"Error creating backup: {e}")

    def _cleanup_old_backups(self):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = list(SAVE_DIR.glob("leaderboard_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old backups
            for backup_file in backup_files[self.backup_count:]:
                backup_file.unlink()
                print(f"Removed old backup: {backup_file.name}")
                
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
