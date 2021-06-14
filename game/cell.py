class Cell:

    def __init__(self, board, x: int, y: int):
        self.board = board
        self.x = x
        self.y = y
        self.alive = False
        self.nextStat = False

    def isAlive(self):
        return self.alive

    def setAlive(self, alive: bool):
        self.alive = alive
        self.board.game.onCellChange(self.x, self.y)

    def setNextStat(self, alive: bool):
        self.nextStat = alive

    def advance(self):
        self.setAlive(self.nextStat)
        self.setNextStat(self.nextStat)
