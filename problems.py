'''
This file will contain your the code for your problems. 
'''

import numpy as np
import cv2

class Game:
    def __init__(self, problem, pZero, pOne,verbose=True):
      self.problem = problem      
      self.players = [pZero,pOne]   
      self.verbose = verbose   
      if self.verbose:
         self.problem.showState()               
    def playGame(self):
      pCur=0
      while self.problem.isTerminal()==False:           
         move = self.players[pCur].getMove(self.problem)           
         self.problem.doMove(move)
         if self.verbose:
            self.problem.showState()
            print(f"Move {self.problem.ticks}:")
            print(self.problem.state)
         pCur = np.abs(pCur-1)
        
      wIndex = self.problem.getWinner()
      winner = self.players[wIndex]
      if wIndex == -1:
         winner = "DRAW"
      #display final state
      print(f"The Winner is {winner} ({wIndex})!")
      if self.verbose:
         self.problem.showState(4000)
      return wIndex
              
class TicTacToe:
   def __init__(self):
      self.state = np.zeros((3,3))      
      self.ticks=-1      
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      moves = []
      mark = 1
      if np.sum(np.abs(state))%2!=0:
         mark = -1       
      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==0:
               moves.append((mark,(i,j)))
      return moves             
   def getSuccessor(self, move, state):
      mark = move[0]
      loc = move[1]
      state[loc] = mark
      return state
   def doMove(self,move):
      self.state = self.getSuccessor(move,self.state)
      self.ticks+=1
   def isTerminal(self, state=None):
      if state is None:
         state = self.state         
      terminal = False
      val = self.evalTerminal(state)      
      if val ==0 and np.sum(np.abs(state))==9:
         terminal = True
      if val!=0:
         terminal = True
      return terminal
   def evalTerminal(self, state=None):
      if state is None:
         state = self.state
      val = 0      
      
      pZeroWins = [np.max(np.sum(state,0))==3,np.max(np.sum(state,1))==3,np.trace(state)==3,np.trace(state[:,::-1])==3]
      pOneWins = [np.min(np.sum(state,0))==-3,np.min(np.sum(state,1))==-3,np.trace(state)==-3,np.trace(state[:,::-1])==-3]

      if np.any(pZeroWins):
         val = 1
      if np.any(pOneWins):
         val = -1
      return val
   def getWinner(self, state=None):
      if state is None:
         state = self.state
      val = self.evalTerminal(state)
      if val==1:
         return 0 
      elif val==-1:
         return 1
      else:
         return -1
   def showState(self, ms = 1000,state=None):
      if state is None:
         state = self.state  

      screen = np.zeros((150,150)).astype(np.uint8)         
      screen = cv2.line(screen,(0,49),(149,49),255) 
      screen = cv2.line(screen,(0,99),(149,99),255)
      screen = cv2.line(screen,(49,0),(49,149),255) 
      screen = cv2.line(screen,(99,0),(99,149),255)

      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==1:
               screen = cv2.line(screen,(5 +j*50,5+i*50),(44+j*50,44+i*50),255,2,cv2.LINE_AA) 
               screen = cv2.line(screen,(44+j*50,5+i*50),(5 +j*50,44+i*50),255,2,cv2.LINE_AA) 
            if state[i,j]==-1:
               screen = cv2.circle(screen, (25 +j*50,25+i*50), 20, 255, 2,cv2.LINE_AA) 
               
      cv2.imshow('TicTacToe',screen)
      cv2.waitKey(ms)

