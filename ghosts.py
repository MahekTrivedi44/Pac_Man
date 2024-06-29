import pygame  # Import the pygame library for game development
from pygame.locals import *  # Import specific constants from pygame.locals module
from vector import Vector2  # Importing a custom Vector2 class from a module named vector
from constants import *  # Importing constants from a module named constants
from entity import Entity  # Importing Entity class from a module named entity
from modes import ModeController  # Importing ModeController class from a module named modes
from sprites import GhostSprites  # Importing GhostSprites class from a module named sprites
# Define a class Ghost which inherits from Entity
class Ghost(Entity):
    # Constructor method to initialize Ghost objects
    def __init__(self, node, pacman=None, blinky=None):
        # Call the constructor of the superclass (Entity)
        Entity.__init__(self, node)
        # Set attributes specific to Ghost objects
        self.name = GHOST  # Name of the ghost
        self.points = 200  # Points earned when ghost is captured
        self.goal = Vector2()  # Target position for the ghost
        self.directionMethod = self.goalDirection  # Method for determining ghost's movement direction
        self.pacman = pacman  # Reference to the Pacman object
        self.mode = ModeController(self)  # Mode controller for ghost's behavior
        self.blinky = blinky  # Reference to the Blinky ghost object
        self.homeNode = node  # Node where ghost starts
    # Method to reset ghost's attributes
    def reset(self):
        Entity.reset(self)  # Call reset method of superclass (Entity)
        self.points = 200  # Reset points earned
        self.directionMethod = self.goalDirection  # Reset method for determining movement direction
    # Method to update ghost's state
    def update(self, dt):
        self.sprites.update(dt)  # Update ghost's sprites
        self.mode.update(dt)  # Update ghost's mode (scatter, chase, etc.)
        if self.mode.current is SCATTER:  # If current mode is scatter
            self.scatter()  # Execute scatter behavior
        elif self.mode.current is CHASE:  # If current mode is chase
            self.chase()  # Execute chase behavior
        Entity.update(self, dt)  # Call update method of superclass (Entity)
    # Method defining ghost's behavior when in scatter mode
    def scatter(self):
        self.goal = Vector2()  # Set goal position to default (no specific target)
    # Method defining ghost's behavior when in chase mode
    def chase(self):
        self.goal = self.pacman.position  # Set goal position to Pacman's current position
    # Method to spawn the ghost
    def spawn(self):
        self.goal = self.spawnNode.position  # Set goal position to spawn node's position
    # Method to set the node where the ghost spawns
    def setSpawnNode(self, node):
        self.spawnNode = node  # Set spawn node attribute to given node

        
    # Method to start ghost's spawn mode
    def startSpawn(self):
        self.mode.setSpawnMode()  # Set ghost's mode to spawn
        if self.mode.current == SPAWN:  # If current mode is spawn
            self.setSpeed(150)  # Set ghost's speed
            self.directionMethod = self.goalDirection  # Set direction method
            self.spawn()  # Spawn the ghost

    # Method to start ghost's freight mode
    def startFreight(self):
        self.mode.setFreightMode()  # Set ghost's mode to freight
        if self.mode.current == FREIGHT:  # If current mode is freight
            self.setSpeed(50)  # Set ghost's speed
            self.directionMethod = self.randomDirection  # Set direction method

    # Method to set ghost's behavior in normal mode
    def normalMode(self):
        self.setSpeed(100)  # Set ghost's speed
        self.directionMethod = self.goalDirection  # Set direction method
        self.homeNode.denyAccess(DOWN, self)  # Deny access to a particular direction at home node

# Define a subclass Blinky which inherits from Ghost
class Blinky(Ghost):
    # Constructor method to initialize Blinky objects
    def __init__(self, node, pacman=None, blinky=None):
        # Call the constructor of the superclass (Ghost)
        Ghost.__init__(self, node, pacman, blinky)
        # Set attributes specific to Blinky objects
        self.name = BLINKY  # Name of the ghost
        self.color = RED  # Color of the ghost
        self.sprites = GhostSprites(self)  # Initialize ghost sprites

