import glfw
from OpenGL.GL import *
import numpy as np

keyList = []

def render():
    global keyList

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    #####
    for i in keyList:
        if i=='q':
            glTranslatef(-0.1, 0, 0)
        elif i=='e':
            glTranslatef(0.1, 0, 0)
        elif i=='a':
            glRotatef(10, 0, 0, 1)
        elif i=='d':
            glRotatef(10, 0, 0, -1)
    #####

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, .0]))
    glEnd()
    
def key_callback(window, key, scancode, action, mods):
    global keyList

    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Q: # Translate by -0.1 in x direction
            keyList.insert(0, 'q')
        elif key==glfw.KEY_E: # Translate by 0.1 in x direction
            keyList.insert(0, 'e')
        elif key==glfw.KEY_A: # Rotate by 10 degrees counterclockwise
            keyList.insert(0, 'a')
        elif key==glfw.KEY_D: # Rotate by 10 degrees clockwise
            keyList.insert(0, 'd')
        elif key==glfw.KEY_1: # Reset the triangle with identity matrix
            keyList.clear()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2017029834", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()