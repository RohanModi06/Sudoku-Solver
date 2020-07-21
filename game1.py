import pygame, sys
import requests
from bs4 import BeautifulSoup
from param import *
from cell1 import *


class Sudoku:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.playing = True
        self.grid= testBoard1
        self.selected = None
        self.mouse_pos = None
        self.state = "game"
        self.finished = False
        self.cell_changed = False
        self.play_buttons = []
        self.locked_cells= []
        self.incorrect_cells = []
        self.empty_cells = []
        self.font = pygame.font.SysFont("arial", cellSize//2)
        self.Puzzle("1")
        self.load()
        
        
        
        

    def run(self):
        while self.playing:
            if self.state == "game":
                self.game_event()
                self.game_update()
                self.game_draw()
            
        pygame.quit()
        sys.exit()
            
    def game_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.OnGrid()
                if selected:
                    self.selected=selected
                    # print(self.selected)
                else:
                    # print("not on board")
                    self.selected = None
                    for button in self.play_buttons:
                        if button.highlighted:
                            button.click()
                    
            if event.type == pygame.KEYDOWN:
                if self.selected!=None and list(self.selected) not in self.locked_cells:
                    
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cell_changed = True
                        
                
    def game_update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for i in self.play_buttons:
            i.update(self.mouse_pos)
        
        if self.cell_changed:
            self.incorrect_cells= []
            self.check_cells()
            # if self.filled():
                
            #     if len(self.incorrect_cells) == 0:
            #         self.finished = True
        
    
    def game_draw(self):
        self.window.fill(WHITE)
        for i in self.play_buttons:
            i.draw(self.window)
        if self.selected:
            self.drawCell(self.window,self.selected)
        self.draw_cells(self.window, self.incorrect_cells, INCORRECTCELLCOLOUR)
        if self.finished:
            self.draw_cells(self.window, self.empty_cells, GREEN)
        self.draw_cells(self.window, self.locked_cells, LOCKEDCELLCOLOUR)
        self.draw_num(self.window)
        
        self.draw_grid(self.window)
        pygame.display.update()
        self.cell_changed = False
      
    def draw_cells(self, window, cells, color):
        
        for cell in cells:
            pygame.draw.rect(window, color, (gridPos[0]+ cell[0]*cellSize,gridPos[1]+cell[1]*cellSize, cellSize, cellSize))  
             
    
    def drawCell(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE, (gridPos[0]+ pos[0]*cellSize,gridPos[1]+pos[1]*cellSize, cellSize, cellSize))
    
    def draw_grid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH-150, HEIGHT-150), 3)
        for i in range(9):
            breadth=3 if i%3==0 else 1;
            pygame.draw.line(window, BLACK, (gridPos[0] + i*cellSize, gridPos[1]), (gridPos[0] + i*cellSize, gridPos[1]+450), breadth)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + i*cellSize), (gridPos[0]+450, gridPos[1] + i*cellSize), breadth)  
            
    def OnGrid(self):
        if self.mouse_pos[0]<gridPos[0] or self.mouse_pos[1]<gridPos[1] or self.mouse_pos[0]> gridPos[0] + gridSize or self.mouse_pos[1]>gridPos[1]+gridSize:
            return False
        
        else:
            return ((self.mouse_pos[0]-gridPos[0])//cellSize, (self.mouse_pos[1]-gridPos[1])//cellSize)
        
    
    def load_buttons(self):
        self.play_buttons.append(Button(  20, 40, WIDTH//7, 40,
                                            function=self.check_cells,
                                            color=(27,142,207),
                                            text="Check"))
        self.play_buttons.append(Button(  140, 40, WIDTH//7, 40,
                                            color=(117,172,112),
                                            function=self.Puzzle,
                                            par="1",
                                            text="Easy"))
        self.play_buttons.append(Button(  WIDTH//2-(WIDTH//7)//2, 40, WIDTH//7, 40,
                                            color=(204,197,110),
                                            function=self.Puzzle,
                                            par="2",
                                            text="Medium"))
        self.play_buttons.append(Button( 380, 40, WIDTH//7, 40,
                                            color=(199,129,48),
                                            function=self.Puzzle,
                                            par="3",
                                            text="Hard"))
        self.play_buttons.append(Button(  500, 40, WIDTH//7, 40,
                                            color=(207,68,68),
                                            function=self.Puzzle,
                                            par="4",
                                            text="Evil"))
        
    def draw_text(self,window, text, pos, color=BLACK):
        font = self.font.render(text, False, color)
        font_height = font.get_height()
        font_width = font.get_width()
        pos[0]+= (cellSize - font_width)//2
        pos[1]+= (cellSize - font_height)//2
        window.blit(font, pos)
        
    def draw_num(self, window):
        for rind, row in enumerate(self.grid):
            for cind, num in enumerate(row):
                if num!=0:
                    pos = [cind*cellSize+gridPos[0], rind*cellSize+gridPos[1]]
                    self.draw_text(window, str(num), pos)
                    
                    
    def filled(self):
        for row in self.grid:
            for num in row:
                if num==0:
                    return False
        return True
                    
    def check_cells(self, call=False):
        self.check_rows()
        self.check_columns()
        self.check_box()
        if call:
            if self.filled():
                if len(self.incorrect_cells) == 0:
                    self.finished = True
                    
        
        
    def check_box(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                # print("re-setting possibles")
                for i in range(3):
                    for j in range(3):
                        # print(x*3+i, y*3+j)
                        xidx = x*3+i
                        yidx = y*3+j
                        if self.grid[yidx][xidx]==0:
                            continue;
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                                self.incorrect_cells.append([xidx, yidx])
                                # print(self.incorrect_cells)
                            if [xidx, yidx] in self.locked_cells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.locked_cells:
                                            self.incorrect_cells.append([xidx2, yidx2])
                                            # print(self.incorrect_cells)

    def check_rows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                if self.grid[yidx][xidx]==0:
                    continue;
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                        # print(self.incorrect_cells)
                    if [xidx, yidx] in self.locked_cells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.locked_cells:
                                self.incorrect_cells.append([k, yidx])
                                # print(self.incorrect_cells)


    def check_columns(self):
        for xidx in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx]==0:
                    continue;
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.locked_cells and [xidx, yidx] not in self.incorrect_cells:
                        self.incorrect_cells.append([xidx, yidx])
                        # print(self.incorrect_cells)
                    if [xidx, yidx] in self.locked_cells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.locked_cells:
                                self.incorrect_cells.append([xidx, k])
                                # print(self.incorrect_cells)


    def Puzzle(self, diff):
        # diff= 1-4
        self.finished = False
        source_doc = requests.get("https://nine.websudoku.com/?level={}".format(diff)).content
        bsp = BeautifulSoup(source_doc)
        
        ids = ["f"+str(i)+str(j) for i in range(9) for j in range(9) ]
        
        puzzle= []
        for i in ids:
            puzzle.append(bsp.find('input', id=i))
            
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(puzzle):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()
        # return board
        
                    
    def load(self):
        self.play_buttons= []
        self.load_buttons()
        self.locked_cells = []
        self.incorrect_cells= []
        self.finished = False
        for yind, row in enumerate(self.grid):
            for xind, num in enumerate(row):
                if num!=0:
                    self.locked_cells.append([xind, yind])
                else:
                    self.empty_cells.append([xind, yind])
                    
                    
        # print(self.locked_cells)
        
    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False