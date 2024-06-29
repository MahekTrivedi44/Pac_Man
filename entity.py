import pygame  # Import the pygame library for game development.
from pygame.locals import *  # Import constants from pygame.locals module.
from vector import Vector2  # Import Vector2 class from vector module.
from constants import *  # Import constants from constants module.
from random import randint  # Import randint function from random module.

class Entity(object):  # Define a class named Entity.
    def __init__(self, node):  # Constructor method for initializing instances of the Entity class.
        self.name = None  # Initialize the name attribute to None.
        # Define movement directions with corresponding vectors.
        self.directions = {UP:Vector2(0, -1), DOWN:Vector2(0, 1), LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP  # Initialize the direction attribute to STOP.
        self.setSpeed(100)  # Set the speed attribute.
        self.radius = 10  # Radius of the entity.
        self.collideRadius = 3  # Radius for collision detection.
        self.color = WHITE  # Color of the entity.
        self.visible = True  # Boolean indicating if the entity is visible.
        self.disablePortal = False  # Boolean indicating if portals are disabled.
        self.goal = None  # Initialize the goal attribute to None.
        # Define the default method for determining direction.
        self.directionMethod = self.randomDirection
        self.setStartNode(node)  # Set the starting node for the entity.
        self.image = None  # Initialize the image attribute to None.

    def setPosition(self):  # Method to set the position of the entity.
        self.position = self.node.position.copy()  # Set the position attribute.

    def update(self, dt):  # Method to update the entity's state.
        # Update the position based on direction and speed.
        self.position += self.directions[self.direction] * self.speed * dt
        # Check if the entity has overshot its target node.
        if self.overshotTarget():
            self.node = self.target  # Update the current node to the target node.
            directions = self.validDirections()  # Get valid movement directions.
            direction = self.directionMethod(directions)  # Determine next direction.
            if not self.disablePortal:
                # Check if the current node has a portal neighbor.
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]  # Move through the portal.
            self.target = self.getNewTarget(direction)  # Determine the new target node.
            if self.target is not self.node:
                self.direction = direction  # Update the direction.
            else:
                self.target = self.getNewTarget(self.direction)  # Keep moving in the current direction.
            self.setPosition()  # Set the new position.

    def validDirection(self, direction):  # Method to check if a direction is valid.
        if direction is not STOP:  # Ensure direction is not STOP.
            if self.name in self.node.access[direction]:  # Check if the entity can access the direction from the current node.
                if self.node.neighbors[direction] is not None:  # Check if there is a neighbor in the specified direction.
                    return True  # Direction is valid.
        return False  # Direction is invalid.

    def getNewTarget(self, direction):  # Method to get the new target node based on direction.
        if self.validDirection(direction):  # Check if the direction is valid.
            return self.node.neighbors[direction]  # Return the neighbor node in the specified direction.
        return self.node  # Return the current node if direction is invalid.

    def overshotTarget(self):  # Method to check if the entity has overshot its target node.
        if self.target is not None:  # Ensure target node is defined.
            vec1 = self.target.position - self.node.position  # Vector from current node to target node.
            vec2 = self.position - self.node.position  # Vector from current node to current position.
            node2Target = vec1.magnitudeSquared()  # Squared magnitude of vector to target node.
            node2Self = vec2.magnitudeSquared()  # Squared magnitude of vector to current position.
            return node2Self >= node2Target  # Check if current position is beyond target node.
        return False  # Return False if target node is not defined.

    def reverseDirection(self):  # Method to reverse the entity's direction.
        self.direction *= -1  # Reverse the direction.
        temp = self.node  # Swap current node and target node.
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):  # Method to check if a direction is opposite to the entity's current direction.
        if direction is not STOP:  # Ensure direction is not STOP.
            if direction == self.direction * -1:  # Check if direction is opposite to current direction.
                return True  # Direction is opposite.
        return False  # Direction is not opposite.

    def validDirections(self):  # Method to get valid movement directions.
        directions = []  # List to store valid directions.
        for key in [UP, DOWN, LEFT, RIGHT]:  # Iterate over possible directions.
            if self.validDirection(key):  # Check if direction is valid.
                if key != self.direction * -1:  # Ensure direction is not opposite to current direction.
                    directions.append(key)  # Add valid direction to list.
        if len(directions) == 0:  # If no valid directions found.
            directions.append(self.direction * -1)  # Add opposite direction to list.
        return directions  # Return list of valid directions.

    def randomDirection(self, directions):  # Method to select a random direction from a list of valid directions.
        return directions[randint(0, len(directions) - 1)]  # Return a randomly selected direction.

    def goalDirection(self, directions):  # Method to select direction towards a goal.
        distances = []  # List to store distances to goal for each direction.
        for direction in directions:  # Iterate over valid directions.
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal  # Vector to goal.
            distances.append(vec.magnitudeSquared())  # Calculate squared distance and append to list.
        index = distances.index(min(distances))  # Find index of direction with minimum distance to goal.
        return directions[index]  # Return direction towards goal.

    def setStartNode(self, node):  # Method to set the starting node for the entity.
        self.node = node  # Set current node to starting node.
        self.startNode = node  # Set starting node attribute.
        self.target = node  # Set target node to starting node.
        self.setPosition()  # Set position to starting node position.
    def setBetweenNodes(self, direction):  
        # Method to set the entity between two nodes in a specified direction.
        if self.node.neighbors[direction] is not None:  
            # Check if there is a neighbor node in the specified direction.
            self.target = self.node.neighbors[direction]  
            # Set the target node to the neighbor node in the specified direction.
            self.position = (self.node.position + self.target.position) / 2.0  
            # Set the position of the entity to the midpoint between the current node and the target node.
    def reset(self):
        # Method to reset the entity's attributes to default values.
        self.setStartNode(self.startNode)  
        # Reset the entity's starting node.
        self.direction = STOP  
        # Reset the entity's direction to STOP.
        self.speed = 100  
        # Reset the entity's speed to 100.
        self.visible = True  
        # Set the entity's visibility to True.
    def setSpeed(self, speed):
        # Method to set the speed of the entity.
        self.speed = speed * TILEWIDTH / 16  
        # Set the entity's speed, adjusting it based on TILEWIDTH.
    def render(self, screen):
        # Method to render the entity on the screen.
        if self.visible:  
            # Check if the entity is visible.
            if self.image is not None:  
                # If the entity has an image assigned to it.
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2  
                # Calculate adjustment based on TILEWIDTH and TILEHEIGHT.
                p = self.position - adjust  
                # Calculate the position of the entity.
                screen.blit(self.image, p.asTuple())  
                # Draw the image of the entity on the screen at the calculated position.
            else:
                p = self.position.asInt()  
                # If no image is assigned, draw a circle representing the entity.
                pygame.draw.circle(screen, self.color, p, self.radius)  
                # Draw a circle representing the entity on the screen.
