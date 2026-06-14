#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 21:22:38 2025

@author: Marianne2
"""
# This simulation models the gravitational interaction between the Earth and the Moon.
# It computes their positions and velocities over time using Newton's law of gravitation and explicit Euler integration.
# The simulation also includes the Earth's axial rotation, although this is not taken into account in the gravitational calculations.
# The motion is calculated based on an initial set of parameters, including masses,
# initial positions, velocities, and time step. The results are used to plot the 
# trajectories of the Earth and Moon, with the simulation running for a specified 
# duration and time step size. 



import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from PIL import Image
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

#constants (in SI units)
G = 6.67430e-11 
M_earth = 5.972e24
M_moon = 7.348e22
R_earth = 6.371e6
R_moon = 1.737e6
R_earth_moon = 3.844e8
T_moon = 27.3 * 24 * 3600
T_earth_rotation = 24 * 3600

#timeframe settings
dt = 3600 #seconds
steps = 500 #number of time steps

#creating the plot
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.set_facecolor('black')
ax.grid(False)
ax.set_axis_off()

#making the earth look like earth and adding rotation
#earth_texture = Image.open("earth_visual.jpg")

def plot_earth(rotation_angle):
    """
    Plots a 3D model of the Earth with a given rotation angle.

    The function generates a spherical representation of the Earth using a 
    parametric surface plot and applies a rotation transformation around 
    the z-axis.

    Parameters:
    -----------
    rotation_angle : float
        The angle (in radians) by which the Earth is rotated around the z-axis.

    Returns:
    --------
    None
        The function modifies the global 3D plot by adding the Earth's surface.
    """
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = R_earth * np.outer(np.cos(u), np.sin(v))
    y = R_earth * np.outer(np.sin(u), np.sin(v))
    z = R_earth * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Apply rotation
    x_rot = x * np.cos(rotation_angle) - y * np.sin(rotation_angle)
    y_rot = x * np.sin(rotation_angle) + y * np.cos(rotation_angle)
    
    ax.plot_surface(x_rot, y_rot, z, rstride=1, cstride=1, facecolors=green / 255.0)

earth_rotation_speed = (2 * np.pi) / (T_earth_rotation / dt)  # Rotation per time step

#initial positions of Earth and Moon
pos_earth = np.array([0, 0, 0], dtype=float)
pos_moon = np.array([R_earth_moon, 0, 0], dtype=float)
vel_earth = np.array([0,0,0],dtype=float)
vel_moon = np.array([0,1022,0],dtype=float)

#storing positions to be calculated
earth_pos = []
moon_pos = []

#using Newtons' gravitational law to calculate updated positions for each timeframe and storing them in above arrays
for i in range(steps):
    r = np.linalg.norm(pos_moon - pos_earth)
    F = G*M_earth*M_moon/(r**2) #gravitational force
    
    #acceleration
    acc_earth = F/M_earth * (pos_moon - pos_earth)/r
    acc_moon = -F/M_moon * (pos_moon - pos_earth)/r
    
    #velocity
    vel_moon += acc_moon * dt
    vel_earth += acc_earth * dt
    
    #position
    pos_moon += vel_moon * dt
    pos_earth += vel_earth * dt
    

    earth_pos.append(pos_earth.copy())
    moon_pos.append(pos_moon.copy())

earth_pos = np.array(earth_pos)
moon_pos = np.array(moon_pos)

earth, = ax.plot([], [], [], 'o', color='green', markersize=R_earth/1e6)
moon, = ax.plot([], [], [], 'o', color='white', markersize=R_moon/1e6)

def update(frame):
    earth.set_data(earth_pos[frame, 0], earth_pos[frame, 1])
    earth.set_3d_properties(earth_pos[frame, 2])
    
    moon.set_data(moon_pos[frame, 0], moon_pos[frame, 1])
    moon.set_3d_properties(moon_pos[frame, 2])
    
    return earth, moon

ax.set_xlim(-5e8, 5e8)
ax.set_ylim(-5e8, 5e8)
ax.set_zlim(-2e8, 2e8)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

ani = FuncAnimation(fig, update, frames=steps, interval=50, blit=True)
plt.show()

ani.save("animation.gif", writer=animation.PillowWriter(fps=20))
