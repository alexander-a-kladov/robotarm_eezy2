#!/usr/bin/python3


import sys, serial
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class SliderApp(QWidget):
    def __init__(self):
        super().__init__()
        #self.to_arduino = serial.Serial('/dev/ttyUSB0', 9600)
        self.setWindowTitle("Robot Arm Control")
        self.setGeometry(100, 100, 500, 300)  # (x, y, width, height)
        
        layoutv = QVBoxLayout()

        layout = QHBoxLayout()
        self.slider_claw = QSlider(Qt.Horizontal, self)
        self.slider_claw.setMaximum(180)
        self.slider_claw.setValue(90)
        layout.addWidget(self.slider_claw)
        self.label_claw = QLabel("0", self)
        layout.addWidget(self.label_claw)
        layoutv.addLayout(layout)
        self.update_label_claw()
        
        layout = QHBoxLayout()
        self.slider_rotate = QSlider(Qt.Horizontal, self)
        self.slider_rotate.setMaximum(180)
        self.slider_rotate.setValue(90)
        layout.addWidget(self.slider_rotate)
        self.label_rotate = QLabel("0", self)
        layout.addWidget(self.label_rotate)
        layoutv.addLayout(layout)
        self.update_label_rotate()
        
        layout = QHBoxLayout()
        self.slider_fb = QSlider(Qt.Horizontal, self)
        self.slider_fb.setMaximum(180)
        self.slider_fb.setValue(90)
        layout.addWidget(self.slider_fb)
        self.label_fb = QLabel("0", self)
        layout.addWidget(self.label_fb)
        layoutv.addLayout(layout)
        self.update_label_fb()
        
        layout = QHBoxLayout()
        self.slider_ud = QSlider(Qt.Horizontal, self)
        self.slider_ud.setMaximum(180)
        self.slider_ud.setValue(90)
        layout.addWidget(self.slider_ud)
        self.label_ud = QLabel("0", self)
        layout.addWidget(self.label_ud)
        layoutv.addLayout(layout)
        self.update_label_ud()

        layout_v = QVBoxLayout()
        layout_buttons = QHBoxLayout()
        layout_vertical = QHBoxLayout()
        self.left_hanoi_pb = QPushButton("left")
        self.center_hanoi_pb = QPushButton("center")
        self.right_hanoi_pb = QPushButton("right")
        self.claw_hanoi_pb = QPushButton("claw")
        layout_buttons.addWidget(self.left_hanoi_pb)
        layout_buttons.addWidget(self.center_hanoi_pb)
        layout_buttons.addWidget(self.right_hanoi_pb)
        layout_buttons.addWidget(self.claw_hanoi_pb)
        self.slider_hanoi_vertical = QSlider(Qt.Horizontal, self)

        self.slider_hanoi_vertical.setMaximum(5)
        self.slider_hanoi_vertical.setValue(2)
        layout_vertical.addWidget(self.slider_hanoi_vertical)
        self.label_hanoi_vertical = QLabel("0", self)
        layout_vertical.addWidget(self.label_hanoi_vertical)
        layout_v.addLayout(layout_buttons)
        layout_v.addLayout(layout_vertical)
        layoutv.addLayout(layout_v)
        self.update_label_hanoi_vertical()

        # Connect the slider's valueChanged signal to the update_label slot
        self.slider_claw.valueChanged.connect(self.update_label_claw)
        self.slider_rotate.valueChanged.connect(self.update_label_rotate)
        self.slider_fb.valueChanged.connect(self.update_label_fb)
        self.slider_ud.valueChanged.connect(self.update_label_ud)
        self.slider_hanoi_vertical.valueChanged.connect(self.update_label_hanoi_vertical)

        self.left_hanoi_pb.pressed.connect(self.left_hanoi_pressed)
        self.center_hanoi_pb.pressed.connect(self.center_hanoi_pressed)
        self.right_hanoi_pb.pressed.connect(self.right_hanoi_pressed)
        self.claw_hanoi_pb.pressed.connect(self.claw_hanoi_pressed)

        self.setLayout(layoutv)

    def update_label_claw(self):
        value = self.slider_claw.value()
        self.label_claw.setText(f"{value}")
        self.write_to_arduino((str(value)+"\n").encode())

    def update_label_rotate(self):
        value = self.slider_rotate.value()
        self.label_rotate.setText(f"{value}")
        self.write_to_arduino((str(value+200)+"\n").encode())

    def update_label_fb(self):
        value = self.slider_fb.value()
        self.label_fb.setText(f"{value}")
        self.write_to_arduino((str(value+400)+"\n").encode())

    def update_label_ud(self):
        value = self.slider_ud.value()
        self.label_ud.setText(f"{value}")
        self.write_to_arduino((str(value+600)+"\n").encode())

    def update_label_hanoi_vertical(self):
        value = self.slider_hanoi_vertical.value()
        self.label_hanoi_vertical.setText(f"{value}")

    def left_hanoi_pressed(self):
        print("left")

    def center_hanoi_pressed(self):
        print("center")

    def right_hanoi_pressed(self):
        print("right")
    
    def claw_hanoi_pressed(self):
        print("claw")

    def write_to_arduino(self, command):
        print(command)
        #self.to_arduino.write(command)
        #data = self.to_arduino.read()
        #print(data)



def main():
    app = QApplication(sys.argv)
    window = SliderApp()
    window.show()
    sys.exit(app.exec_())
    window.to_arduino.close()

if __name__ == "__main__":
    main()
    

