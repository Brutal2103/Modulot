# Modulot
# Code: Peter Adams
# I made this game for the Commodore 64 in nov. 2017
# Check it out here: https://csdb.dk/release/?id=160647
#
# Now this is my first pygame (and python) project made in 2022.

from pickle import TRUE
import pygame
import random
import Levels

pygame.init()

# Setup
width,height = 600,600
screen = pygame.display.set_mode((width,height))
picture = pygame.image.load('images/chalkboard.jpg')
background = pygame.transform.scale(picture, (width, height))
instructions_font = pygame.font.Font('freesansbold.ttf', 16)
font = pygame.font.Font('font/FreeSansBold.ttf', 20)
font2 = pygame.font.Font('font/FreeSansBold.ttf',72)
font3 = pygame.font.Font('font/youmurderer-bb.regular.ttf',80)
font4 = pygame.font.Font('font/youmurderer-bb.regular.ttf',50)
font5 = pygame.font.Font('font/youmurderer-bb.regular.ttf',30)
pygame.display.set_caption('Modulot')

file = 'sound/Modulot_II.ogg'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.

# Variables
WHITE = (255,255,255)
GREEN = (51,102,0)
BLACK = (0,0,0)
RED = (255,0,0)
GREY1 = (150,150,150)
DGREY = (50,50,50)
GREY3 = (120,120,120)
modulot = 0
pos = 0
msg = ""
x = y = 50
change_x = 0
change_y = 0
current_level = 1
game_grid = []
mod_grid=[0]*256
mod_list =[]
green_boxes =[]
check_grid=[]
start_grid=[]
level_complete = 0
musicpaused = False
cheat_mode = False
time = Levels.TIME[current_level]
m=0
game_over = 0
score = 0

# Functions
def create_game_grid(current_level):
    game_grid.clear()
    for i in Levels.LEVEL[current_level]:
        if i == 0:
            game_grid.append(10)
        else:
            game_grid.append(random.randint(0,9))
    return game_grid

def create_check_grid():
    start_grid.clear()
    check_grid.clear()
    for i in game_grid:
        if i == 10:
            start_grid.append(0)
            check_grid.append(0)
        else:
            start_grid.append(1)
            check_grid.append(1)

    i=0
    while i < 256:
        if i ==0:
            check_grid[0] = start_grid[1]+start_grid[16]+start_grid[17]
        elif i == 15:
            check_grid[15] = start_grid[14]+start_grid[31]+start_grid[30]
        elif i == 240:
            check_grid[240] = start_grid[241]+start_grid[240-15]+start_grid[240-16]
        elif i == 255:
            check_grid[255] = start_grid[254]+start_grid[254-16]+start_grid[254-17]
        elif 0<i<15:
            check_grid[i] = start_grid[i-1]+start_grid[i+1]+start_grid[i+15]+start_grid[i+16]+start_grid[i+17]
        elif 240<i<255:
            check_grid[i] = start_grid[i-1]+start_grid[i+1]+start_grid[i-15]+start_grid[i-16]+start_grid[i-17]
        elif i>0 and i<240 and i % 16 == 0:
            check_grid[i] = start_grid[i+1]+start_grid[i-15]+start_grid[i-16]+start_grid[i+16]+start_grid[i+17]
        elif i>15 and i<255 and (i+1) % 16 == 0:
            check_grid[i] = start_grid[i-1]+start_grid[i-17]+start_grid[i-16]+start_grid[i+15]+start_grid[i+16]
        else:
            check_grid[i] = start_grid[i-1]+start_grid[i+1]+start_grid[i-17]+start_grid[i-16]+start_grid[i-15]+start_grid[i+15]+start_grid[i+16]+start_grid[i+17]
        i+=1

