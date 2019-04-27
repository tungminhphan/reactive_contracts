"""
Tung Phan
April 26, 2019
Improved animation for "three islands" example
"""

import sys, os
current_path = os.path.abspath('.')
parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # for abs path
sys.path.append(current_path)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, RegularPolygon, Shadow
import matplotlib as mpl
from PIL import Image

fig = plt.figure()
ax = fig.add_axes([0,0,1,1]) # get rid of white border
plt.axis('equal')

N = 5 # NxN gridworld
X_lim = 1200 # world size in pixels
Y_lim = 1200 # world size in pixels
xs = np.linspace(0, X_lim, N+1)
ys = np.linspace(0, Y_lim, N+1)
w, h = xs[1] - xs[0], ys[1] - ys[0]

# define paths to image files
background_path = parent_path + '/imglib/three_islands.png'
crate_path = parent_path + '/imglib/crate.png'
robot1_path = parent_path + '/imglib/robot1.png'
robot2_path = parent_path + '/imglib/walker1.png'

# load image files
background = Image.open(background_path).transpose(Image.FLIP_TOP_BOTTOM)
crate = Image.open(crate_path)
robot2_film = Image.open(robot2_path)
robot1 = Image.open(robot1_path)

def add_to_scene(fig, xy):
    """
    add to scene with offset automatically applied
    """
    global background
    fig = fig.transpose(Image.FLIP_TOP_BOTTOM)
    xy = to_offset(xy, fig.size)
    background.paste(fig, (int(xy[0]), int(xy[1])), fig)

def add_crate_at(xy):
    global crate
    x, y = xy
    add_to_scene(crate, (x,y))

def reset_background():
    global background
    background.close()
    background = Image.open(background_path).transpose(Image.FLIP_TOP_BOTTOM)

def add_robot1_at(xy):
    global background, robot1
    x, y = xy
    add_to_scene(robot1, (x,y))

def to_offset(xy_center, hw):
    """
    xy_center: where the center of the fig should be
    hw: (height of fig, width of fig)
    """
    xc, yc = xy_center
    h, w = hw
    return (xc - w/2, yc - w/2)

def to_facing_dir(step, rem):
    start = run[step]
    if step + 1 == len(run):
        end = start
    else:
        end = run[step+1]
    delta = np.array(end) - np.array(start)
    delta_x = delta[0]
    delta_y = delta[1]
    if delta_x == 0:
        if delta_y > 0:
            return 'n'
        elif delta_y < 0:
            return 's'
    elif delta_y == 0:
        if delta_x > 0:
            return 'e'
        elif delta_x < 0:
            return 'w'
    return 'rest'

def add_robot2_at(step, rem):
    global robot2_film, run

    film_grid_dim = [8, 16]
    x,y = to_xy(step, rem)
    film_fig = robot2_film
    scale_factor = 2
    film_fig = film_fig.resize(tuple([int(scale_factor * k) for k in film_fig.size])) # rescaling

    facing_dir = {'e', 'w', 'n', 's'}
    dir_ = to_facing_dir(step, rem)
    if dir_ == 'e':
        j = 2
    elif dir_ == 'w':
        j = 6
    elif dir_ == 'n':
        j = 4
    elif dir_ == 's':
        j = 0
    else:
        j = 1

    if dir_ != 'rest':
        i = int(rem * 45) # adjust rhythm/pacing here
    else:
        i = 2 # resting pose

    width, height = film_fig.size
    sub_height = height / film_grid_dim[0]
    sub_width = width / film_grid_dim[1]
    lower = ((i % film_grid_dim[1]) * sub_width, j * sub_height)
    upper = (((i % film_grid_dim[1])+1) * sub_width, (j+1) * sub_height)
    crop_area = (int(lower[0]), int(lower[1]), int(upper[0]), int(upper[1]))
    robot_fig = film_fig.crop(crop_area)

    add_to_scene(robot_fig, (x, y))

run = [[0,0], [0,0], [1,0], [1, 1], [2,1], [2,2], [2,2],[2,3],[3,3],[3,4], [3,3],[2,3],[1,3],[1,2],[1,1],[0,1],[0,0]]
run = run + run
frames_per_step = 60

def grid_to_coords(ij):
    global xs, ys
    i, j = ij
    return (xs[i] + xs[1]/2, ys[j] + ys[1]/2)

def to_xy(step, rem):
    """
    """
    global run
    start = grid_to_coords(run[step])
    if step + 1 == len(run):
        end = start
    else:
        end = grid_to_coords(run[step+1])
    delta = np.array(end) - np.array(start)
    xy = np.array(start) + delta*rem
    return [int(xy[0]), int(xy[1])]

def to_step(frame):
    return frame // frames_per_step

def to_rem(frame):
    return (frame % frames_per_step) / (frames_per_step)

def animate(frame):
    reset_background() # clear background

    step = to_step(frame)
    rem = to_rem(frame)

#    add_robot1_at(to_xy(step,rem))
    add_robot2_at(step,rem)

#    add_crate_at(to_xy(step,rem))

    stage = ax.imshow(background, origin='lower')
    return stage,

num_frames = len(run) * frames_per_step
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=1,
        blit=True, repeat=False)
plt.show()
