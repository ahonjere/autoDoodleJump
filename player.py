from json.encoder import INFINITY
import numpy as np
import time
from pynput.keyboard import Key, Controller

# How many pixels under the characters top left corner
# the closest platform below has to be
PIX_BELOW_CHAR = 200*0.25
class Player:
    def __init__(self):
        # (x,y,time)
        self.keyboard_ = Controller()
        self.loc_ = np.array([0,0,0])
        self.prevLoc_ = np.array([0,0,0])
        self.speed_ = np.array([0,0,0])
        self.prevSpeed_  = np.array([0,0,0])
        self.accel_ = np.array([0,0,0])


    def updateLocation(self, loc):
        curr_time_s = time.time_ns()/1000000000
        #print(curr_time_s)
        self.prevLoc_ = self.loc_
        self.loc_ = np.array([loc[0], loc[1], curr_time_s])
        #print(self.loc_)
        self.prevSpeed_ = self.speed_
        self.speed_ = np.hstack(((self.loc_[0:2]-self.prevLoc_[0:2])/(self.loc_[2]-self.prevLoc_[2]), curr_time_s))
        
        self.accel_ = np.hstack(((self.speed_[0:2] - self.prevSpeed_[0:2])/(self.speed_[2]-self.prevSpeed_[2])))


    def getLocation(self):
        return self.loc_[0:1]
    

    def getSpeed(self):
        return self.speed_[0:1]


    def calcClosestBelow(self, platformLocs):
        distance = platformLocs[0] - np.repeat(self.loc_[1], len(platformLocs[1]))
        i = -1 
        min = 99999
        min_idx = 0
        for dist in distance:
            i += 1
            if(dist < min and dist > PIX_BELOW_CHAR):
                min = dist
                min_idx = i
        return min_idx


    def move(self, closestBelow):
        diffX = self.loc_[0] - closestBelow[0]
        print("diffX: {}".format(diffX))
        
        if(diffX < 20*0.25):
            self.keyboard_.press(Key.right)

        elif diffX > 200*0.25:
            self.keyboard_.press(Key.left)
        else:
            self.keyboard_.release(Key.right)
            self.keyboard_.release(Key.left)

    