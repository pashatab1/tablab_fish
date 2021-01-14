#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:41:44 2021

@author: tabatabai
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def snake_coordinates(x,y):
    """
    snake_coordinates function
    Purpose: Identify head position (x_head,y_head) and calculate
            center of mass (x_com, y_com) from list of x and y positions
      
    Inputs: x,y - x and y are pandas series and all xy data are related to same snake at same time
    Assumes numpy imported as np
    
    Returns: [x_head,y_head,x_com, and y_com] 
    APT
    """
    x_head = x.iloc[-1]
    y_head = y.iloc[-1]
    x_com = x.mean()
    y_com = y.mean()
    return np.array([x_head,y_head,x_com,y_com])



def all_snake_coordinates(df):
    """Calls snake_coordinates to find snake coordinates (COM and Head) for all 
    snakes in a snake file.
    
    Inputs: df - dataframe output by df = read_snake_file(filename)
    
    Returns: stats_df- dataframe containing COM and Head pixel positions for 
                        each snake in every frame
    
    APT
    """
    
    snake_stats = []
    num_snakes = int(df.snake_no.max())
    for snake in range(1,num_snakes+1): # Go through each snake
        frame_this_snake = df.frame[df.snake_no == snake]
        xpos_this_snake = df.xpos[df.snake_no == snake]
        ypos_this_snake = df.ypos[df.snake_no == snake]
        
        for frame in range(int(frame_this_snake.min()),int(frame_this_snake.max())+1): # Go through each frame
            [x_head,y_head,x_com,y_com] = snake_coordinates(xpos_this_snake[frame_this_snake == frame], 
                                                         ypos_this_snake[frame_this_snake == frame])
            
            stats_with_snake_info = np.concatenate(([snake,frame], [x_head,y_head,x_com,y_com]), axis=None)
            snake_stats.append(stats_with_snake_info)
            print(stats_with_snake_info)
       
    # turn that list into a dataframe
    stats_df = pd.DataFrame(snake_stats, columns=["snake_no","frame", "xhead", "yhead", "xcom","ycom"])
    
    return stats_df


def plot_snake_coordinates(stats_df, save_path_str):
    """
    Makes plot of snakes. Circles at COM and arrow connecting COM to head
    
    Inputs: stats dataframe, built by all_snake_coordinates
            save_path_str- string of path to save figure, including filename
                            Ex: save_path_str ='./tracking.png'
    APT
    """
    # plotting red dot at COM and arrow from COM to head
    plt.plot(stats_df.xcom,stats_df.ycom,'or',label = 'Center Of Mass')
    
    plt.quiver(stats_df.xcom, stats_df.ycom, (stats_df.xhead - stats_df.xcom),(-stats_df.yhead + stats_df.ycom),label = 'Center of Mass to Head')
    plt.axis('square')
    plt.xlim([0, 3000])
    plt.ylim([0, 3000])
    plt.xlabel('X position (px)')
    plt.ylabel('Y position (px)')
    #plt.legend(loc = 'lower left')
    plt.title('Title Here')
    
    plt.gca().invert_yaxis()
    plt.savefig(save_path_str)
    plt.show()