"""
Module: greedy snake

the common snake game.

Authors:
1) Garrett - gcarney@sandiego.edu
2) Natalie - natalienguyen@sandiego.edu

Date: 11-16-2021
"""



import random
import tkinter as tk
from tkinter.constants import NW, SOLID
from tkinter.font import Font
from enum import Enum
import time


class Snake:
    """ This is the controller """
    def __init__(self):
        """ Initializes the game of life """
        # Define parameters
        self.NUM_ROWS = 30
        self.NUM_COLS = 30
        self.DEFAULT_STEP_TIME_MILLIS = 1000
        self.is_running = False

        self.start_time = 0
        self.pause_time = 0

        # Set up step time
        self.step_time_millis = self.DEFAULT_STEP_TIME_MILLIS

        #Create model
        self.model = SnakeModel(self.NUM_ROWS,self.NUM_COLS)

        # Create view
        self.view = SnakeView(self.NUM_ROWS, self.NUM_COLS)

        #initialize food and head

        self.view.make_food(self.model.current_food_location[0], self.model.current_food_location[1])
        self.view.make_head(self.model.snake_location[0][0],self.model.snake_location[0][1])

        # Start
        self.view.set_start_handler(self.start_handler)
        
        # Pause
        self.view.set_pause_handler(self.pause_handler)

        # Step speed
        self.view.set_step_speed_handler(self.step_speed_handler)

        # Reset 
        self.view.set_reset_handler(self.reset_handler)

        # Quit
        self.view.set_quit_handler(self.quit_handler)

        #wraparound handler 
        self.view.set_wraparound_handler(self.wraparound_handler)

        #left handler
        self.view.set_left_key_handler(self.left_handler)

        #right handler
        self.view.set_right_key_handler(self.right_handler)

        #up handler
        self.view.set_up_key_handler(self.up_handler)

        #down handler
        self.view.set_down_key_handler(self.down_handler)

        # Start the simulation
        self.view.window.mainloop()

    def start_handler(self):
        """ Start simulation  """
        print("Start simulation")
        if not self.is_running:
            self.is_running = True
            self.view.schedule_next_step(self.step_time_millis, 
                                        self.continue_simulation)            
            if self.start_time!=0:
                self.start_time = self.start_time + (time.time() - self.pause_time)
            else:
                self.start_time = time.time()


        
    def pause_handler(self):
        """ Pause simulation """
        print("Pause simulation")
        if self.is_running:
            self.pause_time = time.time()
            self.view.cancel_next_step()
            self.is_running = False
        
    def reset_handler(self):
        """ Reset simulation using view and model reset buttons """
        print("Reset simulation")
        self.pause_handler()
        if self.model.game_over:
            self.model.game_over = False
            self.view.game_over_var = ""
            self.view.game_over_textbox["text"] = self.view.game_over_var
        self.model.reset()
        self.view.reset()
        self.view.make_food(self.model.current_food_location[0], self.model.current_food_location[1])
        self.view.make_head(self.model.snake_location[0][0],self.model.snake_location[0][1])
        self.start_time = time.time()




    def quit_handler(self):
        """ Quit life program """
        print("Quit program")
        self.view.window.destroy()

    def step_speed_handler(self, value):
        """ Adjust simulation speed"""
        print("Step speed: Value = %s" % (value))
        self.step_time_millis = self.DEFAULT_STEP_TIME_MILLIS // int(value)

    def wraparound_handler(self):
        """ toggle whether wraparound is allowed"""
        if self.model.game_over:
            return
        if self.model.wraparound:
            self.model.wraparound = False
        else:
            self.model.wraparound = True
        print("wraparound called")
    
    def left_handler(self, event):
        ''' move the snakes direction to the West'''
        if self.model.game_over:
            pass
        else:
            self.model.current_direction = "W"

    
    def right_handler(self, event):
        ''' move the snakes direction to the east'''
        if self.model.game_over:
            pass
        else:
            self.model.current_direction = "E"


    def up_handler(self, event):
        ''' move the snakes direction to the north'''
        if self.model.game_over:
            pass
        else:
            self.model.current_direction = "N"


    def down_handler(self, event):
        ''' move the snakes direction to the south'''
        if self.model.game_over:
            pass
        else:
            self.model.current_direction = "S"


    
    def continue_simulation(self):
        """ Perform another step of the simulation, and schedule
            the next step.
        """
        self.one_step()
        self.view.schedule_next_step(self.step_time_millis, self.continue_simulation)
    
    def one_step(self):
        ''' perform one step of simulation '''
        #update model
        self.model.one_step()

        # Update the view
        if not self.model.game_over:
            for row in range(self.NUM_ROWS):
                for col in range(self.NUM_COLS):
                    if self.model.is_body(row, col):
                        self.view.make_body(row, col)
                    elif self.model.is_head(row,col):
                        self.view.make_head(row, col)
                    elif self.model.is_food(row,col):
                        self.view.make_food(row,col)
                    else:
                        self.view.make_empty(row,col)
            self.view.score_var = self.model.points
            self.view.timer = time.time() - self.start_time
            #self.view.timer = float(self.view.time_var) - self.start_time - self.pause_time
            self.view.time_var = "{:.2f}".format(self.view.timer)
            self.view.points_per_sec_var = "{:.2f}".format((float(self.view.score_var)/float(self.view.timer)))
            self.view.update_scores()
        #instead of add score just update the labels
        else:
            self.view.cancel_next_step()
            self.view.game_over_var = "Game Over"
            self.view.game_over_textbox["text"] = self.view.game_over_var
    


    


