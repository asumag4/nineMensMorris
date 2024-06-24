Notes: 
- This game will be a recreation of the two player game, Nine Men's Morris. 
1. Players will be able to place their tokens down 
2. Players will then be able to re-position their markers 
2b. If they have a three in a row, they are granted the ability to remove markers 

(05/15/2024) Will start small and create only the board game as of now 

(0/5/17/2024) 
Notes:
1. gameBoard should be it's own surface 
2. use for loop +list to draw the concentric rectangles on the gameBoard 
3. Make function creatMap() more concise with a for loop 
4. Create images for all, you already have all the shapes in variables, just so the game can look better! 

Progress Report: 
1. Made the board layout 
2. Made sprites for the "positions" so that a player's "tokens" can interact with them. Set occupancy states

(05/18/2024)
Notes: 
1. Was able to display the player's tokens, however the functionality was no there yet. 
2. Having issues making the drag and drop functionality to work.

(05/20/2024)
1. With the help of ChatGPT, the solution for the drag and drop functionality was to initalize the 
players outside of the while loop (because it would keep refreshing to the initialized state for the players).
As well, the solution is that the tokens should be a separate sprite class outside of the player class
2. However, because ChatGPT was only able to solve it for Player1, now I will make it so that it will be for both players! 
3. Implemented intialization for both players 
4. Now the solution for the positions would have to be similar to the solution for 
4a. *DONE Class baseManager that over-archs/ monitors all the positions 
4b. *DONE Class base that creates each sprite bases with its own interactive properties 
4c. *INPROGRESS Then implement the clashes between player's tokens and bases 

(05/21/2024)
1. Added the clash between players and tokens and bases 
1a. To Sprite-Base Class: setOccupied() to set the occupancy status of the base 
1b. To Sprite-Base Class: checkCollision method to check if a token is colliding with the base and if the base is not 
already occupied 
1c. Main loop:  When the mouse button is released (pygame.MOUSEBUTTONUP), the code iterates over all bases to check if the 
active token collides with any base. If it does, the token's position is updated to the center of the base, and the base 
is marked as occupied
1d. The 'activeToken' is then set to 'None' to indicate that the token is no longer being dragged. 

(05/24/2024)
Now working on the first stage of the game. 
1. Players will be able to place their tokens down 
2. Do so in sequential order 

(05/30/2024)
Now work on the TAKE_TOKENS stage of the game
1. Must be able to assess "three in a row", either horizontally or vertically
2. Must implement function to TAKE_TOKENS during PLACING_TOKENS

(05/31/2024)
Running into issues where the code is getting too complex. 
1. The problem is being able to checkIfThreeInARow -> letting player take opponent's peices if(true), but in the same loop, if those circumstances !True, 
    then changing turns. 
2. 

(06/02/2024)
For picking up peices: 
gameState = PHASE1
Player must pick up from the sides and place it on the board at an open spot 
Control with vars; placed == False & eliminated == False 
gameState = PHASE2
Player must pick up active pieces on the board and move it, player must not "skip" turns
Control with vars; placed == True & eliminated == False 

For eliminating peices; 
On the opponent's list of tokens, if placed == True && eliminated == False, you may eliminate these peices

(06/03/2024)
Checklist
1. Implement the phases, for phase 1 make sure only the tokens that are to be placed are 
2. Implement the phase for not being able to take the tokens again 
3. Implement the taking of the opponent's tokens 

(06//07/2024)
- Completing the checklist from previous date 
- NEED to fix the accidentally dropping feature with each turn 
- Need to implement a checking system of finishing the turn so that it changes turns. 

(06/14/2024)
- Will need to reconstruct the architecture of the game logic to implement the taking feature 
- Check out the functional solution provided by ChatGPT 

(06/17/2024)
- Implemented the taking feature correctly via functional solution for changing turns + using game loop for eventListener to take an opponent's token 
- Still need to fix bugs from (06/07/2024)
- Next step: add in the feature to move non-eliminated peices 
- Need to fix: can't eliminate non-placed peices 
- Should add: a Turn sign 
- Should add: elimination sign 
