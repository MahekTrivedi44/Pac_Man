import pygame  # Importing the pygame library, used for developing games in Python.
from pygame.locals import *  # Importing specific constants and functions from pygame.locals module.
from vector import Vector2  # Importing the Vector2 class from a custom module named vector.
from constants import *  # Importing constants from a custom module named constants.
from entity import Entity  # Importing the Entity class from a custom module named entity.
from sprites import PacmanSprites  # Importing the PacmanSprites class from a custom module named sprites.

class Pacman(Entity):  # Defining a class named Pacman, which inherits from the Entity class.
    def __init__(self, node):  # Constructor method for Pacman class, takes a node parameter.
        Entity.__init__(self, node)  # Calling the constructor of the parent class with the node parameter.
        self.name = PACMAN  # Setting the name attribute of Pacman object to the value of PACMAN constant.
        self.color = YELLOW  # Setting the color attribute of Pacman object to the value of YELLOW constant.
        self.direction = LEFT  # Setting the initial direction attribute of Pacman object to LEFT.
        self.setBetweenNodes(LEFT)  # Calling a method to set Pacman between nodes in the LEFT direction.
        self.alive = True  # Setting the alive attribute of Pacman object to True.
        self.sprites = PacmanSprites(self)  # Creating an instance of PacmanSprites class and assigning it to sprites attribute.

    def reset(self):  # Method to reset Pacman object to its initial state.
        Entity.reset(self)  # Calling the reset method of the parent class.
        self.direction = LEFT  # Resetting the direction attribute to LEFT.
        self.setBetweenNodes(LEFT)  # Resetting Pacman between nodes in the LEFT direction.
        self.alive = True  # Setting the alive attribute to True.
        self.image = self.sprites.getStartImage()  # Setting the image attribute using a method from the sprites attribute.
        self.sprites.reset()  # Calling the reset method of the sprites attribute.

    def die(self):  # Method to handle Pacman's death.
        self.alive = False  # Setting the alive attribute to False.
        self.direction = STOP  # Setting the direction attribute to STOP.

    def update(self, dt):  # Method to update Pacman's state.
        self.sprites.update(dt)  # Calling the update method of the sprites attribute.
        self.position += self.directions[self.direction] * self.speed * dt  # Updating Pacman's position based on direction, speed, and time.
        direction = self.getValidKey()  # Getting a valid direction from user input.
        if self.overshotTarget():  # Checking if Pacman has overshot its target node.
            # Handling movement when Pacman reaches a target node.
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()  # Reversing Pacman's direction if it's opposite to the current direction.

    def getValidKey(self):  # Method to get valid input direction from the user.
        key_pressed = pygame.key.get_pressed()  # Getting the state of all keyboard keys.
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  # Returning STOP if no valid key is pressed.

    def eatPellets(self, pelletList):  # Method to handle Pacman eating pellets.
        for pellet in pelletList:
            if self.collideCheck(pellet):  # Checking collision between Pacman and pellets.
                return pellet
        return None  # Returning None if no pellet is eaten.

    def collideGhost(self, ghost):  # Method to check collision with ghosts.
        return self.collideCheck(ghost)  # Checking collision between Pacman and ghosts.

    def collideCheck(self, other):  # Method to check collision between Pacman and other objects.
        d = self.position - other.position  # Calculating the distance between Pacman and the other object.
        dSquared = d.magnitudeSquared()  # Calculating the squared magnitude of the distance vector.
        rSquared = (self.collideRadius + other.collideRadius) ** 2  # Calculating the sum of squared radii.
        if dSquared <= rSquared:  # Checking if the squared distance is less than or equal to the squared sum of radii.
            return True  # Returning True if collision occurs.
        return False  # Returning False if no collision occurs.
