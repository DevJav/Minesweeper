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
                if self.grid[x,y] != 10:
                    mine_counter = 0
                    if x > 0 and self.grid[x-1,y] == 10:
                        mine_counter += 1
                    if x < self.height - 1 and self.grid[x+1,y] == 10:
                        mine_counter += 1
                    if y > 0 and self.grid[x,y-1] == 10:
                        mine_counter += 1
                    if y < self.width - 1 and self.grid[x,y+1] == 10:
                        mine_counter += 1

                    if x > 0 and y < self.width - 1 and self.grid[x-1,y+1] == 10:
                        mine_counter += 1
                    if x < self.height - 1 and y < self.width - 1 and self.grid[x+1,y+1] == 10:
                        mine_counter += 1
                    if x > 0 and y > 0 and self.grid[x-1,y-1] == 10:
                        mine_counter += 1
                    if x < self.height - 1 and y > 0 and self.grid[x+1,y-1] == 10:
                        mine_counter += 1

                    self.grid[x,y] = mine_counter

        print(self.grid)

    def get_grid(self):
        return self.hidden_grid
    
    def get_remaining_mines(self):
        unexplored_grid = self.hidden_grid == -33
        number_of_unexplored_cells = unexplored_grid.cumsum()[-1] == self.number_of_mines
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
        self.evaluated_cells.append((x,y))
        value = self.grid[x,y]
        if value == 0:
            if x < self.height - 1 and ((x+1,y) not in self.evaluated_cells):
                self.input_xy(x+1,y)
            if x > 0 and ((x-1,y) not in self.evaluated_cells):
                self.input_xy(x-1,y)
            if y < self.width - 1 and ((x,y+1) not in self.evaluated_cells):
                self.input_xy(x,y+1)
            if y > 0 and ((x,y-1) not in self.evaluated_cells):
                self.input_xy(x,y-1)
            if x > 0 and y < self.width - 1 and (x-1,y+1) not in self.evaluated_cells:
                self.input_xy(x-1,y+1)
            if x < self.height - 1 and y < self.width - 1 and (x+1,y+1) not in self.evaluated_cells:
                self.input_xy(x+1,y+1)
            if x > 0 and y > 0 and (x-1,y-1) not in self.evaluated_cells:
                self.input_xy(x-1,y-1)
            if x < self.height - 1 and y > 0 and (x+1,y-1) not in self.evaluated_cells:
                self.input_xy(x+1,y-1)
        self.hidden_grid[x,y] = value

        return self.hidden_grid

def update_canvas(tk, grid):
    for x in range(height):
        for y in range(width):
            if grid[x,y] == -33:
                color = "black"
            else:
                color = "white"
            tk.create_rectangle(y*20,x*20,y*20+20,x*20+20,activefill=color, fill=color)
            if grid[x,y] != -33 and grid[x,y] != 0:
                tk.create_text(y*20+10,x*20+10,text=str(int(grid[x,y])))
            tk.pack()

def get_click(a):
    x = int(a.y / 20)
    y = int(a.x / 20)
    grid = game.input_xy(x,y)
    update_canvas(tk, grid)
    game.get_remaining_mines()

height = 30
width = 20
n_mines = 30
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