def create_mod_grid():
    i = 0
    while i < len(mod_grid):
        if game_grid[i] < 10:
            mod_grid[i]="."
        else:
            # hoeken
            if i==0:
                mod_grid[i] = (game_grid[i+1]+game_grid[i+16]+game_grid[i+17])
            elif i==15:
                mod_grid[i] = (game_grid[i-1]+game_grid[i+15]+game_grid[i+16])
            elif i==240:
                mod_grid[i] = (game_grid[i+1]+game_grid[i-15]+game_grid[i-16])
            elif i==255:
                mod_grid[i] = (game_grid[i-1]+game_grid[i-16]+game_grid[i-17])
            # bovenste rij
            elif 0<i<15: 
                mod_grid[i] = (game_grid[i-1]+game_grid[i+1]+game_grid[i+15]+game_grid[i+16]+game_grid[i+17])
            # onderste rij
            elif 240<i<255:
                mod_grid[i] = (game_grid[i-1]+game_grid[i+1]+game_grid[i-15]+game_grid[i-16]+game_grid[i-17])
            # rij links
            elif i>0 and i<240 and i % 16 == 0:
                mod_grid[i] = (game_grid[i-16]+game_grid[i-15]+game_grid[i+1]+game_grid[i+16]+game_grid[i+17]) 
            # rij rechts
            elif i>15 and i<255 and (i+1) % 16 == 0:
                mod_grid[i] = (game_grid[i-16]+game_grid[i-17]+game_grid[i-1]+game_grid[i+15]+game_grid[i+16])
            else:
                mod_grid[i] = (game_grid[i-1]+game_grid[i+1]+game_grid[i-17]+game_grid[i-16]+game_grid[i-15]+game_grid[i+15]+game_grid[i+16]+game_grid[i+17])
        i+=1
    for i in range(0,256):
        if mod_grid[i] == ".":
            mod_grid[i] = "."
        elif mod_grid[i]%10 == 0 and check_grid[i] == 0:
            mod_grid[i] = "."
        else:
            mod_grid[i] %=10

    return mod_grid

