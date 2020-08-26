#Edited from 
#https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318

import pygame
import random

figurestoshape = [
     "l",
     "⅃",
      "L",
      "T",
     "□",
      "Z",
      "s"
]

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], #line
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],#mirror L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #   L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],# T
        [[1, 2, 5, 6]],#square
        [[0,1,5,6], [2,6,5,9]],#z
        [[2,1,5,4], [0,4,5,9]]#opposite z
        
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
    

class Tetris:
     level = 2
     score = 0
     state = "pause"
     field = []
     height = 0
     width = 0
     x = 100 #not working
     y = 60
     zoom = 20
     figure = None
     
     def __init__(self, height, width):
          self.height = height
          self.width = width
          for i in range(height):
               new_line = []
               for j in range(width):
                    new_line.append(0)
               self.field.append(new_line)
            
     def new_figure(self):
          self.figure = Figure(round(self.width/2)-2, 0)
        
     def intersects(self):
          intersection = False
          for i in range(4):
               for j in range(4):
                    if i * 4 + j in self.figure.image():
                         if i + self.figure.y > self.height - 1 or \
                              j + self.figure.x > self.width - 1 or \
                              j + self.figure.x < 0 or \
                              self.field[i + self.figure.y][j + self.figure.x] > 0:
                              intersection = True
          return intersection
        
     def freeze(self):
          for i in range(4):
               for j in range(4):
                    if i * 4 + j in self.figure.image():
                         self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
          self.break_lines()
          self.new_figure()
          if self.intersects():
               game.state = "gameover"
          
     def break_lines(self):
          lines = 0
          for i in range(1, self.height):
               zeros = 0
               for j in range(self.width):
                    if self.field[i][j] == 0:
                         zeros += 1
               if zeros == 0:
                    lines += 1
                    for i1 in range(i, 1, -1):
                         for j in range(self.width):
                             self.field[i1][j] = self.field[i1 - 1][j]
          self.score += lines ** 2
     
     def go_space(self):
          if  self.state != "pause":
               while not self.intersects():
                    self.figure.y += 1
               self.figure.y -= 1
               self.freeze()

     def go_down(self):
          if self.state != "pause":
               self.figure.y += 1
          if self.intersects():
               self.figure.y -= 1
               self.freeze()

     def go_side(self, dx):
          if  self.state != "pause":
               old_x = self.figure.x
               self.figure.x += dx
          if self.intersects():
               self.figure.x = old_x

     def rotate(self):
        
          if  self.state != "pause":
               old_rotation = self.figure.rotation
               self.figure.rotate()
          if self.intersects():
               self.figure.rotation = old_rotation

class Text:
    #centering text
    def __init__(self, text, x,y, color, ftype, fsize):
        self.x = x #Horizontal center 
        self.y = y #Vertical center 
        
        font = pygame.font.SysFont(ftype, fsize)
        self.txt = font.render(text, True, color)
        self.size = font.size(text) #(width, height)
    # Draw Method
    def Draw(self, screen):
        drawX = self.x - (self.size[0] / 2)
        drawY = self.y - (self.size[1] / 2)
        
        coords = (drawX, drawY)
        screen.blit(self.txt, coords)
        
        
               
# font = pygame.font.SysFont('Calibri', 25, True, False)
# text_quit = font.render("Press Q to quit", True, BLACK)
# font1 = pygame.font.SysFont('Calibri', 65, True, False)
# text_pause = font1.render("Press P to play", True, (255, 0, 0))

     
     
     

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)


fps = 30
gamesize = []
while len(gamesize) < 2 or (gamesize[0] and gamesize[1] <= 8):
     gamesize.clear()
     gamesize.append(int(input("Input game board height:")))
     gamesize.append(int(input("Input game board width:")))

game = Tetris(int(gamesize[0]),int(gamesize[1]))

size = (int(1.5*game.zoom*(gamesize[1])), int(1.5*game.zoom*(gamesize[0])))
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

game.x, game.y = int(screen.get_size()[0]*0.25 - game.zoom*2), int(screen.get_size()[1]*0.25 - game.zoom*2) 
     #use to center board
pygame.display.set_caption("Tetris")
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()


text_pause = Text("Press P to play", screen.get_size()[0]*0.55, \
          screen.get_size()[1]*0.5, (255,0,0), 'Calibri', 65)
