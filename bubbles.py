import math, pygame, sys, os, copy, time, random
import pygame.gfxdraw
from pygame.locals import *

## Constants, yo ##
FPS          = 60  #frames per second
WINDOWWIDTH  = 640  #(pixel)
WINDOWHEIGHT = 480  #(pixel)
TEXTHEIGHT   = 20  #the size of the score
BUBBLERADIUS = 20  #the radius of each bubble
BUBBLEWIDTH  = BUBBLERADIUS * 2  #the diameter of each bubble
BUBBLEYADJUST = 5  
STARTX = WINDOWWIDTH / 2  #the x axis of the arrow(the position of the middle point of the base of the triangle in the arrow)
STARTY = WINDOWHEIGHT -50  #the y axis of the arrow(the position of the middle point of the base of the triangle in the arrow)
ARRAYWIDTH = 16  #the width of the bubble arrow
ARRAYHEIGHT = 14  #the height of the bubble arrow

RIGHT = 'right'
LEFT  = 'left'
BLANK = '.'

##### COLORS #####
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)

BGCOLOR    = WHITE ##the color of the background 
COLORLIST = [RED, GREEN, BLUE, YELLOW]
     
class Bubble(pygame.sprite.Sprite):
    oddeven = 1; #'1' stands for even and '0' stands for odd
    def __init__(self, color, row=0, column=0,oddeven = 0):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.rect.centerx = STARTX
        self.rect.centery = STARTY
        self.speed = 10 # pixel per frame
        self.color = color
        self.radius = BUBBLERADIUS
        self.angle = 0
        self.row = row
        self.column = column
        self.oddeven = oddeven;


        
    def update(self): # update the top left corner of the rect 30x30
        # update the position of the bubble in the new frame
        if self.angle == 90: #'angle = 90' stands for the arrow points to the upside
            xmove = 0
            ymove = self.speed * -1
        elif self.angle < 90: #'angle = 0' stands for the arrow points to the rightside
            xmove = self.xcalculate(self.angle)
            ymove = self.ycalculate(self.angle)
        elif self.angle > 90: #'angle = 180' stands for the arrow points to the leftside
            xmove = self.xcalculate(180 - self.angle) * -1
            ymove = self.ycalculate(180 - self.angle)
        self.rect.x += xmove
        self.rect.y += ymove


    def draw(self): # draw the bubbles
        pygame.gfxdraw.filled_circle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, self.color) #draw the bubble with the center <centerx,centery>, r = radius and color = color 
        pygame.gfxdraw.circle(DISPLAYSURF, self.rect.centerx, self.rect.centery, self.radius, GRAY) #draw the contour line of the bubble
        

    # calculate the position of the bubbles ini the next frame
    def xcalculate(self, angle):     
        radians = math.radians(angle)        
        xmove = math.cos(radians)*(self.speed)
        return xmove

    def ycalculate(self, angle):
        radians = math.radians(angle)     
        ymove = math.sin(radians)*(self.speed) * -1
        return ymove

    # updata the position of the bubbles in each row when a new row comes up
    def updatey(self):
        self.rect.y = self.rect.y + 35
    
    # adjust positions according the odd or even
    def adjustxy(self,row,column):
        if self.oddeven == 0:
           self.rect.x = 25 + 40*column
        else:
           self.rect.x = 5 + 40*column
        self.rect.y = 5 + 35*row
    
    #change color 
    def changeColor(self,color):
        self.color = color;

