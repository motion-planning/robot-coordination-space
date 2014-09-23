# Takes as input the obstacles and trajectory of a robot from the MSL library
# http://msl.cs.uiuc.edu/msl/

import heapq
import itertools
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # @UnresolvedImport @UnusedImport


### Input Parameters ###
obstacleFilename = '2robotObstacles.txt'  # obstacles generated by MSL (remove trailing empty lines)
policyFilename = '2robotPolicies.txt'  # policy generated by MSL
robotSize = 1  # radius of robots, assumes robots are circular

### Global Variables ###

# Obstacles
obstacles = []

# Robots
# Each robot is represented by a trajectory
# Each trajectory is composed of a series of states
# Each state is composed of ([0] velocity, [1] x-coordinate, [2] y-coordinate, [3] orientation [0-2pi),
robots = []

# Coordination space
cSpace = []

### Functions ###

# Read files and split data by line
def readFile (filename):
    info = []
    with open(filename, 'r') as openFile:
        data = openFile.readlines()
        for line in data:
            info.append(line.split())
    return info

# Extract obstacles
def extractObstacles(info):
    # Each obstacle is a set of points on a line
    for line in info:
        points = []
        # Iterate over all points and add them to an array representing the obstacle
        for endpoint in line:
            point = []
            x, y = map(float, endpoint.strip('()').split(','))
            point.append(float(x))
            point.append(float(y))
            points.append(point)
        obstacles.append(points)

# Extract policy of each robot
def extractPolicies(info):
    for line in info:
        vs = line[0::4]  # velocities (every 4th element starting from 0)
        vs = [float(i) for i in vs]
        xs = line[1::4]  # x-coordinates (every 4th element starting from 1)
        xs = [float(i) for i in xs]
        ys = line[2::4]  # y-coordinates (every 4th element starting from 2)
        ys = [float(i) for i in ys]
        thetas = line[3::4]  # angles (every 4th element starting from 3)
        thetas = [float(i) for i in thetas]

        trajectory = []
        state = [vs[0], xs[0], ys[0], thetas[0], True]  # Assemble initial safe state
        trajectory.append(state)

        for i in range(1, len(vs)):  # Iterate over all other cases
            state = [vs[i], xs[i], ys[i], thetas[i]]  # Assemble each state
            trajectory.append(state)  # Append to create trajectory for each robot
        robots.append(trajectory)  # Add each robot trajectory to list of robots

# Define Coordination Space
def createMatrix():
    # Array holding the size of each dimension (given by number of states for each robot)
    n = []
    for robot in robots:
        n.append(len(robot))
    return createCoordinationSpace(n, 0, [])

# Recursively build n-dimensional array of ints, which represents the Coordination Space
# Input parameters are:
# n (array representing the size of each dimension),
# depth (the current dimension being generated)
# configuration (array representing the current set of states being generated/evaluated)
def createCoordinationSpace(n, depth, configuration):
    # Base case
    # Create the "last" dimensions for the nth robot
    # 0 if no collision, 1 if any robot in that state collides with any other robot in the same state
    if depth == len(n) - 1:
        array = []
        for i in xrange(0, n[depth]):
            configuration.append(i)
            # s = state, given by the position in configuration;
            collision = False
            # Check all collisions in the current state
            for A1 in range(len(configuration)):  # Loop through all states of robots A1, A2
                if collision == False:  # Prevent unnecessary loops
                    for A2 in range(A1 + 1, len(configuration)):
                            if checkCollisions(A1, configuration[A1], A2, configuration[A2]):
                                collision = True
            if collision:
                array.append([1, 0, 0, 0, [0, 0]])
            else:
                array.append([0, 0, 0, 0, [0, 0]])
            configuration.pop()  # Remove configuration that was just checked
        return array

    # Recursive case
    else:
        array = []
        # Recursively call function for each element in each dimension
        for i in xrange(0, n[depth]):
            # Add current dimension being generated to configuration
            configuration.append(i)
            array.append(createCoordinationSpace(n, depth + 1, configuration))
            configuration.pop()
        return array

