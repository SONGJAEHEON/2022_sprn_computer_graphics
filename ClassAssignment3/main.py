import os
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

eye = np.array([3.,3.,3.])
oldeye = np.array([3.,3.,3.])
target = np.zeros((3))
up = np.array([0,1,0])
offset = np.zeros((3))
oldoffset = np.zeros((3))

renderMode = -1

list = []
list2 = []
list3 = []

def render():
    global renderMode, list, list2, list3, totalCnt, orthoView, zoom, xposition, newxposition, yposition, newyposition, vecW, vecU, vecV, dragL, dragR, eye, oldeye, target, up, offset, oldoffset, wireSolid, hierarchical, normalShading
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()    

    glScalef(zoom, zoom, zoom)
    glTranslatef(0, 0, -1); 

    # use orthogonal projection (we'll see details later)
    if(orthoView == True):
        glOrtho(-5,5,-5,5,-10,10)
    else:
        gluPerspective(90, 1, 0.1, 100)

    gluLookAt(eye[0]+oldoffset[0]+offset[0],eye[1]+oldoffset[1]+offset[1],eye[2]+oldoffset[2]+offset[2], target[0]+oldoffset[0]+offset[0],target[1]+oldoffset[1]+offset[1],target[2]+oldoffset[2]+offset[2], 0,1,0)
    drawFrame()

    if(renderMode == 0):
        chnlCnt = 0 # channel count
        level = -1
        v1 = []
        v2 = []
        idx = 0
        mtrxStck = 0
        bfrLevel = level
        level = list[idx][2]
        while(idx <= totalCnt):
            if(list[idx][0].lower() == 'end'):
                idx += 1
                bfrLevel = level
                level = list[idx][2]
            # if level > bfrLevel 요런식으로하면 될듯. 다음 것을 연결하면 되는 경우
            elif(level > bfrLevel):
                j = list[idx][6]
                # tmpList = []
                # for i in range(0, list[idx][6]):
                #     tmpList.append(list2[chnlCnt+i])
                #     j += 1
                # tmpList = list2[idx]
                # euler, zxy = eulerParse(tmpList, chnlCnt)
                # euler, zxy = eulerParse(tmpList, idx, 0, chnlCnt)
                euler, zxy = eulerParse(idx, 0, chnlCnt)
                xang = euler[0]
                yang = euler[1]
                zang = euler[2]
                M = np.identity(4)
                # Rx = np.array([[1,0,0],
                #                 [0,np.cos(xang),-np.sin(xang)],
                #                 [0,np.sin(xang),np.cos(xang)]])
                # Ry = np.array([[np.cos(yang),0,np.sin(yang)],
                #                 [0,1,0],
                #                 [-np.sin(yang,),0,np.cos(yang)]])
                # Rz = np.array([[np.cos(zang),-np.sin(zang),0],
                #                 [np.sin(zang),-np.sin(zang),0],
                #                 [0,0,1]])
                Rx = np.array([[1,0,0],
                                [0, np.cos(xang), -np.sin(xang)],
                                [0, np.sin(xang), np.cos(xang)]])
                Ry = np.array([[np.cos(yang), 0, np.sin(yang)],
                                [0,1,0],
                                [-np.sin(yang), 0, np.cos(yang)]])
                Rz = np.array([[np.cos(zang), -np.sin(zang), 0],
                                [np.sin(zang), np.cos(zang), 0],
                                [0,0,1]])

                if(zxy == 13332): # xyz
                    M[:3,:3] = Rx @ Ry @ Rz
                elif(zxy == 13341): # xzy
                    M[:3,:3] = Rx @ Rz @ Ry
                elif(zxy == 13422): # yxz
                    M[:3,:3] = Ry @ Rx @ Rz
                elif(zxy == 13440): # yzx
                    M[:3,:3] = Ry @ Rz @ Rx
                elif(zxy == 13521): # zxy
                    M[:3,:3] = Rz @ Rx @ Ry
                elif(zxy == 13530): # zyx
                    M[:3,:3] = Rz @ Ry @ Rx
                glMultMatrixf(M.T)
                if(len(euler)>3): # xposotion, yposition, zposition
                    glTranslatef(euler[3],euler[4],euler[5])
                v1 = [list[idx][3], list[idx][4], list[idx][5]]
                v2 = [list[idx+1][3], list[idx+1][4], list[idx+1][5]]
                glPushMatrix()
                mtrxStck += 1
                glColor3ub(156,42,190)
                glBegin(GL_LINES)
                glVertex3fv(np.array(v1)) # start
                glVertex3fv(np.array(v2)) # end
                glEnd()
                # joint 갯수 등으로 끝지점 파악하면 될듯
                chnlCnt += j
                idx += 1
                bfrLevel = level
                level = list[idx][2]
            else:
                # j = list[idx][6]
                bfrLvl, bfrIdx = findBefore(idx)
                i = 1
                while(i < list[idx-1][2]-bfrLvl):
                    glPopMatrix()
                    mtrxStck -= 1
                    i += 1
                v1 = [list[bfrIdx][3], list[bfrIdx][4], list[bfrIdx][5]]
                v2 = [list[idx][3], list[idx][4], list[idx][5]]
                glBegin(GL_LINES)
                glVertex3fv(np.array(v1)) # start
                glVertex3fv(np.array(v2)) # end
                glEnd()
                # chnlCnt += j
                bfrLevel = bfrLvl
                level = list[idx][2]
    elif(renderMode == 1):
        pass


