import airsim
import os

from shutil import copy2
airsim_dir = os.path.dirname(airsim.__file__)
file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
copy2(dir_path+"\\client.py", airsim_dir)
copy2(dir_path+"\\types.py", airsim_dir)


