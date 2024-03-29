# 6.00x Problem Set 7: Simulating robots

import math
import random

import ps7_visualize
import pylab

# For Python 2.7:
from ps7_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, comment out what's above and
# uncomment this line (for Python 2.6):
# from ps7_verify_movement26 import testRobotMovement

#added new comment

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.roomTiles = {}
        for x in range(self.width):
            for y in range(self.height):
                self.roomTiles[(x, y)] = 0
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.roomTiles[(int(math.floor(pos.getX())), int(math.floor(pos.getY())))] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.roomTiles[(m, n)] == 1 
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum(self.roomTiles.values())

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.uniform(0,self.width), random.uniform(0,self.height))
    
    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        check = (int(math.floor(pos.getX())), int(math.floor(pos.getY())))
        return check in self.roomTiles


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.position = self.room.getRandomPosition()
        self.direction = random.randrange(0,361)
        room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!
##room = RectangularRoom(4, 5)
##print room.getRandomPosition()
##position_test = Position(2.6, 2.1)
##print position_test
##print room.isPositionInRoom(position_test)
##print room.getRandomPosition()
##room.cleanTileAtPosition(position_test)
##print room.isTileCleaned(3,2)
##print room.isTileCleaned(2,2)
##print room.getNumCleanedTiles()
##print room.getNumTiles()
##et = Robot(room,4)
##print et.getRobotPosition()

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        
        if not self.room.isPositionInRoom(self.position.getNewPosition(self.direction,self.speed)):
            self.setRobotDirection(random.randrange(0,361)) 
        else:
            new_position= self.position.getNewPosition(self.direction,self.speed)
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(self.getRobotPosition())


# Uncomment this line to see your implementation of StandardRobot in action!
##testRobotMovement(StandardRobot, RectangularRoom)
##et2 =StandardRobot(room,3)
##et2.updatePositionAndClean()

# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    random.seed(0)
    def simRob(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
        anim = ps7_visualize.RobotVisualization(num_robots, width, height)
        
        def createRobot(simRoom, speed, robot_type):
            return robot_type(simRoom,speed)

        def groupRobots(num_robots, speed, simRoom, robot_type):

            allRobots= []
            for i in range(num_robots):
                allRobots.append(createRobot(simRoom,speed,robot_type))
            return allRobots

        def cleanFinished(simRoom, min_coverage):
            if min_coverage == 0:
                return False
            return float(simRoom.getNumCleanedTiles()) / float(simRoom.getNumTiles()) < min_coverage 

        simRoom = RectangularRoom(width, height)
        robots = groupRobots(num_robots, speed, simRoom, robot_type)        
        t = 0
        while cleanFinished(simRoom, min_coverage):
            t += 1
            anim.update(simRoom, robots)
            for i in robots:
                i.updatePositionAndClean()
        anim.done()
        return t

    def trialMean(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
        total_t = 0
        for i in range(num_trials):
            total_t += simRob(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type)
        return float(total_t) / num_trials
    
    return trialMean(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type)


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
##        self.setRobotDirection(random.randrange(0,361))
        angleDec = self.direction/360.0
        turn = 90
        turnDec = turn/360
        angleDec+turnDec*360
        
        self.setRobotDirection(int(round((((abs(((self.direction/360.0)+(1.0/10))-1))*360)),0)))
        print "this is current direction " + str(int(round((((abs(((self.direction/360.0)+(1.0/10))-1))*360)),0))) + ', this is new direction ' + str(self.direction)
        if not self.room.isPositionInRoom(self.position.getNewPosition(self.direction,self.speed)):
            self.setRobotDirection(random.randrange(0,361)) 
        else:
            new_position= self.position.getNewPosition(self.direction,self.speed)
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(self.getRobotPosition())

class turnRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def foo(self,x, y):
        if y +x > 360:
            return y+x - 360
        else:
            return y+x
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
         
        if not self.room.isPositionInRoom(self.position.getNewPosition(self.direction,self.speed)):
            self.setRobotDirection(self.foo(self.direction,115))
        else:
            new_position= self.position.getNewPosition(self.direction,self.speed)
            self.setRobotPosition(new_position)
            self.room.cleanTileAtPosition(self.getRobotPosition())
avg = runSimulation(50, 1, 50, 100, 0.5, 1, turnRobot)
avg2 = runSimulation(50, 1, 50, 100, 0.5, 1, StandardRobot)
print 'Turn robot = ' +str(avg)
print 'Standard robot = ' +str(avg2)
##def showPlot1(title, x_label, y_label):
##    """
##    What information does the plot produced by this function tell you?
##    """
##    num_robot_range = range(1, 11)
##    times1 = []
##    times2 = []
##    for num_robots in num_robot_range:
##        print "Plotting", num_robots, "robots..."
##        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
##        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
##    pylab.plot(num_robot_range, times1)
##    pylab.plot(num_robot_range, times2)
##    pylab.title(title)
##    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
##    pylab.xlabel(x_label)
##    pylab.ylabel(y_label)
##    pylab.show()
##
##showPlot1('title','x','y')
    
##def showPlot2(title, x_label, y_label):
##    """
##    What information does the plot produced by this function tell you?
##    """
##    aspect_ratios = []
##    times1 = []
##    times2 = []
##    for width in [10, 20, 25, 50]:
##        height = 300/width
##        print "Plotting cleaning time for a room of width:", width, "by height:", height
##        aspect_ratios.append(float(width) / height)
##        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
##        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
##    pylab.plot(aspect_ratios, times1)
##    pylab.plot(aspect_ratios, times2)
##    pylab.title(title)
##    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
##    pylab.xlabel(x_label)
##    pylab.ylabel(y_label)
##    pylab.show()
##    
##showPlot2('t','x','y')
# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
