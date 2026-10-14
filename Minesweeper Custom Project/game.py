import pygame 
import os
import constants
from leaderboard import Leaderboard
from board import Board


class Game():
        #  ---------- PART 1: FOUNDATION ----------
    def __init__(self, board):
        self.board = board
        self.grid_width = self.board.cols * constants.TILE_SIZE
        self.x_offset = (constants.SCREEN_WIDTH - self.grid_width) // 2
        self.screen_size = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self.images = {}
        self.load_images()
        self.lost = False 
        self.won = False
        self.first_click = True 
        self.is_custom_game = False
        self.reset_button_rect = pygame.Rect(self.screen_size[0] // 2 -20, 10, 40, 40 )  
        self.timer_started = False
        self.start_time = 0 
        self.current_time = 0
        self.state = constants.STATE_MENU
        # menu page
        start_x = constants.SCREEN_WIDTH // 2 - 140
        self.btn_easy = pygame.Rect(start_x, 120, 280, 45)
        self.btn_medium = pygame.Rect(start_x, 185, 280, 45)
        self.btn_hard = pygame.Rect(start_x, 250, 280, 45)
        self.btn_custom = pygame.Rect(start_x, 315, 280, 45)
        self.btn_lb = pygame.Rect(start_x, 380, 280, 45)
        self.back_button_rect = pygame.Rect(constants.SCREEN_WIDTH//2 -70, constants.SCREEN_HEIGHT - 60, 140, 40)
        # custom page
        self.custom_rows = 10 
        self.custom_cols = 10 
        self.button_row_minus = pygame.Rect(constants.SCREEN_WIDTH  // 2 - 120, 200, 30, 30)
        self.button_row_plus = pygame.Rect(constants.SCREEN_WIDTH  // 2 + 90, 200, 30, 30 )
        self.button_col_minus = pygame.Rect(constants.SCREEN_WIDTH // 2 - 120, 260, 30, 30)
        self.button_col_plus = pygame.Rect(constants.SCREEN_WIDTH // 2 + 90, 260, 30, 30)
        self.button_play_custom = pygame.Rect(constants.SCREEN_WIDTH // 2 - 70, 380, 140, 40)
        # leaderboard page
        self.leaderboard_manager = Leaderboard()
        tab_width = 90
        gap = 10
        start_x = constants.SCREEN_WIDTH // 2 - (tab_width * 3 + gap * 2) // 2
        self.tab_easy_rect = pygame.Rect(start_x, 105, tab_width, 35)
        self.tab_medium_rect = pygame.Rect(start_x + tab_width + gap, 105, tab_width, 35)
        self.tab_hard_rect = pygame.Rect(start_x + (tab_width + gap) * 2, 105, tab_width, 35)

        self.player_name = ""
        self.input_rect = pygame.Rect(constants.SCREEN_WIDTH // 2 - 100, 150, 200, 40 )      
        self.search_text = ""
        self.found_index = -1    

    def load_images(self):
        path = "assets/images"
        for filename in os.listdir(path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                full_path = os.path.join(path, filename)
                image = pygame.image.load(full_path)
                image = pygame.transform.scale(image, (constants.TILE_SIZE, constants.TILE_SIZE))
                name_only = filename.split(".")[0]
                self.images[name_only] = image

        print(f"Loaded Successfully {len(self.images)} pictures !")
        for key in self.images:
            print(f"Key: {key} | Value: {self.images[key]}")
                      
    def run(self):
        pygame.init()
        self.font = pygame.font.SysFont('consolas', 30, bold=True)
        self.title_font = pygame.font.SysFont('consolas', 35, bold=True)
        self.list_font = pygame.font.SysFont('consolas', 24)
        self.screen = pygame.display.set_mode(self.screen_size)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == constants.STATE_MENU:
                    self.handle_menu_events(event)
                elif self.state == constants.STATE_PLAYING:
                    self.handle_playing_events(event)
                elif self.state == constants.STATE_LEADERBOARD:
                    self.handle_leaderboard_events(event)
                elif self.state == constants.STATE_INPUT:
                    self.handle_input_events(event)
                elif self.state == constants.STATE_CUSTOM:
                    self.handle_custom_events(event)

                
            if self.state == constants.STATE_PLAYING:
                if self.timer_started and not self.lost and not self.won:
                    self.current_time = (pygame.time.get_ticks() - self.start_time) // 1000 


            self.screen.fill(constants.GRAY)
            if self.state == constants.STATE_MENU:
                self.draw_menu()
            elif self.state == constants.STATE_PLAYING:
                self.draw_play()
            elif self.state == constants.STATE_LEADERBOARD:
                self.draw_leaderboard()
            elif self.state == constants.STATE_INPUT:
                self.draw_input_name()
            elif self.state == constants.STATE_CUSTOM:
                self.draw_custom_menu()

            pygame.display.flip()
        pygame.quit()

                                                    # ---------- PART 2: LOGIC GAME ----------
    def check_won(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                piece  = self.board.grid[r][c]
                if not piece.is_opened and not piece.has_mine: 
                    return False
        return True
    
    def expand_empty(self,r ,c ):
        if (r >= self.board.rows) or (r < 0) or (c >= self.board.cols) or (c < 0)  :
            return 
        else:   
            piece = self.board.grid[r][c]
            if piece.is_opened or piece.is_flagged: 
                return
            else:
                piece.is_opened = True
                if piece.num_around == 0:
                    for dr in range(-1,2):
                        for dc in range(-1,2):
                            if dr == 0 and dc == 0:
                                continue
                            self.expand_empty(r + dr, c + dc)   

    def reset(self):
        self.board.grid = []
        self.board.create_grid()
        #self.board.place_mines()
        #self.board.calculate_neighbors()

        self.lost = False
        self.won = False

        self.timer_started = False
        self.start_time = 0
        self.current_time = 0 

        self.first_click = True

        pygame.display.set_caption("Minesweeper")


    # ---------- PART 3: HANDLE EVENTS ----------

    def handle_playing_events(self, event):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:  # Press I to move to input name state 
                    self.state = constants.STATE_INPUT                                   
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = pos

            if self.reset_button_rect.collidepoint(pos):
                self.reset()
                return
            if self.back_button_rect.collidepoint(pos):
                self.state = constants.STATE_MENU 
                return
            if not self.lost and not self.won:      
                if self.x_offset <= x <= self.x_offset + self.grid_width and constants.Y_OFFSET <= y <= constants.SCREEN_HEIGHT:
                    col = (x - self.x_offset)         // constants.TILE_SIZE
                    row = (y -constants.Y_OFFSET) // constants.TILE_SIZE
                    if 0 <= row < self.board.rows and 0 <= col < self.board.cols:
                        piece = self.board.grid[row][col]                            

                        if event.button == 1 and not piece.is_flagged :
                                if self.first_click:
                                    self.board.place_mines(row,col)
                                    self.board.calculate_neighbors()
                                    self.first_click = False
                                    self.timer_started = True
                                    self.start_time = pygame.time.get_ticks()
                                if piece.has_mine :
                                    piece.open()
                                    self.lost = True
                                else:
                                    self.expand_empty(row,col)
                                    self.won = self.check_won()
                                    if self.won:
                                        pygame.display.set_caption("CONGRATULATIONS! YOU WON !")
                                        if not self.is_custom_game:
                                            self.state = constants.STATE_INPUT

                        if event.button == 3 and not piece.is_opened:
                            piece.toggle_flag()

    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.btn_easy.collidepoint(pos):
                self.is_custom_game = False
                self.board = Board(rows =9, cols = 9 , mines =10)
                self.leaderboard_manager.current_tab = "Easy"
                self.state = constants.STATE_PLAYING  
            if self.btn_medium.collidepoint(pos):
                self.is_custom_game = False
                self.board = Board(rows =12, cols = 12 , mines =25)
                self.leaderboard_manager.current_tab = "Medium"
                self.state = constants.STATE_PLAYING       
            if self.btn_hard.collidepoint(pos):
                self.is_custom_game = False
                self.board = Board(rows =14, cols = 18 , mines =50)
                self.leaderboard_manager.current_tab = "Hard"
                self.state = constants.STATE_PLAYING     
            if self.btn_custom.collidepoint(pos):
                self.is_custom_game = True 
                self.state = constants.STATE_CUSTOM
                return
            if self.btn_lb.collidepoint(pos):
                self.state = constants.STATE_LEADERBOARD
                return                      
            if self.state == constants.STATE_PLAYING:
                self.grid_width = self.board.cols * constants.TILE_SIZE
                self.x_offset = (constants.SCREEN_WIDTH-self.grid_width) //2
                self.reset()  

    def handle_leaderboard_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.back_button_rect.collidepoint(pos):
                self.state = constants.STATE_MENU 
            elif self.tab_easy_rect.collidepoint(pos):
                self.leaderboard_manager.current_tab = "Easy"
                self.found_index = -1
            elif self.tab_medium_rect.collidepoint(pos):
                self.leaderboard_manager.current_tab = "Medium"
                self.found_index = -1
            elif self.tab_hard_rect.collidepoint(pos):
                self.leaderboard_manager.current_tab = "Hard"
                self.found_index = -1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.found_index = self.leaderboard_manager.search_player(self.search_text)
                self.search_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.search_text = self.search_text[:-1]
            elif len(self.search_text) < 15:
                self.search_text += event.unicode
                self.found_index = -1

    def handle_input_events(self,event):
        # HANDLE TYPING
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.leaderboard_manager.add_scores(self.player_name, self.current_time)
                self.state = constants.STATE_LEADERBOARD
                pygame.display.set_caption("Minesweeper") 
                self.player_name = ""
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif len(self.player_name) < 15:
                self.player_name += event.unicode

    def handle_custom_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.back_button_rect.collidepoint(pos):
                self.state = constants.STATE_MENU

            if self.button_row_minus.collidepoint(pos):
                if self.custom_rows > 5:
                    self.custom_rows -= 1 
            if self.button_row_plus.collidepoint(pos):
                if self.custom_rows < 14:
                    self.custom_rows += 1

            if self.button_col_minus.collidepoint(pos):
                if self.custom_cols > 5:
                    self.custom_cols -= 1
                    
            if self.button_col_plus.collidepoint(pos):
                if self.custom_cols < 18:
                    self.custom_cols += 1

            if self.button_play_custom.collidepoint(pos):
                custom_mines = (self.custom_rows * self.custom_cols) * 15 // 100

                self.board = Board(rows=self.custom_rows, cols=self.custom_cols, mines=custom_mines)

                self.grid_width = self.board.cols * constants.TILE_SIZE
                self.x_offset =  (constants.SCREEN_WIDTH - self.grid_width) // 2

                self.reset()
                self.state = constants.STATE_PLAYING

    # ---------- PART 4: DRAWING OUTPUTS ----------

    def draw_play(self):
        self.draw_reset_button()

        self.draw_timer()
        
        self.draw_mine_counter()

        for r in range(self.board.rows):
            for c in range(self.board.cols):
                piece  = self.board.grid[r][c]
               
                if piece.is_opened:
                    if piece.has_mine:
                        image = self.images["bomb-at-clicked-block"] 
                    else:
                        image = self.images[str(piece.num_around)]    
                elif self.lost == True and piece.has_mine :
                        image = self.images["unclicked-bomb"]
                elif self.lost == True and piece.is_flagged and not piece.has_mine :
                        image = self.images["wrong-flag"]
                else:
                    if piece.is_flagged:
                        image = self.images["flag"]
                    else: 
                        image = self.images["empty-block"]

                
                pos = (self.x_offset + c * constants.TILE_SIZE, r * constants.TILE_SIZE + constants.Y_OFFSET)
                self.screen.blit(image, pos)

        # BACK BUTTON
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.back_button_rect)
        back_text = self.font.render("BACK", True, constants.RED)
        self.back_button_rect.width = back_text.get_width() +20
        self.back_button_rect.x = constants.SCREEN_WIDTH//2 - self.back_button_rect.width//2
        self.screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5 ))

    def draw_custom_menu(self):
        #TITLE 
        title = self.title_font.render("CUSTOM BOARD", True, constants.BLACK)
        self.screen.blit(title, (constants.SCREEN_WIDTH//2 - title.get_width()//2, 80))

        #Row custom buttons
        row_text = self.font.render(f"ROWS: {self.custom_rows:02}", True, constants.BLACK)
        self.screen.blit(row_text, (constants.SCREEN_WIDTH // 2 - row_text.get_width() // 2, 200))
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.button_row_minus)
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.button_row_plus)
        self.screen.blit(self.font.render("-", True, constants.WHITE), (self.button_row_minus.x + 8, self.button_row_minus.y))
        self.screen.blit(self.font.render("+", True, constants.WHITE), (self.button_row_plus.x + 8, self.button_row_plus.y))

        #Col custom button
        col_text = self.font.render(f"COLS: {self.custom_cols:02}", True, constants.BLACK)
        self.screen.blit(col_text, (constants.SCREEN_WIDTH // 2 - col_text.get_width() // 2, 260)) 
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.button_col_minus)
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.button_col_plus)
        self.screen.blit(self.font.render("-", True, constants.WHITE), (self.button_col_minus.x + 8, self.button_col_minus.y))
        self.screen.blit(self.font.render("+", True, constants.WHITE), (self.button_col_plus.x + 8, self.button_col_plus.y))

        #calculate mine ( 15% )
        mines = (self.custom_cols * self.custom_rows) * 15 //100 
        mine_text = self.list_font.render(f"Mines: {mines}", True, constants.RED)
        self.screen.blit(mine_text, (constants.SCREEN_WIDTH//2 - mine_text.get_width()//2, 320))

        #Play button
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.button_play_custom)
        play_text = self.font.render("START", True, constants.WHITE)
        self.screen.blit(play_text, (self.button_play_custom.x+ 25, self.button_play_custom.y + 5))

        # BACK button
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.back_button_rect)
        back_text = self.font.render("BACK", True, constants.RED)
        self.screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_menu(self):
        title_text = self.font.render("MINESWEEPER", True , constants.BLACK)
        self.screen.blit(title_text, (constants.SCREEN_WIDTH//2 - 80, 40))

        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.btn_easy)
        text_easy = self.font.render("1.EASY (9x9)", True, constants.WHITE)
        pos_easy = (self.btn_easy.centerx - text_easy.get_width() //2 , self.btn_easy.centery - text_easy.get_height() //2 )
        self.screen.blit(text_easy, pos_easy)

        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.btn_medium)
        text_medium = self.font.render("2.MEDIUM (12x12)", True, constants.WHITE)
        pos_medium = (self.btn_medium.centerx - text_medium.get_width() // 2, self.btn_medium.centery - text_medium.get_height() //2 )
        self.screen.blit(text_medium, pos_medium)

        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.btn_hard)
        text_hard = self.font.render("3.HARD (14X18)", True, constants.WHITE)
        pos_hard = (self.btn_hard.centerx - text_hard.get_width() // 2, self.btn_hard.centery - text_hard.get_height() //2 )
        self.screen.blit(text_hard, pos_hard )

        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.btn_custom)
        text_custom = self.font.render("4.CUSTOM GAME", True, constants.WHITE)
        pos_custom = (self.btn_custom.centerx - text_custom.get_width() // 2, self.btn_custom.centery - text_custom.get_height() //2 )
        self.screen.blit(text_custom, pos_custom)

        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.btn_lb)
        text_lb = self.font.render("5.LEADERBOARD", True, constants.WHITE)
        pos_lb = (self.btn_lb.centerx - text_lb.get_width() // 2, self.btn_lb.centery - text_lb.get_height() //2 )
        self.screen.blit(text_lb, pos_lb)

    def draw_leaderboard(self):
        # TOP 10 text
        top10_text = self.title_font.render("TOP 12 PLAYERS", True, constants.RED)
        title_rect = top10_text.get_rect(center = (constants.SCREEN_WIDTH//2, 40))
        self.screen.blit(top10_text, title_rect)

        # 3 tab button
        tabs = [
                ("Easy", self.tab_easy_rect),
                ("Medium", self.tab_medium_rect),
                ("Hard", self.tab_hard_rect)
        ] 
        for label, rect in tabs :
            color = constants.LIGHT_GREEN if self.leaderboard_manager.current_tab == label else constants.DARK_GRAY
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            btn_level_text = self.list_font.render(label, True, constants.WHITE)
            text_pos = btn_level_text.get_rect(center= rect.center)
            self.screen.blit(btn_level_text, text_pos)
        
        
        #SEARCH BAR
        search_display = self.list_font.render(f"SEARCH: {self.search_text}", True, constants.BLACK)
        search_rect = search_display.get_rect(center= (constants.SCREEN_WIDTH//2, 160))
        self.screen.blit(search_display, search_rect)

        current_list = self.leaderboard_manager.scores[self.leaderboard_manager.current_tab]

        # RECORDS PARTS
        for i, entry in enumerate(current_list):
                center_x = constants.SCREEN_WIDTH // 2
                y_pos = 200 + (i*35) 
                color = constants.GOLD if i == 0 else constants.DARK_GRAY
                if i == self.found_index:
                    highlight_rect = pygame.Rect(center_x - 120, y_pos, 240, 30)
                    pygame.draw.rect(self.screen, constants.LIGHT_GREEN, highlight_rect)

                rank_text = self.list_font.render(f"{i+1}. "          , True, color)
                name_text = self.list_font.render(f"{entry['name']} ", True, color)
                time_text = self.list_font.render(f"{entry['time']}s ", True, color)

                self.screen.blit(rank_text, (center_x -160, y_pos))
                self.screen.blit(name_text, (center_x - 120, y_pos))
                self.screen.blit(time_text, (center_x + 100, y_pos))


        # BACK BUTTON
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.back_button_rect)
        back_text = self.font.render("BACK", True, constants.RED)
        self.back_button_rect.width = back_text.get_width() +20
        self.back_button_rect.x = constants.SCREEN_WIDTH//2 - self.back_button_rect.width//2
        self.screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5 ))

    def draw_input_name(self):
        # ASK FOR NAME
        prompt_text = self.font.render("ENTER YOUR NAME:", True, constants.BLACK)
        promt_rect = prompt_text.get_rect(center = (constants.SCREEN_WIDTH//2, 115))
        self.screen.blit(prompt_text, promt_rect)

        # RECEIVING NAME
        pygame.draw.rect(self.screen, constants.DARK_GRAY, self.input_rect)
        name_surface = self.font.render(self.player_name, True, constants.WHITE)
        self.input_rect.width =  max(200, name_surface.get_width() + 20 )
        self.input_rect.x = (constants.SCREEN_WIDTH - self.input_rect.width) //2
        text_rect = name_surface.get_rect(center= self.input_rect.center)
        self.screen.blit(name_surface, text_rect)

    def draw_reset_button(self):
        if self.won:
            img_key = "face-win"
        elif self.lost:
            img_key = "face-lose"
        else:
            img_key = "face-playing"

        self.screen.blit(self.images[img_key], self.reset_button_rect)

    def draw_timer(self):
        time_text = self.font.render(f"{self.current_time:03}" ,True, constants.RED)
        time_x = self.x_offset + self.grid_width - time_text.get_width()
        time_bg_rect = pygame.Rect(time_x -5, 15, 60, 35)
        pygame.draw.rect(self.screen, constants.BLACK, time_bg_rect)
        self.screen.blit(time_text, (time_x, 20))

    def draw_mine_counter(self):
        flag_used = self.board.get_flag_count()
        remaining_mines = self.board.mines - flag_used
        mine_count_text = self.font.render(f"{remaining_mines:03}", True, constants.RED)
        mine_bg_rect = pygame.Rect(self.x_offset - 5, 15, 60, 35)
        pygame.draw.rect(self.screen, constants.BLACK, mine_bg_rect)
        self.screen.blit(mine_count_text, (self.x_offset, 20))


    

    












