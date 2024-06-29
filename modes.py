# Import constants from the constants FILE
from constants import *
# Define a class MainMode
class MainMode(object):
    # Constructor method
    def __init__(self):
        # Initialize timer variable to 0
        self.timer = 0
        # Call the scatter method upon initialization
        self.scatter()
    # Update method to update the mode
    def update(self, dt):
        # Increment timer by the time difference (dt)
        self.timer += dt
        # Check if timer exceeds the set time for the mode
        if self.timer >= self.time:
            # If mode is SCATTER, switch to chase mode
            if self.mode is SCATTER:
                self.chase()
            # If mode is CHASE, switch to scatter mode
            elif self.mode is CHASE:
                self.scatter()
    # Method to set the mode to scatter
    def scatter(self):
        # Set mode to SCATTER
        self.mode = SCATTER
        # Set time for this mode
        self.time = 7
        # Reset timer
        self.timer = 0
    # Method to set the mode to chase
    def chase(self):
        # Set mode to CHASE
        self.mode = CHASE
        # Set time for this mode
        self.time = 20
        # Reset timer
        self.timer = 0
# Define a class ModeController
class ModeController(object):
    # Constructor method
    def __init__(self, entity):
        # Initialize timer variable to 0
        self.timer = 0
        # Set time to None
        self.time = None
        # Create an instance of MainMode class
        self.mainmode = MainMode()
        # Set current mode to the mode of MainMode instance
        self.current = self.mainmode.mode

        
        # Assign the entity to the controller
        self.entity = entity 
    # Method to update the mode
    def update(self, dt):
        # Call update method of MainMode instance
        self.mainmode.update(dt)
        # Check if current mode is FREIGHT
        if self.current is FREIGHT:
            # Increment timer by time difference (dt)
            self.timer += dt
            # Check if timer exceeds set time
            if self.timer >= self.time:
                # Set time to None
                self.time = None
                # Call entity's normal mode method
                self.entity.normalMode()
                # Set current mode to the mode of MainMode instance
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]: # Check if current mode is SCATTER or CHASE
            # Set current mode to the mode of MainMode instance
            self.current = self.mainmode.mode
        # Check if current mode is SPAWN
        if self.current is SPAWN:
            # Check if entity is at spawn node
            if self.entity.node == self.entity.spawnNode:
                # Call entity's normal mode method
                self.entity.normalMode()
                # Set current mode to the mode of MainMode instance
                self.current = self.mainmode.mode
    # Method to set the mode to FREIGHT
    def setFreightMode(self):
        # Check if current mode is SCATTER or CHASE
        if self.current in [SCATTER, CHASE]:
            # Reset timer
            self.timer = 0
            # Set time for FREIGHT mode
            self.time = 7
            # Set current mode to FREIGHT
            self.current = FREIGHT
        # Check if current mode is already FREIGHT
        elif self.current is FREIGHT:
            # Reset timer
            self.timer = 0
    # Method to set the mode to SPAWN
    def setSpawnMode(self):
        # Check if current mode is FREIGHT
        if self.current is FREIGHT:
            # Set current mode to SPAWN
            self.current = SPAWN
