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

fig = plt.figure(figsize=(3,3))
ax = fig.add_axes([0,0,1,1]) # get rid of white border
ax.set_axis_off()
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
crates_path = parent_path + '/imglib/black_plate.png'
robot1_path = parent_path + '/imglib/disc.png'
robot1b_path = parent_path + '/imglib/walker7.png'
robot2_path = parent_path + '/imglib/walker4.png'
factory1_path = parent_path + '/imglib/silver_plate.png'
factory2_path = parent_path + '/imglib/gold_plate.png'
bridge_path = parent_path + '/imglib/bridge1.png'
broken_bridge_path = parent_path + '/imglib/broken_bridge.png'
draw_bridge_path = parent_path + '/imglib/bridge3.png'
button1_path = parent_path + '/imglib/buttons.png'
broken_button1_path = parent_path + '/imglib/broken_buttons.png'
button2_path = parent_path + '/imglib/buttons.png'
broken_button2_path = parent_path + '/imglib/broken_buttons.png'


# load image files
background = Image.open(background_path).transpose(Image.FLIP_TOP_BOTTOM)
crate = Image.open(crate_path)
crates = Image.open(crates_path)
robot1 = Image.open(robot1_path)
robot1b_film = Image.open(robot1b_path)
robot2_film = Image.open(robot2_path)
factory1 = Image.open(factory1_path)
factory2 = Image.open(factory2_path)
bridge = Image.open(bridge_path)
draw_bridge = Image.open(draw_bridge_path)
button1_film = Image.open(button1_path)
button2_film = Image.open(button2_path)

def add_to_scene(fig, xy):
    """
    add to scene with offset automatically applied
    """
    global background
    fig = fig.transpose(Image.FLIP_TOP_BOTTOM)
    xy = to_offset(xy, fig.size)
    background.paste(fig, (int(xy[0]), int(xy[1])), fig)

def add_crate():
    global crate
    x, y = to_xy('box')
    add_to_scene(crate, (x,y))

def add_crates():
    global crates
    x, y = grid_to_coords((2,0))
    add_to_scene(crates, (x,y))

def add_factory1():
    global factory1
    x, y = grid_to_coords((0,4))
    add_to_scene(factory1, (x,y))

def add_factory2():
    global factory1
    x, y = grid_to_coords((4,3))
    add_to_scene(factory2, (x,y))

def add_bridge():
    global bridge, fails, step
    if 'bridge' in fails[step]:
        bridge = Image.open(broken_bridge_path)
    else:
        bridge = Image.open(bridge_path)
    x, y = grid_to_coords((2,4))
    add_to_scene(bridge, (x,y))

def add_draw_bridge():
    global draw_bridge
    x, y = grid_to_coords((1,2))
    xy_r1 = get_data('robot1')[step]
    xy_r2 = get_data('robot2')[step]
    if xy_r1 == [0,1] or xy_r2 == [0,1] or xy_r1 == [0, 3] or xy_r2 == [0,3]:
        add_to_scene(draw_bridge, (x,y))

def reset_background():
    global background, ax
    ax.cla() # very important for speeding up saving
    background.close()
    background = Image.open(background_path).transpose(Image.FLIP_TOP_BOTTOM)

def add_robot1(): # disk or plate
    global robot1
    x, y = to_xy('robot1')

    dir_ = to_facing_dir('robot1')
    if dir_ == 'e':
        robot = robot1
    elif dir_ == 'w':
        robot = robot1.transpose(Image.ROTATE_180)
    elif dir_ == 'n':
        robot = robot1.transpose(Image.ROTATE_270)
    elif dir_ == 's':
        robot = robot1.transpose(Image.ROTATE_90)
    else:
        robot = robot1

    add_to_scene(robot, (x,y))

def to_offset(xy_center, hw):
    """
    xy_center: where the center of the fig should be
    hw: (height of fig, width of fig)
    """
    xc, yc = xy_center
    h, w = hw
    return (xc - h/2, yc - w/2)

def to_facing_dir(thing):
    global step
    if thing == 'robot2':
        local_run = get_data('robot2')
    elif thing == 'robot1b':
        local_run = get_data('robot1b')
    elif thing == 'robot1':
        local_run = get_data('robot1')

    start = local_run[step]
    if step + 1 == len(local_run):
        end = start
    else:
        end = local_run[step+1]
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

def add_button1():
    global button1_film, step

    if 'button1' in fails[step]:
        button1_film = Image.open(broken_button1_path)
    else:
        button1_film = Image.open(button1_path)

    film_fig = button1_film
    film_grid_dim = [1, 2]
    x, y = grid_to_coords((0,1))
    scale_factor = 0.25
    film_fig = film_fig.resize(tuple([int(scale_factor * k) for k in film_fig.size])) # rescaling

    j = 0
    # current positions of the robots
    xy_r1 = get_data('robot1')[step]
    xy_r2 = get_data('robot2')[step]
    if xy_r1 == [0,1] or xy_r2 == [0,1]:
        i = 1
    else:
        i = 0
    width, height = film_fig.size
    sub_height = height / film_grid_dim[0]
    sub_width = width / film_grid_dim[1]
    lower = ((i % film_grid_dim[1]) * sub_width, j * sub_height)
    upper = (((i % film_grid_dim[1])+1) * sub_width, (j+1) * sub_height)
    crop_area = (int(lower[0]), int(lower[1]), int(upper[0]), int(upper[1]))
    button_fig = film_fig.crop(crop_area)
    ax.imshow(button_fig)
    add_to_scene(button_fig, (x, y))

