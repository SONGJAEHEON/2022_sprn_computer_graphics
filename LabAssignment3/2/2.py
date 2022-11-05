# [Practice] Uniform Scale
import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.array([[1., 0., .0],
            [0., 1., .0],
            [0., 0., 1.]])
newM = np.array([[1., 0., .0],
                    [0., 1., .0],
                    [0., 0., 1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0,.5,1.]))[:-1])
    glVertex2fv((T @ np.array([.0,.0,1.]))[:-1])
    glVertex2fv((T @ np.array([.5,.0,1.]))[:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    global newM

    degreeTen = np.radians(10)
    if action != glfw.RELEASE:
        return
    elif key==glfw.KEY_W: # Scale by 0.9 in X dir.
        newM = np.array([[.9, 0., .0],
                        [0., 1., .0],
                        [0., 0., 1.]])
    elif key==glfw.KEY_E: # Scale by 1.1 in X dir.
        newM = np.array([[1.1, 0., .0],
                        [0., 1., .0],
                        [0., 0., 1.]])
    elif key==glfw.KEY_S: # Rotate by 10 degrees counterclockwise.
        newM = np.array([[np.cos(degreeTen), -np.sin(degreeTen), 0.],
                      [np.sin(degreeTen), np.cos(degreeTen), 0.],
                      [0.,          0.,         1.]])
    elif key==glfw.KEY_D: # Rotate by 10 degrees clockwise
        newM = np.array([[np.cos(-degreeTen), -np.sin(-degreeTen), 0.],
                      [np.sin(-degreeTen), np.cos(-degreeTen), 0.],
                      [0.,          0.,         1.]])
    elif key==glfw.KEY_X: # Shear by a factor of -0.1 in X dir.
        newM = np.array([[1., -0.1, .0],
                        [0., 1., .0],
                        [0., 0., 1.]])
    elif key==glfw.KEY_C: # Shear by a factor of 0.1 in X dir.
        newM = np.array([[1., 0.1, .0],
                        [0., 1., .0],
                        [0., 0., 1.]])
    elif key==glfw.KEY_R: # Reflection accross X axis.
        newM = np.array([[1., 0., .0],
                        [0., -1., .0],
                        [0., 0., 1.]])
    elif key==glfw.KEY_1: # Reset the triangle with identity matrix.
        gComposedM = np.array([[1., 0., .0],
                        [0., 1., .0],
                        [0., 0., 1.]])

def main():
    global gComposedM
    global newM

    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029834",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        gComposedM = newM @ gComposedM

        render(gComposedM)

        newM = np.array([[1., 0., .0],
                [0., 1., .0],
                [0., 0., 1.]])

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()