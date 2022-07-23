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

def startGame():
    play_button = auto.locateOnScreen(PLAY_BUTTON_TEMPL)
    print(play_button)
    if play_button:
        auto.click(play_button)
    print("Game Started!")

def updateLocations():
    res = cv2.matchTemplate(img2,CHAR_TEMPL,cv2.TM_SQDIFF_NORMED)
    res2 = cv2.matchTemplate(img2,PLATFORM_TEMPL,cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    loc_platform = np.where(res2 <= 0.15)
    return min_loc, loc_platform

#print("Sleeping...")
#time.sleep(2)
#print("Sleep Over!")
#startGame()


w, h = CHAR_TEMPL.shape[0:2]
w2, h2 = PLATFORM_TEMPL.shape[0:2]

while True:
    start = time.time_ns()
    frame = ImageGrab.grab(bbox=GAMEWINDOW)
    frame_np = np.array(frame)
    

    img2 = frame_np.copy()
    
    top_left, platform_loc = updateLocations()

    for pt in zip(*platform_loc[::-1]):
        cv2.rectangle(img2, pt, (pt[0] + h2, pt[1] + w2), (0,0,255), 2)
        

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum


    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img2,top_left, bottom_right, 255, 2)
    
    cv2.imshow("test",img2)
    cv2.waitKey(1)
    
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)
    # plt.show()
    stop = time.time_ns()
    print("Time elapsed: {} ms".format((stop-start)/1000000))

