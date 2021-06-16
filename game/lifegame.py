import copy
import tkinter as tk
from game.board import Board


class LifeGame:

    def __init__(self):
        self.board = Board(self)
        self.gui = GUI(self)

    def run(self):
        self.gui.run()

    def onCellChange(self, row: int, col: int):
        self.gui.onCellChange(row, col)

    def step(self):
        for row in range(self.board.ROW):
            for col in range(self.board.COL):
                if self.board.isAliveAt(row, col):
                    count = self.board.countAroundAliveAt(row, col)
                    self.board.setNextStatAt(row, col, count == 2 or count == 3)
                else:
                    self.board.setNextStatAt(row, col, self.board.countAroundAliveAt(row, col) == 3)
        self.board.step()


# GUI

class GUI:
    # Cell
    CELL_SIZE = 16
    CELL_WIDTH = 1
    # UI
    BLANK_WIDTH = 256
    BUTTON_AUTORUN_TEXT_OFF = 'オートラン'
    BUTTON_AUTORUN_TEXT_ON = 'オートラン(停止)'

    def __init__(self, lifegame):
        self.app = tk.Tk()
        self.lifegame = lifegame

        # GUI
        # Setting
        width = self.lifegame.board.ROW * self.CELL_SIZE + self.CELL_WIDTH
        height = self.lifegame.board.COL * self.CELL_SIZE + self.CELL_WIDTH
        self.app.title('LifeGame')
        self.app.geometry(str(width + self.BLANK_WIDTH) + 'x' + str(height))
        self.app.resizable(width=False, height=False)
        # UIs
        self.stepButton = tk.Button(self.app, text="進む", width=15, height=1, command=self.lifegame.step)
        self.stepButton.place(x=width, y=0)
        self.autoMode = False
        self.autoMode_period = 333
        self.autoButton = tk.Button(self.app, text=self.BUTTON_AUTORUN_TEXT_OFF, width=15, height=1, command=self.clickAutoButton)
        self.autoButton.place(x=width, y=40)
        self.SpeedScale = tk.Scale(self.app, from_=1, to=10, orient=tk.HORIZONTAL, command=self.onSpeedScaleChanged)
        self.SpeedScale.place(x=width + 128, y=28)
        # Canvas
        self.canvas = tk.Canvas(self.app, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0)
        # Draw Cells
        for row in range(self.lifegame.board.ROW):
            for col in range(self.lifegame.board.COL):
                x = self.CELL_SIZE * row
                y = self.CELL_SIZE * col
                cell = self.canvas.create_rectangle(x, y, x + self.CELL_SIZE, y + self.CELL_SIZE, width=self.CELL_WIDTH,
                                                    fill="white",
                                                    tag=self.colmToTag(row, col))
        self.canvas.bind('<Button-1>', self.click_canvas)

    def run(self):
        self.app.mainloop()

    def click_canvas(self, event):
        # クリックしたセルのタグを求める
        row = int(event.x / self.CELL_SIZE)
        col = int(event.y / self.CELL_SIZE)
        if row >= self.lifegame.board.ROW: row = self.lifegame.board.ROW
        if col >= self.lifegame.board.COL: col = self.lifegame.board.COL
        celltag = self.colmToTag(row, col)

        self.lifegame.board.reverseAliveAt(row, col)

    def onCellChange(self, row: int, col: int):
        fill = "red" if self.lifegame.board.cells[row][col].isAlive() else "white"
        self.canvas.itemconfig(self.colmToTag(row, col), fill=fill)

    # callbackTask
    def autoStep(self):
        if self.autoMode:
            self.lifegame.step()
            self.app.after(self.autoMode_period, self.autoStep)

    def colmToTag(self, row: int, col: int):
        return 'cell' + str(row) + ':' + str(col)

    # UIs
    # AutoButton
    def clickAutoButton(self):
        self.autoMode = not self.autoMode
        if self.autoMode:
            self.autoStep()
            self.autoButton.configure(text=self.BUTTON_AUTORUN_TEXT_ON)
        else:
            self.autoButton.configure(text=self.BUTTON_AUTORUN_TEXT_OFF)
    # SpeedScale
    def onSpeedScaleChanged(self, scale_val):
        self.autoMode_period = int(1000 / int(scale_val))
