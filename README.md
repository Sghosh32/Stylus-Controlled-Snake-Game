# Virtual-Drawing-Pad
#### Task:- Creating a virtual drawing pad that will track an object referred to as a "stylus" and sketch out its motion.

#### A) Assigning HSV values to the stylus
1. Use a camera to capture the frames.
2. Create trackbars to find the lower and higher HSV range of the stylus.
3. Convert the frame from BGR to HSV.
4. Create an array of the HSV values obtained.
5. Make a mask that sees the lower and the higher HSV values of the stylus.

#### B) Creating the Virtual Drawing Pad
1. Create a drawing space.
2. Use a camera to capture the frames.
3. Flip the frames horizontally to avoid lateral inversion.
4. Convert the frames from BGR to HSV.
5. Put the values of the lower and higher HSV values obtained in part A.
6. Create a mask using the values in point 5
7. Convert the mask from BGR to Grayscale and apply thresholding accordingly.
8. Applying closing on the mask to remove the noise present in the frames being captured.
9. Dilation is applied after closing to remove the dark areas in the mask and it is applied multiple times to get a consistent shade.
10. The contour of the image obtained after dilation is found.
11. Find the contour with the largest area and note down its index.
12. Find the moment and the centroid of the largest contour.
13. Allot an initial and a final condition to start the loop.
14. The centroid of the contour is tracked to draw the line.
15. Display the sheet and the frame.
16. If 'esc' is pressed, destroy all the windows.

# Stylus-Controlled-Snake-Game
#### Task:- Creating a snake game which can be played using a stylus

1. Initialize the coordinates of the centroid of the stylus, score, and define some colors.
2. Set the size of the game window.

### A) Frame Capturing:-
1. Use the camera to capture the frames.
2. Flip the frames horizontally to avoid lateral inversion.
3. Apply Gaussian blur to reduce the noise in the frames captured.
4. Convert the frames from BGR to HSV.
5. Put the values of the lower and higher HSV values in different arrays.
6. Create a mask using the values in point 5.
7. Applying closing on the mask to remove the noise present in the frames being captured.
8. Dilation is applied after closing to remove the dark areas in the mask and it is applied twice to get a consistent shade.
9. Thresholding is applied to get the required part in the stylus.
10. The contour is obtained after dilation is done.
11. Draw 2 diagonal lines to divide the area into 4 different triangles, namely UP, DOWN, LEFT, and RIGHT.
12. Find the moment and the centroid of the stylus.
13. If 'esc' is pressed, break the frame-capturing sequence. 

![Snap](https://user-images.githubusercontent.com/89793505/137143426-98663d3e-9de2-46fe-81f3-ac8ae3f8dcfa.png)
### **Dividing the frame into 4 equal regions** 

### B) Defining Functions:-
1. Define a function to calculate the area of a triangle.
2. Define a function to check if a point lies inside a triangular region or not.
3. Call the centroid coordinates from the 'program' function and define 4 direction variables namely up, down, left, and right which will check if the stylus is in that particular    triangular area or not.
4. Define a function to show the score when the game is being played.
5. Define a function to show the final score and a 'GAME OVER' screen after the game is over.
6. Define some functions which will act as obstacles in the snake game.
7. Use the random function to randomly call any of the defined obstacles.

![ezgif com-gif-maker](https://user-images.githubusercontent.com/89793505/137146636-dca5119c-4865-42c5-a94b-3d0384e25208.gif)
### Snake movement in the region of stylus detection

### C) Snake Game Logic:-
1. Call the centroid coordinates and use the 4 direction variables defined in point 3 in part B.
2. Assign those directions to the snake's movements.
3. Make sure the snake's next movement cannot be the reverse of the current direction it's moving in.
4. If the snake's movements match any of the direction variables, move the snake in that specific direction.
5. Use the random function to select the x and y coordinates of the food.
6. When the snake eats the food, increment the score by 10 and the length of the snake.
7. Call the hurdle function to add a hurdle to the snake game.
8. For the game to be over, we need either of the conditions to be true:-
   1. The snake's head touching the boundary of the screen.
   2. The snake's head touching its own body.
   3. The snake's head touching any of the obstacles.
   
### Video Demonstration:-
https://drive.google.com/file/d/1RUTrF50AfOItFan_zOPF-X7gkU6N10GI/view?usp=sharing
