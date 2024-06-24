# Nine Men's Morris 

import pygame
from sys import exit
import pygame.sprite
import time

pygame.init()

# Open up the window
WINDOW_WIDTH = 1280 * 0.8
WINDOW_HEIGHT = 1000 * 0.8 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Nine Men\'s Morris')

# Create parameters for the game
clock = pygame.time.Clock()
activeToken = None

testFont = pygame.font.Font(None, 50)
testWriteOut = ''

INTRO = 0 
PHASE1 = 1
PHASE2 = 2
gamePhase = PHASE1

PLAY = 3 
TAKE = 4
gameState = 3

# Checked Turns Variable 
checkTurns = 0

# player1 = True, player2 = False
turn = True

# Game board parameters
gameBoardDimensions = 701
LAYER1FACTOR = 3 / 4
LAYER2FACTOR = 2 / 4
LAYER3FACTOR = 1 / 4

def createMap():
    THICKLINES = 8
    THINLINES = 6

    # Draw the "arena"
    # Layer 1
    layer1Shift = (gameBoardDimensions - (gameBoardDimensions * LAYER1FACTOR)) / 2
    layer1 = pygame.draw.rect(screen, (0, 0, 0), [((WINDOW_WIDTH - gameBoardDimensions) / 2) + layer1Shift, ((WINDOW_HEIGHT - gameBoardDimensions) / 2) + layer1Shift, gameBoardDimensions * LAYER1FACTOR, gameBoardDimensions * LAYER1FACTOR], THINLINES)

    # Layer 2
    layer2Shift = (gameBoardDimensions - (gameBoardDimensions * LAYER2FACTOR)) / 2
    layer2 = pygame.draw.rect(screen, (0, 0, 0), [((WINDOW_WIDTH - gameBoardDimensions) / 2) + layer2Shift, ((WINDOW_HEIGHT - gameBoardDimensions) / 2) + layer2Shift, gameBoardDimensions * LAYER2FACTOR, gameBoardDimensions * LAYER2FACTOR], THICKLINES)

    # Layer 3
    layer3Shift = (gameBoardDimensions - (gameBoardDimensions * LAYER3FACTOR)) / 2
    layer3 = pygame.draw.rect(screen, (0, 0, 0), [((WINDOW_WIDTH - gameBoardDimensions) / 2) + layer3Shift, ((WINDOW_HEIGHT - gameBoardDimensions) / 2) + layer3Shift, gameBoardDimensions * LAYER3FACTOR, gameBoardDimensions * LAYER3FACTOR], THINLINES)

    pygame.draw.line(screen, (0, 0, 0), layer3.midleft, layer1.midleft, THICKLINES)
    pygame.draw.line(screen, (0, 0, 0), layer3.midright, layer1.midright, THICKLINES)
    pygame.draw.line(screen, (0, 0, 0), layer3.midtop, layer1.midtop, THICKLINES)
    pygame.draw.line(screen, (0, 0, 0), layer3.midbottom, layer1.midbottom, THICKLINES)

    return layer1, layer2, layer3

# Sprite-Base Class: creates the sprite base to interact with tokens on the map
class Base(pygame.sprite.Sprite):
    def __init__(self, color, radius, position):
        super().__init__()

        self.occupied = False

        self.color = color
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
    
    def setOccupied(self, status):
        self.occupied = status

    def checkCollision(self, token):
        return self.rect.colliderect(token.rect) and not self.occupied

# baseManager Class: manages bases that are created
class BaseManager:
    def __init__(self, layer1, layer2, layer3):
        self.bases = pygame.sprite.Group()
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3

    def createBases(self):
        for layer in [self.layer1, self.layer2, self.layer3]:
            for side in ['topright', 'topleft', 'midtop', 'midbottom', 'midleft', 'midright', 'bottomleft', 'bottomright']:
                base = Base("black", 16, getattr(layer, side))
                self.bases.add(base)
        return self.bases
    
    def draw(self, surface):
        self.bases.draw(surface)

""" 
Sprite-Token class: tokens that are held by each Sprite-Player class 
- To use the click and drag function, 1. create Image 2. create Rect 3. Update Image to rect when rect is dragged by the mouse 
"""
class Token(pygame.sprite.Sprite):
    def __init__(self, color, radius, position):
        super().__init__()
        self.position = position
        self.color = color
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=position)

        self.placed = False
        self.eliminated = False

    # Update method so that whenever the rect is moved, the image of the circle is also moved
    def update(self, position):
        self.rect.center = position

    def eliminate(self):
        self.color = "black"
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.position)  

    def setPlaced(self, status): 
        self.placed = status

# Sprite-Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, identifier):
        super().__init__()
        self.tokens = pygame.sprite.Group()
        self.id = identifier
        self.combinations = {
            "x" : [],
            "y" : [],
        }
    
    def createTokens(self):
        if self.id == 1:
            circleColor = "blue"
            xPosition = (WINDOW_WIDTH / 2) - (gameBoardDimensions / 2) - (200 * 0.5)
        else:
            circleColor = "red"
            xPosition = (WINDOW_WIDTH / 2) + (gameBoardDimensions / 2) + (200 * 0.5) 
        circleRadius = 20
        yPosition = 100

        for i in range(9):
            token = Token(circleColor, circleRadius, (xPosition, yPosition))
            yPosition += 45
            self.tokens.add(token)
    
    def draw(self, surface):
        self.tokens.draw(surface)

    def setCombos(self, axis, coordinates):
        self.combinations[axis].append(coordinates)

    # Keep updated on the rows that have been made and that have been removed
    def threeCombos(self, listOfCoordinates, axis): 
        for coord in listOfCoordinates:
            if coord not in self.combinations[axis]: 
                self.combinations[axis].append(coord)
                # Call the function to remove the opponent's token 
                takeOpponentToken()
            elif coord in self.combinations[axis]: 
                changeTurn()
        for value in self.combinations[axis]: 
            if value not in listOfCoordinates:
                self.combinations[axis].remove(value)
                changeTurn()

# Initialize player1
player1 = Player(1)
player1.createTokens()
# Intialize player2
player2 = Player(2)
player2.createTokens()

# Create the map and bases
layer1, layer2, layer3 = createMap()
basesInit = BaseManager(layer1, layer2, layer3)
bases = basesInit.createBases()

def changeTurn():
    global checkTurns 
    global turn

    checkTurns += 1 
    print(checkTurns)
    if checkTurns == 2: 
        turn = not turn 
        print(turn) # DEBUG
        checkTurns = 0

# Just a simple script that will find three numbers in a given list 
def checkThreeOccurrences(numbers):
    countDict = {}

    for number in numbers:
        if number in countDict:
            countDict[number] += 1
        else:
            countDict[number] = 1

        if countDict[number] == 3:
            print("Found three in a row") # DEBUG
            return countDict

    return None


def listThree(dict):
    """
    Create a function that will iterate over the dictionary, 
    and only append numbers that have a value of 3 
    """
    listOfThrees = []
    for key, value in dict.items():
        if value == 3:
            listOfThrees.append(key)
        else: 
            continue
    return listOfThrees 

def checkHistoryThree(player, listOfCoordinates, axis):
    threeInRow = checkThreeOccurrences(listOfCoordinates)
    print(threeInRow) # DEBUG 
    if (threeInRow != None): 
        threeInRow = listThree(threeInRow)
        player.threeCombos(threeInRow, axis)
    else:
        changeTurn()

def takeOpponentToken():
    global gameState 
    gameState = 4 

def takingToken(opponentsTokens, activeToken, turn, checkTurns, gameState):
    for token in opponentsTokens:
        if token.rect.collidepoint(event.pos) and token.placed == True:
            activeToken = token
            activeToken.eliminated = True
            activeToken.rect.x = (WINDOW_WIDTH / 2) + (gameBoardDimensions / 2) + 200
            activeToken.eliminate()
            activeToken = None
            turn = not turn
            checkTurns = 0
            gameState = 3 
    return activeToken, turn, checkTurns, gameState

