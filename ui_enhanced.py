## game/ui_enhanced.py
python
"""
Enhanced UI Manager - Professional User Interface
===============================================

Advanced UI system with:
- Animated menus and transitions
- Modern styling and effects
- Comprehensive input handling
- Responsive design
"""

import pygame
import math
import time
from typing import Dict, List, Optional, Tuple, Any

from settings_enhanced import *

class Button:
    """Enhanced button class with animations and effects."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int] = UI_PRIMARY, 
                 text_color: Tuple[int, int, int] = WHITE):
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_scale = 1.0
        self.hover_alpha = 0.0
        self.clicked = False
        self.enabled = True
        
    def update(self, dt: float):
        """Update button animations."""
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = self.rect.collidepoint(mouse_pos) and self.enabled
        
        # Hover animation
        target_scale = BUTTON_HOVER_SCALE if is_hovering else 1.0
        self.hover_scale += (target_scale - self.hover_scale) * 0.1
        
        target_alpha = 0.3 if is_hovering else 0.0
        self.hover_alpha += (target_alpha - self.hover_alpha) * 0.1
    
    def handle_event(self, event) -> bool:
        """Handle button events. Returns True if clicked."""
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        return False
    
    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        """Render the button with effects."""
        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.hover_scale)
        scaled_height = int(self.rect.height * self.hover_scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Button background
        alpha = 200 if self.enabled else 100
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*self.color, alpha), 
                        (0, 0, scaled_width, scaled_height), border_radius=10)
        
        # Hover effect
        if self.hover_alpha > 0:
            hover_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            pygame.draw.rect(hover_surface, (255, 255, 255, int(self.hover_alpha * 255)), 
                           (0, 0, scaled_width, scaled_height), border_radius=10)
            button_surface.blit(hover_surface, (0, 0))
        
        # Border
        pygame.draw.rect(button_surface, WHITE, 
                        (0, 0, scaled_width, scaled_height), 2, border_radius=10)
        
        screen.blit(button_surface, scaled_rect)
        
        # Text
        text_color = self.text_color if self.enabled else (128, 128, 128)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        screen.blit(text_surface, text_rect)

class UIManager:
    """Enhanced UI Manager for all interface elements."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.fonts = {}
        self.buttons = {}
        self.current_menu = None
        self.animation_time = 0
        self.input_text = ""
        self.input_active = False
        
        # Load fonts
        self._load_fonts()
        
        # Initialize menu buttons
        self._initialize_buttons()
        
        print("UI Manager initialized successfully!")
    
    def _load_fonts(self):
        """Load all required fonts."""
        try:
            # Try to load custom fonts
            font_path = FONTS_DIR / "game_font.ttf"
            if font_path.exists():
                for name, size in FONT_SIZES.items():
                    self.fonts[name] = pygame.font.Font(str(font_path), size)
            else:
                # Use system fonts
                for name, size in FONT_SIZES.items():
                    self.fonts[name] = pygame.font.Font(None, size)
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Fallback to default fonts
            for name, size in FONT_SIZES.items():
                self.fonts[name] = pygame.font.Font(None, size)
    
    def _initialize_buttons(self):
        """Initialize all menu buttons."""
        # Main menu buttons
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        self.buttons['main_menu'] = [
            Button(center_x, start_y - 60, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Start Game"),
            Button(center_x, start_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Instructions"),
            Button(center_x, start_y + 60, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Level Select"),
            Button(center_x, start_y + 120, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Leaderboard"),
            Button(center_x, start_y + 180, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Settings"),
            Button(center_x, start_y + 240, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Daily Missions"),
            Button(center_x, start_y + 300, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Quit", UI_DANGER)
        ]
        
        # Difficulty selection buttons
        self.buttons['difficulty'] = []
        for i, (key, diff) in enumerate(DIFFICULTIES.items()):
            y_pos = start_y + (i - 2) * 80
            self.buttons['difficulty'].append(
                Button(center_x, y_pos, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, 
                      diff['name'], diff['color'])
            )
        
        # Add back button
        self.buttons['difficulty'].append(
            Button(center_x, start_y + 300, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Back", UI_SECONDARY)
        )
    
    def update(self, dt: float):
        """Update UI animations and effects."""
        self.animation_time += dt
        
        # Update all buttons
        for menu_buttons in self.buttons.values():
            if isinstance(menu_buttons, list):
                for button in menu_buttons:
                    button.update(dt)
    
    def render_animated_title(self, title: str, x: int, y: int, 
                            alpha: int = 255, scale: float = 1.0):
        """Render animated title with effects."""
        # Create title surface
        title_surface = self.fonts['title'].render(title, True, UI_PRIMARY)
        
        # Apply effects
        if scale != 1.0:
            new_size = (int(title_surface.get_width() * scale), 
                       int(title_surface.get_height() * scale))
            title_surface = pygame.transform.scale(title_surface, new_size)
        
        title_surface.set_alpha(alpha)
        
        # Add glow effect
        glow_surface = self.fonts['title'].render(title, True, WHITE)
        if scale != 1.0:
            glow_surface = pygame.transform.scale(glow_surface, new_size)
        glow_surface.set_alpha(alpha // 4)
        
        # Render glow
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            glow_rect = glow_surface.get_rect(center=(x + offset[0], y + offset[1]))
            self.screen.blit(glow_surface, glow_rect)
        
        # Render main title
        title_rect = title_surface.get_rect(center=(x, y))
        self.screen.blit(title_surface, title_rect)
    
    def render_main_menu(self, animation_time: float):
        """Render the main menu with animations."""
        # Animated background
        self._render_animated_background(animation_time)
        
        # Title
        title_y = 150 + int(math.sin(animation_time * 2) * 10)
        self.render_animated_title("COSMIC DEFENDERS", SCREEN_WIDTH // 2, title_y)
        
        # Subtitle
        subtitle = self.fonts['medium'].render("Enhanced Edition", True, UI_INFO)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, title_y + 80))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu buttons with staggered animation
        for i, button in enumerate(self.buttons['main_menu']):
            # Staggered entrance animation
            entrance_delay = i * 0.1
            if animation_time > entrance_delay:
                button_alpha = min(1.0, (animation_time - entrance_delay) * 2)
                button.render(self.screen, self.fonts['medium'])
    
    def handle_main_menu_events(self, event) -> Optional[str]:
        """Handle main menu events."""
        button_actions = ["start_game", "instructions", "level_select", 
                         "leaderboard", "settings", "daily_missions", "quit"]
        
        for i, button in enumerate(self.buttons['main_menu']):
            if button.handle_event(event):
                return button_actions[i]
        
        return None
    
    def render_name_input(self):
        """Render name input screen."""
        # Background
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("ENTER YOUR NAME", SCREEN_WIDTH // 2, 200)
        
        # Input box
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 25, 400, 50)
        pygame.draw.rect(self.screen, UI_SECONDARY, input_rect, border_radius=10)
        pygame.draw.rect(self.screen, UI_PRIMARY, input_rect, 3, border_radius=10)
        
        # Input text
        text_surface = self.fonts['large'].render(self.input_text, True, WHITE)
        text_rect = text_surface.get_rect(center=input_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Cursor
        if self.input_active and int(time.time() * 2) % 2:
            cursor_x = text_rect.right + 5
            pygame.draw.line(self.screen, WHITE, 
                           (cursor_x, input_rect.centery - 15), 
                           (cursor_x, input_rect.centery + 15), 2)
        
        # Instructions
        instruction = self.fonts['medium'].render("Press ENTER to continue, ESC to go back", True, UI_INFO)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(instruction, instruction_rect)
    
    def handle_name_input_events(self, event) -> Optional[str]:
        """Handle name input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text.strip():
                return self.input_text.strip()
            elif event.key == pygame.K_ESCAPE:
                return "back"
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable() and len(self.input_text) < 20:
                self.input_text += event.unicode
        
        self.input_active = True
        return None
    
    def render_difficulty_select(self):
        """Render difficulty selection screen."""
        # Background
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("SELECT DIFFICULTY", SCREEN_WIDTH // 2, 150)
        
        # Difficulty buttons with descriptions
        for i, (button, (key, diff)) in enumerate(zip(self.buttons['difficulty'][:-1], DIFFICULTIES.items())):
            button.render(self.screen, self.fonts['medium'])
            
            # Description
            desc_y = button.rect.centery + 35
            desc_surface = self.fonts['small'].render(diff['description'], True, UI_INFO)
            desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH // 2, desc_y))
            self.screen.blit(desc_surface, desc_rect)
            
            # Score multiplier
            mult_text = f"Score x{diff['score_mult']}"
            mult_surface = self.fonts['small'].render(mult_text, True, diff['color'])
            mult_rect = mult_surface.get_rect(center=(SCREEN_WIDTH // 2 + 150, button.rect.centery))
            self.screen.blit(mult_surface, mult_rect)
        
        # Back button
        self.buttons['difficulty'][-1].render(self.screen, self.fonts['medium'])
    
    def handle_difficulty_select_events(self, event) -> Optional[str]:
        """Handle difficulty selection events."""
        difficulty_keys = list(DIFFICULTIES.keys())
        
        for i, button in enumerate(self.buttons['difficulty'][:-1]):
            if button.handle_event(event):
                return difficulty_keys[i]
        
        # Back button
        if self.buttons['difficulty'][-1].handle_event(event):
            return "back"
        
        return None
    
    def render_level_select(self, unlocked_levels: set):
        """Render level selection screen."""
        # Background
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("SELECT LEVEL", SCREEN_WIDTH // 2, 100)
        
        # Level grid
        levels_per_row = 5
        start_x = SCREEN_WIDTH // 2 - (levels_per_row * 80) // 2
        start_y = 200
        
        for level in range(1, MAX_LEVELS + 1):
            row = (level - 1) // levels_per_row
            col = (level - 1) % levels_per_row
            
            x = start_x + col * 80
            y = start_y + row * 80
            
            # Level button
            is_unlocked = level in unlocked_levels
            color = UI_SUCCESS if is_unlocked else UI_SECONDARY
            
            level_rect = pygame.Rect(x - 30, y - 30, 60, 60)
            pygame.draw.rect(self.screen, color, level_rect, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, level_rect, 2, border_radius=10)
            
            # Level number
            text_color = WHITE if is_unlocked else (128, 128, 128)
            level_text = self.fonts['medium'].render(str(level), True, text_color)
            level_text_rect = level_text.get_rect(center=level_rect.center)
            self.screen.blit(level_text, level_text_rect)
            
            # Required score for locked levels
            if not is_unlocked and level in LEVEL_REQUIREMENTS:
                req_score = LEVEL_REQUIREMENTS[level]
                req_text = self.fonts['small'].render(f"{req_score:,}", True, UI_WARNING)
                req_rect = req_text.get_rect(center=(x, y + 45))
                self.screen.blit(req_text, req_rect)
        
        # Back button
        back_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, 
                           MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, "Back", UI_SECONDARY)
        back_button.render(self.screen, self.fonts['medium'])
    
    def handle_level_select_events(self, event, unlocked_levels: set) -> Optional[int]:
        """Handle level selection events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check level buttons
            levels_per_row = 5
            start_x = SCREEN_WIDTH // 2 - (levels_per_row * 80) // 2
            start_y = 200
            
            for level in range(1, MAX_LEVELS + 1):
                if level not in unlocked_levels:
                    continue
                    
                row = (level - 1) // levels_per_row
                col = (level - 1) % levels_per_row
                
                x = start_x + col * 80
                y = start_y + row * 80
                
                level_rect = pygame.Rect(x - 30, y - 30, 60, 60)
                if level_rect.collidepoint(event.pos):
                    return level
            
            # Check back button
            back_rect = pygame.Rect(SCREEN_WIDTH // 2 - MENU_BUTTON_WIDTH // 2, 
                                  SCREEN_HEIGHT - 130, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
            if back_rect.collidepoint(event.pos):
                return "back"
        
        return None
    
    def render_hud(self, health: int, max_health: int, score: int, wave: int, active_powerups: Dict):
        """Render game HUD."""
        # Health bar
        health_rect = pygame.Rect(HUD_MARGIN, HUD_MARGIN, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        health_percent = health / max_health
        
        # Health bar background
        pygame.draw.rect(self.screen, UI_DANGER, health_rect, border_radius=5)
        
        # Health bar fill
        fill_width = int(HEALTH_BAR_WIDTH * health_percent)
        fill_rect = pygame.Rect(HUD_MARGIN, HUD_MARGIN, fill_width, HEALTH_BAR_HEIGHT)
        
        if health_percent > 0.6:
            health_color = UI_SUCCESS
        elif health_percent > 0.3:
            health_color = UI_WARNING
        else:
            health_color = UI_DANGER
        
        pygame.draw.rect(self.screen, health_color, fill_rect, border_radius=5)
        
        # Health text
        health_text = self.fonts['small'].render(f"Health: {health}/{max_health}", True, WHITE)
        self.screen.blit(health_text, (HUD_MARGIN, HUD_MARGIN + HEALTH_BAR_HEIGHT + 5))
        
        # Score
        score_text = self.fonts['medium'].render(f"Score: {score:,}", True, WHITE)
        self.screen.blit(score_text, (HUD_MARGIN, HUD_MARGIN + 50))
        
        # Wave
        wave_text = self.fonts['medium'].render(f"Wave: {wave}", True, WHITE)
        self.screen.blit(wave_text, (HUD_MARGIN, HUD_MARGIN + 80))
    
    def _render_animated_background(self, time: float):
        """Render animated background effects."""
        # Animated gradient
        for y in range(0, SCREEN_HEIGHT, 4):
            intensity = int(20 + 10 * math.sin(time * 2 + y * 0.01))
            color = (intensity // 3, intensity // 2, intensity)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y), 4)
    
    def render_instructions(self):
        """Render instructions screen."""
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("INSTRUCTIONS", SCREEN_WIDTH // 2, 80)
        
        # Instructions content
        instructions = [
            "CONTROLS:",
            "WASD / Arrow Keys - Move",
            "Space - Shoot",
            "X / Shift - Special Ability (Time Freeze)",
            "ESC - Pause",
            "",
            "POWER-UPS:",
            "Green - Health Boost",
            "Cyan - Energy Shield",
            "Yellow - Rapid Fire",
            "Purple - Multi Shot",
            "Orange - Screen Clear",
            "",
            "ENEMIES:",
            "Red - Basic Enemy (100 pts)",
            "Yellow - Fast Enemy (150 pts)",
            "Purple - Heavy Enemy (300 pts)",
            "Green - Zigzag Enemy (200 pts)",
            "Orange - Boss Enemy (1000 pts)",
            "",
            "Press ESC to return to menu"
        ]
        
        y_offset = 150
        for line in instructions:
            if line == "":
                y_offset += 10
                continue
            
            if line.endswith(":"):
                color = UI_PRIMARY
                font = self.fonts['medium']
            else:
                color = WHITE
                font = self.fonts['small']
            
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 25
    
    def render_pause_menu(self):
        """Render pause menu overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause title
        pause_text = self.fonts['xlarge'].render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instructions = [
            "Press ESC to resume",
            "Or click below:"
        ]
        
        y_offset = SCREEN_HEIGHT // 2 - 50
        for instruction in instructions:
            text_surface = self.fonts['medium'].render(instruction, True, UI_INFO)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 40
    
    def handle_pause_menu_events(self, event) -> Optional[str]:
        """Handle pause menu events."""
        # Simple implementation - just return to game on ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "resume"
        return None
    
    def render_settings(self, audio_manager):
        """Render settings screen."""
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("SETTINGS", SCREEN_WIDTH // 2, 100)
        
        # Audio settings
        y_offset = 200
        settings_items = [
            ("Master Volume", audio_manager.master_volume),
            ("Music Volume", audio_manager.music_volume),
            ("SFX Volume", audio_manager.sfx_volume)
        ]
        
        for name, value in settings_items:
            # Label
            label_surface = self.fonts['medium'].render(name, True, WHITE)
            self.screen.blit(label_surface, (SCREEN_WIDTH // 2 - 200, y_offset))
            
            # Volume bar
            bar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, y_offset + 5, 200, 20)
            pygame.draw.rect(self.screen, UI_SECONDARY, bar_rect, border_radius=5)
            
            fill_width = int(200 * value)
            fill_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, y_offset + 5, fill_width, 20)
            pygame.draw.rect(self.screen, UI_PRIMARY, fill_rect, border_radius=5)
            
            # Value text
            value_text = self.fonts['small'].render(f"{int(value * 100)}%", True, WHITE)
            self.screen.blit(value_text, (SCREEN_WIDTH // 2 + 170, y_offset + 5))
            
            y_offset += 60
        
        # Back button
        back_text = self.fonts['medium'].render("Press ESC to go back", True, UI_INFO)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(back_text, back_rect)
    
    def handle_settings_events(self, event) -> Optional[str]:
        """Handle settings events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None
    
    def render_leaderboard(self, leaderboard_data: List[Dict]):
        """Render leaderboard screen."""
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("HALL OF FAME", SCREEN_WIDTH // 2, 100)

        # Headers
        headers = ["Rank", "Name", "Score", "Difficulty"]
        header_x_positions = [SCREEN_WIDTH // 2 - 200, SCREEN_WIDTH // 2 - 50, 
                             SCREEN_WIDTH // 2 + 50, SCREEN_WIDTH // 2 + 150]
        
        y_offset = 180
        for i, header in enumerate(headers):
            header_surface = self.fonts['medium'].render(header, True, UI_PRIMARY)
            header_rect = header_surface.get_rect(center=(header_x_positions[i], y_offset))
            self.screen.blit(header_surface, header_rect)

        # Separator line
        pygame.draw.line(self.screen, UI_PRIMARY,
                        (SCREEN_WIDTH // 2 - 250, y_offset + 25),
                        (SCREEN_WIDTH // 2 + 250, y_offset + 25), 2)
        
        # Leaderboard entries
        y_offset += 50
        for i, entry in enumerate(leaderboard_data[:10]):  # Top 10
            rank_color = UI_WARNING if i < 3 else WHITE
            
            # Rank
            rank_surface = self.fonts['medium'].render(f"#{i + 1}", True, rank_color)
            rank_rect = rank_surface.get_rect(center=(header_x_positions[0], y_offset))
            self.screen.blit(rank_surface, rank_rect)
            
            # Name
            name_surface = self.fonts['medium'].render(entry['name'], True, WHITE)
            name_rect = name_surface.get_rect(center=(header_x_positions[1], y_offset))
            self.screen.blit(name_surface, name_rect)
            
            # Score
            score_surface = self.fonts['medium'].render(f"{entry['score']:,}", True, UI_SUCCESS)
            score_rect = score_surface.get_rect(center=(header_x_positions[2], y_offset))
            self.screen.blit(score_surface, score_rect)
            
             # Difficulty
            diff_color = DIFFICULTIES.get(entry['difficulty'], {}).get('color', WHITE)
            diff_surface = self.fonts['medium'].render(entry['difficulty'], True, diff_color)
            diff_rect = diff_surface.get_rect(center=(header_x_positions[3], y_offset))
            self.screen.blit(diff_surface, diff_rect)
            
            y_offset += 40
        
        # Back instruction
        back_text = self.fonts['medium'].render("Press ESC to go back", True, UI_INFO)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
    
    def render_game_over(self, score: int, high_score: int):
        """Render game over screen."""
        self._render_animated_background(self.animation_time)
        
        # Game Over title
        game_over_text = self.fonts['xlarge'].render("GAME OVER", True, UI_DANGER)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.fonts['large'].render(f"Final Score: {score:,}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if score >= high_score:
            hs_text = self.fonts['medium'].render("NEW HIGH SCORE!", True, UI_SUCCESS)
        else:
            hs_text = self.fonts['medium'].render(f"High Score: {high_score:,}", True, UI_INFO)
        hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(hs_text, hs_rect)
        
        # Options
        options = [
            "Press SPACE to play again",
            "Press ESC for main menu"
        ]
        
        y_offset = 450
        for option in options:
            option_surface = self.fonts['medium'].render(option, True, UI_INFO)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(option_surface, option_rect)
            y_offset += 40
    
    def handle_game_over_events(self, event) -> Optional[str]:
        """Handle game over events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "restart"
            elif event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None
    
    def render_level_complete(self, level: int, score: int):
        """Render level complete screen."""
        self._render_animated_background(self.animation_time)
        
        # Level Complete title
        complete_text = self.fonts['xlarge'].render("LEVEL COMPLETE!", True, UI_SUCCESS)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(complete_text, complete_rect)
        
        # Level info
        level_text = self.fonts['large'].render(f"Level {level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(level_text, level_rect)
        
        # Score
        score_text = self.fonts['medium'].render(f"Score: {score:,}", True, UI_INFO)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(score_text, score_rect)
        
        # Options
        options = [
            "Press SPACE for next level",
            "Press ESC for main menu"
        ]
        
        y_offset = 400
        for option in options:
            option_surface = self.fonts['medium'].render(option, True, UI_INFO)
            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(option_surface, option_rect)
            y_offset += 40
    
    def handle_level_complete_events(self, event) -> Optional[str]:
        """Handle level complete events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "next_level"
            elif event.key == pygame.K_ESCAPE:
                return "main_menu"
        return None
    
    def render_daily_missions(self, missions: List[Dict]):
        """Render daily missions screen."""
        self._render_animated_background(self.animation_time)
        
        # Title
        self.render_animated_title("DAILY MISSIONS", SCREEN_WIDTH // 2, 100)
        
        # Mission list
        y_offset = 200
        for i, mission in enumerate(missions):
            # Mission background
            mission_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y_offset - 20, 600, 80)
            pygame.draw.rect(self.screen, UI_SECONDARY, mission_rect, border_radius=10)
            pygame.draw.rect(self.screen, UI_PRIMARY, mission_rect, 2, border_radius=10)
            
            # Mission text
            mission_text = f"Mission {i + 1}: {mission['type'].title()}"
            text_surface = self.fonts['medium'].render(mission_text, True, WHITE)
            self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - 280, y_offset - 10))
            
            # Target and reward
            target_text = f"Target: {mission['target']}"
            reward_text = f"Reward: {mission['reward'].replace('_', ' ').title()}"
            
            target_surface = self.fonts['small'].render(target_text, True, UI_INFO)
            reward_surface = self.fonts['small'].render(reward_text, True, UI_SUCCESS)
            
            self.screen.blit(target_surface, (SCREEN_WIDTH // 2 - 280, y_offset + 15))
            self.screen.blit(reward_surface, (SCREEN_WIDTH // 2 - 280, y_offset + 35))

            y_offset += 100

        # Back instruction
        back_text = self.fonts['medium'].render("Press ESC to go back", True, UI_INFO)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
