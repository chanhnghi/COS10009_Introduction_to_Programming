import constants
from piece import Piece
import random 

class Board:
    def __init__(self, rows = constants.ROWS, cols = constants.COLS, mines = constants.MINES):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = []
        self.create_grid()

    def create_grid(self):
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                piece = Piece()
                row.append(piece)
            self.grid.append(row)   

    def place_mines(self, ex_row, ex_col):
        num_of_mines = 0
        while num_of_mines < self.mines:
            row = random.randint(0, self.rows -1)
            col = random.randint(0, self.cols -1)
            target_piece = self.grid[row][col]
            if not target_piece.has_mine and (row, col) != (ex_row, ex_col) :
                target_piece.has_mine = True  
                num_of_mines += 1

    def calculate_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                piece =  self.grid[r][c]

                if piece.has_mine :
                    continue
                mine_count = 0 
                for i in range(-1,2):
                    for j in range(-1,2):
                        nr, nc = r+i, c+j
                        if 0 <= nc < self.cols and 0 <= nr <self.rows:
                            if self.grid[nr][nc].has_mine:
                                mine_count += 1
                piece.set_num_around(mine_count)

    def get_flag_count(self):
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_flagged :
                    count += 1
        return count 

    def print_board_console(self):
        for r in range(self.rows):
            for c in range(self.cols):
                piece = self.grid[r][c]
                if piece.has_mine:
                    print("x", end=" ")
                else:
                    print(piece.num_around, end=" ")
            print()

if __name__ == "__main__":
    board = Board()
    board.place_mines(0,0)
    board.calculate_neighbors()
    print("---MINESWEEPER BOARD LOGIC ---")
    board.print_board_console() 


                