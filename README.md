# Visual-Policy Deployment on Real Unitree GO1 Robot Dog
* This project used the following two packages: `unitree_ros2` and `vision4leg`
* The [unitree_ros2](https://github.com/katie-hughes/unitree_ros2) package comes from Katie Hughes and Nick Morales.
* The [Vision4Leg](https://github.com/Mehooz/vision4leg) package comes from Mehooz, the official implementation for the paper [Learning Vision-Guided Quadrupedal Locomotion End-to-End with Cross-Modal Transformers](https://arxiv.org/abs/2107.03996) and [Vision-Guided Quadrupedal Locomotion in the Wild with Multi-Modal Delay Randomization](https://arxiv.org/abs/2109.14549).

## Notes
The execution loop is called in execute_locotransformer.py →executor.execute(EXECUTION_TIME)
“Execute” function is defined in control_loop_execution.main_executor
In main_executor.execute function: main_execution function is called, this is where robot states, camera frames, and actions are computed; Then in the main_execution function, command is computed and sent using a robot interface
The robot_controller thread is started in main_executor.execute function so command can be sent; after starting the thread robot_controller.control_function is called which starts a loop to repeatedly sending computed command