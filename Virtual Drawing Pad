#Importing necessary libraries
import numpy as np 
import cv2 as cv

sheet = np.zeros((720, 800, 3), np.uint8) #Creating a black background to draw upon
sheet = cv.bitwise_not(sheet, sheet) #Creating a white background(optional)
x1, y1 = 0, 0 #Used for initializing the loop

cap = cv.VideoCapture(0) #Starts capturing the video
def program(x):
    pass
while(True):

    ret, frame = cap.read() #Reading frames from the camera
    frame = cv.flip(frame, 1) #flips the frame horizontally
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #Converting frame from bgr to hsv

    lower = np.array([26, 101, 185], dtype = np.uint8) #Lower HSV values of object 
    upper = np.array([47, 255, 255], dtype = np.uint8) #Higher HSV values of object 
  
    # Creation of a mask
    mask = cv.inRange(hsv, lower,upper) #Assigning range of hsv values for mask
    res = cv.bitwise_and(frame, frame, mask=mask) #Detection of yellow colour
    res_gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY) #Converting from bgr to gray
    ret, thresh = cv.threshold(res_gray, 24, 255, 0) #Thresholding 
    
    #Morphological Transforms
    matrix = np.ones((4, 4), np.uint8) #Kernel defined specifically for closing and dilation
    close = cv.morphologyEx(mask, cv.MORPH_CLOSE, matrix) #Closing operation on mask to remove noise
    dilate = cv.dilate(close, matrix, iterations = 2) #Dilation operation to remove dark areas in the mask

    #Finding contours of the object
    contours, _ = cv.findContours(dilate, 1, 2) #Contour detection
    contour_areas = [cv.contourArea(c) for c in contours] #Finding areas of all the contours
    cnt = contours[np.argmax(contour_areas)] #Index of the largest contour present 
    #Finding moment and centroid of the largest contour
    M = cv.moments(thresh) 
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    cv.drawContours(frame, contours, -1, (0, 0, 255), 4) #Highlighting the contour with the largest area 

    if x1 != 0 and y1 != 0: #Alloting condition for the 1st iteration
        cv.line(sheet, (x1, y1), (x, y), (255, 0, 0), 7) #Draw line between previous and current coordinate
    #Assigning the old coordinates to the end points of the new line for all the next iterations
    x1 = x
    y1 = y
    cv.imshow('white', sheet) #Displaying of the drawing pad
    cv.imshow('window', frame) #Displaying frame which tracks the centroid of the object

    if cv.waitKey(1) == ord('q'): #Delay of 1 millisecond to wait for user input
        break
#Release the capture and destroy all the open windows
cap.release()
cv.destroyAllWindows()


