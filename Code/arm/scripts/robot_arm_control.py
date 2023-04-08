import GUI
import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle
from ArmRos import ArmROS
import rospy


if __name__ == '__main__':
    try:
        arm_ros = ArmROS()
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        ex = GUI.ArmControlGUI()
        ex.show()
        arm_ros.spin()

        sys.exit(app.exec_())
    except rospy.ROSInterruptException:
        pass

  