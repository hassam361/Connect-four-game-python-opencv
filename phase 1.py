import cv2
import numpy as np;
import math
class Circle_node:
    def __init__(self):
        self.drawn=False
        self.color='white'
        self.cX=-1
        self.cY=-1
        
class Board:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.img=None
        self.width=800
        self.height=540
        self.board=[[Circle_node() for j in range(cols)] for i in range(rows)]
        
    def init_image(self,img_path,width=800,height=540):
        self.img = cv2.imread(img_path)
        self.img=cv2.resize(self.img, (width, height))
        self.width,self.height=width,height
        cv2.namedWindow('Connect four game')
        self.detect_circles(self.img.copy())
        
    

    def detect_circles(self,im):
        
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        # Mask things that are in the "red" corner of HSV
        Lower = (0, 0, 0)
        Upper = (0, 0, 255)
        maskR = cv2.inRange(hsv, Lower, Upper)
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
        self.show_img(im)
        self.show_img(maskR)
        self.init_consider_circles(consider_circles)
        
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
                if self.board[i][j].drawn==False:
                    print('0',end=' ')
                else:
                    print('X',end=' ')
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
    def check_if_inside_circle(self,cX,cY,R): 
        if math.pow((ix-cX),2)+math.pow((iy-cY),2)<=math.pow(R,2):
            cv2.circle(self.img,(cX,cY),60,(0,0,255),-1)
            return True 
        else:
            return False
        
    def iterate_circle_cords(self):
        for i in range(self.rows):
            for j in range(self.cols):
                ret_bool=self.check_if_inside_circle(self.board[i][j].cX,self.board[i][j].cY,60)
                if ret_bool:
                    self.board[i][j].drawn=True
    
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
        cv2.destroyAllWindows()
        self.print_board()
                    
            
   
# initialize the board 
board=Board(4,6)

board.init_image("simple_board.jpg",800,540)

board.run_game()