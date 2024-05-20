from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

obstacles={'stop':False}  #dictionary representing game obstacles
obs_flag=True
player_pos=[250,20]  # flag to indicate  obstacles generation
lives=3
score=0
gameover=False

def draw_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(abs(x), abs(y))
    glEnd()

def controller_circle(x, y, r):
    zone1_points = midpoint_circle(r)
    whole_circle = create_whole_circle(zone1_points)
    for i in whole_circle:
        draw_point(i[0] + x, i[1] + y)
    for i in whole_circle:
        i[0]+=x
        i[1]+=y
    return whole_circle

def midpoint_circle(r):
    d = 1 - r
    x = 0
    y = r
    intermediate = [[x, y]]
    
    while x <= y:
        if d >= 0:
            x += 1
            y -= 1
            intermediate.append([x, y])
            d = d + 2 * x - 2 * y + 5
        else:
            x += 1
            d = d + 2 * x + 3
            intermediate.append([x, y])
    
    return intermediate

def create_whole_circle(zone1_points):
    all_points = []

    for point in zone1_points:
        x, y = point
        # Octant 1
        all_points.append([x, y])
        # Octant 2
        all_points.append([-x, y])
        # Octant 3
        all_points.append([y, -x])
        # Octant 4
        all_points.append([-y, -x])
        # Octant 5
        all_points.append([-x, -y])
        # Octant 6
        all_points.append([x, -y])
        # Octant 7
        all_points.append([-y, x])
        # Octant 0
        all_points.append([y, x])
    return all_points

def midpoint_line(points):
    #to sort points based on x co-ordinates
    if points[0][0] >= points[1][0]:
        points[0], points[1] = points[1], points[0]  

    dx = points[1][0] - points[0][0] #del_X
    dy = points[1][1] - points[0][1] #del_Y
    d = dy - (dx // 2) #decision parameter bresenham algo
    x = points[0][0] 
    y = points[0][1]
    
    intermediate = [[x, y]] #list of intermediate points
    
    while x < points[1][0]: #until second x co-ordinate
        x += 1
        if d < 0:
            d += dy
        else:
            y += 1
            d += dy - dx
        intermediate.append([x, y])
    
    return intermediate

def controller_line(points):
    list1 = [] # to creat points after transformation 
    square = [[-10, -10], [-10, 10], [10, 10], [10, -10]]  # sqr define

    # iterate through each pair of consecutv input list
    for i in range(len(points) - 1): 
        zone = decide_zone([points[i], points[i + 1]]) #dtrmn zn
        convert = converttozero([points[i], points[i + 1]], zone) #Tozero(1st oct)
        interpoint = midpoint_line(convert) #calc inter for covtd zone
        zonepoint = returntooriginal(interpoint, zone) #cnvrt 2 original
        
        list1.extend(zonepoint)

    #for the last line segment
    zone = decide_zone([points[-1], points[0]])
    convert = converttozero([points[-1], points[0]], zone)
    interpoint = midpoint_line(convert)
    zonepoint = returntooriginal(interpoint, zone)
    list1.extend(zonepoint)

    for j in square:
        list1.append(j)
    for j in list1:
        draw_point(j[0], j[1])
    return points

def decide_zone(decide):
    dx=decide[0][0]-decide[1][0]
    dy=decide[0][1]-decide[1][1]
    if dx>0 and dy>=0 and abs(dx) >= abs(dy):
        return 0
    elif dx>=0 and dy>0 and abs(dx) < abs(dy):
        return 1
    elif dx<0 and dy>=0 and abs(dx) <= abs(dy):
        return 2
    elif dx<=0 and dy>0 and abs(dx) > abs(dy):
        return 3
    elif dx<0 and dy<=0 and abs(dx) >= abs(dy):
        return 4
    elif dx<=0 and dy<0 and abs(dx) < abs(dy):
        return 5

    elif dx>0 and dy<=0 and abs(dx) <= abs(dy):
        return 6

    elif dx>=0 and dy<0 and abs(dx) > abs(dy):
        return 7

def converttozero(zeroth,a): # a = zone/octant
    zeroth = [point[:] for point in zeroth] 
    if a==0:
        zeroth[0][0],zeroth[0][1]=zeroth[0][0],zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=zeroth[1][0],zeroth[1][1]
        return zeroth
    
    elif a==1:
        zeroth[0][0],zeroth[0][1]=zeroth[0][1],zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=zeroth[1][1],zeroth[1][0]
        return zeroth

    elif a==2:
        zeroth[0][0],zeroth[0][1]=zeroth[0][1],zeroth[0][0]*-1
        zeroth[1][0],zeroth[1][1]=zeroth[1][1],-1*zeroth[1][0]
        return zeroth

    elif a==3:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][0],zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][0],zeroth[1][1]
        return zeroth

    elif a==4:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][0],-1*zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][0],-1*zeroth[1][1]
        return zeroth

    elif a==5:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][1],-1*zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][1],-1*zeroth[1][0]
        return zeroth

    elif a==6:
        zeroth[0][0],zeroth[0][1]=-1*zeroth[0][1],zeroth[0][0]
        zeroth[1][0],zeroth[1][1]=-1*zeroth[1][1],zeroth[1][0]
        return zeroth

    elif a==7:
        zeroth[0][0],zeroth[0][1]=zeroth[0][0],-1*zeroth[0][1]
        zeroth[1][0],zeroth[1][1]=zeroth[1][0],-1*zeroth[1][1]
        return zeroth
    
