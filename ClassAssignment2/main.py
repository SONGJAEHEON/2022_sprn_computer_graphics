import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes 

orthoView = False
zoom = .5
xposition = 0.
newxposition = 0.
yposition = 0.
newyposition = 0.
vecW=vecU=vecV = np.ones((3))
dragL = False
dragR = False

eye = np.array([3.,3.,3.])
oldeye = np.array([3.,3.,3.])
target = np.zeros((3))
up = np.array([0,1,0])
offset = np.zeros((3))
oldoffset = np.zeros((3))

gVertexArrayIndexed = []
gIndexArray = []

firstDrag = False

fCnt = 0
vtcCnt3 = 0
vtcCnt4 = 0
vtcCnt5 = 0

faceList = []
fType = 0

wireSolid = True
hierarchical = False
normalShading = True

def render():
    global hierarchical, faceList
    # enable depth test (we'll see details later)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    if(wireSolid):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glScalef(zoom, zoom, zoom)
    glTranslatef(0, 0, -1); 

    # use orthogonal projection (we'll see details later)
    if(orthoView == True):
        glOrtho(-5,5,-5,5,-10,10)
    else:
        gluPerspective(90, 1, 0.1, 100)

    gluLookAt(eye[0]+oldoffset[0]+offset[0],eye[1]+oldoffset[1]+offset[1],eye[2]+oldoffset[2]+offset[2], target[0]+oldoffset[0]+offset[0],target[1]+oldoffset[1]+offset[1],target[2]+oldoffset[2]+offset[2], 0,1,0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)

    glPushMatrix()
    lightPos = (100., 100., 100., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    glPushMatrix()
    lightPos = (-100., -100., -100., 0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    # glPushMatrix()
    lightColor = (1., 0., 0., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    # glPopMatrix()

    # glPushMatrix()
    lightColor = (0., 0., 1., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)
    # glPopMatrix()

    glPushMatrix()
    objectColor = (.5, .5, .5, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glPopMatrix()

    if(hierarchical == False):
        drawFrame()
        draw_glDrawElements()
            
    else: # hierarchical == True
        objPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),"obj_files")
        t = glfw.get_time()        
        glPushMatrix()
        glTranslatef(0, 0, np.cos(t))
        roadPath = os.path.join(objPath, "road.obj")
        readFile(roadPath)
        draw_glDrawElements()
        
        glPushMatrix()
        glScalef(.4, .4, .4)
        glTranslatef(np.sin(t), .5, 6 + np.sin(t))
        carPath = os.path.join(objPath, "car.obj")
        readFile(carPath)
        draw_glDrawElements()

        glPushMatrix()
        glTranslatef(0, np.sin(t), -6)
        glScalef(0.01, 0.01, 0.01)
        glRotatef(-60, 1, 0, 0)
        glRotatef(t*(180/np.pi), 1, 0, 0)
        dolphinPath = os.path.join(objPath, "dolphin.obj")
        readFile(dolphinPath)
        draw_glDrawElements()
        glPopMatrix()

        glPushMatrix()
        glScalef(.5, .5, .5)
        glTranslatef(-7., 4+2*np.sin(t), 2*np.cos(t))
        ballPath = os.path.join(objPath, "ball.obj")
        readFile(ballPath)
        draw_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        glPushMatrix()
        glScalef(.4, .4, .4)
        glTranslatef(2 + np.cos(t), 1, -7)
        sofaPath = os.path.join(objPath, "sofa.obj")
        readFile(sofaPath)
        draw_glDrawElements()

        glPushMatrix()
        glRotatef(t*(180/np.pi), 0, 1, 0)
        glTranslatef(-2., 1., -1.)
        glScalef(.2, .2, .2)
        treePath = os.path.join(objPath, "tree.obj")
        readFile(treePath)
        draw_glDrawElements()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(1, 2, np.sin(t))
        clockPath = os.path.join(objPath, "clock.obj")
        readFile(clockPath)
        draw_glDrawElements()
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,3.]))
    glColor3ub(100, 100, 100)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,-3.]))
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([-3.,0.,0.]))
    for i in range(1, 31):
        glVertex3fv(np.array([i/10,0.,-3.]))
        glVertex3fv(np.array([i/10,0.,3.]))
        glVertex3fv(np.array([-i/10,0.,-3.]))
        glVertex3fv(np.array([-i/10,0.,3.]))
    for j in range(1, 31):
        glVertex3fv(np.array([-3.,0.,j/10]))
        glVertex3fv(np.array([3.,0.,j/10]))
        glVertex3fv(np.array([-3.,0.,-j/10]))
        glVertex3fv(np.array([3.,0.,-j/10]))
    glEnd()

def draw_glDrawElements():
    global gVertexArrayIndexed, gIndexArray, faceList
    if(fType == 1):
        varr = np.array(faceList, 'float32')
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(GL_FLOAT, 3*varr.itemsize, varr)
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))
    elif(fType == 2):
        varr = np.array(faceList, 'float32')
        # varr = faceList
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/3))
    elif(fType == 3):
        varr = np.array(faceList, 'float32')
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))
    elif(fType == 4):
        varr = np.array(faceList, 'float32')
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
        glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))
    

