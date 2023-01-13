import evdev
from evdev import InputDevice, categorize, ecodes

class PS4Controller:
    def __init__(self) -> None:     
        # Connect to the controller
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == 'Wireless Controller':
                self.ps4 = InputDevice(device.fn)
                break

        # Print out device information
        print(self.ps4)
        self.left_x_value=0
        self.left_y_value=0
        self.right_x_value=0
        self.right_y_value=0
        
    def _map(self,x, in_min, in_max, out_min, out_max):
        """gets a number and maps it from one ragne to another range.

        Returns:
           float: the number in the new range
        """
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)    
    
    def get_Left_thumb(self) ->list:
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.left_x_value = event.value
                if event.code == evdev.ecodes.ABS_Y:
                    self.left_y_value = event.value
            return [self._map(self.left_x_value,0,255,-100,100),self._map(self.left_y_value,255,0,-100,100)]
    
    def get_Right_thumb(self) ->list:
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_RX:
                    self.right_x_value = event.value
                if event.code == evdev.ecodes.ABS_RY:
                    self.right_y_value = event.value
            return [self._map(self.right_x_value,0,255,-100,100),self._map(self.right_y_value,255,0,-100,100)]
    
    def Tri(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False
                
    def Square(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False   
                     
    def X(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
                  
    def Circle(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def TR(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def TR2(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def LR(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def LR2(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def options(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def share(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
    def kill(self):
        for event in self.ps4.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.
                    return True
                else:
                    return False  
        
ctrl=PS4Controller()
while True: 
    print(ctrl.get_Right_thumb())

