from platform import platform
import pyautogui
import time
import cv2
import numpy as np
import player
import dxcam
from PIL import ImageGrab
from matplotlib import pyplot as plt

# (x_left, y_top, x_right, y_bottom)
GAMEWINDOW = (660,107,1260,1000)
PLAY_BUTTON_TEMPL = r".\templates\play_button.png"
CHAR_TEMPL = r".\templates\character.png"
PLATFORM_TEMPL = r".\templates\platform.png"

SCALEFACTOR = 0.5
CHAR_TEMPL = cv2.imread(CHAR_TEMPL)
CHAR_TEMPL = cv2.resize(CHAR_TEMPL, None, fx=SCALEFACTOR, fy=SCALEFACTOR)
PLATFORM_TEMPL = cv2.imread(PLATFORM_TEMPL)
PLATFORM_TEMPL = cv2.resize(PLATFORM_TEMPL, None, fx=SCALEFACTOR, fy=SCALEFACTOR)

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
    
    # Get min and max matches
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_char)
    
    # TM_SQDIFF_NORMED => best match is the minimum
    loc_char = min_loc
    loc_platform = np.array(np.where(res_platform <= 0.05))
    

    return loc_char, loc_platform


def start_game():
    play_button = pyautogui.locateOnScreen(PLAY_BUTTON_TEMPL)
    print(play_button)
    if play_button:
        pyautogui.click(play_button)
    print("Game Started!")

 

def main():
    char = player.Player()
    camera = dxcam.create()
    while True:
        start = time.time_ns()
        gameFrame = camera.grab(region=GAMEWINDOW)
        if(gameFrame is None):
            continue
        else:
            gameFrame = cv2.cvtColor(gameFrame, cv2.COLOR_BGR2RGB)
            gameFrame = cv2.resize(gameFrame, None, fx=SCALEFACTOR, fy=SCALEFACTOR)
        
            #print("FrameGrab: {} ms".format((tok-start)/1000000))
            charLoc, platformLocs = update_locations(gameFrame)

            
            stop_locations = time.time_ns()
            
            # As locating stuff takes the most time, lets use the time 
            # it takes as an estimation of dt
            # Maybe not needed
            est_time_ms = (stop_locations - start)/1000000000

            #draw_game(gameFrame, charLoc, platformLocs)
            
            charLoc = np.array(charLoc)
            
            char.updateLocation(charLoc)#, est_time_ms/1000)
            if len(platformLocs[0]) != 0:
                closestIdx = char.calcClosestBelow(platformLocs)
                closest = np.array(platformLocs[:,closestIdx])
                char.move(closest)
                draw_game(gameFrame, charLoc, closest)
            
            stop_loop = time.time_ns()
            print("Time for one iteration: {} ms".format((stop_loop-start)/1000000))
        

main()