def key_callback(window, key, scancode, action, mods):
    global orthoView, zoom, xposition, newxposition, yposition, newyposition, vecW, vecU, vecV, dragL, dragR, eye, oldeye, target, up, offset, oldoffset, wireSolid, hierarchical, normalShading
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
            eye = np.array([3.,3.,3.])
            oldeye = np.array([3.,3.,3.])
            target = np.zeros((3))
            up = np.array([0,1,0])
            offset = np.zeros((3))
            oldoffset = np.zeros((3))
        if key==glfw.KEY_H: # animating hierarchical model rendering mode
            if(hierarchical):
                hierarchical = False
            else:
                hierarchical = True
        if key==glfw.KEY_Z: # toggle wireframe / solid mode (similar to 'z' in Blender)
            if(wireSolid):
                wireSolid = False
            else:
                wireSolid = True
        if key==glfw.KEY_S: # toggle 'shading using normal data in obj file' <-> 'forced smooth shading'
            if(normalShading):
                normalShading = False
            else:
                normalShading = True

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

def drop_callback(window, paths): # The callback function receives an array of paths encoded as UTF-8.The callback function receives an array of paths encoded as UTF-8.
    global fCnt, vtcCnt3, vtcCnt4, vtcCnt5, gVertexArrayIndexed, gIndexArray, firstDrag

    for path in paths:
        head, tail = os.path.split(path)
        fileName = tail
        readFile(path)
    print('file name: ' + fileName)
    print('total number of faces: ', fCnt)
    print('number of faces with 3 verticies: ', vtcCnt3)
    print('number of faces with 4 verticies: ', vtcCnt4)
    print('number of faces with more than 4 verticies: ', vtcCnt5)


def readFile(path):
    global fCnt, vtcCnt3,  vtcCnt4, vtcCnt5, gVertexArraySeparate, gIndexArray, faceList, fType
    fCnt = 0
    vtcCnt3 = 0
    vtcCnt4 = 0
    vtcCnt5 = 0
    faceList = []
    f = open(path, 'r')
    vertexList = []
    vertexNormalList = []
    textureList = []
    faceElement = []
    lines = f.readlines()
    for line in lines:
        words = line.split()
        vertex = []
        length = len(words)
        if(length == 0):
            continue
        elif words[0][0] == '#':
            continue
        elif words[0] == 'o':
            objectType = words[1]
        elif words[0] == 'v':
            i = 1
            while(i < length):
                vertex.append(words[i])
                i += 1
            vertexList.append(tuple(vertex))
        elif words[0] == 'vn':
            i = 1
            while(i < length):
                vertex.append(words[i])
                i += 1
            vertexNormalList.append(tuple(vertex))
        elif words[0] == 'vt':
            # i = 1
            # while(i < length):
            #     vertex.append(words[i])
            #     i += 1
            # vertex.append('0')
            # textureList.append(tuple(vertex))
            continue
        elif words[0] == 'usemtl':
            material = words[1]
        elif words[0] == 's':
            shading = words[1]
        elif words[0] == 'f':
            fCnt += 1
            i = 1
            figureForm = length - 1
            if(figureForm == 3):
                vtcCnt3 += 1
            elif(figureForm == 4):
                vtcCnt4 += 1
            else:
                vtcCnt5 += 1
            if(length<5):
                while(i < length):
                    numbers = words[i].split('/')
                    numLength = len(numbers)
                    if(numLength == 1):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 1
                    elif(numLength == 2):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        # faceElement.append(tuple(textureList[(int(numbers[1])-1)]))
                        if(not fType):
                            fType = 2
                    elif(numLength == 3):
                        if(numbers[1] == ''):
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 3
                        else:
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            # faceElement.append(tuple(textureList[(int(numbers[1])-1)]))
                            if(not fType):
                                fType = 4

                    i += 1
            else: # figure with more than 4 vertices
                while(i < length-2):
                    numbers = words[i].split('/')
                    numLength = len(numbers)
                    if(numLength == 1):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 1
                    elif(numLength == 2):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 2
                    elif(numLength == 3):
                        if(numbers[1] == ''):
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 3
                        else:
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 4
                    numbers = words[i+1].split('/')
                    numLength = len(numbers)
                    if(numLength == 1):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 1
                    elif(numLength == 2):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 2
                    elif(numLength == 3):
                        if(numbers[1] == ''):
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 3
                        else:
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 4
                    numbers = words[length-1].split('/')
                    numLength = len(numbers)
                    if(numLength == 1):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 1
                    elif(numLength == 2):
                        faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                        if(not fType):
                            fType = 2
                    elif(numLength == 3):
                        if(numbers[1] == ''):
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 3
                        else:
                            faceElement.append(tuple(vertexNormalList[(int(numbers[2])-1)]))
                            faceElement.append(tuple(vertexList[(int(numbers[0])-1)]))
                            if(not fType):
                                fType = 4
                    i += 1
        else:
            continue

        # faceList = np.array(faceElement, 'float32')
        faceList = faceElement

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1280, 1280, 'OpenGL viewer', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
