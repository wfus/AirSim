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
        self.obstacle_pos = dict()
        self.original_pos = dict()
        self.c = client
        self.moving_objects = 0
        self.resetting = False

        # Get the original positions of all the obstacles to reset it later
        for obj_id in self.obstacles:
            self.original_pos[obj_id] = self.c.simGetObjectPose(obj_id)

    def reset(self):
        """Reset all objects to original state"""
        for obj_id, pose in self.original_pos.items():
            self.c.simSetObjectPose(obj_id, pose, teleport=True)
        
        self.resetting = True
        while self.moving_objects > 0:
            print("Polling until all environment threads done to reset.")
            pass
        self.resetting = False
        self.obstacle_pos = dict()
        

    def _move_obstacle_thread(self, obj_id, pos_start, pos_end, dur):
        """Takes a tuple of object_id, start_pose, end_pose, and duration and
        turns this into smooth movement manually. Unfortunately, airsim is
        very not thread safe, so we'll actually just use this thread to update
        where our object SHOULD be and then have a tick function that updates"""
        pos_curr = copy.deepcopy(pos_start)
        time_start = time.time()
        self.moving_objects += 1
        while time.time() - time_start < dur:
            time_diff = time.time() - time_start
            diff = (pos_end.position - pos_start.position) * time_diff / float(dur)
            pos_curr.position = diff + pos_start.position
            # Store where the obstacle should be in a dictionary.
            self.obstacle_pos[obj_id] = pos_curr
            if self.resetting:
                break
        self.moving_objects -= 1
    
    def tick(self):
        """Actually moves the obstacles to where they should be. We need this
        in our main loop since airsim will die if you run the obstacle movement
        on its own thread due to tornado"""
        for obstacle_id, pose in self.obstacle_pos.items():
            self.c.simSetObjectPose(obstacle_id, pose, teleport=False)

    def move_obstacle(self):
        """Gets a random obstacle and moves it for a few seconds. Since we are
        moving with collisions turned on, make SURE that your the obstacle
        you are moving isn't touching another obstacle."""
        obstacle_id = np.random.choice(self.obstacles)
        pose1 = self.c.simGetObjectPose(obstacle_id)
        pose2 = copy.deepcopy(pose1)
        dx, dy = np.random.uniform(-20, 20), np.random.uniform(-20, 20)
        pose2.position = pose1.position + airsim.Vector3r(dx, dy, 0)
        thread = threading.Thread(target=self._move_obstacle_thread,
                                  args=(obstacle_id, pose1, pose2, 5.0))
        thread.start()
    
    def move_obstacle_at_drone(self, speed=1.0):
        pos_drone = self.c.getMultirotorState().kinematics_estimated.position
        x, y = pos_drone.x_val, pos_drone.y_val
        print("Drone currently at coords %s" % str((x, y)))
        obstacle_id = np.random.choice(self.obstacles)
        pose1 = self.c.simGetObjectPose(obstacle_id)
        pose2 = copy.deepcopy(pose1)
        pose2.position = pose1.position + (airsim.Vector3r(x, y, 0) - pose1.position) * 2
        dist = pose1.position.distance_to(pose2.position)
        thread = threading.Thread(target=self._move_obstacle_thread,
                                  args=(obstacle_id, pose1, pose2, dist / speed))
        thread.start()
    
    def _distance_from_object(self, x, y, object_id):
        """Finds distance away from specific object id.
            @param x (float): x location of the drone
            @param y (float): y location of the drone
            @param object_id (str): obstacle_id, a string
        """
        pose1 = self.c.simGetObjectPose(object_id)
        obj_x, obj_y = pose1.position.x_val, pose1.position.y_val
        return ((obj_x - x) ** 2 + (obj_y - y) ** 2) ** 0.5
        
    def distance_from_nearest_object(self):
        """Calculates distance of drone from nearest object"""
        pos_drone = self.c.getMultirotorState().kinematics_estimated.position
        x, y = pos_drone.x_val, pos_drone.y_val
        return min([self._distance_from_object(x, y, obj_id) for obj_id in self.obstacles])


if __name__ == '__main__':
    c = airsim.MultirotorClient()
    c.confirmConnection()
    c.enableApiControl(True)
    c.takeoffAsync().join()

    a = ObstacleEnvironment(c)
    a.move_obstacle_at_drone()
