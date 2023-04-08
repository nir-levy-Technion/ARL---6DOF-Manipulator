from Control import Arm
import rospy
import rclpy

from std_msgs.msg import Int32, Float64
from sensor_msgs.msg import JointState

class ArmROS(Arm):
    def __init__(self):
        super(ArmROS, self).__init__()

        rospy.init_node('robotic_arm_control')

        # Publishers
        self.joint_states_pub = rospy.Publisher('/joint_states', JointState, queue_size=1)
        self.positions_pub = rospy.Publisher('/positions', Float64, queue_size=1)
        self.velocities_pub = rospy.Publisher('/velocities', Float64, queue_size=1)
        self.torques_pub = rospy.Publisher('/torques', Float64, queue_size=1)
        self.currents_pub = rospy.Publisher('/currents', Float64, queue_size=1)
        
        
        # Subscribers
        self.positions_sub = rospy.Subscriber('/positions', Float64, self.position_callback)
        self.velocities_sub = rospy.Subscriber('/velocities', Float64, self.velocity_callback)
        self.torques_sub = rospy.Subscriber('/torques', Float64, self.torque_callback)
        self.currents_sub = rospy.Subscriber('/currents', Float64, self.current_callback)
        
    def position_callback(self, msg):
        self.set_Current_Pos(msg.data)
    def velocity_callback(self, msg):  
        self.set_Current_Vel(msg.data)
    def torque_callback(self, msg): 
        self.set_Current_Tor(msg.data)
    def current_callback(self, msg): 
        self.set_Current_Cur(msg.data)
    
    def publish_joint_states(self):
        joint_state = JointState()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        joint_state.position = self.get_Current_Pos()
        self.joint_state_pub.publish(joint_state)

    def publish_positions(self): 
        self.positions_pub.publish(self.get_Current_Pos())
    
    def publish_velocities(self): 
        self.velocities_pub.publish(self.get_Current_Vel())
    
    def publish_torques(self): 
        self.torques_pub.publish(self.get_Current_Tor())
    
    def publish_currents(self): 
        self.currents_pub.publish(self.get_Current_Cur())
        
    def spin(self):
        rate = rospy.Rate(10) # 10 Hz
        while not rospy.is_shutdown():
            self.publish_joint_states()
            rate.sleep()
