import glfw
from OpenGL.GL import *
import numpy as np

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    # point p=(0.5, 0) / vector v=(0.5, 0)

    # draw point p
    glBegin(GL_POINTS)
    ###
    # glVertex2fv((M @ np.array([1., .0, 1.]))[:-1])
    glVertex3fv((M @ np.array([.5, .0, .0, 1.]))[:-1])
    ###
    glEnd()

    # draw vector v
    glBegin(GL_LINES)
    ###
    v0 = np.array([.0, .0, .0, .0])
    v1 = np.array([.5, .0, .0, .0])
    # glVertex2fv((M @ np.array([.0, .0, 1.]))[:-1])
    # glVertex2fv((M @ np.array([.5, .0, 1.]))[:-1])
    glVertex3fv((M @ v0)[:-1])
    glVertex3fv((M @ v1)[:-1])
    ###
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, "2017029834", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        time = glfw.get_time()
        T = np.array([[1., 0., 0., .5],
                    [0., 1., 0., 0.],
                    [0., 0., 1., 0.],
                    [0., 0., 0., 1.]])
        M = np.array([[np.cos(time), -np.sin(time), 0., 0.],
            [np.sin(time), np.cos(time), 0., 0.],
            [0.,            0.,          1., 0.],
            [0.,            0.,         0., 1.]])
        # T = np.array([[1., 0., .5],
        #             [0., 1., 0.],
        #             [0., 0., 1.]])
        M = M @ T
        render(M)
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()