class ConnectFour:                   # start of the code for connect four game
   def __init__(self):
      self.state = np.zeros((6,7))   # the board is 6x7 in connect four
      self.ticks=-1
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      moves = []
      mark = 1                       # player 0 = 1 player 1 = -1
      if np.sum(np.abs(state))%2!=0:
         mark = -1
      for col in range(7):           # checks the top row to see if there is a piece there
         if state[0,col]==0:         # top square empty = column not full = you can place a piece there
            moves.append((mark,col))
      return moves
   def getSuccessor(self, move, state):
      mark = move[0]
      col = move[1]
      for row in range(5,-1,-1):     # start at the bottom row and go up
         if state[row,col]==0:       # find the lowest empty square
            state[row,col] = mark    # mark the square as 1 or -1 to show which player moved there
            break
      return state
   def doMove(self,move):
      self.state = self.getSuccessor(move,self.state)
      self.ticks+=1
   def isTerminal(self, state=None):
      if state is None:
         state = self.state
      terminal = False
      val = self.evalTerminal(state)
      if val==0 and np.sum(np.abs(state))==42:   # nobody won and the board is full = draw
         terminal = True
      if val!=0:                                 # someone won
         terminal = True
      return terminal
   def evalTerminal(self, state=None):           # checks if anyone has won in any direction
      if state is None:
         state = self.state
      val = 0

      for row in range(6):                       # horizontal check
         for col in range(4):
            total = state[row,col] + state[row,col+1] + state[row,col+2] + state[row,col+3]
            if total==4:                         # if player 0 won it will total up 4
               val = 1
            if total==-4:                        # if player 1 won it will total up -4
               val = -1

      for row in range(3):                       # vertical check
         for col in range(7):
            total = state[row,col] + state[row+1,col] + state[row+2,col] + state[row+3,col]
            if total==4:
               val = 1
            if total==-4:
               val = -1

      for row in range(3):                       # diagonal check going down-right
         for col in range(4):
            total = state[row,col] + state[row+1,col+1] + state[row+2,col+2] + state[row+3,col+3]
            if total==4:
               val = 1
            if total==-4:
               val = -1

      for row in range(3,6):                     # diagonal check going up-right
         for col in range(4):
            total = state[row,col] + state[row-1,col+1] + state[row-2,col+2] + state[row-3,col+3]
            if total==4:
               val = 1
            if total==-4:
               val = -1
      return val
   def getWinner(self, state=None):
      if state is None:
         state = self.state
      val = self.evalTerminal(state)
      if val==1:
         return 0                    # player 0 won
      elif val==-1:
         return 1                    # player 1 won
      else:
         return -1                   # draw
   
   def showState(self, ms = 1000,state=None):     # draws the board in a pop up window
      if state is None:
         state = self.state

      screen = np.zeros((300,350,3)).astype(np.uint8)     # window is 300 tall and 350 wide, the 3 makes it a color picture
      screen[:,:] = (255,0,0)                             # makes the whole background blue like a connect four board

      for i in range(state.shape[0]):                     # goes through every row
         for j in range(state.shape[1]):                  # goes through every column
            color = (255,255,255)                         # empty spot = white
            if state[i,j]==1:
               color = (0,0,255)                          # player 0 = red
            if state[i,j]==-1:
               color = (0,255,255)                        # player 1 = yellow
            screen = cv2.circle(screen, (25 +j*50,25+i*50), 20, color, -1,cv2.LINE_AA)   # draws a filled circle in the middle of the square

      cv2.imshow('ConnectFour',screen)                    # shows the board
      cv2.waitKey(ms)                                     # keeps the board up for milliseconds before the next move

