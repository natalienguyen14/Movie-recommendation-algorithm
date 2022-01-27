"""
File: moving_circles.py
Author: Long Pham, Natalie Nguyen
Date: 10/21/2021
Description: Program that gets two circle locations from the
user, then draws a line between them, and
displays the distance between them midway along
the line. The user can drag either circle around,
and the distance is kept updated.
"""

# Imports
import tkinter as tk
from enum import Enum
import math

class MovingCircles:
    def __init__(self):
        # Set variables for the canvas and circles
        self.canvas_size = 400

        self.circle_radius = 20
        self.delta_time_millis = 0
        self.fill_color = 'red'
        self.check_if = None

        self.circle1_x = None
        self.circle1_y = None

        self.circle2_x = None
        self.circle2_y = None

        self.window = tk.Tk()
        self.window.title("Moving Circles")

        self.state = State.FIRST_CIRCLE

        # Create the canvas and buttons for the program.
        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack()
        self.canvas = tk.Canvas(self.canvas_frame, height = self.canvas_size, width = self.canvas_size)
        self.canvas.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()
        self.clear_button = tk.Button(self.button_frame, text = "Clear", command = self.clear)
        self.clear_button.grid(row = 1, column = 1, padx = 2)
        self.quit_button = tk.Button(self.button_frame, text = "Quit", command = self.quit)
        self.quit_button.grid(row = 1, column = 2, padx = 2)

        # Set up mouse click handlers for user
        # to specify the two balls
        self.canvas.bind("<ButtonRelease-1>", self.mouse_click_handler)
        self.canvas.bind("<B1-Motion>", self.step_handler)

        self.window.mainloop()

    def mouse_click_handler(self, event):
        """ Handle mouse click. """
        # Create if statements for 3 states for the program. First state is where user creates first circle.
        if self.state == State.FIRST_CIRCLE:
            # Get the circle1 point
            self.circle1_x = event.x
            self.circle1_y = event.y
            self.canvas.create_oval(
                self.circle1_x - self.circle_radius,
                self.circle1_y - self.circle_radius,
                self.circle1_x + self.circle_radius,
                self.circle1_y + self.circle_radius,
                fill = self.fill_color, tags = ("all", "circle1"))
            self.state = State.SECOND_CIRCLE
        # Second state is for creating the second circle as well as line between 
        # the circles and text stating the distance between the circles.
        elif self.state == State.SECOND_CIRCLE:
            # Get the circle2 point
            self.circle2_x = event.x
            self.circle2_y = event.y
            self.canvas.create_line(
                self.circle1_x, self.circle1_y,
                self.circle2_x, self.circle2_y,
                fill = self.fill_color, tags = ("all", "line"))
            self.canvas.create_oval(
                self.circle2_x - self.circle_radius,
                self.circle2_y - self.circle_radius,
                self.circle2_x + self.circle_radius,
                self.circle2_y + self.circle_radius,
                fill = self.fill_color, tags = ("all", "circle2"))
            self.distance_x = abs(self.circle2_x - self.circle1_x)
            self.distance_y = abs(self.circle2_y - self.circle1_y)
            self.distance = math.sqrt((self.distance_x ** 2) + (self.distance_y ** 2)) - 40
            if self.distance < 0:
                self.distance = 0.0
            self.canvas.create_text(
                (self.circle1_x + self.circle2_x) / 2, (self.circle1_y + self.circle2_y) / 2,
                text = f'{self.distance:.2f}', tags = ("all", "text"))
            self.state = State.ADJUSTABLE
        # Third state is for being able to adjust and move the circles
        elif self.state == State.ADJUSTABLE:
            self.check_if = 0

    def step_handler(self, event):
        """ Perform one step of the simulation. """
        # Get location of mouse, and move the circle to current location
        # change circle1 x and y values to current

        if self.state == State.ADJUSTABLE:
            self.cur_x = event.x
            self.cur_y = event.y
            if ((self.cur_x > self.circle1_x - self.circle_radius) and (self.cur_x < self.circle1_x + self.circle_radius) and (self.cur_y > self.circle1_y - self.circle_radius) and (self.cur_y < self.circle1_y + self.circle_radius)) or self.check_if == 1:
                self.canvas.move('circle1', self.cur_x - self.circle1_x, self.cur_y - self.circle1_y)

                self.canvas.delete("line")
                self.canvas.delete("text")
                self.circle1_x = self.cur_x
                self.circle1_y = self.cur_y
                
                self.check_if = 1
            elif ((self.cur_x > self.circle2_x - self.circle_radius) and (self.cur_x < self.circle2_x + self.circle_radius) and (self.cur_y > self.circle2_y - self.circle_radius) and (self.cur_y < self.circle2_y + self.circle_radius)) or self.check_if == 2:
                self.canvas.move('circle2', self.cur_x - self.circle2_x, self.cur_y - self.circle2_y)
                
                self.canvas.delete("line")
                self.canvas.delete("text")
                self.circle2_x = self.cur_x
                self.circle2_y = self.cur_y
                
                self.check_if = 2

            # Update the line and text
            self.canvas.create_line(
                self.circle1_x, self.circle1_y,
                self.circle2_x, self.circle2_y,
                fill = self.fill_color, tags = ("all", "line"))

            self.distance_x = abs(self.circle2_x - self.circle1_x)
            self.distance_y = abs(self.circle2_y - self.circle1_y)
            self.distance = math.sqrt((self.distance_x ** 2) + (self.distance_y ** 2)) - 40
            if self.distance < 0:
                self.distance = 0.0
            self.canvas.create_text(
                (self.circle1_x + self.circle2_x) / 2, (self.circle1_y + self.circle2_y) / 2,
                text = f'{self.distance:.2f}', tags = ("all", "text"))

    # Quit and clear buttons at the bottom of the window
    def quit(self):
        """Quit the simulation"""
        self.window.destroy()
    
    def clear(self):
        """Clears the simulation so that it can start again"""
        self.canvas.delete("all")
        self.state = State.FIRST_CIRCLE

class State(Enum):
    # Assign a number based on the state of the program
    FIRST_CIRCLE = 1
    SECOND_CIRCLE = 2
    ADJUSTABLE = 3

if __name__ == "__main__":
    # Create GUI
    MovingCircles()