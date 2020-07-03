import cv2
import numpy as np;
import math
import random
import time
class Circle_node:
    def __init__(self):
        self.drawn=False
        self.color='white'
        self.value='0'
        self.cX=-1
        self.cY=-1
class ROS:
    def __init__(self):
        self.winner='0'
    
    def checkIsConsecutiveFourInList(self,values):
        
        for i in range(len(values) - 3):
            isEqual = True
            k=0
            for j in range(i, i + 3):
                if values[j] == '0' or values[j] != values[j + 1]:
                    isEqual = False
                    break
                k+=1
            if isEqual:
                self.winner=values[k-1]
                return True
        return False

    def isConsecutiveFour(self,values):
        numberOfRows = len(values)
        numberOfColumns = len(values[0])
        # Check rows
        
        for i in range(numberOfRows):
            if self.checkIsConsecutiveFourInList(values[i]):
                return True


        # Check for columns 
        for j in range(numberOfColumns):
            column = numberOfRows * ['0']
            # Get a column into an array
            for i in range(numberOfRows):
                column[i] = values[i][j]

            if self.checkIsConsecutiveFourInList(column):
                return True
        # Check major diagonal (lower part)
        for i in range(numberOfRows - 3):
            numberOfElementsInDiagonal = min(numberOfRows - i, numberOfColumns)
            diagonal = numberOfElementsInDiagonal * ['0']
            for k in range(numberOfElementsInDiagonal):
                diagonal[k] = values[k + i][k]
            if self.checkIsConsecutiveFourInList(diagonal):
                return True
        # Check major diagonal (upper part)
        for j in range(1, numberOfColumns - 3):
            numberOfElementsInDiagonal = min(numberOfColumns - j, numberOfRows)
            diagonal = numberOfElementsInDiagonal * ['0']
            for k in range(numberOfElementsInDiagonal):
                diagonal[k] = values[k][k + j]
                if self.checkIsConsecutiveFourInList(diagonal):
                    return True
        # Check sub-diagonal (left part)
        for j in range(3, numberOfColumns):
            numberOfElementsInDiagonal = min(j + 1, numberOfRows)
            diagonal = numberOfElementsInDiagonal * ['0']
            for k in range(numberOfElementsInDiagonal):
                diagonal[k] = values[k][j - k]
                if self.checkIsConsecutiveFourInList(diagonal):
                    return True
        # Check sub-diagonal (right part)
        for i in range(1, numberOfRows - 3):
            numberOfElementsInDiagonal = min(numberOfRows - i, numberOfColumns)
            diagonal = numberOfElementsInDiagonal * ['0']
            for k in range(numberOfElementsInDiagonal):
                diagonal[k] = values[k + i][numberOfColumns - k - 1]
                if self.checkIsConsecutiveFourInList(diagonal):
                    return True
        return False

