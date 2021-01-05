"""
read_snake_file function
Purpose: read .txt file outputted by JFilament
        convert this information into a dataframe df
        
        df has columns: snake_no, frame, pixel, xpos, ypos
        moving down df, you see all frames for a snake before moving to a new snake

Inputs: filename - path and file name to .txt file from snakes
        Assumes pandas read as pd
                numpy read as np

Returns: df - dataframe containing id's, frames, and positions
Dec 2020, APT confirms that pixel position is correct w.r.t. drawing direction
    (If you draw from tail to head, first pixel is at tail, last pixel is at head)

Created on Fri Dec 18 13:17:40 2020

@author: tabatabai
"""
def main(filename):
    with open(filename) as textFile:
        for _ in range(9): # does header always end by line 8? First line read after will be #
            next(textFile)
        lines = [np.array(line.split()) for line in textFile]
    
    stack = np.array([])  # initialize empty stack 
    snake_no = 0  
    for line in lines: # convert to np array and concatenate
        if len(line)>1: # Avoid converting # and 0 to float
            line_with_snake_no = np.hstack([snake_no,line.astype(np.float)])
            stack = np.vstack([stack,line_with_snake_no]) if stack.size else line_with_snake_no
        elif line[0] == '#':
            print('in')
            snake_no = snake_no + 1
    
    df = pd.DataFrame(data=stack, columns=["snake_no","frame", "pixel", "xpos", "ypos","zpos"])
    df=df.drop(columns=['zpos'])
    return df