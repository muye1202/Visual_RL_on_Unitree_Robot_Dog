from rclpy.node import Node
from a1_hardware.control_loop_execution.rl_policy_wrapper import PolicyWrapper
from a1_hardware.control_loop_execution.main_executor import Executor
from a1_hardware.a1_utilities.robot_controller import RobotController
from a1_hardware.a1_utilities.realsense import A1RealSense
from a1_hardware.a1_utilities.a1_sensor_process import *
import pickle
import torch
import torchrl.networks.nets as networks
import torchrl.policies as policies
from torchrl.utils import get_params
import glob
import os
import rclpy
import sys


PARAM_PATH = "/home/muyejia1202/final_project/vision4leg/config/mpc/locotransformer/thin_goal.json"
NORM_PATH = "/home/muyejia1202/final_project/archive/data.pkl"

params = get_params(PARAM_PATH)
with open(NORM_PATH, 'rb') as f:
    obs_normalizer = pickle.load(f)
params['net']['activation_func'] = torch.nn.ReLU
obs_normalizer_mean = obs_normalizer._mean
obs_normalizer_var = obs_normalizer._var
get_image_interval = 4    #params['env']['env_build']['get_image_interval']
num_action_repeat = params['env']['env_build']['num_action_repeat']

params['net']['base_type'] = networks.base.MLPBase
encoder = networks.base.LocoTransformerEncoder(
    in_channels=4,
    state_input_dim=84,
    **params["encoder"]
)

pf = policies.GaussianContPolicyLocoTransformer(
    encoder=encoder,
    state_input_shape=84,
    visual_input_shape=(4, 64, 64),
    output_shape=6,
    **params["net"],
    **params["policy"]
).to("cuda:0")

policyComputer = PolicyWrapper(
    pf, 
    obs_normalizer_mean, 
    obs_normalizer_var, 
    get_image_interval, 
    save_dir_name=None,
    no_tensor=True,
    action_range=[0.05, 0.5, 0.5]
)

class deploy_policy(Node):
    
    def __init__(self):
        super().__init__("deploy_policy")
        
        
def main(args=None):
    rclpy.init(args=args)
    robot_pub = deploy_policy()
    rclpy.spin(robot_pub)
    rclpy.shutdown()


if __name__ == '__main__':
    main()