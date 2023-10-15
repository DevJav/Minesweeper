import itertools
import random
import numpy as np
import tkinter

class Minesweeper:
    def __init__(self, height, width, number_of_mines):
        self.height = height
        self.width = width
        self.number_of_mines = number_of_mines
        self.evaluated_cells = []
        self.new_game()

    def new_game(self):
        self.grid = np.zeros((self.height, self.width))
        self.hidden_grid = np.zeros((self.height, self.width))
        self.hidden_grid = self.hidden_grid - 33
        for _ in range(self.number_of_mines):
            row = random.randrange(0,self.height)
            col = random.randrange(0,self.width)
            self.grid[row, col] = 10

        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row, col] != 10:
                    mine_counter = 0
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
                    for dcol, drow in directions:
                        new_row, new_col = row + dcol, col + drow
                        if 0 <= new_row < self.height and 0 <= new_col < self.width and self.grid[new_row, new_col] == 10:
                            mine_counter += 1
                    self.grid[row, col] = mine_counter


    def get_grid(self):
        return self.hidden_grid
    
    def get_remaining_mines(self):
        unexplored_grid = self.hidden_grid == -33
        number_of_unexplored_cells = unexplored_grid.cumsum()[-1]
        if (number_of_unexplored_cells == self.number_of_mines):
            print("You win!")
            exit()
        return number_of_unexplored_cells

    def input_row_col(self, row, col):
        if self.grid[row, col] != 10:
            return self.compute_input(row, col)
        print("You loose!")
        exit()
            
    def compute_input(self, row, col):
        cells_to_evaluate = [(row, col)]
        while cells_to_evaluate:
            row, col = cells_to_evaluate.pop()
            value = self.grid[row,col]
            
            if value == 0:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
                for drow, dcol in directions:
                    new_row, new_col = row + drow, col + dcol
                    if 0 <= new_row < self.height and 0 <= new_col < self.width and ((new_row, new_col) not in self.evaluated_cells) and ((new_row, new_col) not in cells_to_evaluate):
                        cells_to_evaluate.append((new_row, new_col))

            self.hidden_grid[row, col] = value
            self.evaluated_cells.append((row, col))

        return self.hidden_grid

def update_canvas(tk, grid):
    for row, col in itertools.product(range(height), range(width)):
        color = "#AA4367" if grid[row, col] == -33 else "black"
        tk.create_rectangle(col*rect_size, row*rect_size,col*rect_size+rect_size, row*rect_size+rect_size, fill=color, outline="")
        if grid[row, col] not in [-33, 0]:
            tk.create_text(col * rect_size + (rect_size / 2), row * rect_size + (rect_size / 2), text = str(int(grid[row, col])), font=("Arial", 15), fill="white")
        tk.pack()

def get_click(a):
    x = int(a.y / rect_size)
    y = int(a.x / rect_size)
    grid = game.input_row_col(x,y)
    update_canvas(tk, grid)
    game.get_remaining_mines()

height = 20
width = 20
n_mines = 40
rect_size = 40

game = Minesweeper(height,width,n_mines)
game.new_game()
grid = game.get_grid()
root = tkinter.Tk()
root.title("Minesweeper")
tk = tkinter.Canvas(root, width=(width*rect_size), height=height*rect_size)
tk.bind("<Button-1>", func=get_click)
update_canvas(tk, grid)
root.mainloop()
