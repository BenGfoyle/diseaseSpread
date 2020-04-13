"""
@author: BenGfoyle
@overview: Use random motion to measure disease spread over time.
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import random as rn
import numpy as np

numInfected = 1000
numSusceptible = 10000
maxMove = 0.1
infChance = 0.5
infRadius = 0.01
lethal = 0.05
testAccuracy = 0
#===============================================================================
class person:
    """
    Overview: Define a person in the simulation
    """
    def __init__(self, role, xPos, yPos):
        """
        Each person in simulation has a role: infected, susceptible, removed.
        If removed: Cannot Spead. Cannot Contract.
        If susceptivle: Cannot Spread. Can Contract
        If Infected: Can Spread. Cannot Contract
        """
        self.role = role
        self.xPos = xPos #Position in xPlane
        self.yPos = yPos #Position in yPlane

#===============================================================================

#===============================================================================
def makePlot(x,y,plotName):
    """
    Overview: Make scatter plot of two parameters.
    """
    plt.ylabel("Number of People")
    plt.xlabel("Days")
    plt.plot(x,y,label = plotName)
#===============================================================================

#===============================================================================
def socialDistance():
    """
    Overview: Accounts for person staying a distance away from another.
    """
    return
#===============================================================================

#===============================================================================
def quaranteen():
    """
    Overview: Remove certain parties from the population.
    """
    return
#===============================================================================

#===============================================================================
def population():
    """
    Overview: Define population breakdown. Always starts with 0 recovered
    """
    infPop = [person("Infected",rn.random(),rn.random()) for i in range(0,numInfected)]
    susPop = [person("Susceptible",rn.random(),rn.random()) for i in range(0,numSusceptible)]
    simulation(infPop,susPop,maxMove,infChance,infRadius)
#===============================================================================

#===============================================================================
def contract(sxPos,syPos,infPop, infChance, infRadius):
    """
    Overview: Check surrounding area for infected memebrs. If in range, chance
    to get infected.
    """
    distance = lambda x,y: np.sqrt((x - sxPos)**2 + (y - syPos)**2)
    for i in infPop:
        if distance(i.xPos,i.yPos) <= infRadius:
            if rn.random() <= infChance:
                return True
#===============================================================================

#===============================================================================
def simulation(infPop,susPop,maxMove,infChance,infRadius):
    """
    Overview: Simulate disease spread until population is cured, or dead.
    Population exiats in a box size 1 x 1. Max movement per person dictated by
    maxMove parameter.
    """
    day = 1
    dead = []
    removed = []
    infPopSize = [len(infPop)]
    susPopSize = [len(susPop)]
    deadPopSize = [0]
    remPopSize = [0]
    outOfBounds = lambda coord: 1 if coord > 1 else (0 if coord < 0 else coord)
    while (infPopSize[-1] > 0):
        for i in infPop:
            if rn.random() <= testAccuracy: #check if medical tests show posative
                removed.append(i)
                infPop.remove(i)
            elif rn.random() <= lethal: #check if perosn dies to disease
                dead.append(i)
                infPop.remove(i)
            else:
                i.xPos = i.xPos + rn.uniform(-maxMove,maxMove)
                i.yPos = i.yPos + rn.uniform(-maxMove,maxMove)
                i.xPos = outOfBounds(i.xPos)
                i.yPos = outOfBounds(i.yPos)

        for s in susPop:
            s.xPos = s.xPos + rn.uniform(-maxMove,maxMove)
            s.yPos = s.yPos + rn.uniform(-maxMove,maxMove)
            s.xPos = outOfBounds(s.xPos)
            s.yPos = outOfBounds(s.yPos)
            if contract(s.xPos, s.yPos, infPop, infChance, infRadius):
                infPop.append(s)
                susPop.remove(s)
        infPopSize.append(len(infPop))
        susPopSize.append(len(susPop))
        remPopSize.append(len(removed))
        deadPopSize.append(len(dead))

        day += 1

    initalParameters = "Initial Infected:"+str(numInfected)+\
    "\nInitial Susceptible:"+str(numSusceptible)+\
    "\nMax Movement per day:"+str(maxMove)+\
    "\nInfection Chance:"+str(infChance)+\
    "\nInfection Radius:"+str(infRadius)+\
    "\nLethality:"+str(lethal)+\
    "\nMedical Test Accuracy"+str(testAccuracy)


    makePlot([x for x in range(1,day+1)], infPopSize,"#Infected")
    makePlot([x for x in range(1,day+1)], susPopSize,"#Susceptible")
    makePlot([x for x in range(1,day+1)], remPopSize,"#Recovered")
    makePlot([x for x in range(1,day+1)], deadPopSize,"#Dead")
    plt.annotate(initalParameters,(0,50))
    plt.legend()
    plt.grid()
    plt.show()
#===============================================================================
population()
