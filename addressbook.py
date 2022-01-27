# File: addressbook.py
# Author: Natalie Nguyen and Alizea Hinz
# Date: 9/27/2021
# Description: 

import tkinter as tk

class Address:
    def __init__(self, name, street, city, state, zip):
        """ 
        Constructor for Address class.
        You will add parameters to this constructor. 
        """
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

class AddressBook:
    def __init__(self):
        """ Constructor for AddressBook class """
        # Create main window
        self.window = tk.Tk()
        self.window.title("Address Book")
        self.window.configure(bg = "white")
        self.DEFAULT_GREETING_STRING = "            "
        self.address_list = []
        self.current_index = 0

        self.top_frame = tk.Frame(self.window, bg = 'white')
        self.top_frame.configure(bg = "white")
        self.top_frame.grid(row = 1, column = 1)

        self.second_frame = tk.Frame(self.window, bg = 'red')
        self.second_frame.configure(bg = "white")
        self.second_frame.grid(row = 2, column = 1)

        self.middle_frame = tk.Frame(self.window, bg = 'white')
        self.middle_frame.configure(bg = "white")
        self.middle_frame.grid(row = 3, column = 1)

        self.bottom_frame = tk.Frame(self.window, bg = 'white')
        self.bottom_frame.configure(bg = "white")
        self.bottom_frame.grid(row = 4, column = 1)

        # Add name label
        self.name_label = tk.Label(self.top_frame, text = "Name", bg = 'white')
        self.name_label.grid(row = 1, column = 1, sticky = "W")
        # sticky = "W" forces the widget to be placed against the west boundary of the its cell.
        
        # Add name field
        self.name_var = tk.StringVar()  # A special string variable that will be associated
                                            # with the name entry field.  Whatever the user
                                            # types into the entry field can be accessed 
                                            # through this variable.
        self.name = tk.Entry(self.top_frame, width = 40, textvariable=self.name_var, bg = 'white')
        self.name.grid(row = 1, column = 2, sticky = "NW", columnspan = 1)
        
        # Add street label
        self.street_label = tk.Label(self.top_frame, text = "Street", bg = 'white')
        self.street_label.grid(row = 2, column = 1, sticky = "W")
        
        # Add street name field
        self.street_var = tk.StringVar() 
        self.street = tk.Entry(self.top_frame, width = 40, textvariable=self.street_var, bg = 'white')
        self.street.grid(row = 2, column = 2, sticky = "NW", columnspan = 1)
      
        # Add city label
        self.city_label = tk.Label(self.second_frame, text = "City  ", bg = 'white')
        self.city_label.grid(row = 3, column = 1, sticky = "W")
        
        # Add city field
        self.city_var = tk.StringVar() 
        self.city = tk.Entry(self.second_frame, textvariable=self.city_var, bg = 'white')
        self.city.grid(row = 3, column = 2, sticky = "NW")
        
        # Add state label
        self.state_label = tk.Label(self.second_frame, text = "State", bg = 'white')
        self.state_label.grid(row = 3, column = 5)
       
        # Add state field
        self.state_var = tk.StringVar() 
        self.state = tk.Entry(self.second_frame, width = 5, textvariable=self.state_var, bg = 'white')
        self.state.grid(row = 3, column = 6, columnspan = 1)
        
        # Add zip label
        self.zip_label = tk.Label(self.second_frame, text = "Zip", bg = 'white')
        self.zip_label.grid(row = 3, column = 7)
        
        # Add zip field
        self.zip_var = tk.StringVar() 
        self.zip = tk.Entry(self.second_frame, width = 5, textvariable=self.zip_var, bg = 'white')
        self.zip.grid(row = 3, column = 8, columnspan = 1)
        
        # Add filename label
        self.filename_label = tk.Label(self.bottom_frame, text = "Filename", bg = 'white')
        self.filename_label.grid(row = 2, column = 1, sticky = "W")
       
        # Add filename field
        self.filename_var = tk.StringVar()  
        self.filename = tk.Entry(self.bottom_frame, width = 10, textvariable=self.filename_var, bg = 'white')
        self.filename.grid(row = 2, column = 2, columnspan = 1)
       
        # Load File button
        self.load_file_button = tk.Button(self.bottom_frame, text = "Load File", command=self.Load_file, bg = 'white')
        self.load_file_button.grid(row = 2, column = 3)

        # Save to File button
        self.save_file_button = tk.Button(self.bottom_frame, text = "Save to File", command=self.Save_file, bg = 'white')
        self.save_file_button.grid(row = 2, column = 4)

        # Quit button
        self.quit_button = tk.Button(self.bottom_frame, text = "Quit", command=self.Quit, bg = 'white')
        self.quit_button.grid(row = 2, column = 5)

        # Add button
        self.add_button = tk.Button(self.middle_frame, text = "Add", command=self.Add, bg = 'white')
        self.add_button.grid(row = 1, column = 1)
        
        # Delete button
        self.delete_button = tk.Button(self.middle_frame, bg = 'white', text = "Delete", command=self.Delete)
        self.delete_button.grid(row = 1, column = 2)

        # Add First button
        self.first_button = tk.Button(self.middle_frame, text = "First", command=self.First, bg = 'white')
        self.first_button.grid(row = 1, column = 3)

        # Add Next button
        self.next_button = tk.Button(self.middle_frame, text = "Next", command=self.Next, bg = 'white')
        self.next_button.grid(row = 1, column = 4)

        # Add Previous button
        self.previous_button = tk.Button(self.middle_frame, text = "Previous", command=self.Previous, bg = 'white')
        self.previous_button.grid(row = 1, column = 5)

        # Add Last button
        self.last_button = tk.Button(self.middle_frame, text = "Last", command=self.Last, bg = 'white')
        self.last_button.grid(row = 1, column = 6)
        
        # Add address field
        self.address_string = tk.StringVar() 
        self.address_string.set(self.DEFAULT_GREETING_STRING)
        #self.address = tk.Label(self.bottom_frame, textvariable = self.address_string)
        #self.address.grid(row = 3, column = 2, sticky="W", padx = 10, pady = 10)


        # Extra space is divided among all of the rows, 
        # so they should be evenly spaced outl
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

        # Extra space is divided among all of the columns, 
        # so they should be evenly spaced outl
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)


    def Add(self):
        """ Adds currently displayed address to list of addresses.  """
        if (self.name_var.get() == "") or (self.street_var.get() == "") or (self.city_var.get() == "") or (self.state_var.get() == "") or (self.zip_var.get() == ""):
            pass
        else:
            self.address_list.append(Address(self.name_var.get(),self.street_var.get(), 
                                    self.city_var.get(), self.state_var.get(), self.zip_var.get()))

    def First(self):
        """ Displays first address in the list"""
 
        if len(self.address_list) > 0: #if something is in the list, prints first item in list in entry fields
            first = self.address_list[0]
            self.name_var.set(first.name)
            self.street_var.set(first.street)
            self.city_var.set(first.city)
            self.state_var.set(first.state)
            self.zip_var.set(first.zip)
            self.current_index = 0
        elif len(self.address_list) == 0:
            print("No addresses in the address book. ")

    def Next(self):
        """ Displays next address in the list"""

        if self.current_index < len(self.address_list)-1:
            self.current_index += 1
            next_address = self.address_list[self.current_index]
            self.name_var.set(next_address.name)
            self.street_var.set(next_address.street)
            self.city_var.set(next_address.city)
            self.state_var.set(next_address.state)
            self.zip_var.set(next_address.zip)
        elif self.current_index == len(self.address_list): # doesn't continue if on last index
            pass
        elif len(self.address_list) == 0: # case for empty list
            self.name_var.set('')
            self.street_var.set('')
            self.city_var.set('')
            self.state_var.set('')
            self.zip_var.set('')

    def Previous(self):
        """ Displays previous address in the list"""

        if self.current_index == 0: # if it is the first item in the list, does nothing
            pass
        elif len(self.address_list) == 0: # if list is empty
            self.name_var.set('')
            self.street_var.set('')
            self.city_var.set('')
            self.state_var.set('')
            self.zip_var.set('')
        elif self.current_index < len(self.address_list): # goes to previous index and displays in entry fields
            self.current_index -= 1
            previous_address = self.address_list[self.current_index]
            self.name_var.set(previous_address.name)
            self.street_var.set(previous_address.street)
            self.city_var.set(previous_address.city)
            self.state_var.set(previous_address.state)
            self.zip_var.set(previous_address.zip)


    def Last(self):
        """ Displays last address in the list"""
        if len(self.address_list) > 0: # goes to last item in the list
            last = self.address_list[len(self.address_list)-1]
            self.name_var.set(last.name)
            self.street_var.set(last.street)
            self.city_var.set(last.city)
            self.state_var.set(last.state)
            self.zip_var.set(last.zip)
            self.current_index = len(self.address_list)-1
        elif len(self.address_list) == 0: # if list is empty
            print("No addresses in the address book. ")
    
    def Delete(self):
        """ Deletes address from address book """
        if len(self.address_list) == 0: # is list is empty
            pass
        elif len(self.address_list) == 1: # deletes last remaining item in the list and displays nothing
            self.address_list.pop(self.current_index)
            self.name_var.set('')
            self.street_var.set('')
            self.city_var.set('')
            self.state_var.set('')
            self.zip_var.set('')
        elif len(self.address_list) > 0:
            #displays next address after the one that is deleted
            if self.current_index < (len(self.address_list) - 1):
                self.address_list.pop(self.current_index)
                #shift everything back one index
                self.current_index -= 1
                self.Next()
            else: # displays previous address if there is no next address
                self.address_list.pop(self.current_index)
                self.current_index -= 1
                previous_address = self.address_list[self.current_index]
                self.name_var.set(previous_address.name)
                self.street_var.set(previous_address.street)
                self.city_var.set(previous_address.city)
                self.state_var.set(previous_address.state)
                self.zip_var.set(previous_address.zip)
       
    def Load_file(self):
        """ Reads file and displays it in address book"""
        if self.filename_var.get() == '': # if entry field for filename is empty
            pass
        else:
            f = open(self.filename_var.get(), 'r')
            line_count = 0
            self.address_list = [] # clears current list
            for line in f: # goes through file and adds a complete address to the list every five lines
                line_count += 1
                if line_count == 5:
                    self.zip_var.set(line.strip())
                    line_count = 0 # restart counter
                    self.Add() #adds complete address to list
                elif line_count == 4:
                    self.state_var.set(line.strip())
                elif line_count == 3:
                    self.city_var.set(line.strip())
                elif line_count == 2:
                    self.street_var.set(line.strip())
                elif line_count == 1:
                    self.name_var.set(line.strip())
            self.First()
        

    def Save_file(self):
        """Saves the address to the filename in the entry field"""
        if self.filename_var.get() == '': # if entry field is empty, do nothing
            pass
        elif (self.name_var.get() == "") or (self.street_var.get() == "") or (self.city_var.get() == "") or (self.state_var.get() == "") or (self.zip_var.get() == ""):
            pass
        else:
            f = open(self.filename_var.get(), "w")
            for i in range(len(self.address_list)): # writes contents of list in the file for each address
                address = self.address_list[i]
                f.write(address.name + '\n')
                f.write(address.street + '\n')
                f.write(address.city + '\n')
                f.write(address.state + '\n')
                f.write(address.zip + '\n')


    def Quit(self):
        """Quits program, closes window"""
        self.window.destroy()

    def go(self):
        """ Start the event loop """
        self.window.mainloop()

def main():
    # Create the GUI program
    program = AddressBook()

    # Start the GUI event loop
    program.go()

if __name__ == "__main__":
    main()   
