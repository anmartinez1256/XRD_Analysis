#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize 
from scipy.signal import argrelmax
import itertools


# In[168]:


def read_data(txt_file, connect = False):
    txt_file = open(txt_file, "r")
    angle = []
    counts = []
    coefficient = [800, 100, 10, 1]
    #checks if the file is a connected file or not
    if connect:
        #use while TRUE because readline moves down one line
        connector_coefficient = 0
        while True:
            #determine which multiplier to use
            try:
                data = txt_file.readline()
                #need to multiply the data to line up the various pieces
                if data == '\n':
                    #skip \n pieces of data
                    connector_coefficient += 1
                    continue
                #reads line, strips whitespace, splits around comma, maps to float
                listed_data = list(map(float, data.strip().split(',')))
                angle.append(listed_data[0])
                counts.append(np.log(listed_data[1] * coefficient[connector_coefficient]))
            except:
                return (np.array(angle), normalize(counts))
    else:
        while True:
            try:
                data = txt_file.readline().strip().split(",")
                if len(data) == 2 and not float(data[1]) == 0:
                    angle.append(float(data[0]))
                    counts.append(np.log(float(data[1])))
                else:
                    break
            except:
                break
    return (np.array(angle), normalize(counts))


# In[169]:


def normalize(data):
    q = max(data)
    v = map(lambda x: x/max(data), data)
    return np.array(list(v))


# In[170]:


def plot_data(angle, counts, maxima = None):
    plt.title("Intensity vs Angle")
    plt.xlabel("Angle(2θ)")
    plt.ylabel("Relative Intensity")
    plt.plot(angle, counts)
    if maxima is not None:
        plt.scatter(angle[maxima], counts[maxima])


# In[171]:


def find_extrema(counts, orde):
    a = argrelmax(counts, order = orde)[0]
    return a


# In[181]:


def calculate_thickness(angle, maxima):

    def equation(m_tuple, n_tuple):
        wavelength = 0.154187
        m, theta_m = m_tuple
        n, theta_n = n_tuple
        d = (wavelength/2) * (m-n)/(np.sin(theta_m/2) - np.sin(theta_n/2))
        return d
    
    #get m and angles
    m = list(range(len(maxima)))
    diffraction_fringes = list(zip(m, angle[maxima]))
    
    thickness = []
    for i, m in enumerate(diffraction_fringes[:-1]):
        n = diffraction_fringes[i+1]
        thickness.append(equation(m, n))
    print(thickness)


# In[182]:

if __name__ == "__main__":
    file_path = input("TYPE FILE PATH HERE: ")
    angle, counts = read_data(file_path)
    angle_c, counts_c = read_data(file_path, True)
    maxima = find_extrema(counts, 10)
    maxima_c = find_extrema(counts_c, 10)
    #plot_data(angle, counts, maxima)
    #plot_data(angle_c, counts_c, maxima_c)
    calculate_thickness(angle_c, maxima_c)


# In[ ]:




