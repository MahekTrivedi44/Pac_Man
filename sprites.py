import pygame  # Importing the pygame library for game development.
from constants import *  # Importing constants module containing game constants.
import numpy as np  # Importing numpy library for numerical operations.
from animation import Animator  # Importing Animator class from animation module.
from Choose import *  # Importing Choose module.

BASETILEWIDTH = 16  # Setting the base width of a tile.
BASETILEHEIGHT = 16  # Setting the base height of a tile.
DEATH = 5  # Constant representing the death state.
numlives = 3  # Initializing the number of lives.
class Spritesheet(object):  # Defining a class for handling sprite sheets.
    def __init__(self):  # Constructor method for Spritesheet class.
        self.sheet = pygame.image.load(sp).convert()  # Loading sprite sheet image.
        transcolor = self.sheet.get_at((0,0))  # Getting the color of the top-left pixel as transparent color.
        self.sheet.set_colorkey(transcolor)  # Setting transparent color for the sprite sheet.
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)  # Calculating width of sprite sheet in pixels.
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)  # Calculating height of sprite sheet in pixels.
        self.sheet = pygame.transform.scale(self.sheet, (width, height))  # Scaling the sprite sheet.

    def getImage(self, x, y, width, height):  # Method to extract image from sprite sheet.
        x *= TILEWIDTH  # Calculating x-coordinate of image in pixels.
        y *= TILEHEIGHT  # Calculating y-coordinate of image in pixels.
        self.sheet.set_clip(pygame.Rect(x, y, width, height))  # Setting clipping region on sprite sheet.
        return self.sheet.subsurface(self.sheet.get_clip())  # Returning the clipped portion as image.
class PacmanSprites(Spritesheet):  # Class for handling Pacman sprites.
    def __init__(self, entity):  # Constructor method for PacmanSprites class.
        Spritesheet.__init__(self)  # Calling constructor of parent class.
        self.entity = entity  # Storing the Pacman entity.
        self.entity.image = self.getStartImage()  # Setting the initial image for Pacman.
        self.animations = {}  # Initializing dictionary to hold animations.
        self.defineAnimations()  # Defining animations for Pacman.
        self.stopimage = (8, 0)  # Default image when Pacman stops moving.
    def defineAnimations(self):  # Method to define animations for Pacman.
        # Defining animations for different directions and actions.
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)             
    def update(self, dt):  # Method to update Pacman's animation.
        if self.entity.alive == True:  # Checking if Pacman is alive.
            if self.entity.direction == LEFT:  # If Pacman is moving left.
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))  # Updating image based on animation frame.
                self.stopimage = (8, 0)  # Setting the default stop image for left direction.
            elif self.entity.direction == RIGHT:  # If Pacman is moving right.
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))  # Updating image based on animation frame.
                self.stopimage = (10, 0)  # Setting the default stop image for right direction.
            elif self.entity.direction == DOWN:  # If Pacman is moving down.
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))  # Updating image based on animation frame.
                self.stopimage = (8, 2)  # Setting the default stop image for down direction.
            elif self.entity.direction == UP:  # If Pacman is moving up.
                self.entity.image = self.getImage(*self.animations[UP].update(dt))  # Updating image based on animation frame.
                self.stopimage = (10, 2)  # Setting the default stop image for up direction.
            elif self.entity.direction == STOP:  # If Pacman is not moving.
                self.entity.image = self.getImage(*self.stopimage)  # Setting the stop image.
        else:  # If Pacman is not alive.
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))  # Updating image based on death animation.

    def reset(self):  # Method to reset animations.
        for key in list(self.animations.keys()):  # Iterating over animation keys.
            self.animations[key].reset()  # Resetting each animation.

    def getStartImage(self):  # Method to get the starting image for Pacman.
        return self.getImage(8, 0)  # Returning the image for Pacman facing left.

    def getImage(self, x, y):  # Method to get image from sprite sheet.
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)  # Returning the image.


class GhostSprites(Spritesheet):  # Class for handling Ghost sprites.
    def __init__(self, entity):  # Constructor method for GhostSprites class.
        Spritesheet.__init__(self)  # Calling constructor of parent class.
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}  # Dictionary to map ghost names to their x-coordinate.
        self.entity = entity  # Storing the Ghost entity.
        self.entity.image = self.getStartImage()  # Setting the initial image for Ghost.

    def update(self, dt):  # Method to update Ghost's animation.
        x = self.x[self.entity.name]  # Getting the x-coordinate of the Ghost.

        # Checking the current mode of the Ghost.
        if self.entity.mode.current in [SCATTER, CHASE]:  # If Ghost is in scatter or chase mode.
            if self.entity.direction == LEFT:  # If Ghost is moving left.
                self.entity.image = self.getImage(x, 8)  # Setting image for left movement.
            elif self.entity.direction == RIGHT:  # If Ghost is moving right.
                self.entity.image = self.getImage(x, 10)  # Setting image for right movement.
            elif self.entity.direction == DOWN:  # If Ghost is moving down.
                self.entity.image = self.getImage(x, 6)  # Setting image for downward movement.
            elif self.entity.direction == UP:  # If Ghost is moving up.
                self.entity.image = self.getImage(x, 4)  # Setting image for upward movement.
        elif self.entity.mode.current == FREIGHT:  # If Ghost is in fright mode.
            self.entity.image = self.getImage(10, 4)  # Setting fright mode image.
        elif self.entity.mode.current == SPAWN:  # If Ghost is in spawn mode.
            if self.entity.direction == LEFT:  # If Ghost is moving left.
                self.entity.image = self.getImage(8, 8)  # Setting image for leftward spawn.
            elif self.entity.direction == RIGHT:  # If Ghost is moving right.
                self.entity.image = self.getImage(8, 10)  # Setting image for rightward spawn.
            elif self.entity.direction == DOWN:  # If Ghost is moving down.
                self.entity.image = self.getImage(8, 6)  # Setting image for downward spawn.
            elif self.entity.direction == UP:  # If Ghost is moving up.
                self.entity.image = self.getImage(8, 4)  # Setting image for upward spawn.
               
    def getStartImage(self):  # Method to get the starting image for Ghost.
        return self.getImage(self.x[self.entity.name], 4)  # Returning the image for Ghost's starting position.

    def getImage(self, x, y):  # Method to get image from sprite sheet.
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)  # Returning the image.



