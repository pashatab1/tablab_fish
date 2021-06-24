#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 12:50:01 2021
#Find lifetime of neighbors


@author: tabatabai
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, ConvexHull, convex_hull_plot_2d

def PolyArea(x,y):
    #implementation of Gauss's area formula
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def read_position_data(N_Fish,N_Data_Files,N_Frames,Series_Name):
    #Function read_position_data() takes input paramaters for the series 'Series_Name'
    #and outputs an arrays containing the X and Y postiion data for that series.

    #Notes to make sure this works: N_Frames is important--make sure it's the actual number
    #of frames in the *whole* sample (not just for one "fish") otherwise you will get errors
    
    X = np.zeros((N_Fish,N_Frames)) 
    Y = np.zeros((N_Fish,N_Frames))
    
    if type(Series_Name) != str:
        print('Series_Name must be a string \n Thanks!')
        return

    for index in range(N_Data_Files):
        filename = Series_Name + '_fish%g' % index + '.npz'
        print(filename)
        fish_data = np.load(filename, allow_pickle=True)

        active_frames = fish_data['frame']
        if len(active_frames) != N_Frames:
            num_pixels = np.zeros(N_Frames)
            fish_X = np.zeros(N_Frames)
            fish_Y = np.zeros(N_Frames)

            for i in range(len(active_frames)):
                num_pixels[int(active_frames[i])] = fish_data['num_pixels'][i]
                fish_X[int(active_frames[i])] = fish_data['X'][i]
                fish_Y[int(active_frames[i])] = fish_data['Y'][i]
        else:
            num_pixels = fish_data['num_pixels']
            fish_X = fish_data['X']
            fish_Y = fish_data['Y']
            
        for i in range(N_Frames):
            check = True
            if num_pixels[i] < np.inf:
                for j in range(N_Fish):
                    if X[j,i] == 0 and Y[j,i] == 0 and check == True:
                        X[j,i] = fish_X[i]
                        Y[j,i] = fish_Y[i]
                        check = False
        
    statement = 'Tracking issues detected, fish missing on frames:'
    flag = True
    missing = []
    for i in range(N_Frames): 
        for j in range(N_Fish):
            if X[j,i] == Y[j,i] == 0:
                missing.append(i)
                statement = statement + ' %g' % i
                flag = False
    if flag:
        print('All fish accounted for!')
    else:
        print(statement)
        
    Position = X,Y,missing
    return Position


def find_neighbors(X,Y,N_Frames):
    """Use voronoi polygons to find neighbors of every particle with a closed voronoi area
    
    Outputs dataframe: columns for frame, particles of interest, and
                        neighbors of that particle
    
    """

    df = pd.DataFrame(columns = ['Frame','Fish','Neighbors'])
    for jj in range(N_Frames):
        # Restructures coordinates from .npz files (fish centeric -> frame centric)
        x = []
        y = []
        #if j not in P[2]: #skips frames where errors occur
        for ii in range(N_Fish):
            x.append(X[jj][ii]) #order reversed from test data
            y.append(-Y[jj][ii])    

        points = []
        for k in range(N_Fish):
            points.append([x[k],y[k]])
        vor = Voronoi(points)
        school_hull = find_hull(points)
        print('here')
        
        for reg in vor.regions:
            if -1 not in reg and reg != []:
                # only looks at vertices of closed regions contained within hull
                these_vertices = []
                for v in reg:
                    these_vertices.append(v)
                in_out = in_hull(these_vertices,school_hull)
                if in_out:
                    print('here')
                    
                    neighbors = []
                    for k in range(0,len(vor.ridge_vertices)):
                        # go through ridge vertices to find matches to vertices in closed region
                        v = vor.ridge_vertices[k]
                        if -1 not in v and (v[0] in reg or v[1] in reg):
                            # use index of ridge vertices to find neighboring points
                            neighbors.append(vor.ridge_points[k])
                            #print(neighbors)
                    flat_neighbors = [item for sublist in neighbors for item in sublist]
                    #print(flat_neighbors)  
                    
                    # remove duplicates from point list
                    uniq = []
                    dup = []
                    for i in flat_neighbors:
                        if i not in uniq:
                            uniq.append(i)
                        else:
                            dup.append(i)
                    
                    #remove the last remaining duplicate aka particle we care about
                    uniq.remove(dup[0])                
                    df = df.append({'Frame':jj,'Fish':dup[0],'Neighbors':uniq},ignore_index=True)
        
    return df
                
                
