import move
import PS4Controller
import time
class DynamixelArm:
    
    def __init__(self) -> None:
        """_summary_

        Returns:
            _type_: _description_
        """
        MODE="FORWARD"
        try:
            ctrl=PS4Controller
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
            m.SetCurrentLimit(6000)
            m.SetAccelLimit(500)
            m.SetVelocityLimit(100)

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

    def get_Current_Pos(self):
        """return all current positions 

        Returns:
            list: list of current angles
        """
        self.EnableTorque()
        self.M1_angle=self._map(self.M1.Read_Pos(),-501433,501433,-180,180)
        self.M2_angle=self._map(self.M2.Read_Pos(),-501433,501433,-180,180)
        self.M3_angle=self._map(self.M3.Read_Pos(),-501433,501433,-180,180)
        self.M4_angle=self._map(self.M4.Read_Pos(),-501433,501433,-180,180)
        self.M5_angle=self._map(self.M5.Read_Pos(),-501433,501433,-180,180)
        self.M6_angle=self._map(self.M6.Read_Pos(),-501433,501433,-180,180)
        self.angles=[self.M1_angle,self.M2_angle,self.M3_angle,self.M4_angle,self.M5_angle,self.M6_angle]
        return self.angles
    
    def set_Current_Pos(self,angles):
        """get all angles and set positions 

        Returns:
            void: setting angles 
        """
        for idx in range(self.motors):
            pos=self._map(angles[idx],0,360,-501433,501433)
            if pos>=self.RANGES[idx][0] and pos<=self.RANGES[idx][1]:
                self.motors[idx].Write_Pos(angles[idx])
                self.Sent_Positions[idx]=angles[idx]
            else:
                print("Angle "+str(idx)+" is out of range! ")
    
    def inRange(self,value,id):
        return self.motors[id].DXL_MAXIMUM_POSITION_VALUE>value and self.motors[id].DXL_MINIMUM_POSITION_VALUE<value

    def get_sent_pos(self):
        """get all the positions set 

        Returns:
            list: positions for all motors
        """
        return self.Sent_Positions
    def Home(self):
        finished=False
        while not finished:
            self.motors[1].Enable_Torque()
            self.motors[1].Write_Pos(0)
            if not self.inRange(self.motors[1].Read_Pos(),1):
                raise Exception("Out of range, Homing failed, Try moving the arm and homing again")
            if self.motors[1].Read_Pos()==0:
                print("Motor 2 Home")
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
                            
                            #check if to kill the arm
                            if kill_btn==1:
                                kill_btn=self.ps4.kill()
                                if kill_btn==0:
                                    print("Exit")
                                    self.Exit()
                                 
                            if mode_btn==1  :
                                start_time = time.time()
                                mode_btn=self.ps4.share()
                                if mode_btn==0:
                                    if time.time() - start_time >= 5:
                                        if MODE=="FORWARD":
                                            MODE="INVERSE"
                                            print("MODE CHANGED TO INVERSE KINEMATIC!!! PAY ATTENTION!")
                                        elif MODE=="INVERSE":
                                            MODE="FORWARD"  
                                            print("MODE CHANGED TO FORWARD KINEMATIC!!! PAY ATTENTION!")
                                        elif MODE=="SELFAWARENESS":
                                            MODE="FORWARD"  
                                            print("MODE CHANGED TO FORWARD KINEMATIC!!! PAY ATTENTION!")
                            if mode_btn==1 and MODE!="SELFAWARENESS":
                                current_time = time.time()
                                if last_press_time is not None and current_time - last_press_time <= double_press_threshold:
                                    MODE="SELFAWARENESS"
                                    print("MODE CHANGED TO SELFAWARENESS!!! PAY ATTENTION!")   
                                    last_press_time = current_time
                            
                            if MODE=="FORWARD":
                            #FORWARD KINEMATICS CONTROL  
                                pass  
                            if MODE=="INVERSE":
                            #INVERSE KINEMATICS CONTROL  
                                pass  
                            if MODE=="SELFAWARENESS":
                            #SELFAWARENESS CONTROL  - POLICY RUNNING NEURAL NETWORK 
                                pass 
                            if MODE=="PLANNING":
                            #PLANNING CONTROL  - Running Predetermined Plan
                                pass 
            

    def Exit(self):
        """Kill motors

        Returns:
            void
        """
        self.M1.Close_Port()

arm=DynamixelArm()
print(arm.get_Current_Pos())
arm.DisableTorque()
#arm.Ps4Control()