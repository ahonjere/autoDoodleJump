from platform import platform

import time
import cv2
import numpy as np
import player
import dxcam

from matplotlib import pyplot as plt


DOODLE_WINDOW_SIZE = (560/1920, 850/1080)
CHROME_BANNER_SIZE = (1, 150/1080)

# (x_left, y_top, x_right, y_bottom)


PLAY_BUTTON_TEMPL = r".\templates\play_button.png"
CHAR_TEMPL = r".\templates\character.png"
PLATFORM_TEMPL = r".\templates\platform.png"
MOVING_PLATFORM_TEMPL = r".\templates\moving_platform.png"

SCALEFACTOR = 0.5
MOVING_TRESHOLDS = (0/1920*SCALEFACTOR, 200/1920*SCALEFACTOR)

CHAR_TEMPL = cv2.imread(CHAR_TEMPL)
CHAR_TEMPL = cv2.resize(CHAR_TEMPL, None, fx=SCALEFACTOR, fy=SCALEFACTOR)

PLATFORM_TEMPL = cv2.imread(PLATFORM_TEMPL)
PLATFORM_TEMPL = cv2.resize(PLATFORM_TEMPL, None, fx=SCALEFACTOR, fy=SCALEFACTOR)

MOVING_PLATFORM_TEMPL = cv2.imread(MOVING_PLATFORM_TEMPL)
# Draw captured game with recognized objects for debug purposes
def draw_game(gameFrame, charLoc, platformLocs):
    bottom_right = (charLoc[0] + CHAR_TEMPL.shape[0], charLoc[1] + CHAR_TEMPL.shape[1])
    
    cv2.rectangle(gameFrame,charLoc, bottom_right, 255, 2)
    cv2.rectangle(gameFrame, platformLocs[::-1], (platformLocs[1] + PLATFORM_TEMPL.shape[1], platformLocs[0] + PLATFORM_TEMPL.shape[0]), (0,0,255), 2)
    #for pt in zip(*platformLocs[::-1]):
    #    cv2.rectangle(gameFrame, pt, (pt[0] + PLATFORM_TEMPL.shape[1], pt[1] + PLATFORM_TEMPL.shape[0]), (0,0,255), 2)

    #gameFrame = cv2.cvtColor(gameFrame, cv2.COLOR_BGR2RGB)
    cv2.imshow("test", gameFrame)
    cv2.waitKey(1)


# Updates object locations. Gives top left corner.
def update_locations(gameFrame):
    res_char = cv2.matchTemplate(gameFrame, CHAR_TEMPL, cv2.TM_SQDIFF_NORMED)
    res_platform = cv2.matchTemplate(gameFrame, PLATFORM_TEMPL, cv2.TM_SQDIFF_NORMED)
    res_moving_platform = cv2.matchTemplate(gameFrame, MOVING_PLATFORM_TEMPL, cv2.TM_SQDIFF_NORMED)
    # Get min and max matches
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_char)
    
    # TM_SQDIFF_NORMED => best match is the minimum
    loc_char = min_loc
    loc_platform = np.array(np.where(res_platform <= 0.05))
    loc_moving_platform = np.array(np.where(res_moving_platform <= 0.05))

    if(len(loc_moving_platform != 0)):
        loc_platform[0] = np.append(loc_platform[0], loc_moving_platform[0])
        loc_platform[1] = np.append(loc_platform[1], loc_moving_platform[1])


    return loc_char, loc_platform


def update(gameFrame, char, draw=True):
    start = time.time_ns()
    
    #print("FrameGrab: {} ms".format((tok-start)/1000000))
    
    charLoc, platformLocs = update_locations(gameFrame)

    charLoc = np.array(charLoc)
    flying_path = char.updateLocation(charLoc)

    for point in zip(flying_path[0], flying_path[1]):
        point = (int(point[0]),int(point[1]))
        cv2.drawMarker(gameFrame, point, (255,0,0)) 

    highestReachable = (9999, 9999)
    
    if len(platformLocs) != 0:
        highestReachable = char.calculate_highest_under_flightpath(platformLocs)

    if(highestReachable[0] != 9999):
        cv2.rectangle(gameFrame, highestReachable[::-1], 
                    ((highestReachable[1] + PLATFORM_TEMPL.shape[1]), 
                    highestReachable[0] + PLATFORM_TEMPL.shape[0]), 
                    (0,255,0))

        print((highestReachable[1] + MOVING_TRESHOLDS[1]))
        cv2.rectangle(gameFrame, highestReachable[::-1], 
                    ((int(highestReachable[1] + MOVING_TRESHOLDS[1]*1920)), 
                    highestReachable[0] + 50), 
                    (255,0,0))
    
        char.move(highestReachable, MOVING_TRESHOLDS)

    if draw == True:
        draw_game(gameFrame, charLoc, highestReachable)
    
    stop_loop = time.time_ns()
    print("Time for one iteration: {} ms".format((stop_loop-start)/1000000))
    

def main():
    char = player.Player()
    camera = dxcam.create()
    screen_width = camera.width
    screen_height = camera.height

    gamewindow = (int((screen_width/2 - DOODLE_WINDOW_SIZE[0]/2*screen_width)), 
                    int((screen_height/2 - DOODLE_WINDOW_SIZE[1]/2*screen_height)), 
                    int((screen_width/2 + DOODLE_WINDOW_SIZE[0]/2*screen_width)), 
                    int((screen_height/2 + DOODLE_WINDOW_SIZE[1]/2*screen_height)))
    print(gamewindow)
    while True:
        gameFrame = camera.grab(region=gamewindow)

        if(gameFrame is None):
            continue
        else:
            gameFrame = cv2.cvtColor(gameFrame, cv2.COLOR_BGR2RGB)
            gameFrame = cv2.resize(gameFrame, None, fx=SCALEFACTOR, fy=SCALEFACTOR)
            update(gameFrame, char)


main()

