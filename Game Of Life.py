import pygame
import time



#COLORS
BLACK = "#000000"
WHITE = "#ffffff"
TRANSPARENT_GREY = (127,127,127,127)



#PYGAME SETUP
screen_width = 1520
screen_height = 855
screen_size = (screen_width,screen_height)
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
FPS = 144



def Sign(number):
    if number > 0: return 1
    if number < 0: return -1
    if number == 0: return 0

def BlockGridder(position_on_screen,window_size,z,camera_position):
    grid_position = [0,0]
    position = [0,0]
    position[0] = camera_position[0] - window_size[0]//2 + position_on_screen[0]
    position[1] = camera_position[1] - window_size[1]//2 + position_on_screen[1]
    block_size = window_size[0] // z
    grid_position[0] = (position[0] + block_size/2*Sign(position[0]))*Sign(position[0])//block_size*Sign(position[0])
    grid_position[1] = (position[1] + block_size/2*Sign(position[1]))*Sign(position[1])//block_size*Sign(position[1])
    return grid_position

def BlockRect(window_size,z,camera_position,block_grid_position):
    width = window_size[0]//z
    block_position = [block_grid_position[0]*width,block_grid_position[1]*width]
    zero = [camera_position[0]-window_size[0]//2,camera_position[1]-window_size[1]//2]
    position = [block_position[0]-zero[0],block_position[1]-zero[1]]
    rect = pygame.Rect(position[0]-width//2,position[1]-width//2,width,width)
    return rect

def ConvertToPos(window_size,zoom,grid_position):
    width = window_size[0]//zoom
    position = [grid_position[0]*width,grid_position[1]*width]
    return position


blocks_x_y = {}
zoom = 10
position = [0,0]
keys = {"w":False,"a":False,"s":False,"d":False,"q":False,"e":False}
speed = 10
acceleration = .1
timer_speed = 50

#MAIN LOOP
mode = "edit"
while mode != "exit":



    #====---- GAME EDIT ----====#
    #Pre Code
    if mode == "edit":
        #Main Loop
        while mode == "edit":
            #/////////////////
            clock.tick(FPS)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mode = "exit"

                #UPDATE KEYS
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_w: keys["w"] = not keys["w"]
                    if event.key == pygame.K_a: keys["a"] = not keys["a"]
                    if event.key == pygame.K_s: keys["s"] = not keys["s"]
                    if event.key == pygame.K_d: keys["d"] = not keys["d"]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE: mode = "play"

                #ADD OR TAKE BLOCKS FROM GRID
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    block = BlockGridder(pygame.mouse.get_pos(),screen_size,zoom,position)
                    if not (block[0] in blocks_x_y.keys()):
                        blocks_x_y[block[0]] = []
                        blocks_x_y[block[0]].append(block[1])
                    elif not (block[1] in blocks_x_y[block[0]]):
                        blocks_x_y[block[0]].append(block[1])
                    else:
                        blocks_x_y[block[0]].remove(block[1])
                        if len(blocks_x_y[block[0]]) == 0: 
                            blocks_x_y.pop(block[0])

                #UPDATES ZOOM
                if event.type == pygame.MOUSEWHEEL:
                    center = BlockGridder((screen_width//2,screen_height//2),screen_size,zoom,position)
                    zoom -= event.y*4
                    if zoom < 6: zoom = 6
                    position = ConvertToPos(screen_size,zoom,center)


            #UPDATE MOVEMENT
            position[0] += (keys["d"] - keys["a"]) * speed
            position[1] += (keys["s"] - keys["w"]) * speed


            screen.fill(BLACK)

            mouse = pygame.mouse.get_pos()

            for x in blocks_x_y.keys():
                for y in blocks_x_y[x]:
                    pygame.draw.rect(screen,WHITE,BlockRect(screen_size,zoom,position,[x,y]))

            pygame.display.flip()
            #/////////////////




    #====---- GAMEPLAY ----====#
    #Pre Code
    if mode == "play":
        blocks_x_y_copy = blocks_x_y
        timer = 0
        print("Ticks needed:", timer_speed)
        #Main Loop
        while mode == "play":
            #/////////////////
            clock.tick(FPS)

            blocks_x_y_count = {}

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mode = "exit"

                #UPDATE KEYS
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_w: keys["w"] = not keys["w"]
                    if event.key == pygame.K_a: keys["a"] = not keys["a"]
                    if event.key == pygame.K_s: keys["s"] = not keys["s"]
                    if event.key == pygame.K_d: keys["d"] = not keys["d"]
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e: 
                            print("Ticks needed:", timer_speed)
                            timer_speed += 1
                        elif event.key == pygame.K_q: 
                            print("Ticks needed:", timer_speed)
                            timer_speed -= 1
                            if(timer_speed < 1): timer_speed = 1
                        if event.key == pygame.K_SPACE: mode = "edit"

                #UPDATES ZOOM
                if event.type == pygame.MOUSEWHEEL:
                    center = BlockGridder((screen_width//2,screen_height//2),screen_size,zoom,position)
                    zoom -= event.y*2
                    if zoom < 6: zoom = 6
                    position = ConvertToPos(screen_size,zoom,center)


            #UPDATE MOVEMENT
            position[0] += (keys["d"] - keys["a"]) * speed
            position[1] += (keys["s"] - keys["w"]) * speed

            #UPDATE TIMER
            
            timer -= 1
            if timer <= 0:
                for x in blocks_x_y_copy.keys():
                    for y in blocks_x_y_copy[x]:
                        for x2 in range(int(x)-1,int(x)+2,1):
                            for y2 in range(int(y)-1,int(y)+2,1):
                                if not (int(x) == x2 and int(y) == y2):
                                    if not(x2 in blocks_x_y_count.keys()):
                                        blocks_x_y_count[x2] = {}
                                        blocks_x_y_count[x2][y2] = 1
                                    elif not (y2 in blocks_x_y_count[x2].keys()):
                                        blocks_x_y_count[x2][y2] = 1
                                    else:
                                        blocks_x_y_count[x2][y2] = blocks_x_y_count[x2][y2] + 1
                listToRemove = []
                for x in blocks_x_y_copy.keys():
                    for y in blocks_x_y_copy[x]:
                        if (not (x in blocks_x_y_count.keys())) or (not (y in blocks_x_y_count[x].keys())):
                            listToRemove.append([x,y])
                for i in listToRemove:
                    blocks_x_y_copy[i[0]].remove(i[1])
                    if len(blocks_x_y_copy[i[0]]) == 0:
                        blocks_x_y_copy.pop(i[0])

                for x in blocks_x_y_count.keys():
                    for y in blocks_x_y_count[x].keys():
                        if (x in blocks_x_y_copy.keys()) and (y in blocks_x_y_copy[x]):
                            if blocks_x_y_count[x][y] < 2 or blocks_x_y_count[x][y] > 3:
                                blocks_x_y_copy[x].remove(y)
                                if len(blocks_x_y_copy[x]) == 0:
                                    blocks_x_y_copy.pop(x)
                        else:
                            if blocks_x_y_count[x][y] == 3:
                                if not (x in blocks_x_y_copy.keys()):
                                    blocks_x_y_copy[x] = []
                                    blocks_x_y_copy[x].append(y)
                                else:
                                    blocks_x_y_copy[x].append(y)

                timer = timer_speed

            screen.fill(BLACK)

            mouse = pygame.mouse.get_pos()

            for x in blocks_x_y_copy.keys():
                for y in blocks_x_y_copy[x]:
                    pygame.draw.rect(screen,WHITE,BlockRect(screen_size,zoom,position,[x,y]))

            pygame.display.flip()
            #/////////////////