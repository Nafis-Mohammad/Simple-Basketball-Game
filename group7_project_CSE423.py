from OpenGL.GLUT import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import time

score = 0

def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):          # |m| <= 1
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7

    else:                           # |m| > 1
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6
    return zone


def zoneConvertToZero(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def zoneConvertFromZero(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y



def drawMidpointLine(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = zoneConvertToZero(zone, x1, y1)
    x2, y2 = zoneConvertToZero(zone, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    x = x1
    while x <= x2:
        draw_x, draw_y = zoneConvertFromZero(zone, x, y)
        draw_points(draw_x, draw_y)
        if d > 0:
            d = d + incNE
            y = y + 1
        else:
            d = d + incE
        x += 1



def circlePoints(x, y, ogX, ogY):
    draw_points(x + ogX, y + ogY)       # zone1
    draw_points(y + ogX, x + ogY)       # zone0
    draw_points(-x + ogX, y + ogY)      # zone2
    draw_points(-y + ogX, x + ogY)      # zone3
    draw_points(-y + ogX, -x + ogY)     # zone4
    draw_points(-x + ogX, -y + ogY)     # zone5
    draw_points(x + ogX, -y + ogY)      # zone6
    draw_points(y + ogX, -x + ogY)      # zone7



def drawMidpointCircle(radius, originX, originY):
    d = 1 - radius
    x = 0
    y = radius
    circlePoints(x, y, originX, originY)
    while x < y:
        if d < 0:
            d += 2 * x + 3           # choosing East
            x += 1
        else:
            d += 2 * x - 2 * y + 5   # choosing South-East
            x = x + 1
            y = y - 1
        circlePoints(x, y, originX, originY)


def iterate():
    glViewport(0, 0, 700, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 700, 0.0, 700, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def ballTransform(xCentre, yCentre, radius, dx, dy, sc=0):     # Both translation and scaling
    # a = math.cos(math.radians(angle))
    # b = math.sin(math.radians(angle))
    s = np.array(                   # s for scaling
        [[sc,0], [0,1]]
    )

    t = np.array(                   # t for translation
        [[1,0,dx],[0,1,dy],[0,0,1]]
    )

    centre = np.array(       # converting original x and y centres into appropriate matrix form
        [[xCentre], [yCentre], [1]]
    )

    radius = np.array(      # radius is 1 D ????
        [[radius], [1]]
    )

    newCentre = np.matmul(t, centre)    # calculating new centre
    newRadius = np.matmul(s, radius)    # calculating new Radius
    return newCentre[0][0], newCentre[1][0], newRadius[0][0]  # return x, y, radius


def drawHoop():
    centreX = 350
    drawMidpointLine(centreX-40, 500, centreX-40, 420)      # draw left vertical line
    drawMidpointLine(centreX+40, 500, centreX+40, 420)      # draw right vertical line

def Reset_button():
    glColor3f(255.0, 250.0, 250.0)
    glPointSize(1) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    #R
    glVertex2f(500,630)
    glVertex2f(500,600)
    glVertex2f(500,630)
    glVertex2f(520,630)
    glVertex2f(520,630)
    glVertex2f(520,615)
    glVertex2f(520,615)
    glVertex2f(500,615)
    glVertex2f(500,615)
    glVertex2f(520,600)

    #E
    glVertex2f(530,630)
    glVertex2f(530,600)
    glVertex2f(530,630)
    glVertex2f(540,630)
    glVertex2f(530,615)
    glVertex2f(540,615)
    glVertex2f(530,600)
    glVertex2f(540,600)

    #S
    glVertex2f(550,630)
    glVertex2f(560,630)
    glVertex2f(550,630)
    glVertex2f(550,615)
    glVertex2f(550,615)
    glVertex2f(560,615)
    glVertex2f(560,615)
    glVertex2f(560,600)
    glVertex2f(560,600)
    glVertex2f(550,600)

    #E
    glVertex2f(570,630)
    glVertex2f(570,600)
    glVertex2f(570,630)
    glVertex2f(580,630)
    glVertex2f(570,615)
    glVertex2f(580,615)
    glVertex2f(570,600)
    glVertex2f(580,600)

    #T
    glVertex2f(600,630)
    glVertex2f(600,600)
    glVertex2f(590,630)
    glVertex2f(610,630)

    #=
    glVertex2f(615, 610)
    glVertex2f(630, 610)
    glVertex2f(615, 615)
    glVertex2f(630, 615)


    #R
    glVertex2f(640,630)
    glVertex2f(640,600)
    glVertex2f(640,630)
    glVertex2f(655,630)
    glVertex2f(655,630)
    glVertex2f(655,615)
    glVertex2f(655,615)
    glVertex2f(640,615)
    glVertex2f(640,615)
    glVertex2f(655,600)

    glEnd()



def drawBall(radius, midX, midY):
    glColor3f(0.9294117647, 0.4431372549, 0.09019607843)
    dec = 2
    while radius>=0:
        drawMidpointCircle(radius, midX, midY)
        radius -= 2
        #glutSwapBuffers()


def drawScore():
    numCode = {
        "0": [0, 80, 40, 80, 40, 80, 40, 0, 40, 0, 0, 0, 0, 0, 0, 80],
        "1": [40, 0, 40, 80],
        "2": [0, 80, 40, 80, 40, 80, 40, 40, 40, 40, 0, 40, 0, 40, 0, 0, 0, 0, 40, 0],
        "3": [0, 80, 40, 80, 40, 80, 40, 40, 40, 40, 0, 40, 40, 40, 40, 0, 40, 0, 0, 0],
        "4": [0, 80, 0, 40, 0, 40, 40, 40, 40, 80, 40, 0],
        "5": [40, 80, 0, 80, 0, 80, 0, 40, 0, 40, 40, 40, 40, 40, 40, 0, 40, 0, 0, 0],
        "6": [40, 80, 0, 80, 0, 80, 0, 0, 0, 0, 40, 0, 40, 0, 40, 40, 40, 40, 0, 40],
        "7": [0, 80, 40, 80, 40, 80, 40, 0, 0, 80, 0, 40],
        "8": [0, 80, 40, 80, 40, 80, 40, 0, 40, 0, 0, 0, 0, 0, 0, 80, 0, 40, 40, 40],
        "9": [0, 80, 40, 80, 40, 80, 40, 0, 40, 40, 0, 40, 0, 40, 0, 80, 40, 0, 0, 0],
    }
    start_coordinate = [20, 600]  # stores the coordinates from which the next number should start

    for i in str(score):
        coordinates = numCode[i]  # storing a number's coordinates into coordinates
        j = 0
        while j < len(coordinates):
            drawMidpointLine(coordinates[j] + start_coordinate[0], coordinates[j + 1] + start_coordinate[1],
                       coordinates[j + 2] + start_coordinate[0], coordinates[j + 3] + start_coordinate[1])
            j += 4
        start_coordinate[0] += 60  # space for the next number


def drawEverything(radius=50, midX=350, midY=150):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.9294117647, 0.4431372549, 0.09019607843)
    drawHoop()
    Reset_button()
    drawBall(radius, midX, midY)
    glColor3f(0.0, 1.0, 1.0)
    drawScore()
    glutSwapBuffers()


def throwBall(radius, midX, midY, direction):
    if direction==1:
        dx=-1
        dy=7
    elif direction==3:
        dx=1
        dy=7
    else:
        dx=0
        dy=7

    while midY < 600:  # for "throwing force"
        glClear(GL_COLOR_BUFFER_BIT)
        drawEverything(radius, midX, midY)
        time.sleep(0.008)
        midX, midY, radius = ballTransform(midX, midY, radius, dx, dy, 0.992)
        glFlush()
        glutSwapBuffers()

    # time.sleep(0.02)
    while midY > 350:  # for "landing force"
        glClear(GL_COLOR_BUFFER_BIT)
        drawEverything(radius, midX, midY)
        time.sleep(0.01)
        midX, midY, radius = ballTransform(midX, midY, radius, dx, -dy, 0.997)
        glFlush()
        glutSwapBuffers()


def calcScore(direction):
    global score
    if direction == 2:
        print("NICE JOB")
        score += 1
    return score

def mainProjectTask(direction):
    global score
    midX = 350  # initial circle location
    midY = 150
    radius = 50
    drawEverything()
    #drawEverything(radius, midX, midY)
    throwBall(radius, midX, midY, direction)
    score = calcScore(direction)

    drawEverything(radius, midX, midY)



    #glutPostRedisplay()


def keyboard(key, x, y):
    if key == b'1':
        glClear(GL_COLOR_BUFFER_BIT)
        mainProjectTask(1)

    if key == b'2':
        glClear(GL_COLOR_BUFFER_BIT)
        mainProjectTask(2)
        glFlush()
        glutSwapBuffers()

    if key == b'3':
        glClear(GL_COLOR_BUFFER_BIT)
        mainProjectTask(3)
        glFlush()
        glutSwapBuffers()

    if key == b'r':
        glClear(GL_COLOR_BUFFER_BIT)
        global score
        score = 0
        drawEverything()

    if key == b'x':
        glutDestroyWindow(glutGetWindow())

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    #call the draw methods here
    #transform()
    mainProjectTask(8)                            # task here, pass number of inner circles here
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(700, 700) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboard)

glutMainLoop()
