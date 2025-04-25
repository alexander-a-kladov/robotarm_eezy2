#!/usr/bin/python3


import sys, serial
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class RecordState():
    def __init__(self):
        self.columns = dict()
        self.columns["left"] = list()
        self.columns["center"] = list()
        self.columns["right"] = list()
        self.claws = dict()

        for key in self.columns.keys():
            for r in range(0,6):
                self.columns[key].append(None)
    
    def set_claw(self, claw, value):
        self.claws[claw] = value

    def set_row(self, column, row, values):
        self.columns[column][row] = values
    
    def get_values(self, column, row):
        if self.columns[column]:
            return self.columns[column][row]
        return None
    
    def init_record(self):
        self.record = list()
        self.index = -1
    
    def add_record(self, column, row, claw):
        self.record.append((column,row,claw))

    def get_next_record(self):
        if self.index < len(self.record):
            self.index += 1
            return self.record[self.index]
        return None


class SliderApp(QWidget):
    def __init__(self):
        super().__init__()
        #self.to_arduino = serial.Serial('/dev/ttyUSB0', 9600)
        self.record_state = RecordState()
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
        self.claw_hanoi_pb.setCheckable(True)
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

        layout_buttons = QHBoxLayout()
        self.calibrate_pb = QPushButton("Calibrate")
        self.calibrate_pb.setCheckable(True)
        self.record_pb = QPushButton("Record")
        self.record_pb.setCheckable(True)
        self.play_pb = QPushButton("Play")
        self.play_pb.setCheckable(True)
        self.reverse_pb = QPushButton("Reverse")
        self.reverse_pb.setCheckable(True)
        layout_buttons.addWidget(self.calibrate_pb)
        layout_buttons.addWidget(self.record_pb)
        layout_buttons.addWidget(self.play_pb)
        layout_buttons.addWidget(self.reverse_pb)
        layoutv.addLayout(layout_buttons)

        # Connect the slider's valueChanged signal to the update_label slot
        self.slider_claw.valueChanged.connect(self.update_label_claw)
        self.slider_rotate.valueChanged.connect(self.update_label_rotate)
        self.slider_fb.valueChanged.connect(self.update_label_fb)
        self.slider_ud.valueChanged.connect(self.update_label_ud)
        self.slider_hanoi_vertical.valueChanged.connect(self.update_label_hanoi_vertical)

        self.left_hanoi_pb.pressed.connect(self.left_hanoi_pressed)
        self.center_hanoi_pb.pressed.connect(self.center_hanoi_pressed)
        self.right_hanoi_pb.pressed.connect(self.right_hanoi_pressed)
        self.claw_hanoi_pb.toggled.connect(self.claw_hanoi_toggled)

        self.calibrate_pb.pressed.connect(self.calibrate_pressed)
        self.record_pb.pressed.connect(self.record_pressed)
        self.play_pb.pressed.connect(self.play_pressed)
        self.reverse_pb.pressed.connect(self.reverse_pressed)

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

    def get_values(self):
        value1 = self.slider_rotate.value()
        value2 = self.slider_fb.value()
        value3 = self.slider_ud.value()
        value4 = self.slider_claw.value()
        return (value1, value2, value3, value4)

    def left_hanoi_pressed(self):
        v1, v2, v3, v4 = self.get_values()
        if self.calibrate_pb.isChecked():
            self.record_state.set_row("left", self.slider_hanoi_vertical.value(), (v1, v2, v3))

    def center_hanoi_pressed(self):
        v1, v2, v3, v4 = self.get_values()
        if self.calibrate_pb.isChecked():
            self.record_state.set_row("center", self.slider_hanoi_vertical.value(), (v1, v2, v3))

    def right_hanoi_pressed(self):
        v1, v2, v3, v4 = self.get_values()
        if self.calibrate_pb.isChecked():
            self.record_state.set_row("right", self.slider_hanoi_vertical.value(), (v1, v2, v3))
    
    def claw_hanoi_toggled(self):
        _, _, _, claw = self.get_values()
        

    def calibrate_pressed(self):
        print(f"calibrate {self.calibrate_pb.isChecked()}")

    def record_pressed(self):
        print(f"record {self.record_pb.isChecked()}")
    
    def play_pressed(self):
        print("play")

    def reverse_pressed(self):
        print("reverse")

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
    