text_quit = Text("Press Q to quit", int(4*game.x),game.y-10, BLACK,\
          'Calibri', 25)
text_game_over = Text("Game Over", screen.get_size()[0]*0.5, \
        screen.get_size()[1]*0.5, (255,125,0), 'Calibri', 65)
text_game_over1 = Text("Press R to replay", screen.get_size()[0]*0.52, \
        screen.get_size()[1]*0.6, (255,20,0), 'Calibri', 65)



counter = 0
pressing_down = False
pressing_left = False
pressing_right = False

while not done:
     if game.figure is None:
        game.new_figure()
     counter += 1
     if counter > 100000:
          counter = 0
          
     
     if counter % (fps // game.level // 2) == 0 or pressing_down:
          if game.state == "start":
               game.go_down()
     if pressing_left:
          game.go_side(-1)
          pygame.time.delay(50)
     if pressing_right:
          game.go_side(1)
          pygame.time.delay(50)

     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               done = True
          if event.type == pygame.KEYDOWN :
               
               if event.key == pygame.K_p:
                    if game.state == "start":
                         game.state = "pause"                      
                    elif game.state == "pause":
                         game.state = "start"
                         
               if event.key == pygame.K_UP:
                    game.rotate()
               if event.key == pygame.K_DOWN:
                    pressing_down = True
               if event.key == pygame.K_LEFT and not pressing_right:
                    pressing_left = True
                    pygame.time.delay(100)
                    #game.go_side(-1)
               if event.key == pygame.K_RIGHT and not pressing_left:
                    pressing_right = True
                    pygame.time.delay(100)
                    #game.go_side(1)
               if event.key == pygame.K_SPACE and game.state == "start":
                    game.go_space()
               if event.key == pygame.K_q:
                    done = True
               if event.key == pygame.K_r :
                    game.__init__(int(gamesize[1]), int(gamesize[0]))
          if event.type == pygame.VIDEORESIZE:
               game.x = int(event.w/4)
               game.y = int(event.h/8)
               screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
               screen.fill(WHITE)
               text_pause = Text("Press P to play", screen.get_size()[0]*0.55, \
                         screen.get_size()[1]*0.5, (255,0,0), 'Calibri', 65)
               text_quit = Text("Press Q to quit", int(4*game.x),game.y-10, BLACK,\
                         'Calibri', 25)
               text_score = Text(("Score: " + str(game.score)), game.x+30, game.y-10, \
                         BLACK ,'Calibri', 25)
               text_game_over = Text("Game Over", screen.get_size()[0]*0.27, \
                    screen.get_size()[1]*0.5, (255,125,0), 'Calibri', 20)
               text_game_over1 = Text("Press ESC to replay", screen.get_size()[0]*0.27, \
                    screen.get_size()[1]*0.5, (255,215,0), 'Calibri', 20)


               

     if event.type == pygame.KEYUP:
               if event.key == pygame.K_DOWN:
                    pressing_down = False
               if event.key == pygame.K_LEFT:
                    pressing_left = False
               if event.key == pygame.K_RIGHT:
                    pressing_right = False

     screen.fill(WHITE)
     for i in range(game.height):
          for j in range(game.width):
               pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
               if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                   [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

     if game.figure is not None and game.state != "gameover":
          for i in range(4):
               for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                         pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.zoom * (j + game.figure.x) + 1,
                                        game.y + game.zoom * (i + game.figure.y) + 1,
                                        game.zoom - 2, game.zoom - 2])
                                        
     #print(game.figure.figures[game.figure.type])
     
     if(game.state == "pause"):
          text_pause.Draw(screen)
     
     text_next = Text(("Next shape: "), screen.get_size()[0]/2, game.y -40, \
          BLACK, 'Calibri', 20)
     text_next_object = Text(figurestoshape[game.figure.type], screen.get_size()[0]/2, game.y -25, \
          BLACK, 'Calibri', 35)
     text_next.Draw(screen)
     text_next_object.Draw(screen)
     #print(game.figure.type)
     
     text_score = Text(("Score: " + str(game.score)), game.x+30, game.y-10, \
          BLACK ,'Calibri', 25)
     text_score.Draw(screen)
     text_quit.Draw(screen)

     if game.state == "gameover":
          text_game_over.Draw(screen)
          text_game_over1.Draw(screen)
          
          
     pygame.display.flip()
     clock.tick(fps)

pygame.quit()



