import pygame  # Importing the pygame library, which is used for creating video games.
from pygame.locals import *  # Importing constants and functions from the pygame.locals module.
from constants import *  # Importing constants from a custom module named constants.
from pacman import Pacman  # Importing the Pacman class from a custom module named pacman.
from nodes import NodeGroup  # Importing the NodeGroup class from a custom module named nodes.
from pellets import PelletGroup  # Importing the PelletGroup class from a custom module named pellets.
from ghosts import GhostGroup  # Importing the GhostGroup class from a custom module named ghosts.
from fruit import Fruit  # Importing the Fruit class from a custom module named fruit.
from pauser import Pause  # Importing the Pause class from a custom module named pauser.
from text import TextGroup  # Importing the TextGroup class from a custom module named text.
from sprites import LifeSprites, MazeSprites  # Importing the LifeSprites and MazeSprites classes from a custom module named sprites.
from mazedata import MazeData  # Importing the MazeData class from a custom module named mazedata.
import os
import threading 

SCORE_FILE = "score.txt"
def game_loop(game):
    while True:
        game.update()
class GameController(object):  # Defining a class named GameController.
    def __init__(self):  # Constructor method for the GameController class.
        pygame.init()  # Initializing the pygame module.
        pygame.mixer.init()  # Initialize the mixer module for sound playback
        self.sound_chomp = pygame.mixer.Sound("pacman_chomp.wav")
        self.sound_death = pygame.mixer.Sound("pacman_death.wav")
        self.sound_intermission = pygame.mixer.Sound("pacman_intermission.wav")
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)  # Creating a pygame window with dimensions 448x512 pixels.
        self.background = None  # Initializing background attribute as None.
        self.background_norm = None  # Initializing background_norm attribute as None.
        self.background_flash = None  # Initializing background_flash attribute as None.
        self.clock = pygame.time.Clock()  # Creating a Clock object to help track time.
        self.fruit = None  # Initializing fruit attribute as None.
        self.pause = Pause(True)  # Creating a Pause object with initial value True.
        self.level = 0  # Initializing level attribute with value 0.
        self.lives = 3  # Initializing lives attribute with value 5.
        self.score = 0  # Initializing score attribute with value 0.
        self.textgroup = TextGroup()  # Creating a TextGroup object.
        self.lifesprites = LifeSprites(self.lives)  # Creating a LifeSprites object with initial number of lives.
        self.flashBG = False  # Initializing flashBG attribute with value False.
        self.flashTime = 0.2  # Initializing flashTime attribute with value 0.2.
        self.flashTimer = 0  # Initializing flashTimer attribute with value 0.
        self.fruitCaptured = []  # Initializing fruitCaptured attribute as an empty list.
        self.fruitNode = None  # Initializing fruitNode attribute as None.
        self.mazedata = MazeData()  # Creating a MazeData object.
        self.score = self.loadScore()  # Load the previous score from file
        
    def loadScore(self):
        # Load previous score from the file
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as file:
                score = int(file.read())
            return score
        else:
            return 0
    def saveScore(self):
        # Save the current score to the file
        with open(SCORE_FILE, 'w') as file:
            file.write(str(self.score))

    def setBackground(self):  # Method to set the game background.
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()  # Creating a surface for the normal background.
        self.background_norm.fill(BLACK)  # Filling the normal background surface with black color.
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()  # Creating a surface for the flashing background.
        self.background_flash.fill(BLACK)  # Filling the flashing background surface with black color.
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level % 5)  # Constructing the normal background using maze sprites.
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)  # Constructing the flashing background using maze sprites.
        self.flashBG = False  # Resetting flashBG attribute to False.
        self.background = self.background_norm  # Setting the background attribute to the normal background.

    def startGame(self):  # Method to start the game.
        self.mazedata.loadMaze(self.level)  # Loading maze data for the current level.
        self.mazesprites = MazeSprites(self.mazedata.obj.name + ".txt", self.mazedata.obj.name + "_rotation.txt")  # Creating MazeSprites object based on maze data.
        self.setBackground()  # Setting the game background.
        self.nodes = NodeGroup(self.mazedata.obj.name + ".txt")  # Creating NodeGroup object based on maze data.
        self.mazedata.obj.setPortalPairs(self.nodes)  # Setting portal pairs for maze nodes.
        self.mazedata.obj.connectHomeNodes(self.nodes)  # Connecting home nodes for maze nodes.
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))  # Creating Pacman object with starting node.
        self.pellets = PelletGroup(self.mazedata.obj.name + ".txt")  # Creating PelletGroup object based on maze data.
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)  # Creating GhostGroup object with starting node and Pacman.

        # Setting initial nodes for each ghost.
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        # Adjust ghost speeds based on the current level
        ghost_speeds = {1: 100, 2: 110, 3: 120, 4: 130, 5: 140}  # Define speed values for each level
        ghost_speed = ghost_speeds.get(self.level, 100)  # Get the speed for the current level, default to 100 if not found
        for ghost in self.ghosts:
            ghost.setSpeed(ghost_speed)  # Set the speed for each ghost

        self.nodes.denyHomeAccess(self.pacman)  # Denying home access for Pacman.
        self.nodes.denyHomeAccessList(self.ghosts)  # Denying home access for ghosts.
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)  # Denying access to right for Inky.
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)  # Denying access to left for Clyde.
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)  # Denying access for ghosts based on maze data.
            

    def update(self):
        dt = self.clock.tick(30) / 1000.0  # Calculate time passed since the last frame, in seconds.
        self.textgroup.update(dt)  # Update text group based on the elapsed time.
        self.pellets.update(dt)  # Update pellet group based on the elapsed time.

        # Update ghosts, fruit, and check events only if the game is not paused.
        if not self.pause.paused:
            self.ghosts.update(dt)  # Update ghosts based on the elapsed time.
            if self.fruit is not None:  # If there's a fruit in the game:
                self.fruit.update(dt)  # Update the fruit based on the elapsed time.
            self.checkPelletEvents()  # Check events related to pellets.
            self.checkGhostEvents()  # Check events related to ghosts.
            self.checkFruitEvents()  # Check events related to fruit.

        # Update Pacman's movement if it's alive and the game is not paused.
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)  # Update Pacman's movement based on the elapsed time.
        else:
            self.pacman.update(dt)  # Update Pacman's movement even if it's not alive.
        self.flashBG=False
        # Flash the background if needed.
        if self.flashBG:
            self.flashTimer += dt  # Increment flash timer.
            if self.flashTimer >= self.flashTime:  # If flash timer exceeds the flash time:
                self.flashTimer = 0  # Reset flash timer.
                # Toggle between normal and flashing background.
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        # Update the pause status and execute any method scheduled after a pause.
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()

        self.checkEvents()  # Check for events such as quitting the game or pausing.
        self.render()  # Render all game elements onto the screen.
        


    def checkEvents(self):
        for event in pygame.event.get():  # Iterate through all pygame events.
            if event.type == QUIT:  # If the event is quitting the game
                game.saveScore()  #save score before exiting
                exit()  # Exit the game.
            elif event.type == KEYDOWN:  # If a key is pressed:
                if event.key == K_SPACE:  # If the pressed key is the spacebar:
                    if self.pacman.alive:  # If Pacman is alive:
                        self.pause.setPause(playerPaused=True)  # Set the game to pause mode with player pause.
                        if not self.pause.paused:  # If the game is not paused:
                            self.textgroup.hideText()  # Hide text elements.
                            self.showEntities()  # Show game entities (Pacman, ghosts, etc.).
                        else:
                            self.textgroup.showText(PAUSETXT)  # Show pause text.
                            # self.hideEntities()  # Potentially hiding entities (currently commented out).


    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)  # Check if Pacman eats any pellets.
        if pellet:
            self.sound_chomp.play()# If Pacman eats a pellet:
            self.pellets.numEaten += 1  # Increase the count of pellets eaten.
            self.updateScore(pellet.points)  # Update the game score based on the pellet's points.
            if self.pellets.numEaten == 30:  # If Pacman has eaten 30 pellets:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)  # Allow Inky to move right.
            if self.pellets.numEaten == 70:  # If Pacman has eaten 70 pellets:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)  # Allow Clyde to move left.
            if pellet in self.pellets.pelletList:
                self.pellets.pelletList.remove(pellet)  # Remove the eaten pellet from the list.
            if pellet.name == POWERPELLET:# If the eaten pellet is a power pellet:
                self.ghosts.startFreight()
                self.sound_chomp.stop()
                self.sound_intermission.play()
                # Start the freight mode for ghosts.
            if self.pellets.isEmpty():  # If there are no more pellets left:
                self.flashBG = True  # Set the background to flash.
                self.hideEntities()  # Hide game entities.
                self.pause.setPause(pauseTime=3, func=self.nextLevel)  # Pause the game and proceed to the next level after 3 seconds.

    def checkGhostEvents(self):
        for ghost in self.ghosts:  # Iterate through all ghosts.
            if self.pacman.collideGhost(ghost):  # Check if Pacman collides with the current ghost.
                if ghost.mode.current is FREIGHT:  # If the ghost is in freight mode:
                    self.pacman.visible = False  # Make Pacman invisible.
                    ghost.visible = False  # Make the ghost invisible.
                    self.updateScore(ghost.points)  # Update the score by adding the ghost's points.
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)  # Add text showing the points gained from eating the ghost.
                    self.ghosts.updatePoints()  # Update the points earned from eating ghosts.
                    self.pause.setPause(pauseTime=1, func=self.showEntities)  # Pause the game briefly and then show game entities.
                    ghost.startSpawn()  # Start the process of respawning the ghost.
                    self.nodes.allowHomeAccess(ghost)  # Allow the ghost to access its home node.
                elif ghost.mode.current is not SPAWN:  # If the ghost is not in spawn mode:
                    if self.pacman.alive:  # If Pacman is alive:
                        self.lives -= 1  # Decrease the number of lives.
                        self.lifesprites.removeImage()  # Remove one life sprite from the screen.
                        self.pacman.die()  # Mark Pacman as dead.
                        self.ghosts.hide()  # Hide all ghosts.
                        if self.lives <= 0:  # If no lives left:
                            self.textgroup.showText(GAMEOVERTXT)  # Show game over text.
                            self.pause.setPause(pauseTime=3, func=self.restartGame)  # Pause the game and restart after 3 seconds.
                        else:
                            self.sound_death.play()
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)  # Pause the game and reset the level after 3 seconds.

        
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:  # If a specific number of pellets are eaten:
            if self.fruit is None:  # If there is no existing fruit:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)  # Create a new fruit at a specific position.
                print(self.fruit)  # Print information about the created fruit.
        if self.fruit is not None:  # If there is an existing fruit:
            if self.pacman.collideCheck(self.fruit):  # If Pacman collides with the fruit:
                self.updateScore(self.fruit.points)  # Update the score by adding the fruit's points.
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)  # Add text showing the points
                fruitCaptured = False  # Initialize a variable to track if the fruit is captured.
                for fruit in self.fruitCaptured:  # Iterate through captured fruits.
                    if fruit.get_offset() == self.fruit.image.get_offset():  # If the current fruit is already captured:
                        fruitCaptured = True  # Mark the fruit as captured.
                        break  # Exit the loop.
                if not fruitCaptured:  # If the fruit is not captured:
                    self.fruitCaptured.append(self.fruit.image)  # Add the fruit to the list of captured fruits.
                self.fruit = None  # Remove the existing fruit from the game.
            elif self.fruit.destroy:  # If the fruit is marked for destruction:
                self.fruit = None  # Remove the existing fruit from the game.


    def showEntities(self):
        self.pacman.visible = True  # Set Pacman to be visible.
        self.ghosts.show()  # Show all ghosts.


    def hideEntities(self):
        self.pacman.visible = False  # Set Pacman to be invisible.
        self.ghosts.hide()  # Hide all ghosts.


    def nextLevel(self):
        self.showEntities()  # Show game entities (Pacman and ghosts).
        self.level += 1  # Increment the level number.
        self.pause.paused = True  # Pause the game.
        self.startGame()  # Start the next level.
        self.textgroup.updateLevel(self.level)  # Update the displayed level number.
    def restartGame(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = self.loadScore()  # Load previous score
        self.textgroup.updateScore(self.score)  # Update displayed score
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []
    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)
        self.saveScore()  # Save the score after each update
    def resetLevel(self):
        self.pause.paused = True  # Pause the game.
        self.pacman.reset()  # Reset Pacman's position and state.
        self.ghosts.reset()  # Reset all ghosts.
        self.fruit = None  # Clear any existing fruit.
        self.textgroup.showText(READYTXT)  # Show the "READY" text.
    def render(self):
        self.screen.blit(self.background, (0, 0))  # Render the background onto the screen.
        self.pellets.render(self.screen)  # Render pellets onto the screen.
        if self.fruit is not None:  # If there is a fruit:
            self.fruit.render(self.screen)  # Render the fruit onto the screen.
        self.pacman.render(self.screen)  # Render Pacman onto the screen.
        self.ghosts.render(self.screen)  # Render ghosts onto the screen.
        self.textgroup.render(self.screen)  # Render text elements onto the screen.
        for i in range(len(self.lifesprites.images)): # Render life sprites onto the screen.
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        for i in range(len(self.fruitCaptured)):# Render captured fruit images onto the screen.
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))
        pygame.display.update()  # Update the display to show all rendered elements.
if __name__ == "__main__":
    game = GameController()
    game.startGame()
    game_thread = threading.Thread(target=game_loop, args=(game,))# Start the game loop in a separate thread
    game_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
    game_thread.start()
    # Call game.update() here to keep the main loop running and handle Pygame events
    game_loop(game)
    
