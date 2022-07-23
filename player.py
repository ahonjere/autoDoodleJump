from json.encoder import INFINITY
import numpy as np
import time

class Player:
    def __init__(self):
        # (x,y,time)

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

    def calcClosest(self, platformLocs):
        distance = platformLocs[0] - np.repeat(self.loc_[1], len(platformLocs[1]))
        i = -1 
        min = 99999
        min_idx = 0
        for dist in distance:
            i += 1
            if(dist < min and dist > 200):
                min = dist
                min_idx = i
        print(min)
        print(min_idx)
            
        #print(platformLocs)
        #print(self.loc_[1])
        
        return min_idx
 