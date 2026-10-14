class Piece:
    def __init__(self, has_mine = False):
        self.has_mine = has_mine
        self.is_opened= False
        self.is_flagged = False
        self.num_around = 0 

    def toggle_flag(self):
        if not self.is_opened:
            self.is_flagged = not self.is_flagged

    def open(self):
        if not self.is_flagged:
            self.is_opened = True 

    def set_num_around(self, count):
        self.num_around = count 
        