class Button(object):
    def __init__(self, image_filename, position):
 
        self.position = position
        self.image = pygame.image.load(image_filename)
 
    def render(self, surface):
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2
        surface.blit(self.image, (x, y))
 
    def is_over(self, point):
        point_x, point_y = point
        x, y = self.position
        w, h = self.image.get_size()
        x -= w /2
        y -= h / 2
 
        in_x = point_x >= x and point_x < x + w
        in_y = point_y >= y and point_y < y + h
        return in_x and in_y

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.angle = 90
        arrowImage = pygame.image.load('cannon.png')
        arrowImage.convert_alpha()
        arrowRect = arrowImage.get_rect()
        self.image = arrowImage
        self.transformImage = self.image
        self.rect = arrowRect
        self.rect.centerx = STARTX 
        self.rect.centery = STARTY
        


    def update(self, direction):
        #adjust the angle of the arrow to the range (0,180)
        if direction == LEFT and self.angle < 180:
            self.angle += 1
        elif direction == RIGHT and self.angle > 0:        
            self.angle -= 1
        if self.angle == 180 or self.angle == 0:
            self.angle  = 1

        #rotate the arrow image
        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = STARTX 
        self.rect.centery = STARTY

        
    def draw(self):
        DISPLAYSURF.blit(self.transformImage, self.rect)

class Score(object):
    def __init__(self):
        self.total = 0
        self.font = pygame.font.SysFont('comicsansms', 15)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = WINDOWHEIGHT - 5
        
        
    def update(self, deleteList):
        self.total += ((len(deleteList)) * 10)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)

    def draw(self):
        DISPLAYSURF.blit(self.render, self.rect)

def main():
    global FPSCLOCK, DISPLAYSURF, DISPLAYRECT, MAINFONT, BUBBLE_LEVEL,BUBBLELAYERS
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Puzzle Bobble')
    MAINFONT = pygame.font.SysFont('Helvetica', TEXTHEIGHT)
    DISPLAYSURF, DISPLAYRECT = makeDisplay()
    pygame.mixer.music.load('ogg\s0000.mp3')
    pygame.mixer.music.play()

    #initial interface
    startSreenButtons_height = 74
    startSreenButtons = {}
    startSreenButtons["sb1"] = Button("GameName.png", (WINDOWWIDTH/2, 110))
    startSreenButtons["sb2"] = Button("StartGame.png", (WINDOWWIDTH/2, 220+startSreenButtons_height*0.5))
    startSreenButtons["sb3"] = Button("Instructions.png", (WINDOWWIDTH/2, 220+startSreenButtons_height*1.6))
    startSreenButtons["sb4"] = Button("ExitGame.png", (WINDOWWIDTH/2, 220+startSreenButtons_height*2.7))

    instructionButtons_height = 40
    instructionButtons = {}
    instructionButtons["ib0"] = Button("ib0.png", (WINDOWWIDTH/2, 50))
    instructionButtons["ib1"] = Button("ib1.png", (WINDOWWIDTH/2, 100+instructionButtons_height*0.5+2))
    instructionButtons["ib2"] = Button("ib2.png", (WINDOWWIDTH/2, 100+instructionButtons_height*1.5+2))
    instructionButtons["ib3"] = Button("ib3.png", (WINDOWWIDTH/2, 100+instructionButtons_height*2.5+2))
    instructionButtons["ib4"] = Button("ib4.png", (WINDOWWIDTH/2, 100+instructionButtons_height*3.5+2))
    instructionButtons["ib5"] = Button("ib5.png", (WINDOWWIDTH/2, 100+instructionButtons_height*4.5+2))
    instructionButtons["ib6"] = Button("ib6.png", (WINDOWWIDTH/2, 100+instructionButtons_height*5.5+2))
    instructionButtons["ib7"] = Button("Return.png", (WINDOWWIDTH/2, 100+instructionButtons_height*7.5))

    while True:
         startSreenButtons_pressed = None
         for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                for button_name, button in startSreenButtons.items():
                    if button.is_over(event.pos):
                        startSreenButtons_pressed = button_name
                        break
         if startSreenButtons_pressed is not None:
             if startSreenButtons_pressed == "sb2":
                  break
             elif startSreenButtons_pressed == "sb3":
                  while True:
                    DISPLAYSURF.fill(BGCOLOR)
                    instructionsButtons_pressed = None
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            return
                        if event.type == MOUSEBUTTONDOWN:
                            for button_name, button in instructionButtons.items():
                                if button.is_over(event.pos):
                                    instructionsButtons_pressed = button_name
                                    break
                    if instructionsButtons_pressed is not None:
                        if instructionsButtons_pressed == "ib7":
                            break;
                    for button in instructionButtons.values():
                        button.render(DISPLAYSURF)
                    pygame.display.update()
             elif startSreenButtons_pressed == "sb4":
                  terminate()
         if startSreenButtons_pressed != "sb3":
            for button in startSreenButtons.values():
                button.render(DISPLAYSURF)
            pygame.display.update()
         if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load('ogg\s0000.mp3')
            pygame.mixer.music.play()

    DISPLAYSURF.fill(BGCOLOR)
    button_width = 144
    button_height = 90
    buttons = {}
    buttons["b0"] = Button("difficulty.png", (WINDOWWIDTH/2, 80))
    buttons["b1"] = Button("button1.png", (WINDOWWIDTH/2-1.1*button_width, 200+0.5*button_height))
    buttons["b2"] = Button("button2.png", (WINDOWWIDTH/2, 200+0.5*button_height))
    buttons["b3"] = Button("button3.png", (WINDOWWIDTH/2+1.1*button_width, 200+0.5*button_height))
    buttons["b4"] = Button("button4.png", (WINDOWWIDTH/2-1.1*button_width, 200+1.6*button_height))
    buttons["b5"] = Button("button5.png", (WINDOWWIDTH/2, 200+1.6*button_height))
    buttons["b6"] = Button("button6.png", (WINDOWWIDTH/2+1.1*button_width, 200+1.6*button_height))
    while True:
         button_pressed = None
         for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                for button_name, button in buttons.items():
                    if button.is_over(event.pos):
                        button_pressed = button_name
                        break
         if button_pressed is not None:
             # from game begin to game over 
             if button_pressed == "b1":
                  BUBBLE_LEVEL = 20;
                  BUBBLELAYERS = 2;
                  change_color = 0
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
             if button_pressed == "b2":
                  BUBBLE_LEVEL = 16;
                  BUBBLELAYERS = 2;
                  change_color = 0;
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
             if button_pressed == "b3":
                  BUBBLE_LEVEL = 12;
                  BUBBLELAYERS = 3;
                  change_color = 0;
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
             if button_pressed == "b4":
                  BUBBLE_LEVEL = 8;
                  BUBBLELAYERS = 3;
                  change_color = 0;
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
             if button_pressed == "b5":
                  BUBBLE_LEVEL = 6;
                  BUBBLELAYERS = 4;
                  change_color = 0;
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
             if button_pressed == "b6":
                  BUBBLE_LEVEL = 6;
                  BUBBLELAYERS = 4;
                  change_color = 1;
                  score, winorlose = runGame(change_color)
                  endScreen(score, winorlose)
         for button in buttons.values():
            button.render(DISPLAYSURF)
         if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load('ogg\s0000.mp3')
            pygame.mixer.music.play()
         pygame.display.update()

