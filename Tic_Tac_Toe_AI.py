'''
This program makes an AI that you can play against, but the AI won't lose. 
The original creator of this code is Marcus Koseck.
Feel free to edit the code to do whatever you need it to do. Cheers. 
'''

import pygame
import time
import sys

winner = None
draw = False
boardPlacement = {0:None, 1:None, 2:None,
                      3:None, 4:None, 5:None,
                      6:None, 7:None, 8:None}
XO = 'x'


class Board:
    '''
    This class controls the board. You can make modifications as needed.
    Note: The function 'determineWhosTurn()' is in this class to help continuity of code.
    '''
    def __init__(self):
        self.white = (255,255,255)
        self.lineColor = (10,10,10)
        self.width, self.height = 400,400
        self.screen = pygame.display.set_mode((self.width, self.height+100))
        x = pygame.image.load("xPicture.PNG")
        self.x = pygame.transform.scale(x,(90,90))
        o = pygame.image.load("oPicture.PNG")
        self.o = pygame.transform.scale(o,(90,90))

    def makeBoard(self):
        '''
        Input: None

        Description: This function draws the board

        output: None
        '''
        lineColor = (10,10,10)
        self.screen.fill(self.white)
        
        pygame.draw.line(self.screen, lineColor, (self.width/3,0), (self.width/3 , self.height),7)
        pygame.draw.line(self.screen, lineColor, (self.width/3*2,0),(self.width/3*2,self.height),7)
        pygame.draw.line(self.screen, lineColor, (0,self.height/3), (self.width, self.height/3),7)
        pygame.draw.line(self.screen, lineColor, (0,self.height/3*2),(self.width,self.height/3*2),7)
        self.determineWhosTurn()

    def determineWhosTurn(self):
        '''
        Input: None

        Description: This function determines who's turn it is.

        Output: None
        '''
        global winner, draw, XO
        if winner is None:
            message = XO.upper()+"'s Turn"
        else:
            message = winner[0].upper()+"'s Won!"
        if draw:
            message = "Game Over"

        font= pygame.font.Font(None,30)
        text = font.render(message,1,self.white)

        self.screen.fill((0,0,0),(0,400,500,100))
        textSpace = text.get_rect(center = (self.width/2,500-50))
        self.screen.blit(text,textSpace)
        pygame.display.update()

    def resetGame(self):
        '''
        Input: None

        Output: This function resets the game. It will change all of the variables
        to their default settings

        Output: None
        '''
        global winner, draw, boardPlacement, XO
        time.sleep(3)
        XO = 'x'
        draw = False
        winner = None
        boardPlacement = {0: None, 1:None, 2:None,
                  3:None, 4:None, 5:None,
                  6:None, 7:None, 8: None}
        self.makeBoard()

class Game(Board):
    '''
    This class deals with all of the game functionality
    '''
    def __init__(self, board):
        self.white = board.white
        self.screen = board.screen
        self.width, self.height = 400,400

    def checkWin(self):
        '''
        Input: None

        Description: This function will check the board for a win. A win would be along a row, column, or diagonal

        Output: None
        '''
        global winner, draw, boardPlacement
        #Check if row is complete
        if((boardPlacement[0] == boardPlacement[1] == boardPlacement[2]) and (boardPlacement[0] is not None)):
            winner = boardPlacement[0]
            pygame.draw.line(self.screen, (250,0,0),(0,self.height/3 - self.height/6), (self.width, self.height/3 - self.height/6),4)

        if((boardPlacement[3] == boardPlacement[4] == boardPlacement[5]) and (boardPlacement[3] is not None)):
            winner = boardPlacement[3]
            pygame.draw.line(self.screen, (250,0,0),(0,2*self.height/3 - self.height/6), (self.width, 2*self.height/3 - self.height/6),4)

        if((boardPlacement[6] == boardPlacement[7] == boardPlacement[8]) and (boardPlacement[6] is not None)):
            winner = boardPlacement[3]
            pygame.draw.line(self.screen, (250,0,0),(0,3*self.height/3 - self.height/6), (self.width, 3*self.height/3 - self.height/6),4)

        #Check if Col is complete
        if((boardPlacement[0] == boardPlacement[3] == boardPlacement[6]) and (boardPlacement[0] is not None)):
            winner = boardPlacement[0]
            pygame.draw.line(self.screen, (250,0,0),(self.width/3 - self.width/6,0), (self.width/3-self.width/6,self.height),4)

        if((boardPlacement[1] == boardPlacement[4] == boardPlacement[7]) and (boardPlacement[1] is not None)):
            winner = boardPlacement[0]
            pygame.draw.line(self.screen, (250,0,0),(2*self.width/3 - self.width/6,0), (2*self.width/3-self.width/6,self.height),4)

        if((boardPlacement[2] == boardPlacement[5] == boardPlacement[8]) and (boardPlacement[2] is not None)):
            winner = boardPlacement[0]
            pygame.draw.line(self.screen, (250,0,0),(3*self.width/3 - self.width/6,0), (3*self.width/3-self.width/6,self.height),4)

        #Check Diagnoals 
        if((boardPlacement[0] == boardPlacement[4]==boardPlacement[8]) and (boardPlacement[0] is not None)):
            winner = boardPlacement[0]
            pygame.draw.line(self.screen, (250,70,70),(50,50),(350,350),4)

        if((boardPlacement[2] == boardPlacement[4] == boardPlacement[6]) and (boardPlacement[2] is not None)):
            winner = boardPlacement[2]
            pygame.draw.line(self.screen, (250,70,70),(350,50),(50,350),4)

        count = 0
        for keys in boardPlacement:
            if(boardPlacement[keys] is not None):
                count+=1
        if(count == 9 and winner is None):
            draw = True
        self.determineWhosTurn()
       

