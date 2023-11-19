import chess
import chess.engine
from board import ChessBoard
from engine_dashboard import EngineDashboard
import pygame
import pygame_gui
import string

class ChessGame:
    def __init__(self, screen, board_size=800):
        self.window_size = (1100, 800)
        self.screen = screen
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("C:/Users/erinm/Desktop/VSCodeProjects/MyChessBoard/stockfish.exe")
        self.current_engine_settings = {}
        self.manager = pygame_gui.UIManager(self.window_size)
        self.guiBoard = ChessBoard(board_size)
        dashboard_rect = pygame.Rect(800, 0, 300, 800)
        self.player_color = True
        self.dashboard = EngineDashboard(self.engine, self.manager, dashboard_rect, self.player_color)
        self.selected_piece = None
        self.piece_being_dragged = None
        self.dragging_position = (0, 0)
        self.game_in_progress = True

    def handle_mouse_down(self, location):
        x, y = location
        if 0 <= x < self.guiBoard.board_size and 0 <= y < self.guiBoard.board_size:
            col = x // self.guiBoard.square_size
            if self.guiBoard.player_color:
                row = 7 - (y // self.guiBoard.square_size)
                col = x // self.guiBoard.square_size
            else:
                row = y // self.guiBoard.square_size
                col = 7 - (x // self.guiBoard.square_size)
            square = chess.square(col, row)
            piece = self.board.piece_at(square)
            if piece:  # If there is a piece on the square
                color = 'white' if piece.color else 'black'
                piece_type = self.guiBoard.piece_map[piece.symbol().lower()]
                self.piece_being_dragged = f"{piece_type}_{color}"
                self.dragging_position = location
                self.selected_piece = square

    def handle_mouse_motion(self, location):
        if self.piece_being_dragged:
            self.dragging_position = location

    def handle_mouse_up(self, location):
        if self.piece_being_dragged:
            release_row, release_col = self.calculate_board_position(location)
            new_square = chess.square(release_col, release_row)
            move = chess.Move(self.selected_piece, new_square)
            if self.board.piece_at(self.selected_piece).symbol().lower() == 'p' and (release_row == 0 or release_row == 7):
                promotion_piece = self.guiBoard.show_promotion_popup(self.screen, self.guiBoard.square_size)
                promotion_choice = {'queen': chess.QUEEN, 'rook': chess.ROOK, 'bishop': chess.BISHOP, 'knight': chess.KNIGHT}[promotion_piece]
                move = chess.Move(self.selected_piece, new_square, promotion_choice)
            if move in self.board.legal_moves:
                self.board.push(move)
                # Trigger engine move only after a valid player move
                result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
                if result.move:
                    self.board.push(result.move)
            self.selected_piece = None
            self.piece_being_dragged = None

    def draw(self):
        self.guiBoard.draw_board(self.screen, self.player_color)
        self.guiBoard.draw_pieces(self.screen, self.board, self.player_color)
        if self.piece_being_dragged:
            self.guiBoard.draw_piece_at_position(self.screen, self.piece_being_dragged, self.dragging_position)

    def process_dashboard_event(self, event):
        self.dashboard.process_event(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.dashboard.reset_button:
                    self.reset_game()

    def update_dashboard(self, time_delta):
        self.dashboard.update(time_delta)

    def draw_dashboard(self):
        self.dashboard.draw(self.screen)

    def apply_engine_settings(self, settings):
        # Apply engine settings (Threads, Hash, etc.)
        for option_name, option_value in settings.items():
            self.engine.configure({option_name: option_value})
        self.current_engine_settings = settings 

    def print_engine_settings(self):
        for option_name, option_value in self.current_engine_settings.items():
            print(f"{option_name}: {option_value}")

    def check_game_over(self):
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw due to insufficient material"
        elif self.board.is_seventyfive_moves():
            return "Draw due to 75-move rule"
        elif self.board.is_fivefold_repetition():
            return "Draw due to fivefold repetition"
        return None

    def reset_game(self):
        print("Resetting game...")
        engine_settings = self.dashboard.get_engine_settings()
        self.apply_engine_settings(engine_settings)
        self.print_engine_settings()

        self.board.reset()
        self.player_color = self.dashboard.dashboard_player_color
        self.guiBoard.player_color = self.player_color
        if not self.player_color:
            self.engine_move()

    def draw_game_over_message(self, message):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        self.screen.blit(text_surface, text_rect)

    def engine_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        if result.move:
            self.board.push(result.move)

    def calculate_board_position(self, position):
        x, y = position
        if self.guiBoard.player_color:  # If player is white
            col = x // self.guiBoard.square_size
            row = 7 - (y // self.guiBoard.square_size)
        else:  # If player is black
            col = 7 - (x // self.guiBoard.square_size)
            row = y // self.guiBoard.square_size
        return row, col
        


