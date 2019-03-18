"""Environment control class for the Crazyflie Obstacle Avoidance Challenge.
We will need to manipulate the gameobjects in the environment.
    Path: AirSim/Unreal/Environments/CrazyFlieObstacleDemo
"""
import airsim
import numpy as np
import threading
import time
import copy

DRONE_ID = 'BP_FlyingPawn-1'

class ObstacleEnvironment(object):
    """Takes in the current airsim client connected to the current obstacle
    avoidance demo environment, and provides functions to control the obstacles
    and have them move toward the crazyflie."""
    def __init__(self, client):
        self.obstacles = ['Obstacle1', 'Obstacle2'] 
        self.c = client


    def _move_obstacle_thread(self, obj_id, pos_start, pos_end, dur):
        """Takes a tuple of object_id, start_pose, end_pose, and duration and
        turns this into smooth movement manually."""
        pos_curr = copy.deepcopy(pos_start)
        time_start = time.time()
        print("Trying to move %s" % obj_id)
        while time.time() - time_start < dur:
            time_diff = time.time() - time_start
            diff = (pos_end.position - pos_start.position) * time_diff / float(dur)
            pos_curr.position = diff + pos_start.position
            print("Moving to position %s" % str(pos_curr.position))
            succ = self.c.simSetObjectPose(obj_id, pos_curr, teleport=True)
            time.sleep(0.1)
        return


    def move_obstacle(self):
        """Gets a random obstacle and moves it for a few seconds"""
        obstacle_id = np.random.choice(self.obstacles)
        pose1 = self.c.simGetObjectPose(obstacle_id)
        pose2 = copy.deepcopy(pose1)
        pose2.position = pose1.position + airsim.Vector3r(20, 20, 20)
        thread = threading.Thread(target=self._move_obstacle_thread,
                                  args=(obstacle_id, pose1, pose2, 5.0))
        thread.start()
        

if __name__ == '__main__':
    c = airsim.MultirotorClient()
    c.confirmConnection()
    c.enableApiControl(True)

    a = ObstacleEnvironment(c)
    a.move_obstacle()