# Define a subclass Pinky which inherits from Ghost
class Pinky(Ghost):
    # Constructor method to initialize Pinky objects
    def __init__(self, node, pacman=None, blinky=None):
        # Call the constructor of the superclass (Ghost)
        Ghost.__init__(self, node, pacman, blinky)
        # Set attributes specific to Pinky objects
        self.name = PINKY  # Name of the ghost
        self.color = PINK  # Color of the ghost
        self.sprites = GhostSprites(self)  # Initialize ghost sprites

    # Override scatter method for Pinky's specific behavior
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)  # Set goal to top-right corner of the maze

    # Override chase method for Pinky's specific behavior
    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4  # Set goal to position four tiles ahead of Pacman
        

# Define a subclass Inky which inherits from Ghost
class Inky(Ghost):
    # Constructor method to initialize Inky objects
    def __init__(self, node, pacman=None, blinky=None):
        # Call the constructor of the superclass (Ghost)
        Ghost.__init__(self, node, pacman, blinky)
        # Set attributes specific to Inky objects
        self.name = INKY  # Name of the ghost
        self.color = TEAL  # Color of the ghost
        self.sprites = GhostSprites(self)  # Initialize ghost sprites

    # Override scatter method for Inky's specific behavior
    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)  # Set goal to bottom-right corner of the maze

    # Override chase method for Inky's specific behavior
    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2  # Calculate a vector two tiles ahead of Pacman
        vec2 = (vec1 - self.blinky.position) * 2  # Calculate a vector from Blinky to the calculated point, then double its length
        self.goal = self.blinky.position + vec2  # Set goal to Blinky's position plus the calculated vector

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        # Initialize the Clyde ghost
        Ghost.__init__(self, node, pacman, blinky)  # Call the __init__ method of the Ghost class
        self.name = CLYDE  # Set the name of the ghost to "CLYDE"
        self.color = ORANGE  # Set the color of the ghost to ORANGE
        self.sprites = GhostSprites(self)  # Initialize sprites for Clyde ghost

    def scatter(self):
        # Set the goal for Clyde ghost during scatter mode
        self.goal = Vector2(0, TILEHEIGHT*NROWS)  # Set the goal position to the bottom-left corner of the maze

    def chase(self):
        # Set the goal for Clyde ghost during chase mode
        d = self.pacman.position - self.position  # Calculate the vector from Clyde to Pacman
        ds = d.magnitudeSquared()  # Calculate the squared magnitude of the vector d
        if ds <= (TILEWIDTH * 8)**2:  # If Pacman is within a certain range of Clyde
            self.scatter()  # Set the goal to scatter mode
        else:
            # Otherwise, set the goal to follow Pacman but at a distance ahead
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacman):
        # Initialize a group of ghosts
        self.blinky = Blinky(node, pacman)  # Initialize Blinky ghost
        self.pinky = Pinky(node, pacman)  # Initialize Pinky ghost
        self.inky = Inky(node, pacman, self.blinky)  # Initialize Inky ghost
        self.clyde = Clyde(node, pacman)  # Initialize Clyde ghost
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]  # Store all ghosts in a list
    def __iter__(self):
        return iter(self.ghosts)  # Allow iteration over the ghosts in the group
    def update(self, dt):
        # Update all ghosts in the group
        for ghost in self:
            ghost.update(dt)
    def startFreight(self):
        # Start freight mode for all ghosts in the group
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()  # Reset points for all ghosts
    def setSpawnNode(self, node):
        # Set spawn node for all ghosts in the group
        for ghost in self:
            ghost.setSpawnNode(node)
    def updatePoints(self):
        # Update points for all ghosts in the group
        for ghost in self:
            ghost.points *= 2
    def resetPoints(self):
        # Reset points for all ghosts in the group
        for ghost in self:
            ghost.points = 200
    def hide(self):
        # Hide all ghosts in the group
        for ghost in self:
            ghost.visible = False
    def show(self):
        # Show all ghosts in the group
        for ghost in self:
            ghost.visible = True
    def reset(self):
        # Reset all ghosts in the group
        for ghost in self:
            ghost.reset()
    def render(self, screen):
        # Render all ghosts in the group on the screen
        for ghost in self:
            ghost.render(screen)

            
