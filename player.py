from json.encoder import INFINITY
import numpy as np
import time
import random
from pynput import mouse, keyboard
from matplotlib import pyplot as plt

# How many pixels under the characters top left corner
# the closest platform below has to be
PIX_BELOW_CHAR = 0*0.25
GRAVITY = 500

class Player:
    def __init__(self):
        # (x,y,time)
        self.keyboard_ = keyboard.Controller()
        self.mouse_ = mouse.Controller()
        self.loc_ = np.array([[0,0,0],[0,0,0],[0,0,0]])

        self.speed_ = np.array([0,0,0])
        self.prevSpeed_  = np.array([0,0,0])
        self.accel_ = np.array([0,0,0])
        self.idx_ = 0
        self.prev_time_s_ = 1
        self.curr_time_s_ = 1.0001
        self.flightpath_ = np.array([])
        self.highestReachable_ = np.array([9999,9999])

    def calculate_flight_path(self):
        t = np.linspace(0,1,100)
        x = self.loc_[0][0] + self.speed_[0]*t
        y = (self.loc_[0][1] + (self.speed_[1] + GRAVITY*t)*t)
        return(np.array([x,y]))

    # Update new observation. Returns estimated flight path.
    def updateLocation(self, loc):
        self.prev_time_s_ = self.curr_time_s_
        self.curr_time_s_ = time.time_ns()/1000000000
        
        self.loc_[2] = self.loc_[1]
        self.loc_[1] = self.loc_[0]
        
        self.loc_[0][0] = loc[0]
        self.loc_[0][1] = loc[1]
        #self.loc_[0][2] = curr_time_s
        #print(self.loc_)
        self.prevSpeed_ = self.speed_
        self.speed_ = np.hstack(((self.loc_[0][0:2]-self.loc_[1][0:2])/(self.curr_time_s_-self.prev_time_s_), self.curr_time_s_))
        
        self.accel_ = np.hstack(((self.speed_[0:2] - self.prevSpeed_[0:2])/(self.speed_[2]-self.prevSpeed_[2])))
        
        self.flightpath_ = self.calculate_flight_path()

        return self.flightpath_
        

    def getLocation(self):
        return self.loc_[0:1]
    

    def getSpeed(self):
        return self.speed_[0:1]

    def getFlightPath(self):
        return self.flightpath_

    def calcClosestBelow(self, platformLocs):
        distance = platformLocs[0] - np.repeat(self.loc_[0][1], len(platformLocs[1]))
        i = -1 
        min = 99999
        min_idx = 0
        for dist in distance:
            i += 1
            if(dist < min and dist > PIX_BELOW_CHAR):
                min = dist
                min_idx = i
        return min_idx


    def move(self, target):
        smallestDist = 9999        
        # Calc closest point in flight path
        for point in zip(self.flightpath_[0], self.flightpath_[1]):
            point = np.array(point)
            target = np.array(target)
            dist = np.linalg.norm(point - target[::-1])
            if (dist < smallestDist):
                closestPoint = point
        #print("diffX: {}".format(diffX))
        
        diffX = self.loc_[0][0] - target[1]
        
        if(diffX < -20*0.25):
            print("Move right")
            self.keyboard_.release(keyboard.Key.left)
            self.keyboard_.press(keyboard.Key.right)

        elif diffX > 200*0.25:
            print("Move left")
            self.keyboard_.release(keyboard.Key.right)
            self.keyboard_.press(keyboard.Key.left)
        else:
            print("Stop moving")
            self.keyboard_.release(keyboard.Key.right)
            self.keyboard_.release(keyboard.Key.left)

    def shoot(self, enemy):
        enemyFromChar = self.loc_[0:2] - enemy
        #if (enemyFromChar[1] < -50):
        #    self.mouse_.move(np.array([660,107]) + enemy)
        #    self.mouse_.click(mouse.Button.left)

    def calculate_highest_under_flightpath(self, platformLocs):
        
        highestPointOnPathIdx = np.argmin(self.flightpath_[1,:])
        highestPointOnPath = self.flightpath_[:,highestPointOnPathIdx]
        highestPointOnPath[1] += PIX_BELOW_CHAR # Add treshold to make sure it is reachable
        reachable = []
        self.highestReachable_ = (9999,9999)
        for platform in zip(platformLocs[0], platformLocs[1]):
            
            if (platform[0] > highestPointOnPath[1]):
                if(platform[0] < self.highestReachable_[0]):
                    self.highestReachable_ = platform
                    
        return self.highestReachable_
        

    