# Check for collisions between two robots
def checkCollisions(A1, s1, A2, s2):
    # Treats each robot as a circle, and checks for an overlap between two circles
    # (if distance between circles is less than 2r)
    if ((robots[A1][s1][1] - robots[A2][s2][1]) ** 2 +
        (robots[A1][s1][2] - robots[A2][s2][2]) ** 2) ** 0.5 < 2 * robotSize:
        return True
    else:
        return False

# Plot the trajectories of each robot
def plotPaths():
    # Iterate over every state of every robot
    for idx, robot in enumerate(robots):
        xs = []
        ys = []
        for state in robot:
            xs.append(state[1])
            ys.append(state[2])
        plt.plot(xs, ys, label='Robot: ' + str(idx))

    # Iterate over every point in every obstacle
    for polygon in obstacles:
        polygon.append(polygon[0])
        xs = []
        ys = []
        for i in range(len(polygon)):
            xs.append(polygon[i][0])
            ys.append(polygon[i][1])
        plt.plot(xs, ys)

    plt.suptitle('Paths')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

# Plot the 2D Coordination Space
def plot2DCoordinationSpace():
    xs = []
    ys = []

    # Iterate over every combination of states in Coordination Space
    for x in range(len(cSpace)):
        for y in range(len(cSpace[0])):
            if cSpace[x][y][0] == 1:
                xs.append(x)
                ys.append(y)

    plt.scatter(xs, ys, color='blue')

    plt.xlim([0, len(cSpace)])
    plt.ylim([0, len(cSpace[0])])

    plt.suptitle('2D Coordination Space')
    plt.xlabel('Robot 1')
    plt.ylabel('Robot 2')
    plt.show()

# Plot the 3D Coordination Space
def plot3DCoordinationSpace():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = []
    ys = []
    zs = []

    # Iterate over every combination of states in Coordination Space
    for x in range(len(cSpace)):
        for y in range(len(cSpace[x])):
            for z in range(len(cSpace[x][y])):
                if cSpace[x][y][z][0] == 1:
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)

    ax.scatter(xs, ys, zs)
    ax.set_xlim3d(0, len(cSpace))
    ax.set_ylim3d(0, len(cSpace[0]))
    ax.set_zlim3d(0, len(cSpace[0][0]))

    plt.suptitle('3D Coordination Space')
    xLabel = ax.set_xlabel('Robot 1')
    yLabel = ax.set_ylabel('Robot 2')
    zLabel = ax.set_zlabel('Robot 3')
    plt.show()

def plotCSpace():
    if len(robots) == 2:
        plot2DCoordinationSpace()
    elif len(robots) == 3:
        plot3DCoordinationSpace()

# Return the length of the trajectory of a robot
def findTrajectoryLength(robot):
    trajectoryLength = 0
    prevX = robots[robot][0][1]
    prevY = robots[robot][0][2]

    # Iterate over all states and find the Euclidean distance between the two points
    # Return the sum of all of these distances
    for state in robots[robot]:  # This is going to check the 1st state against itself, which gives 0
        currX = state[1]
        currY = state[2]
        trajectoryLength += math.sqrt((currX - prevX) ** 2 + (currY - prevY) ** 2)
        prevX = currX
        prevY = currY
    return trajectoryLength

# TODO: this does a lot of the same work as findTrajectoryLength and can be combined
# TODO: this can also be combined with extractPolicies
def normalizeTrajectory(robot):
    time = 0.5  # Time interval between robot updates
    trajectoryLength = findTrajectoryLength(robot)

    # Interval length is given by floor of (length of trajectory / (robot speed * update interval time))
    intervals = math.floor(trajectoryLength / (robots[robot][0][0] * time))
    intervalLength = trajectoryLength / intervals  # length of each interval between updates
    distOldStates = 0
    distNewStates = 0

    prevX = robots[robot][0][1]
    prevY = robots[robot][0][2]

    newTrajectory = []

    for state in robots[robot]:
        currX = state[1]
        currY = state[2]
        distOldStates += math.sqrt((currX - prevX) ** 2 + (currY - prevY) ** 2)

        # For every state in robot trajectory, iterate
        # If distance between the current state and the start is larger than the
        # distance between the current normalized state and the start
        # then add the corresponding new state to the new normalized trajectory to "catch up" and
        # increase the distance of the new trajectory by one interval
        # then check again to see if another "new state" lies in the original interval
        while distOldStates > distNewStates:
            dX = currX - prevX
            dY = currY - prevY

            length = math.sqrt(dX ** 2 + dY ** 2)

            dX /= length
            dY /= length

            # Find the % of length that must be added to the new state starting from the last valid original state
            distance = distOldStates - distNewStates
            addDiff = length - distance

            dX *= addDiff
            dY *= addDiff

            newX = prevX + dX
            newY = prevY + dY

            newTrajectory.append([state[0], newX, newY, state[3]])
            distNewStates += intervalLength
        prevX = currX
        prevY = currY
    return newTrajectory

