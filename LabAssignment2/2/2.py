import glfw
from OpenGL.GL import *

arr = {1:GL_POINTS, 2:GL_LINES, 3:GL_LINE_STRIP, 4:GL_LINE_LOOP, 5:GL_TRIANGLES, 6:GL_TRIANGLE_STRIP, 7:GL_TRIANGLE_FAN, 8:GL_QUADS, 9:GL_QUAD_STRIP, 0:GL_POLYGON}
type = arr[4]

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(type)
    glVertex(0.5, 0.5)
    glVertex(-0.5, 0.5)
    glVertex(-0.5, -0.5)
    glVertex(0.5, -0.5)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global arr
    global type
    if key==glfw.KEY_1:
        type = arr[1]
    elif key==glfw.KEY_2:
        type = arr[2]
    elif key==glfw.KEY_3:
        type = arr[3]
    elif key==glfw.KEY_4:
        type = arr[4]
    elif key==glfw.KEY_5:
        type = arr[5]
    elif key==glfw.KEY_6:
        type = arr[6]
    elif key==glfw.KEY_7:
        type = arr[7]
    elif key==glfw.KEY_8:
        type = arr[8]
    elif key==glfw.KEY_9:
        type = arr[9]
    elif key==glfw.KEY_0:
        type = arr[0]


def main():
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
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()