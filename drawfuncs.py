import numpy as np
import cv2 as cv



def make_canvas(size):
    img = np.zeros((size,size,3), np.uint8)
    return img


def make_spots(centery, name):
    cv.circle(img = name,center = centery, radius = 2, color = (0,0,255), thickness= -1)

def make_lines(line, name):
    cv.line(name,line[0],line[1],(255,0,0),1)

def save_img(fname, name):
    cv.imwrite(fname, name)

''' Above are functions that make the spots and line for the "lattice.png" and below the "d_k.png".'''


def make_d_lines(p1, p2, name):
    cv.line(name,p1,p2,(255,0,0),1)
