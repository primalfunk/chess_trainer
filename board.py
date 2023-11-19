import pygame
import chess

class ChessBoard:
    def __init__(self, board_size=800):
        self.player_color = True
        self.board_size = board_size
        self.square_size = self.board_size // 8
        self.images = {}
        self.piece_map = {'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king', 'p': 'pawn'}
        self.load_images()

    def load_images(self):
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                file_path = f"images/{piece}_{color}.png"
                self.images[f"{piece}_{color}"] = pygame.transform.scale(
                    pygame.image.load(file_path),
                    (self.square_size, self.square_size)
                )

    def draw_board(self, screen, player_color):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        
        for row in range(8):
            for col in range(8):
                display_row = 7 - row if player_color else row
                display_col = col if player_color else 7 - col
                color = colors[(display_row + display_col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(display_col * self.square_size, display_row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self, screen, board, player_color):
        for row in range(8):
            for col in range(8):
                display_row = 7 - row if player_color else row
                display_col = col if player_color else 7 - col
                piece = board.piece_at(chess.square(col, row))
                if piece:
                    piece_type = self.piece_map[piece.symbol().lower()]
                    color = "white" if piece.color else "black"
                    piece_name = f"{piece_type}_{color}"
                    screen.blit(self.images[piece_name],
                                pygame.Rect(display_col * self.square_size , display_row * self.square_size, self.square_size, self.square_size))

    def draw_piece_at_position(self, screen, piece, position):
        piece_image = self.images[piece]
        x, y = position
        x -= self.square_size // 2
        y -= self.square_size // 2
        screen.blit(piece_image, (x, y))
