import pygame
import pygame_gui
import chess.engine

class EngineDashboard:
    def __init__(self, engine, manager, rect, player_color):
        self.engine = engine
        self.manager = manager
        self.rect = rect
        self.background_color = pygame.Color("white")
        self.x_offset = self.rect.x
        self.ponder_state = False
        self.limit_strength_state = True
        self.use_nnue_state = False
        self.dashboard_player_color = player_color
        self.label_text_color = pygame.Color("black")

        # Player Color selection
        self.player_color_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_offset + 10, 30), (200, 50)),
            text='White',
            manager=manager)
        
        # Threads Slider
        self.threads_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.x_offset + 10, 90), (280, 20)),
            text='Threads',
            manager=manager)
        self.threads_label.text_colour = self.label_text_color
        self.threads_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.x_offset + 10, 110), (280, 25)),
            start_value=engine.options["Threads"].default,
            value_range=(engine.options["Threads"].min, engine.options["Threads"].max),
            manager=manager)

        # Hash Slider
        self.hash_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.x_offset + 10, 140), (280, 20)),
            text='Hash',
            manager=manager)
        self.hash_label.text_colour = self.label_text_color
        self.hash_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.x_offset + 10, 160), (280, 25)),
            start_value=engine.options["Hash"].default,
            value_range=(engine.options["Hash"].min, engine.options["Hash"].max),
            manager=manager)

        # Skill Level Slider
        self.skill_level_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.x_offset + 10, 190), (280, 20)),
            text='Skill Level',
            manager=manager)
        self.skill_level_label.text_colour = self.label_text_color
        self.skill_level_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.x_offset + 10, 210), (280, 25)),
            start_value=engine.options["Skill Level"].default,
            value_range=(engine.options["Skill Level"].min, engine.options["Skill Level"].max),
            manager=manager)

        # UCI_Elo Slider
        self.uci_elo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.x_offset + 10, 240), (280, 20)),
            text='UCI Elo',
            manager=manager)
        self.uci_elo_label.text_colour = self.label_text_color
        self.uci_elo_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.x_offset + 10, 260), (280, 25)),
            start_value=engine.options["UCI_Elo"].default,
            value_range=(engine.options["UCI_Elo"].min, engine.options["UCI_Elo"].max),
            manager=manager)

        # UCI_LimitStrength Toggle
        self.limit_strength_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_offset + 10, 370), (200, 50)),
            text='Limit Strength: On',
            manager=manager)

        # Use NNUE Toggle
        self.use_nnue_toggle = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_offset + 10, 440), (200, 50)),
            text='Use NNUE: Off',
            manager=manager)
        
        # Reset Button
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_offset + 10, 540), (200, 50)),
            text='Reset Game',
            manager=manager)
        
        self.update_labels()

    def process_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.player_color_toggle:
                    self.dashboard_player_color = not self.dashboard_player_color
                    color_text = 'White' if self.dashboard_player_color else 'Black'
                    self.player_color_toggle.set_text(color_text)
                if event.ui_element == self.limit_strength_toggle:
                    self.limit_strength_state = not self.limit_strength_state
                    self.limit_strength_toggle.set_text(f'Limit Strength: {"On" if self.limit_strength_state else "Off"}')
                if event.ui_element == self.use_nnue_toggle:
                    self.use_nnue_state = not self.use_nnue_state
                    self.use_nnue_toggle.set_text(f'Use NNUE: {"On" if self.use_nnue_state else "Off"}')


    def update(self, time_delta):
        self.manager.update(time_delta)
        self.update_labels()

    def update_labels(self):
        self.threads_label.set_text(f"Threads: {self.threads_slider.get_current_value()}")
        self.hash_label.set_text(f"Hash: {self.hash_slider.get_current_value()}")
        self.skill_level_label.set_text(f"Skill Level: {self.skill_level_slider.get_current_value()}")
        self.uci_elo_label.set_text(f"UCI Elo: {self.uci_elo_slider.get_current_value()}")

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        border_color = pygame.Color("gray")
        border_width = 5
        pygame.draw.rect(screen, border_color, self.rect, border_width)
        self.manager.draw_ui(screen)

    def get_engine_settings(self):
        settings = {
            "Threads": self.threads_slider.get_current_value(),
            "Hash": self.hash_slider.get_current_value(),
            "Skill Level": self.skill_level_slider.get_current_value(),
            "UCI_Elo": self.uci_elo_slider.get_current_value(),
            "UCI_LimitStrength": self.limit_strength_state,
            "Use NNUE": self.use_nnue_state
        }
        return settings
