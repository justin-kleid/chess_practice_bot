"""
Generates the menu for the chess game where settings can be altered via clicking.
"""
import pygame as p
import run_game

ROW_DIM =  8
SQUARE_DIM = 50
BLUE = (8, 96, 168)
TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class MenuInfo(object):
    def __init__(self, display):
        self.font = p.font.SysFont(None, 25)
        self.display = display
        self.display.blit(self.font.render('click to toggle: u to undo, r to reset', True, (255, 255, 255)), (50, 365))
    def add_rect(self, button_type):
        self.rect = p.draw.rect(self.display, (0, 0, 0), button_type)
    def add_start_text(self):
        self.display.blit(self.font.render('START GAME', True, (255, 255, 255)), (150, 40))
    def add_player_mode_text(self, single_player_mode):
        if single_player_mode:
            self.display.blit(self.font.render('Versus Chess AI', True, (255, 255, 255)), (120, 110))
        else:
            self.display.blit(self.font.render('Versus Other Human', True, (255, 255, 255)), (120, 110))
    def add_difficulty_text(self, difficulty):
        self.display.blit(self.font.render('Computer Elo: ' + str(difficulty), True, (255, 255, 255)), (120, 180))
    def add_color_text(self, start_color):
        self.display.blit(self.font.render('Play ' + start_color, True, (255, 255, 255)), (160, 250))
    def add_exit_text(self):
        self.display.blit(self.font.render('EXIT', True, (255, 255, 255)), (180, 320))

# Generates the main menu display, and enables setting toggles. 
def main():
    p.init()
    display = p.display.set_mode((SQUARE_DIM * ROW_DIM, SQUARE_DIM * ROW_DIM))
    clock = p.time.Clock()
    run = True
    single_player_mode = False
    start_color = 'white' 
    difficulty = 1500
    result = ""
    while run:
        display.fill(BLUE)
        start_button = p.Rect(100, 20, 200, 50)
        player_mode_button = p.Rect(100, 90, 200, 50)
        difficulty_button = p.Rect(100, 160, 200, 50)
        color_button = p.Rect(100, 230, 200, 50)
        exit_button = p.Rect(100, 300, 200, 50)       
        menu = MenuInfo(display)
        menu.add_rect(start_button)
        menu.add_start_text()
        menu.add_rect(player_mode_button)
        menu.add_player_mode_text(single_player_mode)
        menu.add_rect(difficulty_button)
        menu.add_difficulty_text(difficulty)
        menu.add_rect(color_button)
        menu.add_color_text(start_color)
        menu.add_rect(exit_button)
        menu.add_exit_text()
        if result == "mate":
            initiate_checkmate(display)
        elif result == "draw":
             initiate_draw(display)
        elif result == "exit": 
            run = False
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            elif event.type == p.MOUSEBUTTONDOWN:
                cursor_position = p.mouse.get_pos()
                if (start_button.collidepoint(cursor_position)):
                    result = run_game.init_game(display, clock, single_player_mode, difficulty, start_color)
                elif (player_mode_button.collidepoint(cursor_position)):
                    if single_player_mode == True:
                        single_player_mode = False
                    else: 
                        single_player_mode = True
                elif (difficulty_button.collidepoint(cursor_position)):
                    if difficulty == 2200:
                        difficulty = 1500
                    else: 
                        difficulty += 100
                elif (color_button.collidepoint(cursor_position)):
                    if start_color == 'white':
                        start_color = 'black'
                    else:
                        start_color = 'white'
                elif (exit_button.collidepoint(cursor_position)):
                    run = False
        p.display.flip()
        clock.tick(60)
        p.display.update()
    p.quit()


# Generate a draw display on the menu screen in case of draw
def initiate_draw(display):
    font = p.font.Font("freesansbold.ttf", 16)
    text = font.render("Draw!", True, RED, BLACK)
    banner = text.get_rect()
    banner.center = (SQUARE_DIM * ROW_DIM // 2, )
    display.blit(text, banner)

# Generate a checkmate display on the menu screen in case of checkmate
def initiate_checkmate(display):
    font = p.font.Font("freesansbold.ttf", 16)
    text = font.render("Checkmate!", True, RED, BLACK)
    banner = text.get_rect()
    banner.center = (SQUARE_DIM * ROW_DIM // 2, 10)
    display.blit(text, banner)




if __name__ == "__main__":
    main()