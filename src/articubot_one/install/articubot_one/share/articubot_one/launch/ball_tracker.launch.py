import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression

def generate_launch_description():

    # Define the package name and mode argument
    my_package_name = 'articubot_one'
    sim_mode = LaunchConfiguration('sim_mode')
    
    # Declare the simulation mode argument (defaults to 'false')
    sim_mode_dec = DeclareLaunchArgument('sim_mode', default_value='false')

    # Get the paths to the tracker parameter files
    tracker_params_sim = os.path.join(get_package_share_directory(my_package_name), 'config', 'ball_tracker_params_sim.yaml')
    tracker_params_robot = os.path.join(get_package_share_directory(my_package_name), 'config', 'ball_tracker_params_robot.yaml')

    # Select the correct parameters file based on simulation mode
    params_path = PythonExpression(['"', tracker_params_sim, '" if "', sim_mode, '" == "true" else "', tracker_params_robot, '"'])

    # Include the ball_tracker launch file, passing relevant arguments
    tracker_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('ball_tracker'), 'launch', 'ball_tracker.launch.py')]),
        launch_arguments={
            'params_file': params_path,
            'image_topic': '/camera/image_raw',  # Ensure this topic exists
            'cmd_vel_topic': '/cmd_vel_tracker',  # Ensure this topic exists
            'enable_3d_tracker': 'true'
        }.items()
    )

    # Return the launch description with the mode declaration and tracker launch
    return LaunchDescription([
        sim_mode_dec,
        tracker_launch,
    ])
