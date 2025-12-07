from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time
import math
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
FPS = 60
PLAYING = 0
PAUSED = 1
GAME_OVER = 2
game_state = PLAYING
score = 0
diamond_speed=100 
catcher_speed=300  
last_time=0
catcher_x=WINDOW_WIDTH // 2
catcher_width=150
catcher_height=20
catcher_y=50 

diamond_x=0
diamond_y=0
diamond_size=15
diamond_color=[1.0, 1.0, 0.0]
base_speed=100 
speed_increase_interval=3 

button_size = 30
buttons = {
    'restart': {'x': 50, 'y': WINDOW_HEIGHT - 50},
    'playpause': {'x': WINDOW_WIDTH // 2, 'y': WINDOW_HEIGHT - 50},
    'exit': {'x': WINDOW_WIDTH - 50, 'y': WINDOW_HEIGHT - 50}
}
def find_zone(x1, y1, x2, y2):#kon zone ae ache
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def convert_to_zone0(x, y, zone):#zone convert
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
    return x, y

def convert_from_zone0(x, y, zone):
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
    return x, y

def draw_line_midpoint(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    
    if x1_z0 > x2_z0:
        x1_z0, x2_z0 = x2_z0, x1_z0
        y1_z0, y2_z0 = y2_z0, y1_z0
    
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    
    x = x1_z0
    y = y1_z0
    
    while x <= x2_z0:
        original_x, original_y = convert_from_zone0(x,y,zone)
        glVertex2f(original_x, original_y)        
        if d > 0:
            d+=incrNE
            y+=1
        else:
            d+=incrE
        x+=1

def draw_diamond(x, y, size, color):
    glColor3f(color[0],color[1],color[2])
    
    glBegin(GL_POINTS)
    draw_line_midpoint(x,y+size,x+size,y)  
    draw_line_midpoint(x+size,y,x,y-size)  
    draw_line_midpoint(x,y-size,x-size,y)  
    draw_line_midpoint(x-size,y,x,y+size)  
    glEnd()

def draw_catcher(x, y, width, height, is_game_over):
    if is_game_over:
        glColor3f(1.0, 0.0, 0.0) 
    else:
        glColor3f(1.0, 1.0, 1.0) 
    
    glBegin(GL_POINTS)
    draw_line_midpoint(x - width/2, y + height, x + width/2, y + height) 
    draw_line_midpoint(x - width/2, y + height, x - width/4, y) 
    draw_line_midpoint(x + width/2, y + height, x + width/4, y)  
    draw_line_midpoint(x - width/4, y, x + width/4, y) 
    glEnd()

def draw_button(x, y, button_type):
    if button_type == 'restart':
        glColor3f(0.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        draw_line_midpoint(x - 10, y, x + 5, y - 10)
        draw_line_midpoint(x - 10, y, x + 5, y + 10)
        draw_line_midpoint(x - 10, y, x + 20, y)
        glEnd()
    
    elif button_type == 'playpause':
        glColor3f(1.0, 0.75, 0.0)  
        glBegin(GL_POINTS)
        if game_state == PLAYING:
            draw_line_midpoint(x-3,y-10,x-3,y+10)
            draw_line_midpoint(x+3,y-10,x+3,y+10)
        else:
            draw_line_midpoint(x-8,y-10,x-8,y+10)
            draw_line_midpoint(x-8,y+10,x+10,y)
            draw_line_midpoint(x-8,y-10,x+10,y)
        glEnd()
    
    elif button_type=='exit':
        glColor3f(1.0, 0.0, 0.0) 
        glBegin(GL_POINTS)
        draw_line_midpoint(x-8,y-8,x+8,y+8)
        draw_line_midpoint(x-8,y+8,x+8,y-8)
        glEnd()

def check_collision(diamond_x, diamond_y, diamond_size, catcher_x, catcher_y, catcher_width, catcher_height):
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top = diamond_y + diamond_size
    diamond_bottom = diamond_y - diamond_size
    
    catcher_left = catcher_x - catcher_width/2
    catcher_right = catcher_x + catcher_width/2
    catcher_top = catcher_y + catcher_height
    catcher_bottom = catcher_y
    
    return (diamond_left < catcher_right and diamond_right > catcher_left and diamond_bottom < catcher_top and diamond_top > catcher_bottom)

def spawn_new_diamond():
    global diamond_x, diamond_y, diamond_color, diamond_speed
    diamond_x = random.randint(diamond_size, WINDOW_WIDTH - diamond_size)
    diamond_y = WINDOW_HEIGHT + diamond_size
    diamond_color = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]
    
    if score > 0 and score % speed_increase_interval == 0:
        diamond_speed = base_speed + (score // speed_increase_interval) * 20

def restart_game():
    global game_state, score, diamond_speed, diamond_x, diamond_y, diamond_color
    game_state = PLAYING
    score = 0
    diamond_speed = base_speed
    spawn_new_diamond()
    print("Starting Over")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher(catcher_x, catcher_y, catcher_width, catcher_height, game_state == GAME_OVER)
    
    if game_state!=GAME_OVER:
        draw_diamond(diamond_x, diamond_y, diamond_size, diamond_color)    
    draw_button(buttons['restart']['x'],buttons['restart']['y'],'restart')
    draw_button(buttons['playpause']['x'],buttons['playpause']['y'],'playpause')
    draw_button(buttons['exit']['x'],buttons['exit']['y'],'exit')
    glutSwapBuffers()

def update(value):
    global diamond_y, game_state, score, last_time
    
    current_time=time.time()
    if last_time==0:
        last_time=current_time    
    delta_time=current_time - last_time
    last_time=current_time
    
    if game_state==PLAYING:
        diamond_y-=diamond_speed * delta_time
        
        if check_collision(diamond_x, diamond_y, diamond_size, catcher_x, catcher_y, catcher_width, catcher_height):
            score+=1
            print(f"Score: {score}")
            spawn_new_diamond()
        
        elif diamond_y < 0:
            game_state = GAME_OVER
            print(f"Game Over! Final Score: {score}")
    
    glutPostRedisplay()
    glutTimerFunc(int(1000/FPS), update, 0)

def keyboard(key, x, y):
    global catcher_x, game_state
    
    if game_state == PLAYING:
        if key == GLUT_KEY_LEFT:
            # Prevent moving past left boundary
            catcher_x = max(catcher_width/2, catcher_x - 15)
        elif key == GLUT_KEY_RIGHT:
            # Prevent moving past right boundary
            catcher_x = min(WINDOW_WIDTH - catcher_width/2, catcher_x + 15)

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = WINDOW_HEIGHT - y  
        
        for btn_name, btn_pos in buttons.items():
            if (abs(x - btn_pos['x']) < button_size and 
                abs(y - btn_pos['y']) < button_size):
                if btn_name == 'restart':
                    restart_game()
                elif btn_name == 'playpause':
                    toggle_pause()
                elif btn_name == 'exit':
                    print(f"Goodbye! Final Score: {score}")
                    glutLeaveMainLoop()

def toggle_pause():
    global game_state
    if game_state == PLAYING:
        game_state = PAUSED
    elif game_state == PAUSED:
        game_state = PLAYING
    elif game_state == GAME_OVER:
        restart_game()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def main():
    global last_time
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    
    init()
    spawn_new_diamond()
    last_time = time.time()
    
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)
    
    glutMainLoop()
if __name__ == "__main__":
    main()