def checkThreeInARow(player, playerTokens):
    # Check basic three in a row
    xPos = [] 
    yPos = []
    for token in playerTokens:
        if token.placed == True:
            xPos.append(token.rect.x)
            yPos.append(token.rect.y)

    checkHistoryThree(player, xPos, "x") 
    checkHistoryThree(player, yPos, "y") 

    return 

def pickUp(playerTokens, gamePhase): 
    for token in playerTokens:
        # Must add, can only pick up tokens that have not been eliminated 
        if gamePhase == PHASE1:
            if token.rect.collidepoint(event.pos) and token.placed == False and token.eliminated == False:
                activeToken = token
                return activeToken
        if gamePhase == PHASE2: 
            # Have to implement a feature where they cannot re-place token in the same base
            if token.rect.collidepoint(event.pos) and token.placed == True and token.eliminated == False:
                activeToken = token
                return activeToken
                
def drop(activeToken):
    # Check if the base is not already taken 

    for base in bases:
        if base.checkCollision(activeToken) and base.occupied != True:
            activeToken.update(base.rect.center)
            activeToken.setPlaced(True) 
            base.setOccupied(True)
            activeToken = None
            
            return activeToken

def turnWrite(turn): 
    if turn: 
        return 'Blue'
    else: 
        return 'Red'
    
while True:
    for event in pygame.event.get():
        # If the window is closed, stop the game 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        """ DRAG AND DROP FEATURE! """
        if gameState == 3:

            # Pick up feature for PHASE1 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if turn == True: 
                        activeToken = pickUp(player1.tokens, gamePhase)
                    else: 
                        activeToken = pickUp(player2.tokens, gamePhase)
                
            # Drop feature: Method for placing the token center on the base upon placing down the token  
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and activeToken is not None:
                    activeToken = drop(activeToken)
                    
                    if turn == 1: 
                        checkThreeInARow(player1, player1.tokens)
                    else: 
                        checkThreeInARow(player2, player2.tokens)
                
            # Dragging feature 
            if event.type == pygame.MOUSEMOTION:
                if activeToken is not None:
                    activeToken.update(event.pos)

        """ TAKE OPPONENTS TOKEN FEATURE """
        if gameState == 4:
            activeToken = None
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    if turn == True: 
                        activeToken, turn, checkTurns, gameState = takingToken(player2.tokens, activeToken, turn, checkTurns, gameState)
                    else: 
                        activeToken, turn, checkTurns, gameState = takingToken(player1.tokens, activeToken, turn, checkTurns, gameState)

    """ DRAWING THE BOARD """

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the game board background
    pygame.draw.rect(screen, '#C19A6B', [((WINDOW_WIDTH - gameBoardDimensions) / 2), ((WINDOW_HEIGHT - gameBoardDimensions) / 2), gameBoardDimensions, gameBoardDimensions])
    pygame.draw.rect(screen, '#654321', [((WINDOW_WIDTH - gameBoardDimensions) / 2), ((WINDOW_HEIGHT - gameBoardDimensions) / 2), gameBoardDimensions, gameBoardDimensions], 7)

    # Draw the bases and players
    basesInit.draw(screen)
    layer1, layer2, layer3 = createMap()

    player1.draw(screen)
    player2.draw(screen)

    # Check if all the tokens are placed 
    checkAllTokens = 0
    if gamePhase == PHASE1:
        for token in player1.tokens:
            if token.placed == True:
                checkAllTokens += 1
        for token in player2.tokens:
            if token.placed == True:
                checkAllTokens += 1
        print(f"Tokens placed: {checkAllTokens}")
        if checkAllTokens == 18:
            print("All tokens are placed")
            gamePhase = PHASE2

    # Check if a player's tokens are in three in a row 

    # Render the turn sign 
    turnWriteOut = turnWrite(turn)
    turnMessageSurface = testFont.render(f'{turnWriteOut}',True, turnWriteOut)
    turnMessageRect = turnMessageSurface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//8))
    screen.blit(turnMessageSurface, turnMessageRect)

    pygame.display.update()
    clock.tick(60)