class FruitSprites(Spritesheet):
    # Define a class named FruitSprites that inherits from the Spritesheet class
    def __init__(self, entity, level):
        # Constructor method to initialize an instance of the FruitSprites class
        Spritesheet.__init__(self)
        # Call the constructor of the parent class (Spritesheet) to initialize inherited attributes
        self.entity = entity
        # Assign the entity parameter to the instance attribute 'entity'
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        # Define a dictionary 'fruits' with keys representing fruit types and values representing their coordinates
        self.entity.image = self.getStartImage(level % len(self.fruits))
        # Set the image attribute of the entity to the result of calling the getStartImage method with a computed index based on the level parameter

    def getStartImage(self, key):
        # Define a method named getStartImage which takes a key as input
        return self.getImage(*self.fruits[key])
        # Call the getImage method with coordinates corresponding to the key in the fruits dictionary and return the result

    def getImage(self, x, y):
        # Define a method named getImage which takes x and y coordinates as input
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)
        # Call the getImage method of the parent class (Spritesheet) with adjusted coordinates and return the result


class LifeSprites(Spritesheet):
    # Define a class named LifeSprites that inherits from the Spritesheet class
    def __init__(self, numlives):
        # Constructor method to initialize an instance of the LifeSprites class
        Spritesheet.__init__(self)
        # Call the constructor of the parent class (Spritesheet) to initialize inherited attributes
        self.resetLives(numlives)
        # Call the resetLives method with the numlives parameter to initialize the instance attribute 'images'

    def removeImage(self):
        # Define a method named removeImage
        if len(self.images) > 0:
            # Check if the length of the 'images' list is greater than 0
            self.images.pop(0)
            # Remove the first element from the 'images' list

    def resetLives(self, numlives):
        # Define a method named resetLives which takes numlives as input
        self.images = []
        # Initialize the instance attribute 'images' as an empty list
        for i in range(numlives):
            # Iterate over a range from 0 to numlives
            self.images.append(self.getImage(0,0))
            # Append an image obtained from calling the getImage method with coordinates (0, 0) to the 'images' list
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)# Define a method named getImage which takes x and y coordinates as input
        # Call the getImage method of the parent class (Spritesheet) with adjusted coordinates and return the result
class MazeSprites(Spritesheet): # Define a class named MazeSprites that inherits from the Spritesheet class
    def __init__(self, mazefile, rotfile):
        # Constructor method to initialize an instance of the MazeSprites class
        Spritesheet.__init__(self)
        # Call the constructor of the parent class (Spritesheet) to initialize inherited attributes
        self.data = self.readMazeFile(mazefile)
        # Assign the result of calling the readMazeFile method with the mazefile parameter to the instance attribute 'data'
        self.rotdata = self.readMazeFile(rotfile)
        # Assign the result of calling the readMazeFile method with the rotfile parameter to the instance attribute 'rotdata'
    def getImage(self, x, y):# Define a method named getImage which takes x and y coordinates as input
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)
        # Call the getImage method of the parent class (Spritesheet) with provided coordinates and return the result
    def readMazeFile(self, mazefile):# Define a method named readMazeFile which takes mazefile as input
        return np.loadtxt(mazefile, dtype='<U1')
        # Load a text file using NumPy and return the result as a numpy array of Unicode strings
    def constructBackground(self, background, y):# Define a method named constructBackground which takes background and y as input
        for row in list(range(self.data.shape[0])):
            # Iterate over each row index in the 'data' attribute
            for col in list(range(self.data.shape[1])):
                # Iterate over each column index in the 'data' attribute
                if self.data[row][col].isdigit():# Check if the current element in 'data' is a digit
                    x = int(self.data[row][col]) + 12# Convert the digit to an integer and add 12 to get the sprite index
                    sprite = self.getImage(x, y)# Get the sprite image using the obtained index and provided y coordinate
                    rotval = int(self.rotdata[row][col])# Obtain rotation value from the corresponding element in 'rotdata'
                    sprite = self.rotate(sprite, rotval)# Rotate the sprite image based on the rotation value
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT)) # Draw the rotated sprite onto the background surface at the appropriate position
                elif self.data[row][col] == '=':
                    # Check if the current element in 'data' is '='
                    sprite = self.getImage(10, 8)
                    # Get a specific sprite image for '='
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                    # Draw the sprite onto the background surface at the appropriate position
        return background
        # Return the modified background surface
    def rotate(self, sprite, value):
        # Define a method named rotate which takes a sprite and a rotation value as input
        return pygame.transform.rotate(sprite, value*90)
        # Rotate the sprite image by the specified angle (multiple of 90 degrees) using pygame's transformation function and return the result
