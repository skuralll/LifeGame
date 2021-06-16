from gui.gui import GUI
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
                    count = self.board.countAroundAliveAt(row, col)
                    if count == 3:
                        # 誕生
                        self.board.setColorDataAt(row, col, self.board.getAroundAverageColor(row, col))
                        self.board.setNextStatAt(row, col, True)
                    else:
                        self.board.setNextStatAt(row, col, False)
        self.board.step()
