#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Determine pixel/inch ratio from linescan across ruler

Inputs:
filename - full path to csv file containing Position and Intensity Value

Assumes:
Image is taken of inch side of ruler, and smallest ticks are 1/8 inch increment

@author: tabatabai
"""

import numpy as np
from math import nan
import matplotlib.pyplot as plt
import pandas as pd

# Read in data
# filename = '/Users/tabatabai/Desktop/linescan_closestToWindow.csv'
# filename = '/Volumes/storage/pasha/2020/201210/linescan_rulerOnAcrylicSheetOnFiberBoardOnRecycleBin.csv'


def main(filename):
    df = pd.read_csv(filename) 
    
    # Plot raw data
    ax1 = plt.subplot(1,2,1)
    plt.plot(df['Distance_(pixels)'], df.Gray_Value) 
    ax1.set_xlim(200,300)
    ax1.set_ylim(60,90)
    ax1.set_ylabel('Pixel Gray Value')
    ax1.set_xlabel('Pixel Position')
    
    # Calculate FFT of Intensities
    y = np.fft.fft(df.Gray_Value.to_numpy()) #calculates fast fourier transform
    y[0] = nan #First position due to data shift (not about 0)
    yystar = y*np.conj(y) # Multiply by complex conjugate - now everything real
    
    # Generate frequencies corresponding to FFT
    xf = np.linspace(0,.5,int(np.floor(len(df.Gray_Value)/2))) # frequencies used in fft
    
    # Plot Power Spectrum
    ax2 = plt.subplot(1,2,2)
    plt.plot(xf,yystar[0:int(np.floor(len(df.Gray_Value)/2))])
    ax2.set_xlim(0, .25)
    ax2.set_ylabel('Power Spectrum')
    ax2.set_xlabel('Frequency (1/d)')
    # plt.savefig('Linescan.png')
    plt.show()
    
    # Convert from frequency to px/inch
    indx = np.nanargmax(yystar[0:int(np.floor(len(df.Gray_Value)/2))]) # Max of power spectrum occurs at this index
    frequency = xf[indx]
    repeating_distance = 1/frequency
    
    print('Repeating distance = ', str(repeating_distance), ' pixels')

    
# inches_per_pixel = 1/(8*repeating_distance) # this is where 1/8 inch increment comes in
# pixels_per_inch = 1/inches_per_pixel

# # Print to screen relevant information 
# print('Repeating distance = ', str(repeating_distance))
# print('Inches per pixel = ', str(inches_per_pixel))
# print('Pixels per inch = ', str(pixels_per_inch))





