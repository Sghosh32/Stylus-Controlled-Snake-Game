
#Importing necessary libraries
import cv2 as cv
import numpy as np
import pygame, sys, time, random, os

cap = cv.VideoCapture(0) #Starts video capture

#Initializing coordinates of centroid
centroid_x = 0
centroid_y = 0

#Size of the game window
width = 640
height = 480

#Initial starting score
score = 0

#Defining some colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
hurdle_color = (50, 92, 96)

#Used to control the fps of the game
clock = pygame.time.Clock()


def program():
    while 1:
        ret, frame = cap.read() #Reads frames from the camera
        frame = cv.flip(frame, 1) #Flips the frame horizontally
        blur = cv.GaussianBlur(frame, (5, 5), 0) #Applying Gaussian Blur to reduce noise
        blur=cv.flip(blur, 1) #Flipping the blurred frame
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV) #Converting from BGR to HSV 
        
        lower = np.array([24, 127, 75], dtype = np.uint8) #Lower HSV values of the stylus
        upper = np.array([179, 255, 255], dtype = np.uint8) #Higher HSV values of the stylus

        mask = cv.inRange(hsv, lower, upper) #Assigning range of HSV values in mask

        #Noise reduction 
        matrix = np.ones((4, 4), np.uint8) #Kernel defined specifically for closing and dilation
        close = cv.morphologyEx(mask, cv.MORPH_CLOSE, matrix) #Closing operation on mask 
        dilate = cv.dilate(close, matrix, iterations = 2) #Dilation operation on mask 
        dilate = cv.flip(dilate, 1) #Flipping the dilated frame
        ret1, thresh = cv.threshold(dilate, 127, 255, 0) #Thresholding

        contours, _ = cv.findContours(thresh, 1, 2) #Finding the contours
        
        #Lines to divide and name the region in the Stylus Detected Frame
        frame = cv.line(frame, (0, 0), (640, 480), (0, 0, 0), 5)
        frame = cv.line(frame, (0, 480), (640, 0), (0, 0, 0), 5)
        frame = cv.putText(frame, 'RIGHT', (520, 250), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv.LINE_8)
        frame = cv.putText(frame, 'LEFT', (25, 250), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv.LINE_8)
        frame = cv.putText(frame, 'UP', (300, 50), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv.LINE_8)
        frame = cv.putText(frame, 'DOWN', (270, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2, cv.LINE_8)

        cv.imshow('Stylus Detected Frame', frame) #Displaying the Stylus Detected Frame
        cv.moveWindow("Stylus Detected Frame", 50, 50) #Adjusting the Stylus Detected Frame on the screen

        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break

        #Finding the centroid coordinates of the stylus
        if len(contours) > 0:
            cnt = contours[0]
            M = cv.moments(cnt)
            centroid_x = int(M['m10'] / M['m00']) #x-coordinate of centroid of stylus
            centroid_y = int(M['m01'] / M['m00']) #y-coordinate of centroid of stylus
            return centroid_x, centroid_y
            
#Defining a function to calculate the area of a triangle
def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


#Defining a Function to check if the given point lies within a triangle region
def region(x1, y1, x2, y2, x3, y3, cx, cy):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(cx, cy, x2, y2, x3, y3)
    A2 = area(x1, y1, cx, cy, x3, y3)
    A3 = area(x1, y1, x2, y2, cx, cy)
    if A == (A1 + A2 + A3):
        return True
    else:
        return False


#Obtaining centroid coordinate and checking its triangle region
cx, cy = program() #Calling the centroid from the program function
up = region(0, 0, 320, 240, 640, 0, cx, cy) #Region for stylus to make the snake go 'UP'
down = region(0, 480, 320, 240, 640, 480, cx, cy) #Region for stylus to make the snake go 'DOWN'
left = region(0, 0, 320, 240, 0, 480, cx, cy) #Region for stylus to make the snake go 'LEFT'
right = region(640, 0, 320, 240, 640, 480, cx, cy) #Region for stylus to make the snake go 'RIGHT'


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (630, 120)
pygame.init() #Initializing the pygame module

#Starting the game window
pygame.display.set_caption('The Snake Game') #Naming the window of the game
window = pygame.display.set_mode((width, height)) #Applying dimensions to the game window


#Declaring variables used in the game
snake_position = [width / 2 - 20, height / 2 - 20] #Initial snake head position
snake_body = [[width / 2 - 20, height / 2 - 20]] #Initial snake body position
food_x = random.randint(70, width - 60) #x-coordinate of food 
food_y = random.randint(70, height - 60) #y-coordinate of food
food_spawn = True #Setting condition that food will be spawned
direction = 'UP' #Initializing the direction of the snake movement
change = direction #Initializing the direction of change in snake movement

#Defining a function when the game gets over
def game_over():
    my_font = pygame.font.SysFont('arial', 50) #Color of the text
    game_over_surface = my_font.render('GAME OVER', True, green) #Game over text
    game_over_rect = game_over_surface.get_rect() #Creating a surface to merge the text to
    game_over_rect.midtop = (width / 2, height / 4) 
    window.fill(blue) #Fills the screen with blue color
    window.blit(game_over_surface, game_over_rect) #Merges the surface and the text
    show_score(0, green, 'times', 40) #Show the final score
    pygame.display.flip() #Make the screen surface visible
    time.sleep(7) #To delay the program from ending by 7 secs
    pygame.quit() #Quiting the game
    sys.quit()


#Defining a Function to display the Score at the top
def show_score(choice, color, font, size):
    pygame.draw.rect(window, (169, 96, 50), pygame.Rect(0, 0, width, 30))
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width / 10, 30)
    else:
        score_rect.midtop = (width / 2.5, height / 1.5)
    window.blit(score_surface, score_rect)


