import pygame
from chess_game import ChessGame

def main():
    pygame.init()
    window_size = (1100, 800)
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    chess_game = ChessGame(screen)

    running = True
    while running:
        time_delta = clock.tick(60)/100.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Process dashboard events
            chess_game.process_dashboard_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                chess_game.handle_mouse_down(location)

            if event.type == pygame.MOUSEMOTION:
                if chess_game.piece_being_dragged:
                    chess_game.dragging_position = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if chess_game.piece_being_dragged:
                    location = pygame.mouse.get_pos()
                    chess_game.handle_mouse_up(location)

        chess_game.update_dashboard(time_delta)
        chess_game.draw()
        chess_game.draw_dashboard()

        game_over_message = chess_game.check_game_over()
        if game_over_message:
            chess_game.draw_game_over_message(game_over_message)

        pygame.display.flip()
        clock.tick(60)
    chess_game.close()
    pygame.quit()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True

if __name__ == "__main__":
    main()