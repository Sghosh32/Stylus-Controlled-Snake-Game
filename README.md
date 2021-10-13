# Stylus-Controlled-Snake-Game
#### Task:- Creating a snake game which can be played using a stylus

1. Initialize the coordinates of the centroid of the stylus, score and define some colors.
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
9. Thresholding is applied to get the required part in stylus.
10. The contour is obtained after dilation is done.
11. Draw 2 diagonal lines to divide the area into 4 different triangles, namely UP, DOWN, LEFT and RIGHT.
12. Find the moment and the centroid of the stylus.
13. If 'esc' is pressed, break the frame capturing sequence. 

### B) Defining Functions:-
1. Define a function to calculate the area of a triangle.
2. Define a function to check if a point lies inside a triangular region or not.
3. Call the centroid coordinates from the 'program' function and define 4 direction variables namely up, down, left and right which will check if the stylus is in that particular    triangular area or not.
4. Define a function to show the score when the game is being played.
5. Define a function to show the final score and a 'GAME OVER' screen after the game gets over.
6. Define some functions which will act as obstacles in the snake game.
7. Use the random function to randomly call any of the defined obstacles.

### C) Snake Game Logic:-
1. Call the centroid coordinates and use the 4 direction variables defined in point 3 in part B.
2. Assign those directions to the snake's movements.
3. Make sure the snake's next movement cannot be the reverse of the current direction it's moving in.
4. If the snake's movements matches any of the direction variables, move the snake in that specific direction.
5. Use the random function to select the x and y coordinate of the food.
6. When the snake eats the food, increment the score by 10 and the length of the snake.
7. Call the hurdle function to add hurdle to the snake game.
8. For the game to be over, we need either of the conditions to be true:-
   1. The snake head touching the boundary of the screen.
   2. The snake head touching its own body.
   3. The snake head touching any of the obstacles.
   
### Video Demonstration:-
https://drive.google.com/file/d/1RUTrF50AfOItFan_zOPF-X7gkU6N10GI/view?usp=sharing