def draw_box():
    global x,y
    if x > 425:
        x = 50
    elif x <50:
        x = 425    
    if y > 425:
        y = 50
    elif y < 50:
        y = 425
    pygame.draw.rect(screen,WHITE,pygame.Rect(x+1,y+1,24,24),2)
  
    calculate_position()
    if pos == 0:
        green_boxes = [pos+1,pos+16,pos+17]
    elif pos == 15:
        green_boxes = [pos-1,pos+15,pos+16]
    elif pos == 240:
        green_boxes = [pos+1,pos-15,pos-16]
    elif pos == 255:
        green_boxes = [pos-1,pos-16,pos-17]
    elif 0<pos<15:
        green_boxes = [pos-1,pos+1,pos+15,pos+16,pos+17]
    elif 240<pos<255:
        green_boxes = [pos-1,pos+1,pos-15,pos-16,pos-17]
    elif 0<pos<240 and pos % 16 == 0:
        green_boxes = [pos+1,pos-15,pos-16,pos+16,pos+17]
    elif 15<pos<255 and (pos+1) % 16 == 0:
        green_boxes = [pos-1,pos-16,pos-17,pos+15,pos+16]
    else:
        green_boxes = [pos-1,pos+1,pos-15,pos-16,pos-17,pos+15,pos+16,pos+17]
    
    for i in green_boxes:
        if game_grid[i] != 10:
            pygame.draw.rect(screen,GREEN,pygame.Rect(52+(i%16)*25,52+(i//16)*25,23,23))

def update_pos():
    global x, y, change_x, change_y
    x += change_x
    y += change_y

def draw_numbers(grid,color):    
    y=0
    for i in range(0,256,16):
        x=0
        for j in range(0,16):
            if grid[i+j] == 10 or grid[i+j] == ".":
                nr = ""
            else:
                nr = str(grid[i+j])        
            number = font.render(nr, TRUE, color)
            screen.blit(number, (x+57, y+50))
            x+=25        
        y+=25

def draw_numbers2(grid,color):    
    y=0
    for i in range(0,256,16):
        x=0
        for j in range(0,16):
            if grid[i+j] == ".":
                nr = ""
            else:
                nr = str(grid[i+j])        
            number = font.render(nr, TRUE, color)
            screen.blit(number, (x+57, y+50))
            x+=25        
        y+=25

def create_mod():
    global modulot
    global mod_list
    global level_complete
    mod_list = list(set(mod_grid))
    mod_list.remove('.')
    mod_list.sort()
    if not mod_list:
        level_complete = 1
    else:
        modulot = mod_list[random.randint(0,len(mod_list)-1)]

def draw_modulot():
    global level_complete
    pygame.draw.rect(screen,GREEN,pygame.Rect(460,50,100,100),10)
    if level_complete == 0:
        number = font2.render(str(modulot), TRUE, WHITE)
        screen.blit(number, (490, 55))
    else:
        number = font2.render(" ", TRUE, WHITE)
        screen.blit(number, (490, 65))
        
def calculate_position():
    global pos
    pos = int(((y-50)/25)*16+((x-50)/25))

def what_to_do_now(pos):
    global msg,time,score
    if game_grid[pos] == 10:
        if mod_grid[pos] !='.':
            if mod_grid[pos] == modulot: 
                msg = "OKAY !"
                time += check_grid[pos]*2
                score += check_grid[pos]*5
                update_game_grid(pos)
                update_mod()
            else:
                msg = "WHOEPS!"
                time -=1
                game_grid[pos] = modulot
                update_mod()
        else:
            msg = "WRONG!"
            time -=1
            game_grid[pos] = modulot
            update_mod()
    else:
        msg = "DUH !"

def update_game_grid(x):
    if x == 0:
        game_grid[x+1] = game_grid[x+16] = game_grid[x+17] = 10
    elif x == 15:
        game_grid[x-1] = game_grid[x+15] = game_grid[x+16] = 10
    elif x == 240:
        game_grid[x+1] = game_grid[x-15] = game_grid[x-16] = 10
    elif x == 255:
        game_grid[x-1] = game_grid[x-16] = game_grid[x-17] = 10
    elif 0<x<15:
        game_grid[x-1]=game_grid[x+1]=game_grid[x+15]=game_grid[x+16]=game_grid[x+17]=10
    elif 240<x<255:
        game_grid[x-1]=game_grid[x+1]=game_grid[x-17]=game_grid[x-16]=game_grid[x-15]=10
    elif 0<pos<240 and pos % 16 == 0:
        game_grid[x-16]=game_grid[x-15]=game_grid[x+1]=game_grid[x+16]=game_grid[x+17]=10
    elif 15<pos<255 and (pos+1) % 16 == 0:
        game_grid[x-16]=game_grid[x-17]=game_grid[x-1]=game_grid[x+15]=game_grid[x+16]=10
    else:
        game_grid[x-17]=game_grid[x-16]=game_grid[x-15]=game_grid[x-1]=game_grid[x+1]=game_grid[x+15]=game_grid[x+16]=game_grid[x+17]=10

def draw_message(msg):
    message = font4.render(msg, TRUE, WHITE)
    screen.blit(message, (460, 150))

def draw_title():
    Titeltext = ["MODULOT","by","Peter Adams","Music by Aldo Chiummo (m to pause)","Help & Support: Jarne Dirken","(c) 2022"]
    screen.blit(font3.render(Titeltext[0], TRUE, BLACK), (146,451))
    screen.blit(font3.render(Titeltext[0], TRUE, GREY3), (145,450))
    screen.blit(font3.render(Titeltext[2], TRUE, BLACK), (96,491))
    screen.blit(font3.render(Titeltext[2], TRUE, GREY3), (95,490))
    screen.blit(font4.render(Titeltext[1], TRUE, BLACK), (228,491)) 
    screen.blit(font4.render(Titeltext[1], TRUE, RED), (227,490))
    screen.blit(font5.render(Titeltext[3], TRUE, BLACK), (91,551))   
    screen.blit(font5.render(Titeltext[3], TRUE, RED), (90,550))
    screen.blit(font5.render(Titeltext[4], TRUE, BLACK), (121,571))
    screen.blit(font5.render(Titeltext[4], TRUE, GREY3), (120,570)) 

def draw_grid():
    for i in range (1,16):
        pygame.draw.line(screen,DGREY,(50+i*25,50),(50+i*25,450),1)
        pygame.draw.line(screen,DGREY,(50,50+i*25),(450,50+i*25),1)
    pygame.draw.rect(screen,WHITE,pygame.Rect(50,50,25*16,25*16),1)

def draw_level(current_level):
    screen.blit(font.render("Level: "+ str(current_level).zfill(2), TRUE, WHITE), (360,20))

def draw_time(time):        
    screen.blit(font.render("Time: "+ str(time).zfill(2)+" sec.", TRUE, WHITE), (200,20))

def draw_score():
    screen.blit(font.render("Score: "+str(score).zfill(6),TRUE,WHITE),(50,20))

def instructions():
    #yy = 475
    yy = 100
    xx = 55
    i = 24
    screen.blit(instructions_font.render("Use arrow keys to move the little white square.", TRUE, WHITE), (xx,yy+i*0))
    screen.blit(instructions_font.render("If the sum of the surrounding numbers ends with", TRUE, WHITE), (xx,yy+i*1))
    screen.blit(instructions_font.render("the big white number in the green square, ", TRUE, WHITE), (xx,yy+i*2))
    screen.blit(instructions_font.render("press Right CTRL to delete those numbers. ", TRUE, WHITE), (xx,yy+i*3))
    screen.blit(instructions_font.render("But if you got it wrong, the number will be added ", TRUE, WHITE), (xx,yy+i*4))
    screen.blit(instructions_font.render("to the grid ! Clear the grid before time ends!", TRUE, WHITE), (xx,yy+i*5))
    screen.blit(instructions_font.render("Press SPACE to pause the game and view", TRUE, WHITE), (xx,yy+i*7))
    screen.blit(instructions_font.render("instructions again.", TRUE, WHITE), (xx,yy+i*8))
    screen.blit(instructions_font.render("Now move to continue and have fun !", TRUE, WHITE), (xx,yy+i*10))

def toggle_music():
        global musicpaused
        if musicpaused:
            pygame.mixer.music.unpause()
            musicpaused = False
        else:
            pygame.mixer.music.pause()
            musicpaused = True

def toggle_cheat():
    global cheat,cheat_mode
    if cheat_mode:
        cheat = 1
        cheat_mode = False
    else:
        cheat = 0
        cheat_mode = True

def update_time():
    global time,m,game_over
    if time <= 0:
        game_over = 1
    m -=1
    if m == -10:
        m = 0
        time -= 1

def update_mod():
    create_check_grid()
    #write(check_grid,"check.txt")
    create_mod_grid()
    #write(mod_grid,"mod.txt")
    create_mod()

def write(grid,file):
    f = open(file, "w")
    for i in range(0,256,16):
        for j in range(0,16):
            f.write(str(grid[i+j])+";")
        f.write("\n")
    f.close()

create_game_grid(current_level)
#write(game_grid,"game.txt")
update_mod()

# ===============================================================================================
def main():
    global current_level, msg, x, y, level_complete, musicpaused,change_x, change_y,time,score,game_over, cheat_mode,cheat
    
    # flags
    key_pressed = 0
    update_mod = 0
    instructions_on = 1
    movement = 0
    game_over = 0
    cheat_mode = 0
    cheat = 0
 
    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                   change_y = 25
                   key_pressed = 1
                elif event.key == pygame.K_UP:
                    change_y = -25
                    key_pressed = 1
                elif event.key == pygame.K_RIGHT:
                    change_x = 25
                    key_pressed = 1
                elif event.key == pygame.K_LEFT:  
                    change_x = -25
                    key_pressed = 1
                elif event.key == pygame.K_RCTRL:
                    update_mod = 1
                elif event.key == pygame.K_SPACE and game_over ==0:
                    instructions_on = 1
                elif event.key == pygame.K_m:
                    toggle_music()
                elif event.key == pygame.K_p and game_over == 1:
                    current_level = 0
                    level_complete = 1
                    instructions_on = 1
                elif event.key == pygame.K_c:
                    toggle_cheat()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_UP):
                    change_y =  0
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    change_x =  0
                elif event.key == pygame.K_p and game_over ==1:
                    game_over = 0
                    score = 0
                    x = y = 50
                                      
        if movement == 1:
            update_pos()
            if cheat == 0:
                update_time()

        if key_pressed == 1:
            msg = ""
            key_pressed = 0
            instructions_on = 0
            movement = 1

        if update_mod == 1:
            calculate_position()
            what_to_do_now(pos)
            draw_message(msg)
            update_mod = 0

        if level_complete == 1:
            current_level +=1
            if current_level > len(Levels.LEVEL)-1:
                current_level = 1
            level_complete =0
            score += time
            time = Levels.TIME[current_level]
            x=y=50
            create_game_grid(current_level)
            create_check_grid()
            create_mod_grid()
            create_mod()
           
        
        screen.blit(background,(0,0))
        draw_grid()

        if game_over == 0:
            draw_level(current_level)
            draw_time(time)
            draw_score()
            draw_box()
            draw_numbers(game_grid,WHITE)
            if cheat == 1:
                screen.blit(font4.render("CHEATER !",TRUE,BLACK),(451,201))
                screen.blit(font4.render("CHEATER !",TRUE,RED),(450,200))
                draw_numbers2(mod_grid,GREY3)
            draw_modulot()
            draw_message(msg)
        
        draw_title()
        
        if game_over == 1:
            screen.blit(font3.render("Time's up !",TRUE,WHITE),(125,200))
            screen.blit(font3.render("GAME OVER", TRUE, RED), (125,225))
            screen.blit(font5.render("Your Score: "+str(score),TRUE,WHITE),(175,300))
            screen.blit(font5.render("Press P to play again",TRUE,WHITE),(150,350))

        if instructions_on ==1:
            draw_numbers(game_grid,DGREY)
            instructions()
            movement = 0
            
        # Update the display
        pygame.display.update()
        clock.tick(10)
    # Done! Time to quit.
    pygame.quit()

# If the name of the file == main -> run main()
if __name__ == '__main__':
    main()