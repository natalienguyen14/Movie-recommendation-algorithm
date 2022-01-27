"""
File: fractal_tree.py
Author: Long Pham, Natalie Nguyen
Date: 10/21/2021
Description: Displays fractal tree
"""

# Imports
import tkinter as tk
import math

class FractalTree:
    def __init__(self):
        """ Initialize the fractal object. """
        # Create the canvas and buttons for the program.
        self.canvas_size = 400

        self.window = tk.Tk()
        self.window.title("Recursion Tree")

        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack()
        self.canvas = tk.Canvas(self.canvas_frame, height = self.canvas_size, width = self.canvas_size, bg = "white")
        self.canvas.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()
        self.advance_button = tk.Button(self.button_frame, text = "Advance", command = self.advance)
        self.advance_button.grid(row = 1, column = 1, padx = 5)
        self.reset_button = tk.Button(self.button_frame, text = "Reset", command = self.reset)
        self.reset_button.grid(row = 1, column = 2, padx = 5)
        self.quit_button = tk.Button(self.button_frame, text = "Quit", command = self.quit)
        self.quit_button.grid(row = 1, column = 3, padx = 5)

        # Set the level of recursion to 0 upon starting the program.
        self.current_levels_of_recursion = 0
        self.draw_fractal(200, 390, 0, 400/3, self.current_levels_of_recursion)

        self.window.mainloop()
        
    def advance(self):
        """ Advance one level of recursion """
        # Create new fractal tree with new level of recursion in mind. Call the function for drawing the fractal.
        self.current_levels_of_recursion += 1
        self.canvas.delete("all")
        self.draw_fractal(200, 390, 0, 400/3, self.current_levels_of_recursion)

    def reset(self):
        """ Reset to 0 levels of recursion """
        # Set the level of recursion to 0 and draw the fractal tree using draw_fractal.
        self.canvas.delete("all")
        self.current_levels_of_recursion = 0
        self.draw_fractal(200, 390, 0, 400/3, self.current_levels_of_recursion)

    def quit(self):
        """ Quit the program """
        self.window.destroy()

    def draw_fractal(self, x1, y1, angle, length, levels_of_recursion):
        # Return when level of recursion eventually gets to -1. Draw one line and call draw_fractal 2 times and recursively.
        if levels_of_recursion == -1:
            return
        else:
            self.canvas.create_line(x1 + math.cos(math.pi/2 + angle), y1 + math.sin(math.pi/2 + angle), x1 + (length)*math.cos(math.pi/2 + angle), y1 - (math.sin(math.pi/2 + angle)*length))
            self.draw_fractal(x1 + (math.cos(math.pi/2 + angle)*length), y1 - (math.sin(math.pi/2 + angle)*length), angle + math.pi/5, length * 0.58, levels_of_recursion - 1)
            self.draw_fractal(x1 - (math.cos(math.pi/2 - angle)*length), y1 - (math.sin(math.pi/2 + angle)*length), angle - math.pi/5, length * 0.58, levels_of_recursion - 1)

if __name__ == "__main__":
    # Create GUI
    FractalTree()