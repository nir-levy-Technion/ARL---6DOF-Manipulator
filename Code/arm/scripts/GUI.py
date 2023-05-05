import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLineEdit, QTextEdit,QCheckBox,QInputDialog,QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSignal,QObject
import qdarkstyle
from PyQt5.QtGui import QImage, QPixmap
from qtwidgets import Toggle
from qtwidgets import AnimatedToggle

class ArmControlGUI(QWidget):
    motor_angle_changed = pyqtSignal(int, int)
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("6-DOF Arm Control")

        # Add the camera QLabel to the layout
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(1920, 1080)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.camera_label)

        # Initialize the camera and timer
        self.camera = cv2.VideoCapture(0)  # 0 is the default camera index, change it if you have multiple cameras
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(15)  # Update the camera feed every 30 ms
        
        motor1_label = QLabel("Motor 1:")
        self.motor1_slider = QSlider(Qt.Horizontal)
        self.motor1_slider.setMinimum(-180)
        self.motor1_slider.setMaximum(180)
        self.motor1_slider.setTickInterval(10)
        self.motor1_slider.setTickPosition(QSlider.TicksBelow)
        self.motor1_angle = QLabel("0")
        
        motor2_label = QLabel("Motor 2:")
        self.motor2_slider = QSlider(Qt.Horizontal)
        self.motor2_slider.setMinimum(-180)
        self.motor2_slider.setMaximum(180)
        self.motor2_slider.setTickInterval(10)
        self.motor2_slider.setTickPosition(QSlider.TicksBelow)
        self.motor2_angle = QLabel("0")
        
        motor3_label = QLabel("Motor 3:")
        self.motor3_slider = QSlider(Qt.Horizontal)
        self.motor3_slider.setMinimum(-180)
        self.motor3_slider.setMaximum(180)
        self.motor3_slider.setTickInterval(10)
        self.motor3_slider.setTickPosition(QSlider.TicksBelow)
        self.motor3_angle = QLabel("0")
        
        motor4_label = QLabel("Motor 4:")
        self.motor4_slider = QSlider(Qt.Horizontal)
        self.motor4_slider.setMinimum(-180)
        self.motor4_slider.setMaximum(180)
        self.motor4_slider.setTickInterval(10)
        self.motor4_slider.setTickPosition(QSlider.TicksBelow)
        self.motor4_angle = QLabel("0")
        
        motor5_label = QLabel("Motor 5:")
        self.motor5_slider = QSlider(Qt.Horizontal)
        self.motor5_slider.setMinimum(-180)
        self.motor5_slider.setMaximum(180)
        self.motor5_slider.setTickInterval(10)
        self.motor5_slider.setTickPosition(QSlider.TicksBelow)
        self.motor5_angle = QLabel("0")
        
        motor6_label = QLabel("Motor 6:")
        self.motor6_slider = QSlider(Qt.Horizontal)
        self.motor6_slider.setMinimum(-180)
        self.motor6_slider.setMaximum(180)
        self.motor6_slider.setTickInterval(10)
        self.motor6_slider.setTickPosition(QSlider.TicksBelow)
        self.motor6_angle = QLabel("0")
        self.motor1_angle_label = QLineEdit("0", self)
        self.motor1_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor1_angle_label, self.motor1_slider,0))

        self.motor2_angle_label = QLineEdit("0", self)
        self.motor2_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor2_angle_label, self.motor2_slider,1))

        self.motor3_angle_label = QLineEdit("0", self)
        self.motor3_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor3_angle_label, self.motor3_slider,2))

        self.motor4_angle_label = QLineEdit("0", self)
        self.motor4_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor4_angle_label, self.motor4_slider,3))

        self.motor5_angle_label = QLineEdit("0", self)
        self.motor5_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor5_angle_label, self.motor5_slider,4))

        self.motor6_angle_label = QLineEdit("0", self)
        self.motor6_angle_label.textChanged.connect(lambda: self.handle_text_changed(self.motor6_angle_label, self.motor6_slider,5))

        self.motor1_slider.valueChanged.connect(self.update_motor1_angle)
        self.motor2_slider.valueChanged.connect(self.update_motor2_angle)
        self.motor3_slider.valueChanged.connect(self.update_motor3_angle)
        self.motor4_slider.valueChanged.connect(self.update_motor4_angle)
        self.motor5_slider.valueChanged.connect(self.update_motor5_angle)
        self.motor6_slider.valueChanged.connect(self.update_motor6_angle)
        slider_design='''QSlider::groove:horizontal {border: 1px solid #bbb;
        background: white;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::sub-page:horizontal {
        background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
            stop: 0 #66e, stop: 1 #bbf);
        background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
            stop: 0 #bbf, stop: 1 #55f);
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::add-page:horizontal {
        background: #fff;
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }

        QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        width: 20px;
        
        margin-top: -10px;
        margin-bottom: -10px;
        border-radius: 10px;
        }

        QSlider::handle:horizontal:hover {
        background:  #444;
        border: 1px solid #444;
         width: 20px;
        
        margin-top: -10px;
        margin-bottom: -10px;
        border-radius: 10px;
        
        }

        QSlider::sub-page:horizontal:disabled {
        background: #bbb;
        border-color: #999;
        }

        QSlider::add-page:horizontal:disabled {
        background: #eee;
        border-color: #999;
        }

        QSlider::handle:horizontal:disabled {
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        }'''
        
        self.motor1_slider.setStyleSheet(slider_design)
        self.motor2_slider.setStyleSheet(slider_design)
        self.motor3_slider.setStyleSheet(slider_design)
        self.motor4_slider.setStyleSheet(slider_design)
        self.motor5_slider.setStyleSheet(slider_design)
        self.motor6_slider.setStyleSheet(slider_design)
        
        get_button = QPushButton("Get Position")
        get_button.clicked.connect(self.get_position)
        set_button = QPushButton("Set")
        set_button.clicked.connect(self.set_arm)
        
        x_label = QLabel("X:")
        self.x_input = QLineEdit()
        y_label = QLabel("Y:")
        self.y_input = QLineEdit()
        z_label = QLabel("Z:")
        self.z_input = QLineEdit()
        get_ik_button = QPushButton("Get IK")
        get_ik_button.clicked.connect(self.get_ik)
        set_ik_button = QPushButton("Set IK")
        set_ik_button.clicked.connect(self.set_ik)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_log)
        init_arm_button=QPushButton("Init Arm")
        init_arm_button.clicked.connect(self.init_arm)
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.append("Welcome to the 6-DOF Arm Control")
        
        self.motor1_torque = AnimatedToggle()
        self.motor2_torque = AnimatedToggle()
        self.motor3_torque = AnimatedToggle()
        self.motor4_torque = AnimatedToggle()
        self.motor5_torque = AnimatedToggle()
        self.motor6_torque = AnimatedToggle()
        self.motor1_torque_label = QLabel("Enable torque")
        self.motor2_torque_label = QLabel("Enable torque")
        self.motor3_torque_label = QLabel("Enable torque")
        self.motor4_torque_label = QLabel("Enable torque")
        self.motor5_torque_label = QLabel("Enable torque")
        self.motor6_torque_label = QLabel("Enable torque")
        
        self.motor1_angle_label.setFixedWidth(100)
        self.motor2_angle_label.setFixedWidth(100)
        self.motor3_angle_label.setFixedWidth(100)
        self.motor4_angle_label.setFixedWidth(100)
        self.motor5_angle_label.setFixedWidth(100)
        self.motor6_angle_label.setFixedWidth(100)
        no_border_style = "QLineEdit { border: none; }"

        self.motor1_angle_label.setStyleSheet(no_border_style)
        self.motor2_angle_label.setStyleSheet(no_border_style)
        self.motor3_angle_label.setStyleSheet(no_border_style)
        self.motor4_angle_label.setStyleSheet(no_border_style)
        self.motor5_angle_label.setStyleSheet(no_border_style)
        self.motor6_angle_label.setStyleSheet(no_border_style)
        
        self.motor1_torque.stateChanged.connect(self.toggle_motor1_torque)
        self.motor2_torque.stateChanged.connect(self.toggle_motor2_torque)
        self.motor3_torque.stateChanged.connect(self.toggle_motor3_torque)
        self.motor4_torque.stateChanged.connect(self.toggle_motor4_torque)
        self.motor5_torque.stateChanged.connect(self.toggle_motor5_torque)
        self.motor6_torque.stateChanged.connect(self.toggle_motor6_torque)

        self.master_torque = QPushButton("Toggle All Torques")
        self.master_torque.clicked.connect(self.toggle_all_torques)

        check_comms_button = QPushButton("Check Comms")
        check_comms_button.clicked.connect(self.check_comms)
        init_arm_button = QPushButton("Init Arm")
        init_arm_button.clicked.connect(self.init_arm)
        pause_resume_button = QPushButton("Pause/Resume")
        pause_resume_button.clicked.connect(self.pause_resume)
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(motor1_label)
        hbox1.addWidget(self.motor1_slider)
        hbox1.addWidget(self.motor1_angle_label)
        hbox1.addWidget(self.motor1_torque_label)
        hbox1.addWidget(self.motor1_torque)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(motor2_label)
        hbox2.addWidget(self.motor2_slider)
        hbox2.addWidget(self.motor2_angle_label)
        hbox2.addWidget(self.motor2_torque_label)
        hbox2.addWidget(self.motor2_torque)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(motor3_label)
        hbox3.addWidget(self.motor3_slider)
        hbox3.addWidget(self.motor3_angle_label)
        hbox3.addWidget(self.motor3_torque_label)
        hbox3.addWidget(self.motor3_torque)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(motor4_label)
        hbox4.addWidget(self.motor4_slider)
        hbox4.addWidget(self.motor4_angle_label)
        hbox4.addWidget(self.motor4_torque_label)
        hbox4.addWidget(self.motor4_torque)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(motor5_label)
        hbox5.addWidget(self.motor5_slider)
        hbox5.addWidget(self.motor5_angle_label)
        hbox5.addWidget(self.motor5_torque_label)
        hbox5.addWidget(self.motor5_torque)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(motor6_label)
        hbox6.addWidget(self.motor6_slider)
        hbox6.addWidget(self.motor6_angle_label)
        hbox6.addWidget(self.motor6_torque_label)
        hbox6.addWidget(self.motor6_torque)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(get_button)
        hbox7.addWidget(set_button)
        hbox7.addWidget(self.master_torque)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(x_label)
        hbox8.addWidget(self.x_input)
        hbox8.addWidget(y_label)
        hbox8.addWidget(self.y_input)
        hbox8.addWidget(z_label)
        hbox8.addWidget(self.z_input)
        hbox8.addWidget(get_ik_button)
        hbox8.addWidget(set_ik_button)
        hbox8.addWidget(clear_button)
        
        hbox9 = QHBoxLayout()
        hbox9.addWidget(check_comms_button)
        hbox9.addWidget(init_arm_button)
        hbox9.addWidget(pause_resume_button)
        hbox9.addWidget(stop_button)
        
        vbox = QVBoxLayout()
        camera_layout = QVBoxLayout()
        camera_layout.addWidget(self.camera_label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)
        vbox.addLayout(hbox9)
        vbox.addWidget(self.message_log)
        # Create a QHBoxLayout to put the camera and controls side by side
        hbox_main = QHBoxLayout()
        hbox_main.addLayout(camera_layout)
        hbox_main.addLayout(vbox)

        self.setLayout(hbox_main)
        
    def init_arm(self):
        # self.arm=Control.Arm()
        pass
        
    def get_position(self):
        # Get current angles from robot arm here
        # get = Control.ThreadWithReturnValue(target=self.arm.get_Current_Pos)
        # get.start()
        # self.angles=get.join()
        try:
            self.motor1_angle.setText(str(self.angles[0]))
            self.motor1_slider.setValue(self.angles[0])
            self.motor2_angle.setText(str(self.angles[1]))
            self.motor2_slider.setValue(self.angles[1])
            self.motor3_angle.setText(str(self.angles[2]))
            self.motor3_slider.setValue(self.angles[2])
            self.motor4_angle.setText(str(self.angles[3]))
            self.motor4_slider.setValue(self.angles[3])
            self.motor5_angle.setText(str(self.angles[4]))
            self.motor5_slider.setValue(self.angles[4])
            self.motor6_angle.setText(str(self.angles[5]))
            self.motor6_slider.setValue(self.angles[5])
            
            self.message_log.append("Current position retrieved.")
            self.message_log.append(self.motor1_angle.text()+","+self.motor2_angle.text()+","+self.motor3_angle.text()+","+self.motor4_angle.text()+","+self.motor5_angle.text()+","+self.motor6_angle.text())
        except Exception as e:
            self.message_log.append("Error getting the position, try again.")
            self.message_log.append(str(e))


    def set_arm(self):
        # Send angles from sliders to robot arm here
        self.message_log.append("Setting arm position...")
        self.message_log.append(self.motor1_angle.text()+","+self.motor2_angle.text()+","+self.motor3_angle.text()+","+self.motor4_angle.text()+","+self.motor5_angle.text()+","+self.motor6_angle.text())
        self.arm.Sent_Positions=[int(self.motor1_angle.text()),int(self.motor2_angle.text()),int(self.motor3_angle.text()),int(self.motor4_angle.text()),int(self.motor5_angle.text()),int(self.motor6_angle.text())]
        self.arm.set_Current_Pos(self.arm.Sent_Positions)

    def get_ik(self):
        # Get inverse kinematics solution here
        x = self.x_input.text()
        y = self.y_input.text()
        z = self.z_input.text()
        self.message_log.append(f"Getting IK solution for x:{x}, y:{y}, z:{z}")
        
        pass

    def set_ik(self):
        # Send inverse kinematics solution to robot arm here
        x = self.x_input.text()
        y = self.y_input.text()
        z = self.z_input.text()
        self.message_log.append("Setting arm position using IK...")
        self.message_log.append(f"Setting arm position using IK for x:{x}, y:{y}, z:{z}")

        pass
        
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            resized_frame = cv2.resize(frame, (1920, 1080))  # Set the desired width and height here
            rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.camera_label.setPixmap(pixmap)


    def closeEvent(self, event):
        self.camera.release()
        event.accept()
    
    def on_button_click(self, index):
        pass
        # self.message_log.append(f"Button {index + 1} clicked")
        # Add the logic for each button here

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        super().closeEvent(event)
    def clear_log(self):
        self.message_log.clear()
        
    def update_motor1_angle(self, angle):
        self.motor1_angle_label.setText(str(angle))

    def update_motor2_angle(self, angle):
        self.motor2_angle_label.setText(str(angle))
        
    def update_motor3_angle(self, angle):
        self.motor3_angle_label.setText(str(angle))

    def update_motor4_angle(self, angle):
        self.motor4_angle_label.setText(str(angle))
        
    def update_motor5_angle(self, angle):
        self.motor5_angle_label.setText(str(angle))

    def update_motor6_angle(self, angle):
        self.motor6_angle_label.setText(str(angle))
    
    def toggle_motor1_torque(self, state):
        # Toggle motor 1 torque here
        pass

    def toggle_motor2_torque(self, state):
        # Toggle motor 2 torque here
        pass

    def toggle_motor3_torque(self, state):
        # Toggle motor 3 torque here
        pass

    def toggle_motor4_torque(self, state):
        # Toggle motor 4 torque here
        pass

    def toggle_motor5_torque(self, state):
        # Toggle motor 5 torque here
        pass

    def toggle_motor6_torque(self, state):
        # Toggle motor 6 torque here
        pass

    def toggle_all_torques(self):
        state = not self.motor1_torque.isChecked()
        self.motor1_torque.setChecked(state)
        self.motor2_torque.setChecked(state)
        self.motor3_torque.setChecked(state)
        self.motor4_torque.setChecked(state)
        self.motor5_torque.setChecked(state)
        self.motor6_torque.setChecked(state)
    def check_comms(self):
        # Add your code to check communications here
        pass

    def pause_resume(self):
        # Add your code to pause or resume the robot arm here
        pass

    def stop(self):
        # Add your code to stop the robot arm here
        pass
        
    def handle_text_changed(self, line_edit, motor_slider, motor_index):
        try:
            new_value = int(line_edit.text())
            if -180 <= new_value <= 180:  # Adjust the range to accept negative values
                motor_slider.setValue(new_value)
                self.motor_angle_changed.emit(motor_index, new_value)
            else:
                line_edit.setText(str(motor_slider.value()))
        except ValueError:
            line_edit.setText(str(motor_slider.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = ArmControlGUI()
    window.resize(1920, 1080)
    window.show()
    sys.exit(app.exec_())
   
  