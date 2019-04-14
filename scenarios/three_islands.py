# Tung Phan
# April 11, 2019
# Animation for `Three Islands' Example

import sys, os
current_path = os.path.abspath('.')
sys.path.append(current_path)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, RegularPolygon, Shadow
import matplotlib as mpl
from helpers import simulator

max_steps = int(sys.argv[2])

fig = plt.figure()
ax = fig.add_axes([0,0,1,1]) # get rid of white border
plt.axis('equal')

N = 5 # NxN gridworld
X_lim = 10 # world size in pixels
Y_lim = 10 # world size in pixels
xs = np.linspace(0, X_lim, N+1)
ys = np.linspace(0, Y_lim, N+1)

# grid lines
for x in xs:
    plt.plot([x, x], [ys[0], ys[-1]], color='black', alpha=0.01, linestyle=':')
for y in ys:
    plt.plot([xs[0], xs[-1]], [y, y], color='black', alpha=0.01, linestyle=':')
# grid "shades" (boxes)
w, h = xs[1] - xs[0], ys[1] - ys[0]

# square = (i, j)
X = list(enumerate(xs[:-1]))
Y = list(enumerate(ys[:-1]))

def color_ij(ij, color):
    x,y = X[ij[0]][1], Y[ij[1]][1]
    ax.add_patch(Rectangle((x, y), w, h, fill=True, color=color, alpha=.8))

# initialization function: plot the background of each frame
green = []
# bottom isle
for i in range(3):
    for j in range(2):
        green.append((i,j))
# top left isle
for i in range(2):
    for j in range(3,5):
        green.append((i,j))
# top right isle
for i in range(3,5):
    for j in range(3,5):
        green.append((i,j))
# water
cyan = []
for i in range(5):
    for j in range(2,3):
        cyan.append((i,j))
for i in range(3,4):
    for j in range(0,2):
        cyan.append((i,j))
for i in range(4,5):
    for j in range(0,2):
        cyan.append((i,j))
for i in range(2,3):
    for j in range(3,5):
        cyan.append((i,j))

# bridges
brown = []
for i in range(1,2):
    for j in range(2,3):
        brown.append((i,j))

for i in range(2,3):
    for j in range(4,5):
        brown.append((i,j))

# bridges off
teal = []
for i in range(1,2):
    for j in range(2,3):
        teal.append((i,j))

# sinks
orange = []
for i in range(0,1):
    for j in range(4,5):
        orange.append((i,j))
for i in range(4,5):
    for j in range(3,4):
        orange.append((i,j))
# sources
orchid = []
for i in range(2,3):
    for j in range(0,1):
        orchid.append((i,j))

color_dict = {'green': green, 'cyan': cyan, 'brown': brown, 'orange': orange, 'orchid': orchid, 'teal': teal}

# generate static world
for color in color_dict:
    for ij in color_dict[color]:
        color_ij(ij, color)

# add houses
# east
house1 = RegularPolygon((w/2+w*4,h/2+h*3), 5, 0.5, fc='k', alpha=1)
ax.add_patch(house1)
# west
house2 = RegularPolygon((w/2+w*0,h/2+h*4), 5, 0.5, fc='k', alpha=0.9)
ax.add_patch(house2)
# south / storage
house3 = RegularPolygon((w/2+w*2,h/2+h*0), 5, 0.5, fc='k', alpha=0.9)
ax.add_patch(house3)

# packages
pack = Rectangle((0,0), w/3, h/3, fc='y', alpha=0.9)
ax.add_patch(pack)
#pack2 = RegularPolygon((w/2+w*4,h/2+h*3), 4, 0.5, fc='y', alpha=0.9)
#ax.add_patch(pack2)

def interpolate_array(arr1, arr2, N):
    interp = []
    for i in range(N):
        new = arr1 + (arr2-arr1)/N

def interpolate_run(run, N, exceptions):
    interpolated = []
    if len(run) <= 1:
        return run
    else:
        for i in range(len(run)-1):
            old = np.array(run[i])
            new = np.array(run[i+1])
            for j in range(N):
                    interp = old + j/N *(new-old)
                    for k in exceptions:
                        interp[k] = new[k]
                    interpolated.append(tuple(interp))
    return interpolated

vars_to_collect = ['x1', 'y1', 'x2', 'y2', 'bridge', 'box']
run = simulator.random_run_from(init_state='0',max_steps=max_steps,variables_to_collect=vars_to_collect)
exceptions = {5}
run = interpolate_run(run,10,exceptions)
num_frames = len(run)
# drawbridge
drawbridge = Rectangle((1*w, 2*h), w, h, color='brown', alpha=0.8)
ax.add_patch(drawbridge)

# permanent bridge
permanent_bridge = Rectangle((2*w, 4*h), w, h, color='brown', alpha=0.8)
ax.add_patch(permanent_bridge)

# add agents
ego = RegularPolygon((w/2+w*0,h/2 + 1*h), 9, 0.8, fc='b', alpha=0.8)
ax.add_patch(ego)
ego2 = RegularPolygon((w/2+w*3,h/2+h*3), 9, 0.5, fc='m', alpha=0.8)
ax.add_patch(ego2)

# add buttons
button1 = Circle((0+w/2, h+h/2), 0.3,
        fill=True, color='red', alpha=.6)
ax.add_patch(button1)
#shadow1 = ax.add_patch(Shadow(button1,-0.06,-0.06))
button2 = Circle((0+w/2, 3*h+h/2), 0.3,
        fill=True, color='red', alpha=.6)
ax.add_patch(button2)
#shadow2 = ax.add_patch(Shadow(button2, -0.06,-0.06))

def animate(i):
    x1,y1,x2,y2,bridge,box = run[i]
    button1.set_alpha((1-bridge)/2+0.1)
    button2.set_alpha((1-bridge)/2+0.1)

    drawbridge.set_alpha(int(bridge+0.5))
#    drawbridge.set_alpha(bridge)
    ego.xy = (x1*w+w/2,y1*h+h/2)
    ego2.xy = (x2*w+w/2,y2*h+h/2)
    if (x2 == 0 and y2 == 4) or (x2 == 4 and y2 == 3):
        ego2.set_fc('r')
    elif (x2 == 2 and y2 == 0):
        ego2.set_fc('b')
    else:
        ego2.set_fc('m')

    if box == 0:
        pack.xy = np.array(ego.xy) + (-w/6,-h/6)
    elif box == 1:
        pack.xy = (2*w+w/2,0*h+h/6)
    elif box == 2:
        pack.xy = (0*w+w/4,4*h+h/5)
    elif box == 3:
        pack.xy = (4*w+w/3,3*h+h/7)
    return drawbridge, ego, ego2, pack, button1, button2

save_video = False
ani = animation.FuncAnimation(fig, animate, frames=num_frames,
        interval=25, blit=True, repeat=False)
if save_video:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps = 30, metadata=dict(artist='Gridworld Simulator'), bitrate=-1)
    now = 'gr1'
    ani.save('../movies/' + now + '.avi', dpi=200)
plt.show()
