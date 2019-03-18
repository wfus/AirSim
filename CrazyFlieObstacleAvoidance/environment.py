"""Environment control class for the Crazyflie Obstacle Avoidance Challenge.
We will need to manipulate the gameobjects in the environment.
    Path: AirSim/Unreal/Environments/CrazyFlieObstacleDemo
"""
import airsim

DRONE_ID = 'BP_FlyingPawn-1'

class ObstacleEnvironment(object):
    """Takes in the current airsim client connected to the current obstacle
    avoidance demo environment, and provides functions to control the obstacles
    and have them move toward the crazyflie."""
    def __init__(self, client):
        self.obstacles = ['Obstacle1', 'Obstacle2'] 

    def move_obstacle(self, obstacle):
        """Gets a random obstacle and moves it for a few seconds"""
        
        return


if __name__ == '__main__':
    pass