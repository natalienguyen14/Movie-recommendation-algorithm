# File: statement_eval.py
# Author: Alizea Hinz and Natalie Nguyen
# Date: 9/23/2021
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements.

import re  # For regular expressions

class bad_statement(Exception):
    pass

def interpret_statements(filename):
    """
    Function that reads statements from the file whose
    name is filename, and prints the result of each statement,
    formatted exactly as described in the psa1 problem statement.  
    interpret_statements must use the evaluate_expression function,
    which appears next in this file.
    """
    
    try:
        # opens file and initializes variables
        f = open(filename)
        variables = {}
        line_count = 0
  
        for line in f: # loops through every line in filename
            try:
                # splits up the line into a list and determines whether it is a statement or an expression
                line_count += 1
                math = line.strip().split("#") 
                stripped = math[0].strip() #strips the first index of any spaces
                if len(math) > 0 and stripped != "":
                    tokens = stripped.split() 
                    if len(tokens)>= 3 and tokens[1] == '=': # for evaluations
                        if re.fullmatch("([a-zA-Z]|_)([a-zA-Z0-9]*|_*)", tokens[0]): # if variable name is valid, adds to dictionary CHECK ME
                            variables[tokens[0]]= evaluate_expression(tokens[2:], variables)
                            print(f"Line {line_count}: {tokens[0]} = {variables[tokens[0]]:.2f}")
                        else:
                            raise bad_statement
                    elif len(tokens) >= 3: # for expressions
                        expressions_value = evaluate_expression(tokens, variables)
                        print(f"Line {line_count}: {stripped} = {expressions_value:.2f}") 
                    elif tokens[0] in variables: # for just variables
                        print(f"Line {line_count}: {tokens[0]} = {variables[tokens[0]]:.2f}") 
                    elif is_float(tokens[0]) and len(tokens) == 1: # for just a float 
                        print(f"Line {line_count}: {tokens[0]} = {float(tokens[0]):.2f}")
                    else:
                        raise bad_statement   
            except (bad_statement, ValueError, TypeError, IndexError):
                print(f"Line {line_count}: Invalid statement") 
    
    except FileNotFoundError:
        print("Invalid File. ")

def evaluate_expression(tokens, variables):
    """
    Function that evaluates an expression represented by tokens.
    tokens is a list of strings that are the tokens of the expression.  
    For example, if the expression is "salary + time - 150", then tokens would be
    ["salary", "+", "time", "-", "150"].  variables is a dictionary that maps 
    previously assigned variables to their floating point values.

    Returns the value that is assigned.

    If the expression is invalid, the BadStatement exception is raised.
    """
    # decides if first item is a variable name or float, and initializes result
    result = 0
    if tokens[0] in variables: 
        result += variables[tokens[0]] 
    else:
        result += float(tokens[0])

    for i in range(1, len(tokens), 2): # goes to every other index in the list to get the operand
        if tokens[i+1] in variables: # determines whether next index is a variable
            if tokens[i] == '+':
                result += float(variables[tokens[i+1]])
            elif tokens[i] == '-':
                result -= float(variables[tokens[i+1]])
            else:
                raise bad_statement
        else: 
            if tokens[i] == '+':
                result += float(tokens[i+1])
            elif tokens[i] == '-':
                result -= float(tokens[i+1])
            else:
                raise bad_statement # makes sure there are no double operators or numbers
            
    return result


def is_float(x): 
    """ Checks if string is a float """
    try:
        float(x) # if is able to convert to a float, then returns a true value
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)