class Player(Board):
    '''
    This class deals with the player functionality
    '''
    def __init__(self,board):
        self.width, self.height = 400,400
        self.screen = board.screen
        self.x = board.x
        self.o = board.o

    def click(self):
        '''
        Input: None

        Description: This function handles where a player clicks on the board. If
        the player clicks on the board, it will record where the player clicked and 
        translate it into the specific row and column that was clicked. 

        Output: None
        '''
        global boardPlacement
        xpos,ypos = pygame.mouse.get_pos()

        if(xpos<self.width/3):
            col=1
        elif(xpos<(self.width/3)*2):
            col=2
        elif(xpos<self.width):
            col=3
        else:
            col = None

        if(ypos<self.height/3):
            row=1
        elif(ypos<(self.height/3)*2):
            row=2
        elif(ypos<self.height):
            row=3
        else:
            row=None

        if(row==1 and col==1 and boardPlacement[0] is None):
            boardPlacement[0] = XO
            self.drawXO(row,col)
        if(row==1 and col==2 and boardPlacement[1] is None):
            boardPlacement[1] = XO
            self.drawXO(row,col)
        if(row==1 and col==3 and boardPlacement[2] is None):
            boardPlacement[2] = XO
            self.drawXO(row,col)
        if(row==2 and col==1 and boardPlacement[3] is None):
            boardPlacement[3] = XO
            self.drawXO(row,col)
        if(row==2 and col==2 and boardPlacement[4] is None):
            boardPlacement[4] = XO
            self.drawXO(row,col)
        if(row==2 and col==3 and boardPlacement[5] is None):
            boardPlacement[5] = XO
            self.drawXO(row,col)
        if(row==3 and col==1 and boardPlacement[6] is None):
            boardPlacement[6] = XO
            self.drawXO(row,col)
        if(row==3 and col==2 and boardPlacement[7] is None):
            boardPlacement[7] = XO
            self.drawXO(row,col)
        if(row==3 and col==3 and boardPlacement[8] is None):
            boardPlacement[8] = XO
            self.drawXO(row,col)
            

    def drawXO(self, row, col):
        '''
        Input: row (integer), column (integer)

        Description: this function is called inside of 'click'. This function will take 
        the specific row and column that the player selected and update the game board
        as needed.

        Output: None
        '''
        global boardPlacement, XO
        if(row==1):
            posx=30
        if(row==2):
            posx = self.width/3 +30
        if(row == 3):
            posx=self.width/3*2 + 30

        if(col==1):
            posy = 30
        if(col==2):
            posy=self.height/3+30
        if(col==3):
            posy=self.height/3*2+30
            
        if(XO=='x'):
            self.screen.blit(self.x, (posy,posx))
            XO = 'o'
        elif(XO=='o'):
            self.screen.blit(self.o,(posy,posx))
            XO = 'x'
        pygame.display.update()