def returntooriginal(points, zone):
    if zone == 0:
        return points  
    elif zone == 1:
        return [[point[1], point[0]] for point in points]

    elif zone == 2:
        return [[point[1], -point[0]] for point in points]

    elif zone == 3:
        return [[-point[0], point[1]] for point in points]

    elif zone == 4:
        return [[-point[0], -point[1]] for point in points]

    elif zone == 5:
        return [[-point[1], -point[0]] for point in points]

    elif zone == 6:
        return [[-point[1], point[0]] for point in points]

    elif zone == 7:
        return [[point[0], -point[1]] for point in points]

def specialKeyListener(key, x, y):
    global player_pos,score
    if not obstacles['stop']:
        if key==GLUT_KEY_UP:  # x-unchanged, Y+=40 /score+=1
            player_pos[0]+=0
            player_pos[1]+=40
            score+=1
            
        if key== GLUT_KEY_DOWN:	# x-unchanged, Y-=40 
            player_pos[0]+=0
            player_pos[1]-=40
            
        if key==GLUT_KEY_RIGHT: # x+=40, Y-unchanged 
            player_pos[0]+=40
            player_pos[1]+=0
            
        if key==GLUT_KEY_LEFT:  # x-=40, Y-unchanged
            player_pos[0]-=40
            player_pos[1]+=0
        
    glutPostRedisplay()
        

def mouseListener(button, state, x, y):
    global obstacles,obs_flag,player_pos,lives
    
    if 10<=x<=50 and 470<=-1*(y-500)<=490: #restart
        if button==GLUT_LEFT_BUTTON: 
            if(state == GLUT_DOWN):
                obstacles={'stop':False}
                obs_flag=True
                player_pos=[250,20]
                lives=3
                
    
    elif 245<=x<=255 and 470<=-1*(y-500)<=490: #pause/play
        if button==GLUT_LEFT_BUTTON: 
            if(state == GLUT_DOWN):
                if not obstacles['stop']:
                    obstacles['stop']=True
                else:
                    obstacles['stop']=False
           
    elif 460<=x<=480 and 470<=-1*(y-500)<=490: #exit
        if button==GLUT_LEFT_BUTTON: 
            if(state == GLUT_DOWN):
                glutLeaveMainLoop() 

    glutPostRedisplay()
    
def retry():
    global player_pos,obstacles,obs_flag
    obstacles={'stop':False}
    obs_flag=True
    player_pos=[250,20]

def check_collision( player):
    global player_pos,obstacles,lives,score
    
    for k, v in obstacles.items():
        if k!='stop':
            val = v['points']
            #checks x
            if val[0][0] >= player_pos[0]+10 >= val[3][0]or val[0][0] >= player_pos[0]-10 >= val[3][0]:
                #checks Y
                if val[0][1] <= player_pos[1]+10 <= val[2][1]:
                    obstacles['stop']=True
                    lives-=1
                    score=0
                    print("Collision detected!")
                    retry()
                    return 



def generate_obstacle(level):
    global obstacles
    x = random.randint(50, 450)  # x-coord for obstacle within [50, 450]
    y = level * 40 #separated by 40 units
    velocity = random.choice([-7,-6,-5,-4,-3-2, 2,3,4,5,6,7])  #[(-7,+7) without 0,1]

    obstacles[level] = {"points": [[x,y],[x,y+30],[x-50,y+30],[x-50,y]], "velocity": velocity}
    
def animation():
    global obstacles
    
    if not obstacles['stop']:
        
        for k,v in obstacles.items():
            
            if k!='stop':
                point=v['points']
                
                if point[0][0]>=500 :
                    v['velocity']=v['velocity']*-1
                    
                if point[3][0]<=0:
                    v['velocity']=v['velocity']*-1
                        
        for i, k in obstacles.items():
            if i!='stop':
                
                if k['points'][0][0]<=500 or k['points'][3][0]>=0:
                    
                    for point in k['points']:
                        point[0] += k["velocity"]

    glutPostRedisplay()

    
def showScreen():
    global obstacles, obs_flag, player_pos, score, lives
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    interation()
    glColor3f(1.0, 1.0, 0.0)
    # creating obstaces
    x = 40
    for level in range(1, 11):
        level_points = controller_line([[0, x], [500, x]])
        x += 40
        if obs_flag:
            generate_obstacle(level)
    obs_flag = False
    # //////////////////////////////////////////
    # creating player
    for i, j in obstacles.items():
        if i!='stop':
            lala = controller_line(j['points'])
    # ////////////////////////////////////////////
    # buttons
    reset=controller_line([[30,490],[10,480],[30,470],[10,480],[50,480],[10,480]])
     
    if not obstacles['stop']:
        pause=controller_line([[245,490],[245,470]])
        pause=controller_line([[255,490],[255,470]])
    else:
        play=controller_line([[245,490],[245,470],[255,480]])
        
        
    exit=controller_line([[460,490],[480,470]])
    exit=controller_line([[460,470],[480,490]])
    # ///////////////////////////////////////////////
    # creating player
    if lives!=0:
        player = controller_circle(player_pos[0], player_pos[1], 10)
    else:
        glColor3f(1,0,0)
        player = controller_circle(player_pos[0], player_pos[1], 10)
    # //////////////////////////////////////////////////
    # check collision, reseting after reaching top and calculating lives
    check_collision( player)
    if player_pos[1]>=410:
        retry()
    if lives==0:
        obstacles['stop']=True
    # ////////////////////////////////////////
    print(f'score: {score}---------lives: {lives}')
    glutSwapBuffers()



    
def interation():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
    
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) 
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") 
glutDisplayFunc(showScreen)
glutIdleFunc(animation)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()