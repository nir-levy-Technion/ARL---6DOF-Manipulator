import move

class DynamixelArm:
    
    def __init__(self) -> None:
        
          self.M1=move.Motor(1)
          self.M2=move.Motor(2)
          self.M3=move.Motor(3)
          self.M4=move.Motor(4)
          self.M5=move.Motor(5)
          self.M6=move.Motor(6)
          self.RANGES=[[-501433,501433],[-501433,501433],[-501433,501433],[-501433,501433],[-501433,501433],[-501433,501433]]
          self.Sent_Positions=[0,0,0,0,0,0]
          self.motors=[self.M1,self.M2,self.M3,self.M4,self.M5,self.M6]
    
    def EnableTorque(self):
        for motor in self.motors:
            motor.Enable_Torque()
            
    def DisableTorque(self):   
        for motor in self.motors:
            motor.Disable_Torque()
    
    
    def _map(self,x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
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
        return self.RANGES

    def get_Current_Pos(self):
        return [self.M1.ReadPos(),self.M2.ReadPos(),self.M3.ReadPos(),self.M4.ReadPos(),self.M5.ReadPos(),self.M6.ReadPos()]
    
    def set_Current_Pos(self,positions):
        for idx in range(self.motors):
            self.motors[idx].Write_Pos(positions[idx])
            self.Sent_Positions[idx]=positions[idx]
    
    def get_sent_pos(self):
        return self.Sent_Positions
    
    def Exit(self):
        self.M1.Close_Port()