N_Fish = 23
N_Data_Files = 23
N_Frames = 20 #If N_frames is too small, there will be an error. If too large, extra frames will show missing, but still function
#Series_Name = '/Volumes/storage/pasha/2021/210226/data/series4full'
Series_Name = '/Volumes/storage/pasha/2021/fromDanny210527/data/series8_1-20'


P = read_position_data(N_Fish,N_Data_Files,N_Frames,Series_Name)
X = P[0]
Y = P[1]





def lifetimes(df,N_Fish,missing):
    '''Reads in dataframe from find_neighbors
    Determines lifetimes of each set of neighbors
    Outputs life
    '''
    life = []
    voronoi_opened_up = 0
    neighbors_changed = 0
    for jj in range(N_Fish):
        df2 = df.loc[df['Fish'] == jj]
        #print(df2.head())
        count = 1

        for kk in range(df2.shape[0]-1):    
            # Compare neighbors in subsequent frames, tallying lifetimes
            n1 = set(df2.iloc[kk]['Neighbors'])
            n2 = set(df2.iloc[kk+1]['Neighbors'])
            # particle is enclosed in subsequent frames and neighbors are same
            stayed_closed  = True
            stayed_same = True
            
            if df2.iloc[kk]['Frame'] not in missing:
                # only keep tabs if this frame has no tracking issues
                if df2.iloc[kk]['Frame'] != (df2.iloc[kk+1]['Frame']-1):
                    #broke up logic for definitional clarity
                    stayed_closed = False
                    voronoi_opened_up += 1
                # elif n1 != n2: # rigid constraint, option 1
                #     stayed_same = False
                #     neighbors_changed += 1
                elif 0.75 * len(n1) >= len(n1.intersection(n2)): # less rigid constraint, option 2
                    stayed_same = False
                    neighbors_changed += 1
                if stayed_closed and stayed_same:
                    count += 1
                else:
                    life.append(count)
                    count = 1   
            else:
                count = 1

    return life,voronoi_opened_up, neighbors_changed

def find_hull(pts):
    #pts = [(x[i],y[i]) for i in range(0,len(x))] # put in right format for ConvexHull
    #hull = ConvexHull(pts)
    hull = Delaunay(pts)
    return hull

def in_hull(pts,hull):
    # From stackexchange
    # Tells if ALL x,y points are in delaunay triangulation (hull)
    # Returns TRUE if all pts in hull, FALSE if not all in hull
    #pts = [(x[i],y[i]) for i in range(0,len(x))] # put in right format for Delaunay
    res = hull.find_simplex(pts)>=0
    return res.all()


# X = [1,1,1,2,2,2,3,3,3]
# Y = [1,2,3,1,2,3,1,2,3]
# test area
X = [[1,1,1,2,2,2,3,3,3],[1,1,1,2,2,2,3,3,3]]
Y = [[1,2,3,1,2,3,1,2,3],[1,2,3,1,2,3,1,2,3]]


N_Frames = 2
N_Fish = 9

df = find_neighbors(X,Y,N_Frames)
print(df)   
[life,voronoi_opened_up, neighbors_changed] = lifetimes(df,N_Fish,P[2])

plt.figure()
plt.hist(life,bins = 30)
plt.show()

print('Number of Voronoi volumes that opened : ' ,str(voronoi_opened_up))
print('Number of neighbors that changed : ' ,str(neighbors_changed))






#hull = find_hull(X,Y)
#res = in_hull([5,1],[1,1],hull)
#print(res)

# Extras
#print(vor.ridge_vertices)
#print(vor.ridge_points) 



