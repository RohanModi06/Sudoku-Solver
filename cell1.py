import pygame


class Button:
    
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), h_color=(189, 189, 189), function=None, par=None):
        self.surface = pygame.Surface((width, height))
        self.pos = (x,y)
        self.rect = self.surface.get_rect(center=(x+width//2,y+height//2))
        self.text = text
        self.color = color
        self.h_color = h_color
        self.function = function
        self.par = par
        self.highlighted = False
        self.width = width
        self.height = height
        
    def update(self, mouse):
        
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False
            
    def draw(self, window):
        self.surface.fill(self.h_color if self.highlighted else self.color)
        if self.text:
            self.draw_text(self.text)
        window.blit(self.surface, self.pos)
        
    def click(self):
        if self.par:
            self.function(self.par)
        else:
            # print(self.function)
            self.function(call=True)
            
    def draw_text(self, text):
        font = pygame.font.SysFont("arial", 20, bold=1)
        text= font.render(text, False, (0,0,0))
        width, height = text.get_size()
        x = (self.width-width)//2
        y = (self.height-height)//2
        self.surface.blit(text, (x, y))
