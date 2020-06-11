

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle,uniform,permutation
import os  # handy system and path functions
import sys  # to get file system encoding
import serial #for sending triggers from this computer to biosemi computer
import csv
from psychopy import visual, core
import glob


win = visual.Window([1920,1080],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True)

vis_deg=4.66
num_dots=6
if num_dots==6: # HAVE TO CHANGE TO MATCH WMAT
    dots_positions={'one':((vis_deg/2), (sqrt(3)/2*vis_deg)),'three':((vis_deg, 0)),'five':(((vis_deg/2), -((sqrt(3)/2)*vis_deg))),
            'seven':(-(vis_deg/2), -((sqrt(3)/2)*vis_deg)),'nine':(-vis_deg, 0),
            'eleven':((-(vis_deg/2), ((sqrt(3)/2)*vis_deg)))}

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6
fixation.autoDraw=True

8

size=(4.66,3.6)

all_dots=[visual.ImageStim(win=win, image=os.getcwd()+'/eyetracker_dots/fill_b_circle.png',size=size,pos=dots_positions[this_pos])  for this_pos in dots_positions.keys()]

print(all_dots)

focus_msg = visual.TextStim(win, text='Please follow the dots around the screen and remain fixated on them for the duration they are on the screen.',units='norm', color=(1,1,1))
focus_msg.size=0.6
get_ready= visual.TextStim(win, text='Get ready!',units='norm', color=(1,1,1))
get_ready.size=0.6

focus_msg.draw()
win.flip()
event.waitKeys()

get_ready.draw()
win.flip()
core.wait(3)
win.flip()

random_order=all_dots#np.random.permutation(all_dots)

for dot in random_order :
    dot.draw()
    win.flip()
    core.wait(3)





