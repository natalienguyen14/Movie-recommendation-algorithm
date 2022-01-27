# File: addressbook.py
# Author: Natalie Nguyen and Alizea Hinz
# Date:
# Description: 

import math 
import datetime
import tkinter as tk

class Display_Clock:
    def __init__(self):
        self.window = tk.Tk() # Create a window
        self.window.title("Current Time") # Set a title

        #instance variables for clock/canvas
        self.canvas_width = 200
        self.canvas_height = 200
        self.center_of_canvas = self.canvas_width/2 ,self.canvas_height/2
        self.radius_percentage = 0.8
        self.second_hand_percentage = 0.8
        self.minute_hand_percentage = 0.65
        self.hour_hand_percentage = 0.5
        self.state = "want to pause"

        #time
        self.current_time = datetime.datetime.now()
        self.current_hour = self.current_time.hour
        self.current_minute = self.current_time.minute
        self.current_second = self.current_time.second
        self.time_interval = 1000

        #computing clock measurements
        self.radius = (self.canvas_width/2)*self.radius_percentage 
        self.second_hand = self.second_hand_percentage * self.radius
        self.minute_hand = self.minute_hand_percentage * self.radius
        self.hour_hand = self.hour_hand_percentage * self.radius

        self.canvas = tk.Canvas(self.window, width = self.canvas_width, height = self.canvas_height, bg = 'white') 
        self.canvas.grid(row = 1, column = 1)

        self.clock_setup()
        
        # Button frame in window
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row = 2, column = 1)

        self.text_of_state = "Stop"
        self.start_button = tk.Button(self.button_frame, text = "Stop", command = self.button_switch)
        self.start_button.grid(row = 1, column = 1)

        self.quit_button = tk.Button(self.button_frame, text = "Quit", command = self.quit)
        self.quit_button.grid(row = 1, column = 2)

        self.canvas.bind(self.button_switch)
        self.update_time()
        # start event loop
        self.window.mainloop() 
        

    def clock_setup(self):
        """ """
        #clock outline and labels
        self.canvas.create_oval((self.canvas_width/2)-self.radius,(self.canvas_height/2)-self.radius,
                                 (self.canvas_width/2)+self.radius,(self.canvas_height/2)+self.radius)
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2 - self.radius*.9, text = "12")
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2 - self.radius*-.9, text = "6")
        self.canvas.create_text(self.canvas_width/2 - self.radius*.9, self.canvas_height/2, text = "9")
        self.canvas.create_text(self.canvas_width/2 - self.radius*-.9, self.canvas_height/2, text = "3")
        self.check_time()
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2 + self.radius*1.1, 
                                text = str(self.current_hour) + ":" + self.display_minute +
                                ":" + self.display_second, tag = "time")
        self.hand_angles()
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.second_x, self.canvas_height/2 + self.second_y, fill = "red", tag = "hands")
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.minute_x, self.canvas_height/2 + self.minute_y, fill = "blue", tag = "hands")
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.hour_x, self.canvas_height/2 + self.hour_y, fill = "green", tag = "hands")
        

    def button_switch(self):
        """   """
        if self.text_of_state == "Stop":
            self.window.after_cancel(self.timer)
            self.text_of_state = "Start"
            self.start_button['text'] = "Start"
        elif self.text_of_state == "Start":
            self.timer = self.canvas.after(self.time_interval, self.update_time)
            self.text_of_state = "Stop"
            self.start_button['text'] = "Stop"
    
    def hand_angles(self):
        """ """
        self.current_time = datetime.datetime.now()
        self.check_time()
        self.current_hour = self.current_time.hour 
        self.current_minute = self.current_time.minute
        self.current_second = self.current_time.second

        # get current angle
        self.second_angle = (self.current_second/60)*(2*math.pi) - math.pi/2
        self.minute_angle = ((self.current_minute + (self.current_second/60.0))/60)*(2*math.pi) - math.pi/2
        self.hour_angle = ((self.current_hour + (self.current_minute/60.0))/12)*(2*math.pi) - math.pi/2

        # Update location
        self.second_x = math.cos(self.second_angle) * self.second_hand
        self.second_y = math.sin(self.second_angle) * self.second_hand
        self.minute_x = math.cos(self.minute_angle) * self.minute_hand
        self.minute_y = math.sin(self.minute_angle) * self.minute_hand
        self.hour_x = math.cos(self.hour_angle) * self.hour_hand
        self.hour_y = math.sin(self.hour_angle) * self.hour_hand
        
    def update_time(self):
        """   """
        self.hand_angles()
        # Redraw
        self.canvas.delete("hands")
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.second_x, self.canvas_height/2 + self.second_y, fill = "red", tag = "hands")
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.minute_x, self.canvas_height/2 + self.minute_y, fill = "blue", tag = "hands")
        self.canvas.create_line(self.center_of_canvas, self.canvas_width/2 + self.hour_x, self.canvas_height/2 + self.hour_y, fill = "green", tag = "hands")
        
        # update time
        self.canvas.delete("time")
        self.check_time()
        self.canvas.create_text(self.canvas_width/2, self.canvas_height/2 + self.radius*1.1, 
                                text = str(self.current_hour) + ":" + self.display_minute +
                                ":" + self.display_second, tag = "time")

        #schedule next event
        self.timer = self.canvas.after(self.time_interval, self.update_time)
    
    def check_time(self):
        if self.current_hour > 12:
            self.current_hour = self.current_hour - 12

        if self.current_second < 10:
            self.display_second = "0" + str(self.current_second)
        else:
            self.display_second = str(self.current_second)

        if self.current_minute < 10:
            self.display_minute = "0" + str(self.current_minute)
        else:
            self.display_minute = str(self.current_minute)

    def quit(self):
        """ Quit the simulation. """
        self.window.destroy()



if __name__ == "__main__":
    Display_Clock()
