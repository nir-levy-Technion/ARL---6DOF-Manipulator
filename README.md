6-DOF Robotic Arm Control with PS4 Controller and ROS Integration

This project provides a complete solution for controlling a 6-DOF robotic arm using a PS4 controller and ROS 2. It includes:

    Graphical user interface (GUI) for the robotic arm control
    Robotic arm class
    Motor class
    PS4 controller class
    CAD files for the robotic arm design
    ROS 2 integration

Below is a brief description of each component:
1. GUI for the robotic arm control

The ArmControlGUI class in the gui.py file provides a PyQt5-based GUI for controlling the robotic arm. The GUI allows you to:

    Manually set the angle of each motor using sliders
    Retrieve the current position of the robotic arm
    Set the position of the robotic arm using inverse kinematics (IK) solutions embedded in the Arm class
    Clear the message log

2. Robotic arm class

The Arm class in the arm.py file represents the 6-DOF robotic arm. The class provides methods for setting joint angles, calculating forward kinematics, and calculating inverse kinematics. The inverse kinematics solver is a part of this class.
3. Motor class

The Motor class in the motor.py file represents an individual motor and provides methods for communication and control of the motor. It is responsible for sending commands to the motors and receiving feedback from them.
4. PS4 controller class

The PS4Controller class in the ps4_controller.py file allows you to read input from a PS4 controller connected to your computer. The class provides methods for reading the state of various buttons and thumbsticks on the controller.
5. CAD files for the robotic arm design

The CAD files included in this project provide the 3D models of the robotic arm components. You can use these files to create a physical replica of the robotic arm or modify the design to suit your specific requirements.
6. ROS 2 integration

This project includes ROS 2 packages and configuration files that enable integration with the Robot Operating System (ROS) for advanced control and communication with other ROS-based systems.
Installation

To install the project and its dependencies, follow these steps:

    Install ROS 2 Humble:
    Follow the official ROS 2 installation guide for your specific platform: ROS 2 Humble Installation

    Clone this repository into your ROS 2 workspace:

    bash

cd <your_ros2_workspace>/src
git clone <repository_url>

Install the required Python packages, if you haven't already:

pip install PyQt5 qdarkstyle evdev

Build the ROS 2 workspace:

bash

    cd <your_ros2_workspace>
    colcon build

Usage

To run the project, follow these steps:

    Source the ROS 2 workspace:

    bash

source <your_ros2_workspace>/install/setup.bash

Run the main GUI application:

arduino

    ros2 run <package_name> gui

    Connect your PS4 controller to your computer, and ensure that it is properly detected by the PS4Controller class.

    Use the GUI to control the robotic arm by adjusting the sliders or entering x, y, and z coordinates for the desired position. You can also use the PS4 controller to control the robotic arm using the provided methods in the PS4Controller class.

Contributing

If youwould like to contribute to this project, please follow these steps:

    Fork the repository on GitHub.
    Create a new branch with a descriptive name for your feature, bugfix, or improvement.
    Commit your changes to your branch, following the coding style and best practices of the existing codebase.
    Open a pull request describing your changes and how they improve the project.
    The project maintainers will review your pull request, provide feedback, and merge it if accepted.

Support

If you encounter any issues or need assistance, please open an issue on the GitHub repository. The project maintainers and community will be happy to help you.
License

This project is licensed under the MIT License. Please see the LICENSE file for more information.
Acknowledgments

We would like to thank the contributors and maintainers of the following projects, which have been invaluable in the development of this robotic arm control solution:

    ROS 2 (Robot Operating System)
    PyQt5
    evdev

We also appreciate the support and feedback from the robotics and ROS communities.
