import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib.colors as mcol

def stretch_line(p1,p2):
    """Stretch line between p1 and p2
    """

    d = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

    cos_teta = abs(p1[0]-p2[0])/d
    teta = math.acos(cos_teta)

    d = d/20
    dx = d*math.cos(teta)
    dy = d*math.sin(teta)

    if (p2[0]-p1[0])>0 and (p2[1]-p1[1])>0:
        p1[0] = p1[0] - dx
        p1[1] = p1[1] - dy
        p2[0] = p2[0] + dx
        p2[1] = p2[1] + dy

    elif (p2[0]-p1[0])<0 and (p2[1]-p1[1])>0:
        p1[0] = p1[0] + dx
        p1[1] = p1[1] - dy
        p2[0] = p2[0] - dx
        p2[1] = p2[1] + dy

    elif (p2[0]-p1[0])<0 and (p2[1]-p1[1])<0:
        p1[0] = p1[0] + dx
        p1[1] = p1[1] + dy
        p2[0] = p2[0] - dx
        p2[1] = p2[1] - dy

    elif (p2[0]-p1[0])>0 and (p2[1]-p1[1])<0:
        p1[0] = p1[0] - dx
        p1[1] = p1[1] + dy
        p2[0] = p2[0] + dx
        p2[1] = p2[1] - dy

    elif (p2[0]-p1[0])>0 and (p2[1]-p1[1])==0:
        p1[0] = p1[0] - d
        p2[0] = p2[0] + d
    elif (p2[0]-p1[0])<0 and (p2[1]-p1[1])==0:
        p1[0] = p1[0] + d
        p2[0] = p2[0] - d
    elif (p2[0]-p1[0])==0 and (p2[1]-p1[1])>0:
        p1[1] = p1[1] - d
        p2[1] = p2[1] + d
    elif (p2[0]-p1[0])==0 and (p2[1]-p1[1])<0:
        p1[1] = p1[1] + d
        p2[1] = p2[1] - d

    return p1,p2

def plotline(p1,p2,color_):
    """Plot lines between p1 and p2
    """

    p1,p2 = stretch_line(p1,p2)

    col = np.array([[p1,p2]])

    lc = mcoll.LineCollection(col, colors=color_, linewidth=2)
    ax = plt.gca()
    ax.add_collection(lc)

def colorline(
    p1, p2, z=None,
    cmap=mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"]),
    norm=plt.Normalize(0.3, 1.05),linewidth=2, alpha=1):
    """Returns a line collection between p1 and p2
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    # to check for numerical input -- this is a hack
    if not hasattr(z, "__iter__"):
        z = np.array([z])

    z = np.asarray(z)

    p_half = [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]


    p1_,p_half_ = stretch_line(p1,p_half)
    segment = [[p1_,p_half_]]
    lc = mcoll.LineCollection(segment, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)
    ax = plt.gca()
    ax.add_collection(lc)

    p_half_,p2_ = stretch_line(p_half,p2)
    segment = [[p_half_,p2_]]
    lc = mcoll.LineCollection(segment, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)
    ax = plt.gca()
    ax.add_collection(lc)

    return lc

def multicolored_lines(p1,p2,v1,v2,norm, colorbar_flag=0):
    """Plots a line between p1 and p2 with colors varying from v1 to v2
    according to norm[0] and norm[1] values
    """
    z = [v1,v2]
    lc = colorline(p1, p2, z=z, norm=plt.Normalize(norm[0],norm[1]))

    if colorbar_flag == 1:
        colorbar_ = plt.colorbar(lc)