#Defining functions for generating obstacles in the game
def hurdle_1():
    pygame.draw.rect(window, hurdle_color, pygame.Rect(300, 130, 240, 20))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(50, 190, 200, 20))

def hurdle_2():
    pygame.draw.rect(window, hurdle_color, pygame.Rect(120, 150, 30, 100))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(120, 140, 120, 20))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(400, 260, 20, 130))

def hurdle_3():
    pygame.draw.rect(window, hurdle_color, pygame.Rect(100, 280, 120, 20))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(220, 280, 20, 130))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(400, 100, 20, 130))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(420, 210, 120, 20))

def hurdle_4():
    pygame.draw.rect(window, hurdle_color, pygame.Rect(100, 140, 200, 20))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(280, 160, 20, 120))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(300, 260, 200, 20))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(480, 280, 20, 100))

def hurdle_5():
    pygame.draw.rect(window, hurdle_color, pygame.Rect(130, 130, 100, 100))
    pygame.draw.rect(window, hurdle_color, pygame.Rect(420, 290, 100, 100))

hur = random.choice([0,1,2,3,4]) #Using the random function to choose an obstacle at random

#Snake Game logic
while True:
    up = region(0, 0, 320, 240, 640, 0, cx, cy)
    down = region(0, 480, 320, 240, 640, 480, cx, cy)
    left = region(0, 0, 320, 240, 0, 480, cx, cy)
    right = region(640, 0, 320, 240, 640, 480, cx, cy)

    #Assigning directions to the snake's movements
    if up:
        change = 'UP'
    if down:
        change = 'DOWN'
    if left:
        change = 'LEFT'
    if right:
        change = 'RIGHT'

    #Making sure the snake cannot move in the opposite direction instantaneously
    if change == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #Snake movements
    if direction == 'UP':
        snake_position[1] -= 7 #Snake moves up 7 units
    if direction == 'DOWN':
        snake_position[1] += 7 #Snake moves down 7 units
    if direction == 'LEFT':
        snake_position[0] -= 7 #Snake moves left 7 units
    if direction == 'RIGHT':
        snake_position[0] += 7 #Snake moves right 7 units

    #Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    #Setting condition to register when the food is eaten
    if (abs(snake_position[0] - food_x) < 10 and abs(snake_position[1] - food_y) < 10):
        score += 10 #Increment in score after eating food
        food_spawn = False
    else:
        snake_body.pop()

    #Food spawning
    if not food_spawn:
        food_x = random.randint(70, width - 60)
        food_y = random.randint(70, height - 60)
    food_spawn = True

    #Displaying the Game Screen
    window.fill((19, 238, 41))
    if hur == 0:
        hurdle_1()
    elif hur == 1:
        hurdle_2()
    elif hur == 2:
        hurdle_3()
    elif hur == 3:
        hurdle_4()
    else:
        hurdle_5()

    pygame.draw.line(window, (245, 102, 66), (0, 64), (640, 64), 10)
    pygame.draw.line(window, (245, 102, 66), (4, 65), (4, 480), 10)
    pygame.draw.line(window, (245, 102, 66), (0, 475), (640, 475), 10)
    pygame.draw.line(window, (245, 102, 66), (634, 65), (634, 480), 10)

    #Snake body
    for position in snake_body:
        pygame.draw.rect(window, black, pygame.Rect(position[0], position[1], 10, 10))

    #Snake food
    pygame.draw.rect(window, red, pygame.Rect(food_x, food_y, 10, 10))

    #Setting conditions for game over
    #Getting out of bounds of the screen
    if snake_position[0] < 10 or snake_position[0] > width - 20:
        game_over()
        break
    if snake_position[1] < 70 or snake_position[1] > height - 20:
        game_over()
        break

    #Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
            break

    # Touching the obstacles
    if hur == 0:
        if (290 < snake_position[0] < 540 and 120 < snake_position[1] < 150) or (
                40 < snake_position[0] < 300 and 180 < snake_position[1] < 210):
            food_spawn = True
            game_over()
            break
    elif hur == 1:
        if (100 < snake_position[0] < 150 and 100 < snake_position[1] < 250) or (
                80 < snake_position[0] < 300 and 160 < snake_position[1] < 210) or (
                390 < snake_position[0] < 420 and 250 < snake_position[1] < 390):
            food_spawn = True
            game_over()
            break
    elif hur == 2:
        if (90 < snake_position[0] < 220 and 270 < snake_position[1] < 300) or (
                210 < snake_position[0] < 240 and 270 < snake_position[1] < 410) or (
                390 < snake_position[0] < 420 and 90 < snake_position[1] < 230) or (
                410 < snake_position[0] < 540 and 200 < snake_position[1] < 230):
            food_spawn = True
            game_over()
            break
    elif hur == 3:
        if (90 < snake_position[0] < 300 and 130 < snake_position[1] < 160) or (
                270 < snake_position[0] < 300 and 150 < snake_position[1] < 280) or (
                290 < snake_position[0] < 500 and 250 < snake_position[1] < 280) or (
                470 < snake_position[0] < 500 and 270 < snake_position[1] < 380):
            food_spawn = True
            game_over()
            break
    else:
        if (120 < snake_position[0] < 230 and 120 < snake_position[1] < 230) or (
                410 < snake_position[0] < 520 and 280 < snake_position[1] < 390):
            food_spawn = True
            game_over()
            break

    show_score(1, black, 'times new roman', 30)
    #Refreshing game screen
    pygame.display.update()
    #Refreshing refresh rate
    clock.tick(10)
    cx, cy = program()

#Release the capture and destroy all the open windows
cv.destroyAllWindows()
cap.release()