def runGame(change_color,):
    musicList =['ogg\s0001.mp3','ogg\s0002.mp3','ogg\s0003.mp3','ogg\s0004.mp3','ogg\s0005.mp3','ogg\s0006.mp3']
    random.shuffle(musicList)
    pygame.mixer.music.load(musicList[0])
    pygame.mixer.music.play()
    track = 0
    gameColorList = copy.deepcopy(COLORLIST)
    gameColorListOrg = copy.deepcopy(COLORLIST)
    direction = None
    launchBubble = False
    newBubble = None
    addLine = False
    oddEven = False
    newLineNum = 1
    newLine = 0 
    
    arrow = Arrow()
    bubbleArray = makeBlankBoard() #initailize the bubble array, which is ARRAYHEIGHT*ARRAYWIDTH
    setBubbles(bubbleArray, gameColorList) #initialize the bubble array in the first BUBBLELAYERS rows with random color
    
    nextBubble = Bubble(gameColorList[0]) #initialize the bubble to launch with random color, and put it on the right bottom corner 
    nextBubble.rect.right = WINDOWWIDTH - 5
    nextBubble.rect.bottom = WINDOWHEIGHT - 5

    score = Score() #initialize the score 
    
      
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        
        #execute corresponding event when getting order from keyboard
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT):
                    direction = LEFT
                elif (event.key == K_RIGHT):
                    direction = RIGHT
                    
            elif event.type == KEYUP:
                direction = None
                if event.key == K_SPACE:
                    launchBubble = True
                    popSound = pygame.mixer.Sound('ogg\s0009.wav')
                    popSound.play()
                elif event.key == K_ESCAPE:
                    terminate()
        
        #launch new bubble
        if launchBubble == True:
            if newBubble == None:
                newBubble = Bubble(nextBubble.color)
                newBubble.angle = arrow.angle
                
            newBubble.update()
            newBubble.draw()
            
            #if the bubble come up against the left or right boundary, change the direction 
            if newBubble.rect.right >= WINDOWWIDTH - 5:
                newBubble.angle = 180 - newBubble.angle
            elif newBubble.rect.left <= 5:
                newBubble.angle = 180 - newBubble.angle

            #calculate the process from launching the bubble to stopping colliding  
            launchBubble, newBubble, score = stopBubble(bubbleArray, newBubble, launchBubble, score)

            

            #determine whether the termination conditions is established
            finalBubbleList = []
            for row in range(len(bubbleArray)):
                for column in range(len(bubbleArray[0])):
                    if bubbleArray[row][column] != BLANK:
                        finalBubbleList.append(bubbleArray[row][column])
                        if bubbleArray[row][column].rect.bottom > (WINDOWHEIGHT - arrow.rect.height - 10):
                            return score.total, 'lose'
            if len(finalBubbleList) < 1:
                return score.total, 'win'

            if newBubble==None:
                newLineNum = newLineNum + 1;
                if newLineNum >= BUBBLE_LEVEL:
                    addLine = True;
                    if oddEven == True:
                        oddEven = False
                    else:
                        oddEven = True
                    newLineNum = 0;                            
            
            #determine the color list of the bubbule to launch
            gameColorList = updateColorList(bubbleArray)
            random.shuffle(gameColorList)
            
                    
                            
            if launchBubble == False:
                
                nextBubble = Bubble(gameColorList[0])
                nextBubble.rect.right = WINDOWWIDTH - 5
                nextBubble.rect.bottom = WINDOWHEIGHT - 5

            

                            
        nextBubble.draw()
        if launchBubble == True:
            coverNextBubble()
        
        arrow.update(direction)
        arrow.draw()


        
        #setArrayPos(bubbleArray)
        if addLine == True:
            addLine = False
            if oddEven == True: 
               updateLine(bubbleArray,gameColorListOrg,0,gameColorListOrg,change_color);
            else:
               updateLine(bubbleArray,gameColorListOrg,1,gameColorListOrg,change_color);
        
        drawBubbleArray(bubbleArray)
        score.draw()


        if pygame.mixer.music.get_busy() == False:
            if track == len(musicList) - 1:
                track = 0
            else:
                track += 1

            pygame.mixer.music.load(musicList[track])
            pygame.mixer.music.play()

            
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeBlankBoard():
    array = []
    
    for row in range(ARRAYHEIGHT):
        column = []
        for i in range(ARRAYWIDTH):
            column.append(BLANK)
        array.append(column)

    return array

