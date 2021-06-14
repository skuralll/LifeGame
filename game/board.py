from game.cell import Cell


class Board:
    # 行列の高さと幅
    ROW = 32
    COL = 32

    def __init__(self, game):
        self.game = game
        self.cells = []
        for row in range(self.ROW):
            rowcells = []
            for col in range(self.COL):
                rowcells.append(Cell(self, row, col))
            self.cells.append(rowcells)

    def step(self):
        for row in range(self.ROW):
            for col in range(self.COL):
                self.cells[row][col].advance()

    def print_cells(self):
        for row in range(self.ROW):
            for col in range(self.COL):
                print("●" if self.cells[row][col].isAlive() else "○", end="")
            print("")

    def getAround(self, x: int, y: int):
        around = []
        minX = max(x - 1, 0)
        minY = max(y - 1, 0)
        maxX = min(x + 1, self.ROW - 1)
        maxY = min(y + 1, self.COL - 1)
        for row in range(minX, maxX + 1):
            for col in range(minY, maxY + 1):
                if not (x == row and y == col):
                    around.append(self.cells[row][col])
        return around

    def countAroundAliveAt(self, x: int, y: int):
        count = 0
        for cell in self.getAround(x, y):
            if cell.isAlive():
                count += 1
        return count

    def isAliveAt(self, x: int, y: int):
        return self.cells[x][y].isAlive()

    def setAliveAt(self, x: int, y: int, alive: bool):
        self.cells[x][y].setAlive(alive)

    def reverseAliveAt(self, x: int, y: int):
        cell = self.cells[x][y]
        cell.setAlive(not cell.isAlive())

    def setNextStatAt(self, x: int, y: int, alive: bool):
        self.cells[x][y].setNextStat(alive)
