#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pair Correlation function for fish
Created on Thu Mar 18 13:14:55 2021

@author: tabatabai
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt


series_root = '/Volumes/storage/pasha/2021/210226/'
series_num = 5
#Example how to read pickled file made above
datafile = open(series_root + 'coordinates/coords_series' + str(series_num) + '.pickle', 'rb')      
XY = pickle.load(datafile)

fake_size=300
N_fake = 100
def fake_crystal():
    x = np.linspace(0, fake_size, N_fake)
    y = np.linspace(0, fake_size, N_fake)
    X, Y = np.meshgrid(x, y)+ 1*np.random.rand(N_fake,N_fake)
    return X, Y

def fake_gas():
    X = fake_size*np.random.rand(N_fake,N_fake)
    Y = fake_size*np.random.rand(N_fake,N_fake)
    return X,Y

X,Y = fake_crystal()


#X,Y = fake_gas()
#X=XY[0]
#Y=XY[1]

#print(X)
#print(X[1])
d=[]
n_pair=0
#make this work for fake data
for ii in range(X.shape[1]): #X.shape[1] is number of frames
    for jj in range(X.shape[0]): #X.shape[0] is number of fish
        for ll in range(ii,X.shape[1]-ii):
            for kk in range(jj,X.shape[0]-jj):
                dist = np.sqrt( (X[jj][ii]-X[kk][ll])**2 + (Y[jj][ii]-Y[kk][ll])**2 )
                if dist>0:
                    d.append(dist)
                    n_pair+=1

# for ii in range(X.shape[1]): #X.shape[1] is number of frames
#     for jj in range(X.shape[0]-1): #X.shape[0] is number of fish
#         for kk in range(jj+1,X.shape[0]):
#             dist = np.sqrt( (X[jj][ii]-X[kk][ii])**2 + (Y[jj][ii]-Y[kk][ii])**2 )
#             d.append(dist)

# tested below to avoid edges. Didn't do much to help
# for ii in range(50,150): #X.shape[1] is number of frames
#     for jj in range(50,149): #X.shape[0] is number of ffish
#         for kk in range(jj+1,X.shape[0]):
#             dist = np.sqrt( (X[jj][ii]-X[kk][ii])**2 + (Y[jj][ii]-Y[kk][ii])**2 )
#             d.append(dist)

#d = [i for i in d if i != 0]
#r = np.linspace(0,10,num=60)
r = np.linspace(0,40,num=200)
dr = np.diff(r)[0]
h, bin_edges = np.histogram(d,bins = r)

plt.figure()
plt.hist(d,bins = r)
plt.show()

total_particles = X.size
disk_area = 2*np.pi*bin_edges[1:]*dr
density = X.size/(fake_size*fake_size)
#density = n_pair/(fake_size*fake_size)
print(n_pair)
print(fake_size)


gr = h/(total_particles * disk_area * density)
plt.figure()
plt.plot(bin_edges[1:]*(N_fake)/fake_size, gr)
plt.show()


# this looks funky, and non normalized. fix to make sure it normalizes
# then worry about only looking at interior elements of convex hull