def add_button2():
    global button2_film, step

    if 'button2' in fails[step]:
        button2_film = Image.open(broken_button2_path)
    else:
        button2_film = Image.open(button2_path)

    film_fig = button2_film
    film_grid_dim = [1, 2]
    x, y = grid_to_coords((0,3))
    scale_factor = 0.25
    film_fig = film_fig.resize(tuple([int(scale_factor * k) for k in film_fig.size])) # rescaling

    j = 0
    # current positions of the robots
    xy_r1 = get_data('robot1')[step]
    xy_r2 = get_data('robot2')[step]
    if xy_r1 == [0,3] or xy_r2 == [0,3]:
        i = 1
    else:
        i = 0

    width, height = film_fig.size
    sub_height = height / film_grid_dim[0]
    sub_width = width / film_grid_dim[1]
    lower = ((i % film_grid_dim[1]) * sub_width, j * sub_height)
    upper = (((i % film_grid_dim[1])+1) * sub_width, (j+1) * sub_height)
    crop_area = (int(lower[0]), int(lower[1]), int(upper[0]), int(upper[1]))
    button_fig = film_fig.crop(crop_area)
    ax.imshow(button_fig)
    add_to_scene(button_fig, (x, y))

def add_robot1b():
    global robot1b_film, run, prog

    film_fig = robot1b_film
    film_grid_dim = [8, 16]
    x,y = to_xy('robot1b')
    scale_factor = 2
    film_fig = film_fig.resize(tuple([int(scale_factor * k) for k in film_fig.size])) # rescaling

    # step
    dir_ = to_facing_dir('robot1b')
    if dir_ == 'e':
        j = 2
    elif dir_ == 'w':
        j = 6
    elif dir_ == 'n':
        j = 4
    elif dir_ == 's':
        j = 0
    else:
        j = 6

    # progress
    if dir_ != 'rest':
        i = int(prog * 100) # adjust rhythm/pacing here
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


def add_robot2():
    global robot2_film, run, prog

    film_grid_dim = [8, 16]
    x,y = to_xy('robot2')
    film_fig = robot2_film
    scale_factor = 2
    film_fig = film_fig.resize(tuple([int(scale_factor * k) for k in film_fig.size])) # rescaling

    # step
    dir_ = to_facing_dir('robot2')
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

    # progress
    if dir_ != 'rest':
        i = int(prog * 45) # adjust rhythm/pacing here
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

def get_data(thing):
    global run
    data = []
    if thing == 'robot1' or thing == 'robot1b':
        for step in run:
            data.append([step[0], step[1]])
    elif thing == 'robot2':
        for step in run:
            data.append([step[2], step[3]])
    elif thing == 'box':
        for i in range(len(run)):
            box = run[i][5]
            if i+1 < len(run):
                picking = run[i+1][5] == 0
            else:
                picking = False
            if box == 0 or picking:
                xy = [run[i][0], run[i][1]]
            elif box == 1:
                xy = [2,0]
            elif box == 2:
                xy = [0,4]
            elif box == 3:
                xy = [4,3]
            data.append(xy)
    return data

def grid_to_coords(ij):
    global xs, ys
    i, j = ij
    return (xs[i] + xs[1]/2, ys[j] + ys[1]/2)

def to_xy(thing):
    global run
    xy_run = get_data(thing)
    start = grid_to_coords(xy_run[step])
    if step + 1 == len(xy_run):
        end = start
    else:
        end = grid_to_coords(xy_run[step+1])
    delta = np.array(end) - np.array(start)
    xy = np.array(start) + delta*prog
    return [int(xy[0]), int(xy[1])]

def to_step(frame):
    return frame // frames_per_step

def to_prog(frame):
    return (frame % frames_per_step) / (frames_per_step)

#run = simulator.run_from(max_steps=max_steps,variables_to_collect=vars_to_collect,
#        init_contract = (start_state, start_guarantee), init_fail = dict(), controller='greedy')
#run = [[0,0], [0,0], [1,0], [1, 1], [2,1], [2,2], [2,2],[2,3],[3,3],[3,4], [3,3],[2,3],[1,3],[1,2],[1,1],[0,1],[0,0]]
run = np.load('../run.npy')
fails = np.load('../fails.npy')
frames_per_step = 15

step = 0 # simulation step
prog = 0 # step progress

def animate(frame):
    global print_frames, step, prog
    if print_frames:
        global num_frames
        print(str(frame) + '/' + str(num_frames))
    step = to_step(frame)
    prog = to_prog(frame)

    reset_background() # clear background
    add_crates()
    add_button1()
    add_button2()
    add_factory1()
    add_factory2()
    add_bridge()
    add_draw_bridge()
    add_crate()
    add_robot2()
    add_robot1b()

    stage = ax.imshow(background, origin='lower')
    return stage,

save_video = True
print_frames = save_video
num_frames = len(run) * frames_per_step
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=30,  blit = True, repeat = False)
if save_video:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps = 30, bitrate=-1)
    now = 'reactive3'
    ani.save('../movies/' + now + '.avi', dpi=200)
if not save_video:
    plt.show()