class SnakeView:
    def __init__(self, num_rows, num_cols):
        """ Initialize view of the game """
        # Constants
        self.CELL_SIZE = 20
        self.CONTROL_FRAME_HEIGHT = 100
        self.SCORE_FRAME_WIDTH = 200
        self.PAD_X_VAL = 25
        self.BORDER_WIDTH = 1

        #label vars 
        self.score_var = 0
        self.timer = 0.0
        self.time_var = "{:.2f}".format(self.timer)
        if float(self.time_var) > 0:
            self.points_per_sec_var = str(round((self.score_var/self.time_var),2))
        else:
            self.points_per_sec_var = '0'
        self.game_over_var = ""
        # Size of grid
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Create window
        self.window = tk.Tk()
        self.window.title("Greedy Snake")

        # Create frame for grid of cells, and put cells in the frame
        self.grid_frame = tk.Frame(self.window, height = num_rows * self.CELL_SIZE,
                                width = num_cols * self.CELL_SIZE)
        self.grid_frame.grid(row = 1, column = 1) # use grid layout manager

        # Create frame for controls
        self.control_frame = tk.Frame(self.window, width = num_cols * self.CELL_SIZE + self.SCORE_FRAME_WIDTH, 
                                height = self.CONTROL_FRAME_HEIGHT)
        self.control_frame.grid(row = 2, column = 1, columnspan=2) # use grid layout manager   
        self.cells = self.add_cells()

        self.control_frame.grid_propagate(False)
        (self.start_button, self.pause_button, 
        self.step_speed_slider, self.reset_button,
         self.quit_button, self.wraparound_box) = self.add_control()

        # Create frame for grid of cells, and put cells in the frame
        self.score_frame = tk.Frame(self.window, height = num_rows * self.CELL_SIZE,
                                width = self.SCORE_FRAME_WIDTH)
        self.score_frame.grid(row = 1, column = 2) # use grid layout manager

        self.score_frame.grid_propagate(False)
        (self.score_label, self.points_textbox,self.time_textbox, self.points_per_sec_textbox, self.game_over_textbox) = self.add_score()
    
    def add_control(self):
        """ 
        Create control buttons and slider, and add them to the control frame 
        """
        start_button = tk.Button(self.control_frame, text="Start")
        start_button.grid(row=1, column=1,padx = self.PAD_X_VAL)
        pause_button = tk.Button(self.control_frame, text="Pause")
        pause_button.grid(row=1, column=2,padx = self.PAD_X_VAL)
        step_speed_slider = tk.Scale(self.control_frame, from_=1, to=10, 
                    label="Step Speed", showvalue=0, orient=tk.HORIZONTAL)
        step_speed_slider.grid(row=1, column=3,padx = self.PAD_X_VAL)
        reset_button = tk.Button(self.control_frame, text="Reset")
        reset_button.grid(row=1, column=4,padx = self.PAD_X_VAL)
        quit_button = tk.Button(self.control_frame, text="Quit")
        quit_button.grid(row=1, column=5,padx = self.PAD_X_VAL)
        wraparound_box = tk.Checkbutton(self.control_frame, text= "Wraparound")
        wraparound_box.grid(row=1, column=6,padx = self.PAD_X_VAL)

        # Vertically center the controls in the control frame
        self.control_frame.grid_rowconfigure(1, weight = 1) 

        # Horizontally center the controls in the control frame
        self.control_frame.grid_columnconfigure(0, weight = 1) 
        self.control_frame.grid_columnconfigure(7, weight = 1) 
                                                            
        return (start_button, pause_button, step_speed_slider, 
                reset_button, quit_button, wraparound_box)
    
    def add_score(self):
        '''
        add the widgets for the score frame
        '''

        score_label = tk.Label(self.score_frame, text = "Score")
        score_label.grid(row=1, column=1, sticky="N")

        points_textbox = tk.Label(self.score_frame, text = "Points: " + str(self.score_var), borderwidth=self.BORDER_WIDTH, relief=SOLID)
        points_textbox.grid(row=2, column=1, sticky="N")

        time_textbox = tk.Label(self.score_frame, text = "Time: " + str(self.time_var), borderwidth=self.BORDER_WIDTH, relief=SOLID)
        time_textbox.grid(row=3, column=1, sticky="N")

        points_per_sec_textbox = tk.Label(self.score_frame, text = "Point per sec: " + self.points_per_sec_var, borderwidth=self.BORDER_WIDTH, relief=SOLID)
        points_per_sec_textbox.grid(row=4, column=1, sticky="N")

        game_over_textbox = tk.Label(self.score_frame, text = self.game_over_var)
        game_over_textbox.grid(row=5, column=1, sticky="N")
        
         # Vertically center the controls in the control frame
        self.score_frame.grid_rowconfigure(1, weight = 1) 
        self.score_frame.grid_rowconfigure(2, weight = 1) 
        self.score_frame.grid_rowconfigure(3, weight = 1) 
        self.score_frame.grid_rowconfigure(4, weight = 1) 
        self.score_frame.grid_rowconfigure(5, weight = 1) 
        self.score_frame.grid_rowconfigure(6, weight = 10) 

        # Horizontally center the controls in the control frame
        self.score_frame.grid_columnconfigure(0, weight = 1) 
        self.score_frame.grid_columnconfigure(7, weight = 1) 


        return(score_label,points_textbox, time_textbox, points_per_sec_textbox, game_over_textbox)

    def update_scores(self):
        '''update the points, points per sec and time labels'''
        self.points_textbox["text"] = "Points: " + str(self.score_var)
        self.time_textbox["text"] = "Time: " + str(self.time_var)
        if float(self.time_var) == 0:
            self.points_per_sec_textbox["text"] = "Points per sec: " + "0"
        else:
            self.points_per_sec_textbox["text"] = "Points per sec: " + str(self.points_per_sec_var)


    def set_start_handler(self, handler):
        """ set handler for clicking on start button to the function handler """
        self.start_button.configure(command = handler)

    def set_pause_handler(self, handler):
        """ set handler for clicking on pause button to the function handler """
        self.pause_button.configure(command = handler)


    def set_reset_handler(self, handler):
        """ set handler for clicking on reset button to the function handler """
        self.reset_button.configure(command = handler)

    def set_quit_handler(self, handler):
        """ set handler for clicking on quit button to the function handler """
        self.quit_button.configure(command = handler)

    def set_step_speed_handler(self, handler):
        """ set handler for dragging the step speed slider to the function handler """
        self.step_speed_slider.configure(command = handler)

    def set_wraparound_handler(self, handler):
        """ set handler for wraparound check box to the function handler """
        self.wraparound_box.configure(command = handler)

    def set_left_key_handler(self, handler):
        """ set handler for left key """
        self.window.bind('<Left>', handler)
    
    def set_right_key_handler(self, handler):
        """ set handler for right key """
        self.window.bind('<Right>', handler)
    
    def set_down_key_handler(self, handler):
        """ set handler for down key """
        self.window.bind('<Down>', handler)
    
    def set_up_key_handler(self, handler):
        """ set handler for up key """
        self.window.bind('<Up>', handler)

    def make_food(self,row,col):
        """ Make the cell in row, col food. """
        self.cells[row][col]['bg'] = 'red'

    def make_head(self,row,col):
        """ Make the cell in row, col the head. """
        self.cells[row][col]['bg'] = 'black'
    
    def make_empty(self,row,col):
        """ Make the cell in row, col empty. """
        self.cells[row][col]['bg'] = 'white'
    
    def make_body(self,row,col):
        """ Make the cell in row, col part of snake body. """
        self.cells[row][col]['bg'] = 'blue'
    
    def reset(self):
        """ reset all cells to empty and update the score frame """
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.make_empty(r, c)
        self.time_var = "0.00"
        self.points_per_sec_var = "0"
        self.update_scores()
         
    def schedule_next_step(self, step_time_millis, step_handler):
        """ schedule next step of the simulation """
        self.start_timer_object = self.window.after(step_time_millis, step_handler)

    def cancel_next_step(self):
        """ cancel the scheduled next step of simulation """
        self.window.after_cancel(self.start_timer_object)

    def add_cells(self):
        """ Add cells to the grid frame """
        cells = []
        for r in range(self.num_rows):
            row = []
            for c in range(self.num_cols):
                frame = tk.Frame(self.grid_frame, width = self.CELL_SIZE, 
                        height = self.CELL_SIZE, borderwidth = 1, 
                        relief = "solid") 
                frame.grid(row = r, column = c) 
                row.append(frame)
            cells.append(row)
        return cells