def setBubbles(array, gameColorList):  #initialize the bubble array with the # of rows =  BUBBLELAYERS, and the # of cols = len(array[row])
    for row in range(BUBBLELAYERS):
        wahh = len(array[row])
        for column in range(len(array[row])):
            random.shuffle(gameColorList)
            newBubble = Bubble(gameColorList[0], row, column)
            if row%2 == 0:  #if the bubble is in the even row ,then oddeven =1
                newBubble.oddeven = 1
            else:  #if the bubble is in the odd row ,then oddeven =0
                newBubble.oddeven = 0
            array[row][column] = newBubble 
            
    setArrayPos(array)

def changeBubblesColor(array, gameColorList):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
               random.shuffle(gameColorList)
               array[row][column].changeColor(gameColorList[0]) 

def setArrayPos(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x = (BUBBLEWIDTH * column) + 5
                array[row][column].rect.y = (BUBBLEWIDTH * row) + 5

    for row in range(1, ARRAYHEIGHT, 2):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.x += BUBBLERADIUS
                

    for row in range(1, ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].rect.y -= (BUBBLEYADJUST * row)

    deleteExtraBubbles(array)

def setArrayPosFirstLine(array, len1):
    if len1%2 == 1:
     adj =  BUBBLERADIUS
    elif len1%2 == 0:
     adj =  0
    for column in range(len1):
      array[0][column].rect.x = (BUBBLEWIDTH * column) + 5 +adj
      array[0][column].rect.y = (BUBBLEWIDTH * 0) + 5
    deleteExtraBubbles(array)

def updateLine(array, gameColorList,numNewline,gameColorListOrg,change_color):
    if change_color == 1:
        changeBubblesColor(array,gameColorListOrg); # function to change color randomly            
                        
    for row in range(ARRAYHEIGHT - 2,-1,-1):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].updatey()

    for row in range(ARRAYHEIGHT - 2,-1,-1):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row + 1][column] = array[row][column]
                array[row][column] = BLANK


    len1 = ARRAYWIDTH
    if numNewline == 0:
        len1 = ARRAYWIDTH -1
    elif numNewline == 1:
        len1 = ARRAYWIDTH

    for column in range(len1):
            random.shuffle(gameColorList)
            newBubble = Bubble(gameColorList[0], 0, column)
            newBubble.oddeven = numNewline
            array[0][column] = newBubble 
 #   if change_color == 1:
 #       changeBubblesColor(array,gameColorList);

    setArrayPosFirstLine(array,len1)

