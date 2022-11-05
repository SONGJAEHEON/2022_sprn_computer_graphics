# [Practice] Uniform Scale
import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # Draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # Draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0,.5,1.]))[:-1])
    glVertex2fv((T @ np.array([.0,.0,1.]))[:-1])
    glVertex2fv((T @ np.array([.5,.0,1.]))[:-1])
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2017029834",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Set the number of screen refresh to wait before calling glfw.swap_buffer().
    # If you monitor's refresh rate is 60hz, the while loop is repeated every 1/60 seconds.
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Get the current time in seconds
        t = glfw.get_time()

        # Set the rotation speed
        th = t

        # Rotation
        R = np.array([[np.cos(th), -np.sin(th), 0.],
                      [np.sin(th), np.cos(th), 0.],
                      [0.,          0.,         1.]])
        
        # Translation
        T = np.array([[1., 0., 0.5],
                    [0., 1., .0],
                    [0., 0., 1.]])

        render(R@T)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()