import random
import numpy as np
import tkinter

class Minesweeper:
    def __init__(self, height, width, number_of_mines):
        self.height = height
        self.width = width
        self.number_of_mines = number_of_mines
        self.evaluated_cells = []

    def new_game(self):
        self.grid = np.zeros((self.height, self.width))
        self.hidden_grid = np.zeros((self.height, self.width))
        self.hidden_grid = self.hidden_grid - 33
        for _ in range(self.number_of_mines):
            x = random.randrange(0,self.height)
            y = random.randrange(0,self.width)
            self.grid[x,y] = 10

        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x, y] != 10:
                    mine_counter = 0
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < self.height and 0 <= new_y < self.width and self.grid[new_x, new_y] == 10:
                            mine_counter += 1
                    self.grid[x, y] = mine_counter


    def get_grid(self):
        return self.hidden_grid
    
    def get_remaining_mines(self):
        unexplored_grid = self.hidden_grid == -33
        number_of_unexplored_cells = unexplored_grid.cumsum()[-1]
        if (number_of_unexplored_cells == self.number_of_mines):
            print("You win!")
            exit()
        return number_of_unexplored_cells

    
    def input_xy(self, x, y):
        if self.grid[x, y] != 10:
            return self.compute_input(x,y)
        print("Game over")
        exit()
        return
            
    def compute_input(self, x, y):
        cells_to_evaluate = [(x,y)]
        while cells_to_evaluate:
            x, y = cells_to_evaluate.pop()
            value = self.grid[x,y]
            
            if value == 0:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.height and 0 <= new_y < self.width and ((new_x, new_y) not in self.evaluated_cells) and ((new_x, new_y) not in cells_to_evaluate):
                        cells_to_evaluate.append((new_x, new_y))

            self.hidden_grid[x,y] = value
            self.evaluated_cells.append((x,y))

        return self.hidden_grid

def update_canvas(tk, grid):
    for x in range(height):
        for y in range(width):
            if grid[x,y] == -33:
                color = "purple"
            else:
                color = "white"
            tk.create_rectangle(y*rect_size,x*rect_size,y*rect_size+rect_size,x*rect_size+rect_size,activefill=color, fill=color)
            if grid[x,y] != -33 and grid[x,y] != 0:
                tk.create_text(y*rect_size+(rect_size/2),x*rect_size+(rect_size/2),text=str(int(grid[x,y])))
            tk.pack()

def get_click(a):
    x = int(a.y / 20)
    y = int(a.x / 20)
    grid = game.input_xy(x,y)
    update_canvas(tk, grid)
    game.get_remaining_mines()

height = 20
width = 20
n_mines = 10
rect_size = 20
game = Minesweeper(height,width,n_mines)
game.new_game()
grid = game.get_grid()
root = tkinter.Tk()
root.title("Minesweeper")
tk = tkinter.Canvas(root, width=(width*rect_size), height=height*rect_size)
tk.bind("<Button-1>", func=get_click)
update_canvas(tk, grid)
root.mainloop()
# while(True):
#     x = int(input("Input X:"))
#     y = int(input("Input Y:"))
#     grid = game.input_xy(x,y)
#     update_canvas(tk, grid)
#     tk.update()