def deleteExtraBubbles(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                if array[row][column].rect.right > WINDOWWIDTH:
                    array[row][column] = BLANK

def updateColorList(bubbleArray):
    newColorList = []

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            if bubbleArray[row][column] != BLANK:
                newColorList.append(bubbleArray[row][column].color)

    colorSet = set(newColorList)

    if len(colorSet) < 1:
        colorList = []
        colorList.append(WHITE)
        return colorList

    else:

        return list(colorSet)

def checkForFloaters(bubbleArray):
    bubbleList = [column for column in range(len(bubbleArray[0]))
                         if bubbleArray[0][column] != BLANK]

    newBubbleList = []

    for i in range(len(bubbleList)):
        if i == 0:
            newBubbleList.append(bubbleList[i])
        elif bubbleList[i] > bubbleList[i - 1] + 1:
            newBubbleList.append(bubbleList[i])

    copyOfBoard = copy.deepcopy(bubbleArray)

    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[0])):
            bubbleArray[row][column] = BLANK
    

    for column in newBubbleList:
        popFloaters(bubbleArray, copyOfBoard, column)

def popFloaters(bubbleArray, copyOfBoard, column, row=0):
    if (row < 0 or row > (len(bubbleArray)-1)
                or column < 0 or column > (len(bubbleArray[0])-1)):
        return
    
    elif copyOfBoard[row][column] == BLANK:
        return

    elif bubbleArray[row][column] == copyOfBoard[row][column]:
        return

    bubbleArray[row][column] = copyOfBoard[row][column]
    

#    if row == 0:
#        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
#        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
#        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
#        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)

    if bubbleArray[row][column].oddeven == 1:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column,     row - 1)
        popFloaters(bubbleArray, copyOfBoard, column - 1, row - 1)

    else:
        popFloaters(bubbleArray, copyOfBoard, column + 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column - 1, row    )
        popFloaters(bubbleArray, copyOfBoard, column,     row + 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row + 1)
        popFloaters(bubbleArray, copyOfBoard, column,     row - 1)
        popFloaters(bubbleArray, copyOfBoard, column + 1, row - 1)

