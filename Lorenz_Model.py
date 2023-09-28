#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 17:25:58 2023

@author: santiago
"""

"""
                                                                              
 This procedure solves the Lorenz system of ordinary differential equations by means of the 4th order Runge Kutta method
 and returns simulation videos as the equations are solved along time. This model, first studied by 
 mathematician and meteorologist Edward Lorenz, constitutes a simplified mathematical model for atmospheric convection.
 It is notable for having chaotic solutions for certain parameter values and initial conditions. In particular, the Lorenz
 attractor is a set of chaotic solutions of the Lorenz system. 
 
 If run with the default values, a standard simulation of the Lorenz attractor is obtained.
 
 
 Execution: lorenz_model(x0, y0, z0, t0, tend, N, a, b, c, path_save)

 Input:

  x0:             Initial conditions for the x-coordinate.
  y0:             Initial conditions for the y-coordinate.
  z0:             Initial conditions for the z-coordinate.
  t0:             Initial integration time.
  tend:           Final integration time.
  N:              Number of divisions in the integration time (tend-t0). It determines the time-step for the integration.
  a:              System's parameter constant proportional to Prandtl number.
  b:              System's parameter constant proportional to Rayleigh number. 
  c:              System's parameter constant.   
  path_save:      Path where the output of the simulation should be saved.

 Output:    
                                            
  It generates a new folder called Output in the indicated path by 'path_save'. Inside the Output folder, a video with the
  obtained simulation is stored.                                                    

"""

def lorenz_model(x0=0.0, y0=1.0, z0=0.0, t0=0, tend=50, N=10000, a=10, b=28, c=8/3, path_save='/home/santiago/Documentos'):
    
    import numpy as np
    import subprocess
    import os
    import shutil
    import matplotlib.pyplot as plt
    
    File_Names = []
    fpath1 = path_save+'/Output'    
    os.mkdir(fpath1)
    
    xcoord = []
    ycoord = []
    zcoord = []
    
    array = np.array([x0, y0, z0])
    
    h = (tend-t0)/N
    tpoints = np.arange(t0, tend, h)
    
    #Function defining the ordinary differential equations:
    
    def equations(array):
        
        x = array[0]
        y = array[1]
        z = array[2]
        
        eq1 = a*(y-x)
        eq2 = b*x-y-x*z
        eq3 = x*y-c*z
        
        return np.array([eq1, eq2, eq3])
    
    flag = 10
    it = 0.0
    
    elev = 20
    azim = -60
    
    #4th order Runge Kutta:
    
    for t in tpoints:
        
        xcoord.append(array[0])
        ycoord.append(array[1])
        zcoord.append(array[2])
        
        k1 = h*equations(array)
        k2 = h*equations(array+0.5*k1)
        k3 = h*equations(array+0.5*k2)
        k4 = h*equations(array+k3)
        
        array += (k1+2*k2+2*k3+k4)/6
        
        #Plot writing every 10 time steps:
        
        print("Solving at time", t)
        
        if flag == 10:
        
            fig=plt.figure(figsize=(10,10))
            ax=fig.add_subplot(111,projection='3d')
            ax.set_xlim(-20, 20)
            ax.set_ylim(-30, 30)
            ax.set_zlim(0, 50)
            ax.plot(xcoord,ycoord,zcoord, 'r')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.view_init(elev, azim)
            filename = "Image_lorenz_model_{:.7f}.png".format(it)
            File_Names.append(filename) 
            fig.savefig(filename)
            plt.close()
            
            shutil.move(filename, fpath1+'/'+filename)
            
            it += 0.0000001
            
        flag += 1
        
        if flag == 11:
            
            flag = 0
    
    #Images generation for a 360º rotation of the final result for the movie:
    
    for i in range(360):        
    
        fig=plt.figure(figsize=(10,10))
        ax=fig.add_subplot(111,projection='3d')
        ax.set_xlim(-20, 20)
        ax.set_ylim(-30, 30)
        ax.set_zlim(0, 50)
        ax.plot(xcoord,ycoord,zcoord, 'r')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.view_init(elev, azim)
        filename = "Image_lorenz_model_{:.7f}.png".format(it)
        File_Names.append(filename) 
        fig.savefig(fpath1+'/'+filename)
        plt.close()
    
        azim += 1
        it += 0.0000001
        
    #Use ffmpeg to combine the images in a movie:
     
    subprocess.run(['ffmpeg','-framerate','30','-pattern_type','glob','-i',fpath1+"/*.png",'-c:v','libx264','-pix_fmt','yuv420p','movie_lorenz_model.mp4'])
    shutil.move('movie_lorenz_model.mp4', fpath1+'/movie_lorenz_model.mp4')
     
    for filename in File_Names:  #Delete the image files
     
        os.remove(fpath1+'/'+filename)
        
    
    return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    