# def eulerParse(list, cnt):
def eulerParse(idx, frame, chnlCnt):
    global list2, list3
    # xp = yp = zp = xr = yr = zr = 0.0
    rtn = [0.0,0.0,0.0,0.0,0.0,0.0]
    zxy = []
    length = len(list2[idx])
    # print(idx)
    for i in range(0, length):
        # if(list2[cnt+i] == 1): # xr
        if(list2[idx][i] == 1): # xr
            # rtn[0] = list3[cnt+i]
            rtn[0] = float(list3[frame][chnlCnt+i])
            zxy.append('x')
        # elif(list2[cnt+i] == 2): # yr
        elif(list2[idx][i] == 2): # xr
            # rtn[1] = list3[cnt+i]
            rtn[1] = float(list3[frame][chnlCnt+i])
            zxy.append('y')
        # elif(list2[cnt+i] == 3): # zr
        elif(list2[idx][i] == 3): # xr
            # rtn[2] = list3[cnt+i]
            rtn[2] = float(list3[frame][chnlCnt+i])
            zxy.append('z')
        # elif(list2[cnt+i] == 4): # xp
        elif(list2[idx][i] == 4): # xp
            # rtn[3] = list3[cnt+i]
            rtn[3] = float(list3[frame][chnlCnt+i])
        # elif(list2[cnt+i] == 5): # yp
        elif(list2[idx][i] == 5): # xp
            # rtn[4] = list3[cnt+i]
            rtn[4] = float(list3[frame][chnlCnt+i])
        # elif(list2[cnt+i] == 6): # zp
        elif(list2[idx][i] == 6): # xp
            # rtn[5] = list3[cnt+i]
            rtn[5] = float(list3[frame][chnlCnt+i])
    return rtn, ord(zxy[0])*100 + ord(zxy[1])*10 + ord(zxy[2])
        
def findBefore(idx):
    global list
    curLvl = list[idx][2]
    bfrLvl = 2000000000
    while(idx > -1):
        idx -= 1
        bfrLvl = list[idx][2]
        if(bfrLvl < curLvl):
            break
    return bfrLvl, idx


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

def key_callback(window, key, scancode, action, mods):
    global spaceBarPrsd, renderMode, orthoView, zoom, xposition, newxposition, yposition, newyposition, vecW, vecU, vecV, dragL, dragR, eye, oldeye, target, up, offset, oldoffset, wireSolid, hierarchical, normalShading
    # global orthoView, zoom, xposition, newxposition, yposition, newyposition, vecW, vecU, vecV, dragL, dragR, eye, oldeye, target, up, offset, oldoffset, wireSolid, hierarchical, normalShading
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_SPACE: # Movement
            spceBarPrsd = 1
        elif key==glfw.KEY_1: # Line rendering mode
            renderMode = 0
        elif key==glfw.KEY_2: # Box rendering mode
            renderMode = 1
        elif key==glfw.KEY_V: # view switching(orthogonal vs perspective)
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
    # global fCnt, vtcCnt3, vtcCnt4, vtcCnt5, gVertexArrayIndexed, gIndexArray, firstDrag
    global file, renderMode
    for path in paths:
        dir, file = os.path.split(path)
        readFile(path)
        renderMode = 0


