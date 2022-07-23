import pyautogui as auto
import time
import cv2
import numpy as np
from PIL import ImageGrab
from matplotlib import pyplot as plt

# (x_left, y_top, x_right, y_bottom)
GAMEWINDOW = (660,107,1260,1000)
PLAY_BUTTON_TEMPL = r".\templates\play_button.png"
CHAR_TEMPL = r".\templates\character.png"
PLATFORM_TEMPL = r".\templates\platform.png"
CHAR_TEMPL = cv2.imread(CHAR_TEMPL)
CHAR_TEMPL = CHAR_TEMPL[...,::-1]
PLATFORM_TEMPL = cv2.imread(PLATFORM_TEMPL)
PLATFORM_TEMPL = PLATFORM_TEMPL[...,::-1]


def start_game():
    play_button = auto.locateOnScreen(PLAY_BUTTON_TEMPL)
    print(play_button)
    if play_button:
        auto.click(play_button)
    print("Game Started!")


# Updates object locations
def update_locations(gameFrame):
    
    res = cv2.matchTemplate(gameFrame, CHAR_TEMPL, cv2.TM_SQDIFF_NORMED)
    res2 = cv2.matchTemplate(gameFrame, PLATFORM_TEMPL, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    loc_platform = np.where(res2 <= 0.15)
    return min_loc, loc_platform


# Draw captured game with recognized objects
def draw_game(gameFrame, charLoc, platformLocs):
    bottom_right = (charLoc[0] + CHAR_TEMPL.shape[0], charLoc[1] + CHAR_TEMPL.shape[1])
    cv2.rectangle(gameFrame,charLoc, bottom_right, 255, 2)
    for pt in zip(*platformLocs[::-1]):
        cv2.rectangle(gameFrame, pt, (pt[0] + PLATFORM_TEMPL.shape[1], pt[1] + PLATFORM_TEMPL.shape[0]), (0,0,255), 2)
    cv2.imshow("test", gameFrame)
    cv2.waitKey(1)
    

def main():
    while True:
        start = time.time_ns()
        gameFrame = np.array(ImageGrab.grab(bbox=GAMEWINDOW))
        charLoc, platformLocs = update_locations(gameFrame)
        draw_game(gameFrame, charLoc, platformLocs)
        stop = time.time_ns()
        print("Time elapsed for one loop: {} ms".format((stop-start)/1000000))

main()