class Quarto:                        # start of the code for quarto
   # each piece is a number 0-15 and has 4 traits (1 = yes, 0 = no): tall, dark, square, hollow
   traits = [[0,0,0,0],[0,0,0,1],[0,0,1,0],[0,0,1,1],
             [0,1,0,0],[0,1,0,1],[0,1,1,0],[0,1,1,1],
             [1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1],
             [1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]
   def __init__(self):
      board = np.zeros((4,4)).astype(int) - 1   # the board is 4x4, -1 = empty square
      piece = np.random.randint(16)             # the first piece to place is picked at random
      self.state = (board,piece)                # the state is the board and the piece to place
      self.ticks=-1
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      board = state[0]
      piece = state[1]
      moves = []
      for i in range(4):
         for j in range(4):
            if board[i,j]==-1:                   # empty square = you can place the piece there
               for p in range(16):
                  if p not in board and p!=piece:   # a piece that is still left to give
                     moves.append((i,j,p))       # move = (row, column, piece to give the other player)
      if len(moves)==0:                          # last piece of the game, nothing left to give
         for i in range(4):
            for j in range(4):
               if board[i,j]==-1:
                  moves.append((i,j,-1))
      return moves
   def getSuccessor(self, move, state):
      board = state[0]
      piece = state[1]
      board[move[0],move[1]] = piece             # place the piece on the square
      return (board,move[2])                     # the other player now has to place the piece the other player gave them
   def doMove(self,move):
      self.state = self.getSuccessor(move,self.state)
      self.ticks+=1
   def isTerminal(self, state=None):
      if state is None:
         state = self.state
      terminal = False
      val = self.evalTerminal(state)
      if val==0 and np.sum(state[0]!=-1)==16:    # nobody won and the board is full = draw
         terminal = True
      if val!=0:                                 # someone won
         terminal = True
      return terminal
   def evalTerminal(self, state=None):
      if state is None:
         state = self.state
      board = state[0]
      win = False

      for i in range(4):                         # row check
         if board[i,0]!=-1 and board[i,1]!=-1 and board[i,2]!=-1 and board[i,3]!=-1:
            for t in range(4):                   # check each of the 4 traits
               total = self.traits[board[i,0]][t] + self.traits[board[i,1]][t] + self.traits[board[i,2]][t] + self.traits[board[i,3]][t]
               if total==4 or total==0:          # all 4 pieces share this trait
                  win = True

      for j in range(4):                         # column check
         if board[0,j]!=-1 and board[1,j]!=-1 and board[2,j]!=-1 and board[3,j]!=-1:
            for t in range(4):
               total = self.traits[board[0,j]][t] + self.traits[board[1,j]][t] + self.traits[board[2,j]][t] + self.traits[board[3,j]][t]
               if total==4 or total==0:
                  win = True

      if board[0,0]!=-1 and board[1,1]!=-1 and board[2,2]!=-1 and board[3,3]!=-1:      # diagonal check going down-right
         for t in range(4):
            total = self.traits[board[0,0]][t] + self.traits[board[1,1]][t] + self.traits[board[2,2]][t] + self.traits[board[3,3]][t]
            if total==4 or total==0:
               win = True

      if board[3,0]!=-1 and board[2,1]!=-1 and board[1,2]!=-1 and board[0,3]!=-1:      # diagonal check going up-right
         for t in range(4):
            total = self.traits[board[3,0]][t] + self.traits[board[2,1]][t] + self.traits[board[1,2]][t] + self.traits[board[0,3]][t]
            if total==4 or total==0:
               win = True

      val = 0
      if win==True:
         if np.sum(board!=-1)%2==1:              # odd number of pieces = player 0 placed the last piece
            val = 1
         else:                                   # even number of pieces = player 1 placed the last piece
            val = -1
      return val
   def getWinner(self, state=None):
      if state is None:
         state = self.state
      val = self.evalTerminal(state)
      if val==1:
         return 0                                # player 0 won
      elif val==-1:
         return 1                                # player 1 won
      else:
         return -1                               # draw
   def showState(self, ms = 1000,state=None):    # draws the board in a pop up window
      if state is None:
         state = self.state
      board = state[0]

      screen = np.zeros((400,400)).astype(np.uint8)              # 4 rows x 4 columns, 100 pixels each
      for k in range(1,4):                                         # 3 lines across and 3 lines down
         screen = cv2.line(screen,(0,k*100),(399,k*100),255)
         screen = cv2.line(screen,(k*100,0),(k*100,399),255)

      for i in range(4):                                           # goes through every row
         for j in range(4):                                        # goes through every column
            if board[i,j]!=-1:                                     # there is a piece here
               p = board[i,j]
               size = 20                                           # short = small
               if self.traits[p][0]==1:
                  size = 40                                        # tall = big
               fill = 2                                            # light = outline
               if self.traits[p][1]==1:
                  fill = -1                                        # dark = filled in
               if self.traits[p][2]==1:                            # square
                  screen = cv2.rectangle(screen,(50+j*100-size,50+i*100-size),(50+j*100+size,50+i*100+size),255,fill)
               else:                                               # round
                  screen = cv2.circle(screen,(50+j*100,50+i*100),size,255,fill,cv2.LINE_AA)
               if self.traits[p][3]==1:                            # hollow = gray dot in the middle
                  screen = cv2.circle(screen,(50+j*100,50+i*100),6,128,-1,cv2.LINE_AA)

      cv2.imshow('Quarto',screen)                                  # shows the board
      cv2.waitKey(ms)                                              # keeps the board up for ms milliseconds
