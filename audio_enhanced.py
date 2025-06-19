## game/audio_enhanced.py
python
"""
Enhanced Audio Manager - Professional Audio System
================================================

Advanced audio management with:
- Dynamic music system
- Sound effect pooling
- Volume controls
- Audio optimization
"""

import pygame
import os
from pathlib import Path
from typing import Dict, Optional

from settings_enhanced import *

class AudioManager:
    """
    Enhanced audio manager for music and sound effects.
    """
    
    def __init__(self):
        """Initialize the audio manager."""
        self.master_volume = MASTER_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.sfx_volume = SFX_VOLUME
        
        # Audio storage
        self.sounds = {}
        self.current_music = None
        self.music_fade_time = 1000  # milliseconds
        
        # Sound pooling for performance
        self.sound_channels = []
        self.max_channels = MAX_CONCURRENT_SOUNDS
        
        # Initialize audio system
        self._initialize_audio()
        
        # Load audio files
        self._load_sounds()
        
        print("Audio Manager initialized successfully!")
    
    def _initialize_audio(self):
        """Initialize pygame audio system."""
        try:
            # Initialize mixer with high quality settings
            pygame.mixer.pre_init(
                frequency=44100,
                size=-16,
                channels=2,
                buffer=512
            )
            pygame.mixer.init()
            
            # Set number of channels for sound effects
            pygame.mixer.set_num_channels(self.max_channels)
            
        except Exception as e:
            print(f"Error initializing audio: {e}")
    
    def _load_sounds(self):
        """Load all sound files."""
        # Create placeholder sounds if files don't exist
        self._create_placeholder_sounds()
        
        # Try to load actual sound files
        for sound_name, file_path in AUDIO_PATHS.items():
            full_path = Path(file_path)
            
            try:
                if full_path.exists():
                    if sound_name.endswith('music'):
                        # Music files are loaded when needed
                        continue
                    else:
                        # Load sound effect
                        sound = pygame.mixer.Sound(str(full_path))
                        self.sounds[sound_name] = sound
                        print(f"Loaded sound: {sound_name}")
                else:
                    print(f"Sound file not found: {file_path}")
                    
            except Exception as e:
                print(f"Error loading sound {sound_name}: {e}")
    
    def _create_placeholder_sounds(self):
        """Create placeholder sounds using pygame's sound generation."""
        try:
            # Create simple placeholder sounds
            import numpy as np
            
            # Shoot sound - short beep
            duration = 0.1
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 800
            wave = np.sin(frequency * 2 * np.pi * t) * 0.3
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            shoot_sound = pygame.sndarray.make_sound(stereo_wave)
            self.sounds['shoot'] = shoot_sound
            
            # Explosion sound - noise burst
            duration = 0.3
            t = np.linspace(0, duration, int(sample_rate * duration))
            noise = np.random.normal(0, 0.2, len(t))
            envelope = np.exp(-t * 5)  # Decay envelope
            wave = noise * envelope
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            explosion_sound = pygame.sndarray.make_sound(stereo_wave)
            self.sounds['explosion'] = explosion_sound
            
            # Power-up sound - ascending tone
            duration = 0.5
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 400 + 200 * t / duration  # Rising frequency
            wave = np.sin(frequency * 2 * np.pi * t) * 0.3 * (1 - t / duration)
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.array([wave, wave]).T
            powerup_sound = pygame.sndarray.make_sound(stereo_wave)
            self.sounds['powerup'] = powerup_sound
            
            print("Created placeholder sounds")
            
        except ImportError:
            print("NumPy not available, using basic placeholder sounds")
            # Create very basic sounds without NumPy
            self._create_basic_placeholder_sounds()
        except Exception as e:
            print(f"Error creating placeholder sounds: {e}")
    
    def _create_basic_placeholder_sounds(self):
        """Create basic placeholder sounds without NumPy."""
        try:
            # Create minimal sound arrays
            sample_rate = 22050
            duration = 0.1
            samples = int(sample_rate * duration)
            
            # Simple beep sound
            import array
            sound_array = array.array('h', [0] * samples * 2)  # Stereo
            for i in range(0, len(sound_array), 2):
                # Simple sine wave approximation
                value = int(10000 * (i % 100 - 50) / 50)
                sound_array[i] = value      # Left channel
                sound_array[i + 1] = value  # Right channel
            
            shoot_sound = pygame.mixer.Sound(sound_array)
            self.sounds['shoot'] = shoot_sound
            
            print("Created basic placeholder sounds")
            
        except Exception as e:
            print(f"Error creating basic sounds: {e}")
    
    def play_sound(self, sound_name: str, volume: float = 1.0):
        """Play a sound effect."""
        if sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            
            # Find available channel
            channel = pygame.mixer.find_channel()
            if channel:
                # Set volume
                final_volume = volume * self.sfx_volume * self.master_volume
                sound.set_volume(final_volume)
                
                # Play sound
                channel.play(sound)
                
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def play_music(self, music_name: str, loops: int = -1, fade_in: bool = True):
        """Play background music."""
        if music_name == self.current_music:
            return
        
        music_path = AUDIO_PATHS.get(music_name)
        if not music_path:
            return
        
        full_path = Path(music_path)
        
        try:
            if full_path.exists():
                # Stop current music
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(self.music_fade_time // 2)
                
                # Load and play new music
                pygame.mixer.music.load(str(full_path))
                
                # Set volume
                music_volume = self.music_volume * self.master_volume
                pygame.mixer.music.set_volume(music_volume)
                
                # Play music
                if fade_in:
                    pygame.mixer.music.play(loops, fade_ms=self.music_fade_time)
                else:
                    pygame.mixer.music.play(loops)
                
                self.current_music = music_name
                print(f"Playing music: {music_name}")
                
            else:
                print(f"Music file not found: {music_path}")
                
        except Exception as e:
            print(f"Error playing music {music_name}: {e}")
    
    def stop_music(self, fade_out: bool = True):
        """Stop background music."""
        try:
            if pygame.mixer.music.get_busy():
                if fade_out:
                    pygame.mixer.music.fadeout(self.music_fade_time)
                else:
                    pygame.mixer.music.stop()
                
                self.current_music = None
                
        except Exception as e:
            print(f"Error stopping music: {e}")
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        
        # Update music volume immediately
        if pygame.mixer.music.get_busy():
            music_volume = self.music_volume * self.master_volume
            pygame.mixer.music.set_volume(music_volume)
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Update music volume immediately
        if pygame.mixer.music.get_busy():
            music_volume = self.music_volume * self.master_volume
            pygame.mixer.music.set_volume(music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def is_music_playing(self) -> bool:
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def pause_music(self):
        """Pause background music."""
        try:
            pygame.mixer.music.pause()
        except Exception as e:
            print(f"Error pausing music: {e}")
    
    def unpause_music(self):
        """Unpause background music."""
        try:
            pygame.mixer.music.unpause()
        except Exception as e:
            print(f"Error unpausing music: {e}")
    
    def cleanup(self):
        """Clean up audio resources."""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            self.sounds.clear()
            print("Audio manager cleaned up")
            
        except Exception as e:
            print(f"Error cleaning up audio: {e}")
