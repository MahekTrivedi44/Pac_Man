import pygame  # Importing the pygame library for game development.
from constants import *  # Importing constants module containing game constants.

class Animator(object):  # Class for handling animation.
    def __init__(self, frames=[], speed=20, loop=True):  # Constructor method for Animator class.
        self.frames = frames  # List of frames for the animation.
        self.current_frame = 0  # Index of the current frame.
        self.speed = speed  # Speed of the animation.
        self.loop = loop  # Whether the animation should loop.
        self.dt = 0  # Time elapsed since the last frame change.
        self.finished = False  # Flag indicating if the animation has finished.

    def reset(self):  # Method to reset the animation.
        self.current_frame = 0  # Resetting current frame to the beginning.
        self.finished = False  # Resetting finished flag.

    def update(self, dt):  # Method to update the animation.
        if not self.finished:  # If animation is not finished.
            self.nextFrame(dt)  # Move to the next frame.
        if self.current_frame == len(self.frames):  # If reached the end of frames.
            if self.loop:  # If animation is set to loop.
                self.current_frame = 0  # Reset to the first frame.
            else:  # If not looping.
                self.finished = True  # Set animation as finished.
                self.current_frame -= 1  # Adjusting current frame index.

        return self.frames[self.current_frame]  # Returning the current frame.

    def nextFrame(self, dt):  # Method to proceed to the next frame.
        self.dt += dt  # Adding elapsed time.
        if self.dt >= (1.0 / self.speed):  # If elapsed time reaches threshold for frame change.
            self.current_frame += 1  # Move to the next frame.
            self.dt = 0  # Reset the elapsed time.