def stopBubble(bubbleArray, newBubble, launchBubble, score):
    deleteList = []
    popSound = pygame.mixer.Sound('ogg/s0008.wav')
    found = False;
   # length = len(bubbleArray)
    for row in range(len(bubbleArray)):
        for column in range(len(bubbleArray[row])):
            
            if (bubbleArray[row][column] != BLANK and newBubble != None):
                if (pygame.sprite.collide_rect(newBubble, bubbleArray[row][column]) and found == False) or newBubble.rect.top < 0:
                    y1 = (float)(newBubble.rect.centery)
                    x1 = (float)(newBubble.rect.centerx)
                    y0 = (float)(bubbleArray[row][column].rect.centery)
                    x0 = (float)(bubbleArray[row][column].rect.centerx)
                    if newBubble.rect.top < 0:
                        newRow, newColumn = addBubbleToTop(bubbleArray, newBubble)
                        
                    elif newBubble.rect.centery >= bubbleArray[row][column].rect.centery:

                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:

                            if bubbleArray[row][column].oddeven == 1:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                    newColumn = column + 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 0
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                            else:
                                newRow = row + 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                   newRow = newRow - 1
                                   newColumn = column + 1
                                   newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                   newBubble.oddeven = 1

                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                                                    
                        elif newBubble.rect.centerx < bubbleArray[row][column].rect.centerx:
                            if bubbleArray[row][column].oddeven == 1:
                                newRow = row + 1
                                newColumn = column - 1
                                if newColumn < 0:
                                    newColumn = 0
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                    newColumn = column - 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 0
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 

                            else:
                                newRow = row + 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow - 1
                                    newColumn = column - 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                                
                            
                    elif newBubble.rect.centery < bubbleArray[row][column].rect.centery:
                        if newBubble.rect.centerx >= bubbleArray[row][column].rect.centerx:
                            if bubbleArray[row][column].oddeven == 1:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                    newColumn = column + 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 0
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                            else:
                                newRow = row - 1
                                newColumn = column + 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                    newColumn = column + 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                            
                        elif newBubble.rect.centerx <= bubbleArray[row][column].rect.centerx:
                            if bubbleArray[row][column].oddeven == 1:
                                newRow = row - 1
                                newColumn = column - 1
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                    newColumn = column - 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 0
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                                
                            else:
                                newRow = row - 1
                                newColumn = column
                                if bubbleArray[newRow][newColumn] != BLANK:
                                    newRow = newRow + 1
                                    newColumn = column - 1
                                    newBubble.oddeven = bubbleArray[row][column].oddeven
                                else:
                                    newBubble.oddeven = 1
                                bubbleArray[newRow][newColumn] = copy.copy(newBubble)
                                bubbleArray[newRow][newColumn].row = newRow
                                bubbleArray[newRow][newColumn].column = newColumn
                                bubbleArray[newRow][newColumn].adjustxy(newRow,newColumn);
                                found = True; 
                    



                    popBubbles(bubbleArray, newRow, newColumn, newBubble.color, deleteList) #only record the position of delete circles
                    
                    
                    if len(deleteList) >= 3: #if we have three more circle to delete ,do it 
                        for pos in deleteList:
                            popSound.play()
                            row = pos[0]
                            column = pos[1]
                            bubbleArray[row][column] = BLANK
                        checkForFloaters(bubbleArray) #delete the floaters
                        
                        score.update(deleteList)

                    launchBubble = False
                    newBubble = None

    return launchBubble, newBubble, score
                   
def addBubbleToTop(bubbleArray, bubble):
    oddeven = 0;
    for column in range(len(bubbleArray[0])):
        if bubbleArray[0][column] != BLANK:
            oddeven = bubbleArray[0][column].oddeven
    
    posx = bubble.rect.centerx
    leftSidex = posx - BUBBLERADIUS

    columnDivision = math.modf(float(leftSidex) / float(BUBBLEWIDTH))
    column = int(columnDivision[1])

    if columnDivision[0] < 0.5:
        if bubbleArray[0][column] == BLANK:
           bubbleArray[0][column] = copy.copy(bubble)
           bubbleArray[0][column].oddeven = oddeven
           bubbleArray[0][column].adjustxy(0,column)
        else:
           bubbleArray[0][column - 1] = copy.copy(bubble)
           bubbleArray[0][column - 1].oddeven = oddeven
           bubbleArray[0][column - 1].adjustxy(0,column - 1)

    else:
        column += 1
        if bubbleArray[0][column] == BLANK:
           bubbleArray[0][column] = copy.copy(bubble)
           bubbleArray[0][column].oddeven = oddeven
           bubbleArray[0][column].adjustxy(0,column)
        else:
           bubbleArray[0][column - 1] = copy.copy(bubble)
           bubbleArray[0][column - 1].oddeven = oddeven
           bubbleArray[0][column - 1].adjustxy(0,column - 1)

    row = 0
    

    return row, column