class AI(Board):
    '''
    This class deals with the AI functionality
    '''
    def determinePosition(self, boardPlacement):
        '''
        Input: the game board (dictionary)


        Description: This function determines the best position in
        the current state of the game. It does this by using the minimax
        algorithm.

        Output: the specific index, for a dictionary, that is the best move (integer)
        '''
        bestMove = -10000
        place = -1
        for i in range(len(boardPlacement)):
            if(boardPlacement[i] is None):
                boardPlacement[i] = 'o'
                score = self.minimax(boardPlacement, False)
                boardPlacement[i] = None
                if(score>bestMove):
                    bestMove = score
                    place = i

        return place

    def minimax(self, position, maximizingPlayer):
        '''
        Input: game board (dictionary) and whether or not the next move is the maximizing player (bool)

        Description: This is the minimax function that acts as the brain for our artifical intelligence.

        Output: 100, if it believes it will win. -100, if it believes it will lose. Otherwise, 0 (a draw).
        '''
        if(self.endOfGameCheck('o')):
            return 100
        elif(self.endOfGameCheck('x')):
            return -100
        elif(self.checkDraw()):
            return 0

        if maximizingPlayer:
            maxEval = -1000
            for key in position.keys():
                if(position[key] is None):
                    position[key] = 'o'
                    score = self.minimax(position, False)
                    position[key] = None
                    if(score>maxEval):
                        maxEval = score
            return maxEval
        else:
            minEval = 1000
            for key in position.keys():
                if(position[key] is None):
                    position[key] = 'x'
                    score = self.minimax(position, True)
                    position[key] = None
                    if(score<minEval):
                        minEval = score
            return minEval

    def aidrawXO(self, place):
        '''
        Input: the index that is the best move for our AI (integer)

        Description: This function draws the X or O that corresponds to
        the AI's game piece. 

        Output:None
        '''
        global XO, boardPlacement
        width, height = 400,400
        posx,posy =0,0

        if(place==0 or place==1 or place==2):
            posx=30
        if(place==3 or place==4 or place==5):
            posx = width/3 +30
        if(place==6 or place==7 or place==8):
            posx=width/3*2 + 30

        if(place==0 or place==3 or place==6):
            posy = 30

        if(place==1 or place==4 or place==7):
            posy=height/3+30

        if(place==2 or place==5 or place==8):
            posy=height/3*2+30

        boardPlacement[place] = XO

        if(XO=='x'):
            self.screen.blit(self.x, (posy,posx))
            XO = 'o'
        elif(XO=='o'):
            self.screen.blit(self.o,(posy,posx))
            XO = 'x'
        pygame.display.update()

    def checkDraw(self):
        '''
        Input: None

        Description: This function checks of the current game position is a draw

        Output: True, if it is a draw. Otherwise, False
        '''
        count = 0
        for keys in boardPlacement:
            if(boardPlacement[keys] is not None):
                count+=1
        if(count == 9 and winner is None):
            return True
        else:
            return False

    def endOfGameCheck(self, piece):
        '''
        Input: the game piece you'd like to win with (an X or an O) (string)

        Description: This function checks if the current game position is a win or a loss.

        Output: True, if the game ends. Otherwise, false.
        '''
        global boardPlacement, winner
        #Check if row is complete
        if((boardPlacement[0] == boardPlacement[1] == boardPlacement[2]) and (boardPlacement[0] == piece)):
            return True

        if((boardPlacement[3] == boardPlacement[4] == boardPlacement[5]) and (boardPlacement[3] == piece)):
            return True

        if((boardPlacement[6] == boardPlacement[7] == boardPlacement[8]) and (boardPlacement[6] == piece)):
            return True

        #Check if Col is complete
        if((boardPlacement[0] == boardPlacement[3] == boardPlacement[6]) and (boardPlacement[0] == piece)):
            return True

        if((boardPlacement[1] == boardPlacement[4] == boardPlacement[7]) and (boardPlacement[1] == piece)):
            return True

        if((boardPlacement[2] == boardPlacement[5] == boardPlacement[8]) and (boardPlacement[2] == piece)):
            return True

        #Check Diagnoals 
        if((boardPlacement[0] == boardPlacement[4]==boardPlacement[8]) and (boardPlacement[0] == piece)):
            return True

        if((boardPlacement[2] == boardPlacement[4] == boardPlacement[6]) and (boardPlacement[2] == piece)):
            return True
        else:
            return False


def main():
    '''
    This is the main function that holds all of the important information
    '''
    pygame.init()
    fps = 30
    gameClock = pygame.time.Clock()

    ai = AI()
    board = Board()
    game = Game(board)
    player1 = Player(board)
    board.makeBoard()

    while True:
        '''
        This is the game loop that will run forever
        '''
        for event in pygame.event.get():
            if(winner or draw):
                board.resetGame()

            if(XO == 'x'):
                if event.type == quit:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    player1.click()
                game.checkWin()
            
            if(winner or draw):
                board.resetGame()

            if(XO == 'o'):
                place = ai.determinePosition(boardPlacement)
                ai.aidrawXO(place)
                game.checkWin()

        pygame.display.update()
        gameClock.tick(fps)
main()


    

