import pyautogui as py
import math
import random
'''
This file will consist of util functions to make PyAutoGUI easier to use for our purposes
as well as add inherent randomness to mouse movements and clicks to throw off bot detection
'''
py.FAILSAFE = False
py.PAUSE = 0.05

def toPercent(absx,absy):
    screenWidth, screenHeight = py.size()
    relx =  round(100*absx/screenWidth, 2)
    rely = round(100*absy/screenHeight, 2)
    return relx, rely

def toAbs(relx, rely):
    screenWidth, screenHeight = py.size()
    absx = int(round(relx*screenWidth/100, 0))
    absy = int(round(rely*screenHeight/100, 0))
    return absx, absy

def position():
    return py.position()


#random movement towards point
def moveTo(x,y):
    currx, curry = position()
    deltax = x - currx
    deltay = y - curry

    screenWidth, screenHeight = py.size()
    c = math.sqrt(screenWidth**2+screenHeight**2) #diagonal length
    diagonal = math.sqrt(deltax**2+deltay**2) #diagonal to move
    mindur, maxdur = 0.005, 0.015
    xInc = abs(deltax)//13
    xVar = abs(deltax)//60
    yInc = abs(deltay)//13
    yVar = abs(deltay)//60


    if diagonal < 0.1*c:
        mindur, maxdur = 0.002, 0.004
        xInc = abs(deltax)//3
        xVar = abs(deltax)//30
        yInc = abs(deltay)//3
        yVar = abs(deltay)//30
    elif diagonal < 0.25*c:
        mindur, maxdur = 0.004, 0.006
        xInc = abs(deltax)//5
        xVar = abs(deltax)//38
        yInc = abs(deltay)//5
        yVar = abs(deltay)//38
    elif diagonal < 0.45*c:
        mindur, maxdur = 0.006, 0.008
        xInc = abs(deltax)//8
        xVar = abs(deltax)//45
        yInc = abs(deltay)//8
        yVar = abs(deltay)//45
    elif diagonal < 0.65*c:
        mindur, maxdur = 0.008, 0.01
        xInc = abs(deltax)//9
        xVar = abs(deltax)//50
        yInc = abs(deltay)//9
        yVar = abs(deltay)//50
    elif diagonal < 0.85*c:
        mindur, maxdur = 0.01, 0.012
        xInc = abs(deltax)//10
        xVar = abs(deltax)//60
        yInc = abs(deltay)//10
        yVar = abs(deltay)//60
    else:
        mindur, maxdur = 0.012, 0.014
        xInc = abs(deltax)//11
        xVar = abs(deltax)//60
        yInc = abs(deltay)//11
        yVar = abs(deltay)//60


    while currx != x or curry != y:
        xToGo, yToGo = currx, curry
        if currx != x:
            if currx < x:
                if xInc + xVar >= x-currx: #we may jump over it so just go to it
                    xToGo = x
                else:
                    xToGo = currx + xInc + random.randint(0, xVar)
            else:
                if xInc + xVar >= abs(x-currx): #we may jump over it so just go to it
                    xToGo = x
                else:   
                    xToGo = currx - xInc - random.randint(0, xVar)
        
        if curry != y:
            if curry < y:
                if yInc + yVar >= y-curry: #we may jump over it so just go to it
                    yToGo = y
                else:
                    yToGo = curry + yInc + random.randint(0, yVar)
            else:
                if yInc + yVar >= abs(y-curry): #we may jump over it so just go to it
                    yToGo = y
                else:   
                    yToGo = curry - yInc - random.randint(0, yVar)

        
        py.moveTo(xToGo, yToGo, random.uniform(mindur,maxdur))
        currx, curry = position()
    
    return

def moveToPercent(x,y):
    x,y = toAbs(x,y)
    currx, curry = position()
    deltax = x - currx
    deltay = y - curry

    screenWidth, screenHeight = py.size()
    c = math.sqrt(screenWidth**2+screenHeight**2) #diagonal length
    diagonal = math.sqrt(deltax**2+deltay**2) #diagonal to move
    mindur, maxdur = 0.005, 0.015
    xInc = abs(deltax)//13
    xVar = abs(deltax)//60
    yInc = abs(deltay)//13
    yVar = abs(deltay)//60


    if diagonal < 0.1*c:
        mindur, maxdur = 0.002, 0.004
        xInc = abs(deltax)//3
        xVar = abs(deltax)//30
        yInc = abs(deltay)//3
        yVar = abs(deltay)//30
    elif diagonal < 0.25*c:
        mindur, maxdur = 0.004, 0.006
        xInc = abs(deltax)//5
        xVar = abs(deltax)//38
        yInc = abs(deltay)//5
        yVar = abs(deltay)//38
    elif diagonal < 0.45*c:
        mindur, maxdur = 0.006, 0.008
        xInc = abs(deltax)//8
        xVar = abs(deltax)//45
        yInc = abs(deltay)//8
        yVar = abs(deltay)//45
    elif diagonal < 0.65*c:
        mindur, maxdur = 0.008, 0.01
        xInc = abs(deltax)//9
        xVar = abs(deltax)//50
        yInc = abs(deltay)//9
        yVar = abs(deltay)//50
    elif diagonal < 0.85*c:
        mindur, maxdur = 0.01, 0.012
        xInc = abs(deltax)//10
        xVar = abs(deltax)//60
        yInc = abs(deltay)//10
        yVar = abs(deltay)//60
    else:
        mindur, maxdur = 0.012, 0.014
        xInc = abs(deltax)//11
        xVar = abs(deltax)//60
        yInc = abs(deltay)//11
        yVar = abs(deltay)//60


    while currx != x or curry != y:
        xToGo, yToGo = currx, curry
        if currx != x:
            if currx < x:
                if xInc + xVar >= x-currx: #we may jump over it so just go to it
                    xToGo = x
                else:
                    xToGo = currx + xInc + random.randint(0, xVar)
            else:
                if xInc + xVar >= abs(x-currx): #we may jump over it so just go to it
                    xToGo = x
                else:   
                    xToGo = currx - xInc - random.randint(0, xVar)
        
        if curry != y:
            if curry < y:
                if yInc + yVar >= y-curry: #we may jump over it so just go to it
                    yToGo = y
                else:
                    yToGo = curry + yInc + random.randint(0, yVar)
            else:
                if yInc + yVar >= abs(y-curry): #we may jump over it so just go to it
                    yToGo = y
                else:   
                    yToGo = curry - yInc - random.randint(0, yVar)

        
        py.moveTo(xToGo, yToGo, random.uniform(mindur,maxdur))
        currx, curry = position()
    
    return



moveTo(2000, 100)
moveToPercent(99,50)