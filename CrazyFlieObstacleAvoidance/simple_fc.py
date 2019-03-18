import airsim
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
from models_torch import SimpleFCDQN
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def action2motion(action, speed=0.25):
    """Turns an action from our fully connected net and turns it into movement.
    Assumes discrete actions space as an integer. Turns it into X, Y, Z
    velocities corresponding to our specific drone."""
    action_dict = {
        0: (0, 0, 0),
        1: (speed, 0, 0),
        2: (0, speed, 0),
        3: (-speed, 0, 0),
        4: (0, -speed, 0),
    }
    try:
        return action_dict[action]
    except KeyError:
        raise RuntimeError("Could not convert discrete action into movement.")

def compute_reward(quad_state, quad_vel, collision_info):
    if collision_info.has_collided:
        reward = -100
    
    return reward


if __name__ == '__main__':
    a = airsim.MultirotorClient()
    a.confirmConnection()
    a.enableApiControl(True)
    a.armDisarm(True)
    
    for _ in range(2):
        a.reset()
        a.confirmConnection()
        a.enableApiControl(True)
        a.armDisarm(True)
        a.takeoffAsync().join()
        for _ in range(100):
            a.moveByVelocityAsync(2.0, 0, 0, 5)
            time.sleep(0.5)
            a.moveByVelocityAsync(-2.0, 0, 0, 5)
            time.sleep(0.5)

        collision_info = client.simGetCollisionInfo()
        if collision_info.has_collided:
            print("WE HIT SOMETHING!@@@")

