import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

orthoView = False
zoom = .5
xposition = 0.
newxposition = 0.
yposition = 0.
newyposition = 0.
vecW=vecU=vecV = np.ones((3))
dragL = False
dragR = False

eye = np.array([1.,1.,1.])
oldeye = np.array([1.,1.,1.])
target = np.zeros((3))
up = np.array([0,1,0])
offset = np.zeros((3))
oldoffset = np.zeros((3))

def render():
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    
    glScalef(zoom, zoom, zoom)

    # use orthogonal projection (we'll see details later)
    if(orthoView == True):
        glOrtho(-2,2,-2,2,-10,10)
    else:
        gluPerspective(45, 1, 0.1, 100)

    gluLookAt(eye[0]+oldoffset[0]+offset[0],eye[1]+oldoffset[1]+offset[1],eye[2]+oldoffset[2]+offset[2], target[0]+oldoffset[0]+offset[0],target[1]+oldoffset[1]+offset[1],target[2]+oldoffset[2]+offset[2], 0,1,0)

    drawFrame()
    drawCube()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glColor3ub(100, 100, 100)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,-1.]))
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([-1.,0.,0.]))
    for i in range(1, 11):
        glVertex3fv(np.array([i/10,0.,-1.]))
        glVertex3fv(np.array([i/10,0.,1.]))
        glVertex3fv(np.array([-i/10,0.,-1.]))
        glVertex3fv(np.array([-i/10,0.,1.]))
    for j in range(1, 11):
        glVertex3fv(np.array([-1.,0.,j/10]))
        glVertex3fv(np.array([1.,0.,j/10]))
        glVertex3fv(np.array([-1.,0.,-j/10]))
        glVertex3fv(np.array([1.,0.,-j/10]))
    glEnd()

def drawCube():
    glColor3ub(255, 115, 0)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([.2,.0,.0]))
    glVertex3fv(np.array([.2,.0,.2]))
    glVertex3fv(np.array([.0,.0,.2]))
    glEnd()
    glColor3ub(162, 255, 0)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([.2,.0,.0]))
    glVertex3fv(np.array([.2,.2,.0]))
    glVertex3fv(np.array([.0,.2,.0]))
    glEnd()
    glColor3ub(68, 0, 255)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([.0,.0,.2]))
    glVertex3fv(np.array([.0,.2,.2]))
    glVertex3fv(np.array([.0,.2,.0]))
    glEnd()
    glColor3ub(0, 179, 255)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.0,.0,.2]))
    glVertex3fv(np.array([.2,.0,.2]))
    glVertex3fv(np.array([.2,.2,.2]))
    glVertex3fv(np.array([.0,.2,.2]))
    glEnd()
    glColor3ub(255, 0, 247)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.2,.0,.0]))
    glVertex3fv(np.array([.2,.0,.2]))
    glVertex3fv(np.array([.2,.2,.2]))
    glVertex3fv(np.array([.2,.2,.0]))
    glEnd()
    glColor3ub(158, 179, 54)
    glBegin(GL_QUADS)
    glVertex3fv(np.array([.0,.2,.0]))
    glVertex3fv(np.array([.2,.2,.0]))
    glVertex3fv(np.array([.2,.2,.2]))
    glVertex3fv(np.array([.0,.2,.2]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global orthoView, zoom, xposition, newxposition, yposition, newyposition, vecW, vecU, vecV, dragL, dragR, eye, oldeye, target, up, offset, oldoffset
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_V: # view switching(orthogonal vs perspective)
            if(orthoView == False):
                orthoView = True
            else:
                orthoView = False
        if key==glfw.KEY_O: # reset
            orthoView = False
            zoom = .5
            xposition = 0.
            newxposition = 0.
            yposition = 0.
            newyposition = 0.
            vecW=vecU=vecV = np.ones((3))
            dragL = False
            dragR = False
            eye = np.array([1.,1.,1.])
            oldeye = np.array([1.,1.,1.])
            target = np.zeros((3))
            up = np.array([0,1,0])
            offset = np.zeros((3))
            oldoffset = np.zeros((3))

def cursor_callback(window, xpos, ypos):
    global xposition, newxposition, yposition, newyposition, dragL, dragR, oldeye, eye, offset, vecU, vecV
    if(dragL == True):
        newxposition = xpos
        newyposition = ypos
        tmpeye = oldeye + (-vecU)*(xposition - newxposition)/300 + (-vecV)*(yposition - newyposition)/300
        eye = tmpeye * (np.sqrt(3)/np.sqrt(tmpeye @ tmpeye))
    if(dragR == True):
        newxposition = xpos
        newyposition = ypos
        offset = -vecU*(xposition - newxposition)/300 - vecV*(yposition - newyposition)/300

def button_callback(window, button, action, mods):
    global xposition, yposition, dragL, dragR, oldeye, eye, target, up, oldoffset, offset, vecU, vecV, vecW
    
    vecW = target-eye
    vecW = vecW / np.sqrt(vecW@vecW)

    vecU = np.cross(up, vecW)
    vecU = vecU / np.sqrt(vecU@vecU)

    vecV = np.cross(vecW, vecU)
    vecV = vecV / np.sqrt(vecV@vecV)

    if(button == glfw.MOUSE_BUTTON_LEFT):
        if(glfw.PRESS == action):
            dragL = True
            pos = glfw.get_cursor_pos(window)
            x, y = pos
            xposition = x
            yposition = y
        elif(glfw.RELEASE == action):
            dragL = False
            oldeye = eye
    if(button == glfw.MOUSE_BUTTON_RIGHT):
        if(glfw.PRESS == action):
            dragR = True
            pos = glfw.get_cursor_pos(window)
            x, y = pos
            xposition = x
            yposition = y
        elif(glfw.RELEASE == action):
            dragR = False
            oldoffset = oldoffset + offset
            offset = np.zeros((3))

def scroll_callback(window, xoffset, yoffset):
    global zoom
    # zoom
    # yoffset은 -1 혹은 1의 값을 가진다. 스크롤에 이용하자.
    if(yoffset == 1): #확대
        if(zoom <= 3):
            zoom += 0.1
        elif(3 < zoom):
            zoom += 0.3
    elif(yoffset == -1): # 축소
        if(zoom > 0.1):
            zoom -= 0.1

def main():
    if not glfw.init():
        return
    window = glfw.create_window(960, 960, 'OpenGL viewer', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()