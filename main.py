import pygame
import chess
import chess.engine

class ChessBoard():
    def __init__(self):
        self.board_size = 800
        self.square_size = self.board_size // 8
        self.images = {} 
        self.piece_map = {'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king', 'p': 'pawn'}

    def load_images(self):
        """Load chess piece images into a dictionary."""
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                file_path = f"images/{piece}_{color}.png"
                print(f"Loading: {file_path}")
                self.images[f"{piece}_{color}"] = pygame.transform.scale(
                    pygame.image.load(f"images/{piece}_{color}.png"),
                    (self.square_size, self.square_size)
                )
        print(self.images.keys())

    def draw_board(self, screen):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                # Flip the board based on player color
                display_row = 7 - row if self.player_color else row
                display_col = col if self.player_color else 7 - col
                color = colors[(display_row + display_col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(display_col * self.square_size, display_row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self, screen, board):
        for row in range(8):
            for col in range(8):
                # Flip the pieces based on player color
                display_row = 7 - row if self.player_color else row
                display_col = col if self.player_color else 7 - col

                piece = board.piece_at(chess.square(col, row))  # Use original col and row here
                if piece:
                    piece_type = self.piece_map[piece.symbol().lower()]
                    color = "white" if piece.color else "black"
                    piece_name = f"{piece_type}_{color}"
                    screen.blit(self.images[piece_name],
                                pygame.Rect(display_col * self.square_size, display_row * self.square_size, self.square_size, self.square_size))

    def draw_piece_at_position(self, screen, piece, position):
        """Draw a single chess piece at the given position."""
        piece_image = self.images[piece]
        x, y = position
        x -= self.square_size // 2
        y -= self.square_size // 2
        screen.blit(piece_image, (x, y))

    def get_display_row(self, row):
        """Convert logical row to display row based on player's color."""
        return row if self.player_color else 7 - row


def main():
    pygame.init()
    guiBoard = ChessBoard()
    guiBoard.player_color = True
    screen = pygame.display.set_mode((guiBoard.board_size, guiBoard.board_size))
    clock = pygame.time.Clock()
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/erinm/Desktop/VSCodeProjects/MyChessBoard/stockfish.exe")
    engine.configure({"Skill Level": 20,
                      "UCI_LimitStrength": True,
                      "UCI_Elo": 1900
                      })
    guiBoard.load_images()
    if not guiBoard.player_color:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)

    selected_piece = None
    piece_being_dragged = None
    dragging_position = (0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # Get mouse position
                col = location[0] // guiBoard.square_size

                if guiBoard.player_color:
                    row = 7 - (location[1] // guiBoard.square_size)
                    col = location[0] // guiBoard.square_size
                else:
                    row = location[1] // guiBoard.square_size
                    col = 7 - (location[0] // guiBoard.square_size)
                square = chess.square(col, row)

                piece = board.piece_at(square)
                if piece:
                    color = "white" if piece.color else "black"
                    piece_type = guiBoard.piece_map[piece.symbol().lower()]
                    piece_being_dragged = f"{piece_type}_{color}"
                    dragging_position = event.pos
                    selected_piece = square 

            elif event.type == pygame.MOUSEMOTION:
                if piece_being_dragged:
                    dragging_position = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if piece_being_dragged:
                    release_pos = pygame.mouse.get_pos()

                    if guiBoard.player_color:
                        # Interpret for white at the bottom
                        release_row = 7 - (release_pos[1] // guiBoard.square_size)
                        release_col = release_pos[0] // guiBoard.square_size
                    else:
                        # Interpret for black at the bottom
                        release_row = release_pos[1] // guiBoard.square_size
                        release_col = 7 - (release_pos[0] // guiBoard.square_size)
                    new_square = chess.square(release_col, release_row)


                    move = chess.Move(selected_piece, new_square)
                    if selected_piece is not None and move in board.legal_moves:
                        board.push(move)
                        result = engine.play(board, chess.engine.Limit(time=0.1))
                        board.push(result.move)
                    selected_piece = None
                    piece_being_dragged = None

        guiBoard.draw_board(screen)
        guiBoard.draw_pieces(screen, board)
        if piece_being_dragged:
            guiBoard.draw_piece_at_position(screen, piece_being_dragged, dragging_position)
        pygame.display.flip()
        clock.tick(60)

    engine.quit()
    pygame.quit()

if __name__ == "__main__":
    main()