class SnakeModel:
    def __init__(self, num_rows, num_cols):
        """ initialize the model of the game """
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.wraparound = False
        #itialize instance variables using function
        self.initialize_cells_and_states()

        
        #itialize food and head
        self.make_food()
        self.make_head()
 

    def make_food(self):
        """ Make the cell in random row and col food. """
        point = self.open_cells.pop(random.randrange(0,len(self.open_cells)))
        row = point[0]
        col = point[1]
        self.state[row][col] = CellState.FOOD
        self.current_food_location = (row,col)

    def make_head(self):
        """ Make the cell in a random row and col the head. """
        point = self.open_cells.pop(random.randrange(0,len(self.open_cells)))
        row = point[0]
        col = point[1]
        self.state[row][col] = CellState.SNAKE_HEAD
        self.snake_location.append((row,col))

    def make_body(self, row, col):
        """ Make the cell in row, col part of snake body. """
        self.state[row][col] = CellState.SNAKE_BODY
        self.open_cells.remove((row,col))
    
    def is_food(self, row, col):
        """ returns true if cell in row, col is food """
        return self.state[row][col] == CellState.FOOD

    def is_body(self, row, col):
        """ returns true if cell in row, col is part of snake body  """
        return self.state[row][col] == CellState.SNAKE_BODY

    def is_head(self, row, col):
        """ returns true if cell in row, col is the snake head  """
        return self.state[row][col] == CellState.SNAKE_HEAD


    def reset(self):
        """ Resets all cells to empty and recreates food and head """
        self.initialize_cells_and_states()
        self.make_food()
        self.make_head()
    

    def initialize_cells_and_states(self):
        '''
        initializes variables here to be utilized in the contructor
        '''
        self.current_food_location = None
        self.snake_location = []
        self.game_over = False
        self.current_direction = "S"
        self.points = 0
        self.open_cells = []
        self.state = []
        for row in range(self.num_rows):
            rows = []
            for col in range(self.num_cols):
                self.open_cells.append((row, col))
                rows.append(CellState.EMPTY)
            self.state.append(rows)
    

    def one_step(self):
        ''' 
        perform one step of simulation 
        call the one step helper with the next iteration snake head cordinates
        if wraparound not enables and reaches wall game over variable asigned to true
        '''
        head_row = self.snake_location[0][0]
        head_col = self.snake_location[0][1]
        if self.current_direction == "E":
            if head_col+1 == self.num_cols and not self.wraparound:
                self.game_over = True
            elif head_col + 1== self.num_cols and self.wraparound:
                self.one_step_helper(head_row,head_col+1-self.num_cols)
            else:
                self.one_step_helper(head_row,head_col+1)
        elif self.current_direction == "W":
            if head_col == 0 and not self.wraparound:
                self.game_over = True
            elif head_col == 0 and self.wraparound:
                self.one_step_helper(head_row,head_col-1+self.num_cols)
            else:
                self.one_step_helper(head_row,head_col-1)
        elif self.current_direction == "N":
            if head_row== 0 and not self.wraparound:
                self.game_over = True
            elif head_row  == 0 and self.wraparound:
                self.one_step_helper(head_row-1+self.num_rows,head_col)
            else:
                self.one_step_helper(head_row-1,head_col)
        else:
            if head_row+1== self.num_rows and not self.wraparound:
                self.game_over = True
            elif head_row + 1== self.num_rows and self.wraparound:
                self.one_step_helper(head_row+1-self.num_rows,head_col)
            else:
                self.one_step_helper(head_row+1,head_col)
    
    def one_step_helper(self, head_row, head_col):
        '''
        checks to see if next cell is body and if it is, enables reset
        makes food and adds point if the cell is food
        calls next states to get snake location, state, and open cell variables.
        '''
        if not self.is_body(head_row,head_col):
            self.next_states(head_row,head_col)
            if self.current_food_location ==None:
                self.make_food()
                self.points+=1
        else:
            self.reset()
        

    def next_states(self,head_row, head_col):
        '''
        edits the next state, open cells, and snake location variables and assigns 
        them to their corresponding variables to be accessed later.
        if the next cell isnt food, it removes the last cell from the snake and shifts snake over.
        '''
        next_state = []
        next_open_cells = []
        next_snake_location = []
        for row in range(self.num_rows):
            rows = []
            for col in range(self.num_cols):
                next_open_cells.append((row, col))
                rows.append(CellState.EMPTY)
            next_state.append(rows)
        next_snake_location.append((head_row,head_col))
        next_open_cells.remove((head_row,head_col))
        next_state[head_row][head_col] = CellState.SNAKE_HEAD
        for point in self.snake_location:
            next_snake_location.append((point[0],point[1]))
            next_open_cells.remove((point[0],point[1]))
            next_state[point[0]][point[1]] = CellState.SNAKE_BODY
        if not self.is_food(head_row,head_col):
            last_point = self.snake_location[-1]
            next_snake_location.remove((last_point[0],last_point[1]))
            next_open_cells.append((last_point[0],last_point[1]))
            next_state[last_point[0]][last_point[1]] = CellState.EMPTY
            next_state[self.current_food_location[0]][self.current_food_location[1]] = CellState.FOOD
            next_open_cells.remove((self.current_food_location[0],self.current_food_location[1]))
        else:
            self.current_food_location = None
        self.state = next_state
        self.open_cells = next_open_cells
        self.snake_location = next_snake_location
        

class CellState(Enum):
    """ 
    Uses enum so that each cell can be assigned a state
    using 1,2,3,4
    """
    FOOD = 1
    SNAKE_HEAD = 2
    SNAKE_BODY = 3
    EMPTY = 4

if __name__ == "__main__":
   snake_game = Snake()

