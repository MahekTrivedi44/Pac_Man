import pygame  # Importing the pygame library for game development.
from vector import Vector2  # Importing a Vector2 class from a custom module.
from constants import *  # Importing constants from another module.

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id  # Assigning an id to the text object.
        self.text = text  # Storing the text content.
        self.color = color  # Storing the color of the text.
        self.size = size  # Storing the font size of the text.
        self.visible = visible  # Storing the visibility status of the text.
        self.position = Vector2(x, y)  # Creating a Vector2 object to store the position of the text.
        self.timer = 0  # Initializing a timer for the text.
        self.lifespan = time  # Storing the lifespan of the text.
        self.label = None  # Initializing the label attribute.
        self.destroy = False  # Flag to indicate if the text should be destroyed.
        self.setupFont("PressStart2P-Regular.ttf")  # Setting up the font for the text.
        self.createLabel()  # Creating the label for the text.

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)  # Loading the font for the text.

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)  # Rendering the text to create the label.

    def setText(self, newtext):
        self.text = str(newtext)  # Setting new text content.
        self.createLabel()  # Recreating the label with the new text.

    def update(self, dt):
        if self.lifespan is not None:  # Checking if the text has a lifespan.
            self.timer += dt  # Incrementing the timer.
            if self.timer >= self.lifespan:  # Checking if the text's lifespan has expired.
                self.timer = 0  # Resetting the timer.
                self.lifespan = None  # Disabling the lifespan.
                self.destroy = True  # Marking the text for destruction.

    def render(self, screen):
        if self.visible:  # Checking if the text is visible.
            x, y = self.position.asTuple()  # Extracting position coordinates.
            screen.blit(self.label, (x, y))  # Rendering the text label on the screen.


class TextGroup(object):
    def __init__(self):
        self.nextid = 10  # Initializing the next available id for text objects.
        self.alltext = {}  # Dictionary to store all text objects.
        self.setupText()  # Setting up text objects.
        self.showText(READYTXT)  # Showing the "READY" text at the beginning.

    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1  # Incrementing the id for the next text object.
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)  # Creating a new text object.
        return self.nextid  # Returning the id of the newly added text object.

    def removeText(self, id):
        self.alltext.pop(id)  # Removing a text object with a specific id from the collection.

    def setupText(self):
        size = TILEHEIGHT  # Setting the font size for text objects.
        # Creating various predefined text objects.
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        # Adding additional text objects for "SCORE" and "LEVEL".
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH, 0, size)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):  # Iterating through all text objects.
            self.alltext[tkey].update(dt)  # Updating each text object.
            if self.alltext[tkey].destroy:  # Checking if a text object needs to be destroyed.
                self.removeText(tkey)  # Removing the text object.

    def showText(self, id):
        self.hideText()  # Hiding all text objects.
        self.alltext[id].visible = True  # Showing a specific text object.

    def hideText(self):
        # Hiding specific text objects.
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))  # Updating the score text object.

    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))  # Updating the level text object.

    def updateText(self, id, value):
        if id in self.alltext.keys():  # Checking if the specified text object exists.
            self.alltext[id].setText(value)  # Updating the text content.

    def render(self, screen):
        for tkey in list(self.alltext.keys()):  # Iterating through all text objects.
            self.alltext[tkey].render(screen)  # Rendering each text object.