def popBubbles(bubbleArray, row, column, color, deleteList):
    if row < 0 or column < 0 or row > (len(bubbleArray)-1) or column > (len(bubbleArray[0])-1):
        return

    elif bubbleArray[row][column] == BLANK:
        return
    
    elif bubbleArray[row][column].color != color:
        return

    for bubble in deleteList:
        if bubbleArray[bubble[0]][bubble[1]] == bubbleArray[row][column]:
            return

    deleteList.append((row, column))

#    if row == 0:
#        popBubbles(bubbleArray, row,     column - 1, color, deleteList)
#        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
#        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
#        popBubbles(bubbleArray, row + 1, column - 1, color, deleteList)


    if bubbleArray[row][column].oddeven == 1:
        
        popBubbles(bubbleArray, row + 1, column,         color, deleteList)
        popBubbles(bubbleArray, row + 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column,         color, deleteList)
        popBubbles(bubbleArray, row - 1, column - 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column + 1,     color, deleteList)
        popBubbles(bubbleArray, row,     column - 1,     color, deleteList)

    else:
        popBubbles(bubbleArray, row - 1, column,     color, deleteList)
        popBubbles(bubbleArray, row - 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row + 1, column,     color, deleteList)
        popBubbles(bubbleArray, row + 1, column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column + 1, color, deleteList)
        popBubbles(bubbleArray, row,     column - 1, color, deleteList)

def drawBubbleArray(array):
    for row in range(ARRAYHEIGHT):
        for column in range(len(array[row])):
            if array[row][column] != BLANK:
                array[row][column].draw()                   

def makeDisplay():
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYRECT = DISPLAYSURF.get_rect()
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.convert()
    pygame.display.update()

    return DISPLAYSURF, DISPLAYRECT   
 
def terminate():
    pygame.quit()
    sys.exit()

def coverNextBubble():
    whiteRect = pygame.Rect(0, 0, BUBBLEWIDTH, BUBBLEWIDTH)
    whiteRect.bottom = WINDOWHEIGHT
    whiteRect.right = WINDOWWIDTH
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, whiteRect)

def endScreen(score, winorlose):
    pygame.mixer.music.load('ogg\s0007.mp3')
    pygame.mixer.music.play()
    endFont = pygame.font.SysFont('comicsansms', 30, True)
    if winorlose == 'win':
        endMessage1 = endFont.render('You ' + winorlose + '!', True, GREEN, BGCOLOR)
    if winorlose == 'lose':
        endMessage1 = endFont.render('You ' + winorlose + '!', True, RED, BGCOLOR)
    endMessage2 = endFont.render(' Your Score is ' + str(score) + '.', True, BLACK, BGCOLOR)
    endMessage3 = endFont.render(' Press Enter to Restart.' , True, BLACK, BGCOLOR)
    endMessage4 = endFont.render(' Press Esc to exit.' , True, BLACK, BGCOLOR)
    #endMessage1Rect = endMessage1.get_rect()
    #endMessage1Rect.center = DISPLAYRECT.center

    DISPLAYSURF.fill(BGCOLOR)
    #DISPLAYSURF.blit(endMessage1, endMessage1Rect)
    DISPLAYSURF.blit(endMessage1, (250,100))
    DISPLAYSURF.blit(endMessage2, (185,170))
    DISPLAYSURF.blit(endMessage3, (150,240))
    DISPLAYSURF.blit(endMessage4, (185,310))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    DISPLAYSURF.fill(BGCOLOR)
                    return
                elif event.key == K_ESCAPE:
                    terminate()     
        
if __name__ == '__main__':
    main()
