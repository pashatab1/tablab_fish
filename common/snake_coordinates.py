#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
snake_coordinates function
Purpose: Identify head position (x_head,y_head) and calculate
        center of mass (x_com, y_com) from list of x and y positions
  
Inputs: x,y - x and y are pandas series and all xy data are related to same snake at same time

Assumes numpy imported as np

Returns: [x_head,y_head,x_com, and y_com] 

@author: tabatabai
"""

def main(x,y):
    x_head = x.iloc[-1]
    y_head = y.iloc[-1]
    x_com = x.mean()
    y_com = y.mean()
    return np.array([x_head,y_head,x_com,y_com])