class Board:
    def __init__(self,rows,cols,mode='user'):
        self.rows=rows
        self.cols=cols
        self.img=None
        self.width=800
        self.height=540
        self.turn=1
        self.quit_game=False
        self.board=[[Circle_node() for j in range(cols)] for i in range(rows)]
        self.data=None
        self.roi=ROS()
        self.mode=mode
        
    def init_image(self,img_path,width=800,height=540):
        self.img = cv2.imread(img_path)
        self.img=cv2.resize(self.img, (width, height))
        self.width,self.height=width,height
        #cv2.namedWindow('Connect four game')
        # initialize data array
        self.data=['0']*self.rows
        for i in range(self.rows):
            self.data[i]=['0']*self.cols
            
        self.detect_circles(self.img.copy(),'white')
        
    

    def detect_circles(self,im,color):
        
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        # Mask things that are in the "red" corner of HSV
        if color=='white':
            Lower = (0, 0, 0)
            Upper = (0, 0, 255)
        
        elif color == 'black':
            Lower= (0, 0, 0)
            Upper= (180, 255, 30)
        elif color=='red':
            redLower= np.array([0,120,70])

            redUpper = np.array([10,255,255])

            mask1=cv2.inRange(hsv, redLower, redUpper)
            redLower=np.array([170,120,70])

            redUpper = np.array([180,255,255])

            mask2=cv2.inRange(hsv, redLower, redUpper)
        if color!='red':
            maskR = cv2.inRange(hsv, Lower, Upper)
            
        else:
            maskR=mask1+mask2
        # Smooth result (better actually with iterations=2)
        maskR = cv2.erode(maskR, None, iterations=1)
        maskR = cv2.dilate(maskR, None, iterations=1)
        
       
        # Detect contours around possible blobs
        cntsR = cv2.findContours(maskR.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cntsR = cntsR[0]
        # draw the biggest contour (c) in green
        consider_circles=[]
        cons_cnt=[]
        for c in cntsR:
        # compute the center of the contour

            x,y,w,h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            area=w*h
            area=np.array(area)
            if area>1500:

                cons_cnt.append(c)
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        
        contours_sorted=self.sort_contours(cons_cnt,maskR.copy())
        #print(contours_sorted)
        for i in range(len(contours_sorted)):
            cont_idx=contours_sorted[i][2]
            c=cons_cnt[cont_idx]
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            #cv2.drawContours(im, [c], -1, (0, 255, 0), 2)

            consider_circles.append((cX,cY))
            cv2.circle(im, (cX, cY), 7, (0, 255, 0), -1)
            #cv2.putText(im, "center", (cX - 20, cY - 20),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        if color== 'white':
            self.init_consider_circles(consider_circles)
        else:
            #self.show_img(im)
            #self.show_img(maskR)
            for i in range(self.rows):
                for j in range(self.cols):
                    for k in range(len(consider_circles)):

                        ret_bool=math.pow((consider_circles[k][0]-self.board[i][j].cX),2)+math.pow((consider_circles[k][1]-self.board[i][j].cY),2)<=math.pow(60,2)
                        if ret_bool:
                            if color=='black':
                                self.board[i][j].value='?'
                            elif color=='red':
                                self.board[i][j].value='X'
                            self.board[i][j].drawn=True
            
    def sort_contours(self,cons_cnt,img):
        # code for sorting contours
        h,w = img.shape[:2]
        # sum all rows
        sumOfRows = np.sum(img, axis=1)

        # loop the summed values
        startindex = 0
        lines = []
        compVal = True
        for i, val in enumerate(sumOfRows):
            # logical test to detect change between 0 and > 0
            testVal = (val > 0)
            if testVal == compVal:
                    # when the value changed to a 0, the previous rows
                    # contained contours, so add start/end index to list
                    if val == 0:
                        lines.append((startindex,i))
                    # update startindex, invert logical test
                        startindex = i+1
                    compVal = not compVal
        # create empty list
       
        lineContours = []
        # find contours (you already have this)
        contours=cons_cnt
       
        for j,cnt in enumerate(contours):

            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            for i,line in enumerate(lines):
                if y >= line[0] and y <= line[1]:
                    lineContours.append([line[0],x,j])
                    break

        # sort list on line number,  x value and contour index
        contours_sorted = sorted(lineContours)
        return contours_sorted 
    
    def show_img(self,img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):

                if self.board[i][j].value=='0':
                    print('0',end=' ')
                elif self.board[i][j].value=='X':
                    print('X',end=' ')
                elif self.board[i][j].value=='?':
                    print('?',end=' ')
              
            print()
    
    def init_consider_circles(self,consider_circles):
        k=0
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].cX=consider_circles[k][0]
                self.board[i][j].cY=consider_circles[k][1]
                k+=1
    # mouse callback function
    def draw_circle(self,event,x,y,flags,param):
        global ix,iy,drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            #cv2.circle(self.img,(x,y),60,(0,0,255),-1)
            
            ix,iy = x,y
            self.iterate_circle_cords()
    def drop_disk_validity(self,cX,cY,R): 
        if math.pow((ix-cX),2)+math.pow((iy-cY),2)<=math.pow(R,2):
            return True 
        else:
            return False
    def drop_disk(self,index,value): # where index is the column where you will place the disk
        for i in range(self.rows,0,-1):
            if self.board[i-1][index].value == '0':
                self.board[i-1][index].drawn=True
                self.board[i-1][index].value=value
                x=self.board[i-1][index].cX
                y=self.board[i-1][index].cY
                if value=='?':
                    cv2.circle(self.img,(x,y),60,(0,0,0),-1)
                elif value=='X':
                    cv2.circle(self.img,(x,y),60,(0,0,255),-1)
                self.check_connected_pairs() # this will check from ROI class
                break
    def get_board_data(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].value=='0':
                    self.data[i][j]='0'
                elif self.board[i][j].value=='X':
                    self.data[i][j]='X'
                elif self.board[i][j].value=='?':
                    self.data[i][j]='?'
        return self.data

    def iterate_circle_cords(self):
        for i in range(self.rows):
            for j in range(self.cols):
                ret_bool=self.drop_disk_validity(self.board[i][j].cX,self.board[i][j].cY,60)
                if ret_bool:
                    #self.board[i][j].drawn=True
                    #cv2.circle(self.img,(cX,cY),60,(0,0,255),-1)
                    
                    self.drop_disk(j,'X')
                    self.turn+=1
                    j=random.randint(0,self.cols-1)
                    self.drop_disk(j,'?')
                    #time.sleep(1)
                    self.turn+=1
                        
    def check_connected_pairs(self):
        
        self.data=self.get_board_data()          
        result=self.roi.isConsecutiveFour(self.data)
        if result==True:
            self.quit_game=True
            
        
        
    def recognize_state(self,user_img):
        #consider_circles=self.detect_circles(self.img.copy(),'white')
        orig_pic=user_img
        self.detect_circles(user_img.copy(),'black')
        self.detect_circles(user_img.copy(),'red')
        self.img=orig_pic.copy()
        if self.mode=='user':
            self.run_game()
        
                                
                            
        
    
    
    def run_game(self):
        # Create a  image, a window and bind the function to window
        img = self.img
        img=cv2.resize(img, (self.width, self.height)) 
        cv2.namedWindow('image')

        cv2.setMouseCallback('image',self.draw_circle)

        while(1):

            cv2.imshow('image',self.img.copy())
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
            elif k == ord('a'):
                print (ix,iy)
            elif k == ord('s'):
                self.recognize_state(self.img)
            elif self.quit_game==True:
                break
        if self.roi.winner=='X':  
            win=cv2.imread('you_win.png',1)
            win=cv2.resize(win, (self.width, self.height))
            self.show_img(win)
            print("Contratulations you have won the game!!!")
        elif self.roi.winner=='?':
            lose=cv2.imread('you_lose.png',1)
            lose=cv2.resize(lose, (self.width, self.height))
            self.show_img(lose)
            print("You lose, Robot has won the match")
        cv2.destroyAllWindows()
        self.print_board()
                    
            
   
# initialize the board 
board=Board(4,6)
im = cv2.imread("state1.jpg")
width,height=800,540
im=cv2.resize(im, (width, height)) 
board.init_image("simple_board.jpg",800,540)
#board.show_img(im)
#board.recognize_state(im)
#board.print_board()
board.run_game()