# -*- coding: utf-8 -*-
"""
Package et_ppmdcommon
=======================================

Common components for the Parallel Programming project assignment
"""
__version__ = "0.4.0"

import numpy as np
import math
import matplotlib.pyplot as plt


class ClosestPacking2D:
    def __init__(self,r):
        """parameters of the rectangular centered unit cell for a 2D closest
        packing of atoms witht radius r.

        Every unit cell contains 2 atoms.
        x   x
          x
        x   x
        """
        self.radius = r
        self.uc_centered_a = r
        self.uc_centered_b = r*np.sqrt(3.0)


#-------------------------------------------------------------------------------
# Utilities for generating atoms in a box
#-------------------------------------------------------------------------------
class Box:
    def __init__(self, xll, yll, xur, yur):
        """
        :param float xll: x-coordinate of lower left corner
        :param float yll: y-coordinate of lower left corner
        :param float xur: x-coordinate of upper right corner
        :param float yur: y-coordinate of upper right corner
        """
        self.xll = float(xll)
        self.yll = float(yll)
        self.xur = float(xur)
        self.yur = float(yur)

    def inside(self,x,y):
        if self.xll <= x and x < self.xur and self.yll <= y and y < self.yur:  # outside above
            return True
        else:
            return False


    def generateAtoms(self, r, noise=None):
        """Generate atom positions on hexagonal closest packing with atomic radius r inside this box.

        The lower and left boundary of the box are inclusive, the upper and right boundaries
        of the box are excluded.

        The more noise you add, the faster the atoms will move. The timestep must be chosen
        such that the fastest atom does not move more than a few percentages of the interatomic
        distance per timesteps.

        :param float r: atom radius = edge length of hexagonal cell = interatomic distance (without noise)
        :param float noise: add random noise to the atom positions. expressed as a fraction of the interatomic distance r.
        :return: two numpy arrays with resp. the x- and y-coordinates of the atoms.
        """
        # Using a rectangular centered unit cell, whose sides are aligned with the box
        a = r
        b = r*np.sqrt(3)

        # coordinates of the unit cells containing the lower left corner
        # of the box and the upper right corner:
        i0 = math.floor(self.xll/a)
        i1 = math.ceil (self.xur/a)
        j0 = math.floor(self.yll/b)
        j1 = math.ceil (self.yur/b)

        # offset of the central atom
        dxc = 0.5*r
        dyc = 0.5*np.sqrt(3.0)*r

        # estimate the number of atoms in the box (conservative)
        nmax = 2*(i1-i0)*(j1-j0)
        x = np.empty((nmax,),dtype=float)
        y = np.empty((nmax,),dtype=float)
        # in general nmax is a bit too large. Hence we count and clip the arrays before returning.

        # generate
        n = -1
        for j in range(j0,j1):
            yj = j*b
            yc = yj + dyc
            for i in range(i0,i1):
                xi = i*a

                if self.inside(xi,yj):
                    n += 1
                    x[n] = xi
                    y[n] = yj

                xc = xi + dxc
                if self.inside(xc,yc):
                    n += 1
                    x[n] = xc
                    y[n] = yc

        # clip the arrays
        x = x[:n+1]
        y = y[:n+1]

        if noise:
            addNoise(x, y, noise*r)

        return x, y


def seed(seed_value=None):
    """Convenience method to set the seed of np.random random number generation."""
    np.random.seed(seed_value)

    
def addNoise(x,y,noise):
    """Displace (x,y) in a random direction by a random amplitude in the interval [0,noise[.

    The values of x and y are modified in place.
    Control the seed by calling np.random.seed(seed_value).

    :param np.array x: array of x-coordinates
    :param np.array y: array of y-coordinates
    """
    n = len(x)
    theta = np.random.random(n)*(2*np.pi) # random angle in [0,2*pi[
    d     = np.random.random(n)*noise     # random amplitude in [0,noise[
    x    += np.cos(theta)*d
    y    += np.sin(theta)*d


#-------------------------------------------------------------------------------
# Plotting utilities
#-------------------------------------------------------------------------------
def figure():
    """Generate a matplotlib figure with equal aspect ratio."""
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_aspect('equal')
    return fig, ax


def plotAtoms(x,y,radius=0.0):
    """Plot the atoms on current matplotlib figure 

    :param np.array x: x-coordinates
    :param np.array y: y-coordinates
    :param float radius: atom radius, if 0.0 dots are plotted
    """
    if radius:
        theta = np.linspace(0,2*np.pi,36,endpoint=True)
        xCircle = radius*np.cos(theta)
        yCircle = radius*np.sin(theta)
        for i in range(len(x)):
            xCircle += x[i]
            yCircle += y[i]
            plt.plot(xCircle,yCircle)
            xCircle -= x[i]
            yCircle -= y[i]
    else:
        plt.plot(x,y,'o')

def plotBox(box):
    """Plot box on current figure
    
    :param Box box: box to plot 
    """
    plt.plot([box.xll, box.xur, box.xur, box.xll, box.xll]
            ,[box.yll, box.yll, box.yur, box.yur, box.yll]
            , '-'
            )
# eof
