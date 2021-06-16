class Cell:

    def __init__(self, board, x: int, y: int, color=None):
        if color is None:
            color = [255, 0, 0]
        self.board = board
        self.x = x
        self.y = y
        self.color = [0, 0, 0] if color is None else color
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

    def setColorData(self, color):
        self.color = [min(255, max(0, int(color[0]))), min(255, max(0, int(color[1]))), min(255, max(0, int(color[2])))]

    def getColorData(self):
        return self.color

    def getColorCode(self):
        return '#%02X%02X%02X' % (self.color[0], self.color[1], self.color[2])
