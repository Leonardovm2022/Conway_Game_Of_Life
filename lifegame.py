import tkinter as tk
import numpy as np

class GameOfLife(tk.Tk):
    def __init__(self, size=20):
        super().__init__()
        self.size = size
        self.title("Game of Life")
        self.grid = np.zeros((self.size, self.size), dtype=bool)
        self.canvas = tk.Canvas(self, width=20*self.size, height=20*self.size)
        self.canvas.pack()
        self.rectangles = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                rect = self.canvas.create_rectangle(20*j, 20*i, 20*(j+1), 20*(i+1), fill="white")
                row.append(rect)
                self.canvas.tag_bind(rect, "<Button-1>", lambda event, row=i, col=j: self.toggle_cell(event, row, col))
            self.rectangles.append(row)
        self.running = False
        self.canvas.bind("<Button-3>", self.start_game)

    def toggle_cell(self, event, row, col):
        self.grid[row][col] = not self.grid[row][col]
        if self.grid[row][col]:
            self.canvas.itemconfig(self.rectangles[row][col], fill="black")
        else:
            self.canvas.itemconfig(self.rectangles[row][col], fill="white")

    def start_game(self, event):
        if not self.running:
            self.running = True
            self.update()
        else:
            self.running = False

    def update(self):
        if not self.running:
            return
        new_grid = np.zeros((self.size, self.size), dtype=bool)
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for ii in range(max(0, i-1), min(self.size, i+2)):
                    for jj in range(max(0, j-1), min(self.size, j+2)):
                        if ii == i and jj == j:
                            continue
                        if self.grid[ii][jj]:
                            count += 1
                if self.grid[i][j]:
                    if count == 2 or count == 3:
                        new_grid[i][j] = True
                else:
                    if count == 3:
                        new_grid[i][j] = True
        self.grid = new_grid
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j]:
                    self.canvas.itemconfig(self.rectangles[i][j], fill="black")
                else:
                    self.canvas.itemconfig(self.rectangles[i][j], fill="white")
        self.after(100, self.update)

if __name__ == "__main__":
    game = GameOfLife()
    game.mainloop()
