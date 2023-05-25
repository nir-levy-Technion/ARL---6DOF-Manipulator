import move
import PS4Controller
import time
from ikpy import chain
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy.utils import geometry
import numpy as np
import socket 
class Arm:
    
    def __init__(self) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        MODE="FORWARD"
        try:
            ctrl=PS4Controller()
            self.ps4=ctrl.PS4Controller()
        except:
            print("No Controller Found")
        self.M1=move.Motor(1)
        self.M2=move.Motor(2)
        self.M3=move.Motor(3)
        self.M4=move.Motor(4)
        self.M5=move.Motor(5)
        self.M6=move.Motor(6)
        self.RANGES=[[-500000,500000],[-301160,306738],[-278852,278852],[-500000,500000],[-301160,301160],[-500000,500000]]
        self.Sent_Positions=[0,0,0,0,0,0]
        self.motors=[self.M1,self.M2,self.M3,self.M4,self.M5,self.M6]
        for m in self.motors:
            m.Disable_Torque()
            m.SetCurrentLimit(15000)
            m.SetAccelLimit(500)
            m.SetVelocityLimit(250)
        self.EnableTorque()
        # try:
        #     self.Home()
        # except:
        #     print("Homing stopped")
            
            
    def EnableTorque(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        for motor in self.motors:
            motor.Enable_Torque()
            
    def DisableTorque(self):   
        """_summary_

        Returns:
            _type_: _description_
        """
        for motor in self.motors:
            motor.Disable_Torque()

    def _map(self,x, in_min, in_max, out_min, out_max):
        """gets a number and maps it from one ragne to another range.

        Returns:
           float: the number in the new range
        """
        return float((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
    def set_range(self,id,min,max):
        """_summary_

        Args:
            int:id
            int:min-angle in degrees
            int-max-angle in degrees
        Returns:
            void
        """
        r0=self._map(min,0,360,-501433,501433)
        r1=self._map(max,0,360,-501433,501433)
        self.RANGES[id][0]=r0
        self.RANGES[id][1]=r1
            
    def set_Ranges(self,ranges):
        """_summary_

        Args:
            ranges (list of ranges [M1[min,max],M2[min,max]...]): list of ranges of every motor min and max in units of degrees.
        """
        for i, r in enumerate(ranges):
            r0=self._map(r[0],0,360,-501433,501433)
            r1=self._map(r[1],0,360,-501433,501433)
            self.RANGES[i][0]=r0
            self.RANGES[i][1]=r1
    
    def get_Ranges(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.RANGES

    def get_Pos(self):
        """return all current positions 

        Returns:
            list: list of current angles
        """
        # self.EnableTorque()
        self.M1_angle=int(self._map(self.M1.Read_Pos(),-501433,501433,-180,180))
        self.M2_angle=int(self._map(self.M2.Read_Pos(),-501433,501433,-180,180))
        self.M3_angle=int(self._map(self.M3.Read_Pos(),-501433,501433,-180,180))
        self.M4_angle=int(self._map(self.M4.Read_Pos(),-501433,501433,-180,180))
        self.M5_angle=int(self._map(self.M5.Read_Pos(),-501433,501433,-180,180))
        self.M6_angle=int(self._map(self.M6.Read_Pos(),-501433,501433,-180,180))
        self.angles=[self.M1_angle,self.M2_angle,self.M3_angle,self.M4_angle,self.M5_angle,self.M6_angle]
        for idx,angle in enumerate(self.angles):
            if angle>360:
                self.angles[idx]=angle-1541769.5
        return self.angles
    
    def set_Pos(self,angles):
        """get all angles and set positions 

        Returns:
            void: setting angles 
        """
        for idx in range(len(self.motors)):
            pos=int(self._map(angles[idx],-180,180,-501433,501433))
            #print(pos)
            # if pos>=self.RANGES[idx][0] and pos<=self.RANGES[idx][1]:
            self.motors[idx].Write_Pos(pos)
            self.Sent_Positions[idx]=pos
            # else:
            #     print("Angle "+str(idx)+" is out of range! ")
    
    def set_motor_pos(self,id,angle):
        pos=int(self._map(angle,-180,180,-501433,501433))
        self.motors[id-1].Write_Pos(pos)
        self.Sent_Positions[id-1]=pos


    
    def set_Pos_order(self,angles,order):
        """get all angles and set positions 

        Returns:
            void: setting angles 
        """
        
        for m in order:
            real_pos=int(self._map(self.motors[m-1].Read_Pos(),-501433,501433,-180,180))
            pos=int(self._map(angles[m-1],-180,180,-501433,501433))
            self.Sent_Positions[m-1]=pos
            self.motors[m-1].Write_Pos(pos)
            time.sleep(3)
                
    def inRange(self,value,id):
        if value>501433:
                value=value-1541769.5
        return self.motors[id].DXL_MAXIMUM_POSITION_VALUE>value and self.motors[id].DXL_MINIMUM_POSITION_VALUE<value

    def get_currents(self):
        """get all the currents set 

        Returns:
            list: currents for all motors
        """
        for motor in self.motors:
            self.currents.append(motor.Read_Current())
        return self.currents
    
    def get_velocities(self):
        """get all the velocities set 

        Returns:
            list: velocities for all motors
        """
        for motor in self.motors:
            self.velocities.append(motor.Read_Velocity())
        return self.velocities 
    
    def get_torques(self):
        pass
        
    def get_sent_pos(self):
        """get all the positions set 

        Returns:
            list: positions for all motors
        """
        return self.Sent_Positions
    def SetXYZWithoutOrientation(self,position, q_init):
        """Inverse Kinemtics without orientation

        Args:
            position (List[]): [x, y, z],
            q_init (q_init = np.array([0, 0, 0, 0, 0, 0])): initial values conditions, joint angles.
        """

        # Create an instance of the Chain class with your robot's links
        my_chain = Chain(name='my_chain', links=[
            OriginLink(),
            URDFLink(name="link1", bounds=(-180, 180), translation_vector=[0, 0, 135], orientation=[0, 1, 0], rotation=0),
            URDFLink(name="link2", bounds=(-180, 180), translation_vector=[0, 0, 30], orientation=[0, 1, 0], rotation=0),
            URDFLink(name="link3", bounds=(-180, 180), translation_vector=[395, 0, 0], orientation=[0, 1, 0], rotation=np.pi),
            URDFLink(name="link4", bounds=(-180, 180), translation_vector=[375, 0, 0], orientation=[1, 0, 0], rotation=0),
            URDFLink(name="link5", bounds=(-180, 180), translation_vector=[0, 0, 30], orientation=[0, 1, 0], rotation=0),
            URDFLink(name="link6", bounds=(-180, 180), translation_vector=[155, 0, 0], orientation=[0, 1, 0], rotation=0),
        ])

        # Define the desired position of the end effector
        end_effector_position = np.array(position + [1])

        # Calculate the joint angles without orientation constraints
        joint_angles = my_chain.inverse_kinematics(end_effector_position, initial_position=q_init, solve_rotation=False)

        print(joint_angles)
        return joint_angles

    def SetXYZ(self,position, orientation, q_init):
        """Inverse Kinemtics

        Args:
            position (List[]): [x,y,z,1],
            orientation (List[,]): [[u_x,v_x,w_x],[u_y,v_y,w_y],[u_z,v_z,w_z]]
            q_init (q_init = np.array([0, 0, 0, 0, 0, 0])): initial values conditions, joint angles.
        """

        # Create an instance of the Chain class with your robot's links
        my_chain = Chain(name='my_chain', links=[
            OriginLink(),
            ModifiedURDFLink(name="link1", bounds=(-180, 180), origin_translation=[0, 0, 135], origin_orientation=np.eye(3), rotation=q_init[0]),
            ModifiedURDFLink(name="link2", bounds=(-180, 180), origin_translation=[0, 0, 30], origin_orientation=np.eye(3), rotation=q_init[1]),
            ModifiedURDFLink(name="link3", bounds=(-180, 180), origin_translation=[395, 0, 0], origin_orientation=np.eye(3), rotation=q_init[2] + np.pi),
            ModifiedURDFLink(name="link4", bounds=(-180, 180), origin_translation=[375, 0, 0], origin_orientation=np.eye(3), rotation=q_init[3]),
            ModifiedURDFLink(name="link5", bounds=(-180, 180), origin_translation=[0, 0, 30], origin_orientation=np.eye(3), rotation=q_init[4]),
            ModifiedURDFLink(name="link6", bounds=(-180, 180), origin_translation=[155, 0, 0], origin_orientation=np.eye(3), rotation=q_init[5]),
        ])

        # Calculate the joint angles with the angle range limits and bounds
        joint_angles = my_chain.inverse_kinematics(target_position=position, target_orientation=orientation, initial_position=q_init)

        print(joint_angles)
        return joint_angles


    def Home(self):
        finished=False
        while not finished:
            self.motors[1].Enable_Torque()
            self.motors[1].Write_Pos(0)
            if not self.inRange(self.motors[1].Read_Pos(),1):
                raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
            if self.motors[1].Read_Pos()==0:
                self.motors[0].Enable_Torque()
                self.motors[0].Write_Pos(0)
                if not self.inRange(self.motors[0].Read_Pos(),0):
                    raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                if self.motors[0].Read_Pos()==0:
                    self.motors[2].Enable_Torque()
                    self.motors[2].Write_Pos(0)
                    if not self.inRange(self.motors[2].Read_Pos(),2):
                        raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                    if self.motors[2].Read_Pos()==0:
                        self.motors[3].Enable_Torque()
                        self.motors[3].Write_Pos(0)
                        if not self.inRange(self.motors[3].Read_Pos(),3):
                            raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                        if self.motors[3].Read_Pos()==0:
                            self.motors[4].Enable_Torque()
                            self.motors[4].Write_Pos(0)
                            if not self.inRange(self.motors[4].Read_Pos(),4):
                                raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                            if self.motors[4].Read_Pos()==0:
                                self.motors[5].Enable_Torque()
                                self.motors[5].Write_Pos(0)
                                if not self.inRange(self.motors[5].Read_Pos(),5):
                                    raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
                                if self.motors[5].Write_Pos(0)==0:
                                    finished=True

        
    def Ps4Control(self):
        start_time = None
        kill=False
        last_press_time = None
        double_press_threshold = 0.5 # seconds

        if self.ps4.options()==1:
            start_time = time.time()
            if self.ps4.options() == 0: # button released
                if start_time is not None:
                    if time.time() - start_time >= 5:
                        print("Started PS4 control")
                        while not kill:
                            kill_btn=self.ps4.kill()
                            mode_btn=self.ps4.share()
                            options_btn=self.ps4.options()
                            #check if to kill the arm
                            if kill_btn==1:
                                kill_btn=self.ps4.kill()
                                if kill_btn==0:
                                    print("Exit")
                                    self.Exit()
                                
                            self.MODE=self.ps4.choose_mode()
                            
                            if self.MODE=="FORWARD":
                            # FORWARD KINEMATICS CONTROL  
                                
                                # Control the robotic arm motors using the PS4 controller
                                angles = self.get_Pos()
                                left_x = self.ps4.get_Left_thumb()[0]
                                left_y = self.ps4.get_Left_thumb()[1]
                                right_x = self.ps4.get_Right_thumb()[0]
                                right_y = self.ps4.get_Right_thumb()[1]
                                L1=self.ps4.L1()
                                L2=self.ps4.L2()
                                R1=self.ps4.R1()
                                R2=self.ps4.R2()

                                # Update motor angles based on thumbstick and trigger inputs
                                angles[0] += left_x/100
                                angles[1] += left_y/100
                                angles[2] += right_x/100
                                angles[3] += right_y/100
                                angles[4] += R1-L1
                                angles[5] += R2-L2

                                # Set motor positions based on updated angles
                                self.set_Pos(angles)

                                # Control the gripper using the D-pad
                                gripper = Gripper()
                                thumbL = self.ps4.ThumbL()
                                thumbR = self.ps4.ThumbR()

                                if thumbL == 1:
                                    gripper.pickup()
                                elif thumbR == 1:
                                    gripper.release()

                                # Delay to prevent the motors from moving too fast
                                time.sleep(0.1)

                                
                            if self.MODE=="INVERSE":
                                # INVERSE KINEMATICS CONTROL
                                target_position = [0, 0, 0]
                                target_orientation= [0, 0, 0]
                                # Use the right thumbstick to control the target position (x, y, z)
                                right_x = self.ps4.get_Right_thumb()[0]
                                right_y = self.ps4.get_Right_thumb()[1]
                                L2 = self.ps4.L2()
                                L1 = self.ps4.L1()

                                target_position[0] += right_x / 100
                                target_position[1] += right_y / 100
                                target_position[2] += (L2 - L1) / 100

                                # Use the left thumbstick to control the target orientation (roll, pitch, yaw)
                                left_x = self.ps4.get_Left_thumb()[0]
                                left_y = self.ps4.get_Left_thumb()[1]
                                R2 = self.ps4.R2()
                                R1 = self.ps4.R1()

                                target_orientation[0] += left_x / 100
                                target_orientation[1] += left_y / 100
                                target_orientation[2] += (R2 - R1) / 100

                                # Calculate the joint angles using the inverse kinematics function
                                joint_angles = self.SetXYZ(target_position, target_orientation,self.get_Pos())

                                # Set motor positions based on the calculated joint angles
                                self.set_Pos(joint_angles)

                                # Control the gripper using the D-pad
                                gripper = Gripper()
                                thumbL = self.ps4.ThumbL()
                                thumbR = self.ps4.ThumbR()

                                if thumbL == 1:
                                    gripper.pickup()
                                elif thumbR == 1:
                                    gripper.release()

                                # Delay to prevent the motors from moving too fast
                                time.sleep(0.1)
  
                            if self.MODE=="SELFAWARENESS":
                            # SELFAWARENESS CONTROL  - POLICY RUNNING NEURAL NETWORK 
                                pass 
                            if self.MODE=="PLANNING":
                            # PLANNING CONTROL  - Running Predetermined Plan
                                pass

            

    def Exit(self):
        """Kill motors

        Returns:
            void
        """
        self.M1.Close_Port()
class ModifiedURDFLink(URDFLink):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.symbolic_transformation_matrix = self._apply_geometric_transformations(theta=self.theta, mu=self.mu, symbolic=False)

class Gripper():
    def __init__(self):
        self.HOST = '172.20.10.7'  # replace with the IP address of your ESP
        self.PORT = 80  # replace with the port number you set up on the ESP
        self.release()

    def pickup(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b'45')
            success = s.recv(1024)
            print('Received', repr(success))
            return success

    def release(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b'90')
            success = s.recv(1024)
            print('Received', repr(success))
            return success
        

arm=Arm()
arm.set_Pos([0,0,0,0,0,0])

arm.SetXYZ([300,300,300],[[0,0,0],[0,0,0],[0,0,0]],[0,0,0,0,0,0])