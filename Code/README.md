6-DOF Robotic Arm Control with PS4 Controller

This project provides a graphical user interface (GUI) to control a 6-DOF robotic arm using a PS4 controller. The project consists of four main components:

    GUI for the robotic arm control
    Robotic arm class
    Motor class
    PS4 controller class

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
Installation

To install the project and its dependencies, follow these steps:

    Install ROS 2 Humble:
    Follow the official ROS 2 installation guide for your specific platform: ROS 2 Humble Installation

    Install the required Python packages, if you haven't already:

    pip install PyQt5 qdarkstyle evdev

Usage

To run the project, follow these steps:

    Run the main GUI application:

    python gui.py

    Connect your PS4 controller to your computer, and ensure that it is properly detected by the PS4Controller class.

    Use the GUI to control the robotic arm by adjusting the sliders or entering x, y, and z coordinates for the desired position. You can also use the PS4 controller to control the robotic arm using the provided methods in the PS4Controller class.

Contributing

If you would like to contribute to this project, please feel free to open a pull request or report any issues. We appreciate your help in improving the project and making it more versatile and user-friendly.