def normalizeAllTrajectories():
    for robot in range(len(robots)):
        robots[robot] = normalizeTrajectory(robot)

# Find the distance between two points in 2D space
# def distTwoPointsIn3D(x1, y1, z1, x2, y2, z2):
def distTwoPointsIn3D(x1, y1, x2, y2):
    xd = x2 - x1
    yd = y2 - y1
#     zd = z2 - z1
#     return math.sqrt(xd ** 2 + yd ** 2 + zd ** 2)
    return math.sqrt(xd ** 2 + yd ** 2)

# Estimated cost, distance from point to goal
# Hard-coded tester for 2D space
# point is a list with the x, y, z coordinates
def costToGo(point):
    x1 = point[0]
    y1 = point[1]
    # z1 = point[2]
    x2 = len(cSpace)
    y2 = len(cSpace[0])
    # z2 = len(cSpace[0][0])
    # return distTwoPointsIn3D(x1, y1, z1, x2, y2, z2)
    return distTwoPointsIn3D(x1, y1, x2, y2)

# Find the neighbors of a point
# def findNeighbors(x, y, z, radius):
#     return [[[cSpace[i][j][k]
#         if  i >= 0 and i < len(cSpace)
#         and j >= 0 and j < len(cSpace[0])
#         and k >= 0 and k < len(cSpace[0][0])
#         else 0
#         for j in range(y - 1 - radius, y + radius)]
#         for i in range(x - 1 - radius, x + radius)]
#         for k in range(z - 1 - radius, z + radius)]

# Find the neighbors of a point
def findNeighbors(point):
    combinations = []
    for d in point:
        combinations.append([d - 1, d, d + 1])
    neighbors = map(list, list(itertools.product(*combinations)))

    # Check if neighbor is parent or occupied
    newNeighbors = []
    for neighbor in neighbors:
        if neighbor[0] >= 0 and neighbor[0] < len(cSpace) and neighbor[1] >= 0 and neighbor[1] < len(cSpace[0]):
            if neighbor != point and cSpace[neighbor[0]][neighbor[1]] != 1:
                newNeighbors.append(neighbor)
    return newNeighbors

def skipSuccessor(list, successor):
    for node in list:
        if node[5] == successor[5]:
            if node[3] <= successor[3]:
                return True
    return False

def aStarSearch():
    # Nodes are:
    # 0: state
    # 1: g
    # 2: h
    # 3: f
    # 4: parent
    # 5: [x, y]

    openList = []
    closedList = []
    node = cSpace[0][0]
    node.append([0, 0])
    heapq.heappush(openList, node)

    while openList:
        q = heapq.heappop(openList)
        for successor in findNeighbors(q[5]):
            if successor[0] == len(cSpace) - 1 and successor[1] == len(cSpace[0]) - 1:
                return successor
            g = q[1] + 1
            h = costToGo(successor)
            successor = [cSpace[successor[0]][successor[1]][0], g, h, g + h, q[5], successor]

            if not skipSuccessor(openList, successor) and not skipSuccessor(closedList, successor):
                heapq.heappush(openList, successor)
        heapq.heappush(closedList, q)

    return "could not find path"

def addPath(parent):
    while parent[5] != [0, 0]:
        print parent
        cSpace[parent[5[0]]][parent[5[1]]][0] = 2
        parent = parent[4]

### Required Function Calls ####
extractObstacles(readFile(obstacleFilename))
extractPolicies(readFile(policyFilename))
normalizeAllTrajectories()
cSpace = createMatrix()
parent = aStarSearch()
addPath(parent)

### Optional Function Calls Here ###
# plotPaths()
# plotCSpace()