def readFile(path):
    global renderMode, list, list2, list3, totalCnt, file, frames, fps, jointCnt, jointList
    f = open(path, 'r')
    totalCnt = 0
    level = 0
    motnDfltChck = -1
    jointCnt = 0
    jointList = []

    tmpList = []
    tmpList2 = []
    tmpList3 = []

    while(1):
        line = f.readline()
        if not line:
            break # 그냥 return하면 되는 건가?
        words = line.split()

        # mode switching
        if(words[0].lower() == 'hierarchy'):
            renderMode = 0
            continue
        elif(words[0].lower() == 'motion'):
            renderMode = 1
            continue
        
        # hierarchy parsing
        if(renderMode == 0):
            if level >= 0:
                if(words[0] == '{'):
                    level += 1
                elif(words[0] == '}'):
                    level -= 1
                    # if(level == 0):
                    #     list.append(tmpList)
                    #     list2.append(tmpList2)
                    #     break
                elif(words[0].lower() == 'root'):
                    totalCnt += 1
                    tmpList.append('root')
                    tmpList.append(words[1])
                    jointCnt += 1
                    jointList.append(words[1])
                    tmpList.append(level) # level
                elif(words[0].lower() == 'offset'):
                    tmpList.append(words[1])
                    tmpList.append(words[2])
                    tmpList.append(words[3])
                elif(words[0].lower() == 'channels'):
                    length = len(words)
                    tmpList.append(length)
                    for i in range(2, length):
                        if(words[i].lower() == 'xposition'):
                            tmpList2.append(4)
                        elif(words[i].lower() == 'yposition'):
                            tmpList2.append(5)
                        elif(words[i].lower() == 'zposition'):
                            tmpList2.append(6)
                        elif(words[i].lower() == 'xrotation'):
                            tmpList2.append(1)
                        elif(words[i].lower() == 'yrotation'):
                            tmpList2.append(2)
                        elif(words[i].lower() == 'zrotation'):
                            tmpList2.append(3)
                elif(words[0].lower() == 'joint'):
                    totalCnt += 1
                    list.append(tmpList)
                    list2.append(tmpList2)
                    tmpList = []
                    tmpList2 = []
                    tmpList.append('root')
                    tmpList.append(words[1])
                    jointCnt += 1
                    jointList.append(words[1])
                    tmpList.append(level) # level
                elif(words[0].lower() == 'offset'):
                    tmpList.append(words[1])
                    tmpList.append(words[2])
                    tmpList.append(words[3])
                elif(words[0].lower() == 'channels'):
                    length = int(words[1])
                    tmpList.append(length)
                    for i in range(2, length):
                        if(words[i].lower() == 'xrotation'):
                            tmpList2.append(1)
                        elif(words[i].lower() == 'yrotation'):
                            tmpList2.append(2)
                        elif(words[i].lower() == 'zposition'):
                            tmpList2.append(3)
                elif(words[0].lower() == 'end'):
                    list.append(tmpList)
                    list2.append(tmpList2)
                    tmpList = []
                    tmpList2 = []
                    tmpList.append('end')
                    tmpList.append(words[1])
                    tmpList.append(level) # level
                elif(words[0].lower() == 'offset'):
                    tmpList.append(words[1])
                    tmpList.append(words[2])
                    tmpList.append(words[3])
        # motion parsing
        elif(renderMode == 1):
            if(motnDfltChck < 1):
                if(words[0].lower().find('frames') > -1):
                    frames = int(words[1])
                    motnDfltChck += 1
                elif(line.lower().find('frame time') > -1):
                    fps = int(1/float(words[2]))
                    motnDfltChck += 1
            else:
                if(len(tmpList3) > 0):
                    list3.append(tmpList3)
                    tmpList3 = []
                for i in words:
                    tmpList3.append(i)
    printFileMetadata()

def printFileMetadata():
    global totalCnt, file, frames, fps, jointCnt, jointList
    print('File name: ' + file)
    print('Number of frames: ', frames)
    print('FPS: ', fps)
    print('Number of joints (including root): ', jointCnt)
    print('List of all joint names: ')
    print(jointList)
    print()

def createVertexAndIndexArrayIndexed():
    varr = np.array()
    iarr = np.array()
    return varr, iarr

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1280, 1280, 'bvh format viewer', None, None)
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
