import pyautogui
from time import sleep, time
from math import cos, radians, sin
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainterPath, QRegion
from pyautogui import position
from sys import exit, argv
from PyQt6.QtWidgets import QApplication, QWidget
from ui import Ui_control_form
import threading

count = 0


class Control(QWidget, Ui_control_form):
    def __init__(self):
        super().__init__()
        global count
        self.movment = None
        self.running = True

        self.ui = Ui_control_form()
        self.ui.setupUi(self)

        # show the control window
        self.show()

        # Keep track of the running thread and its state
        self.thread = None
        self.thread_running = False
        self.ui.pushButton.clicked.connect(self.toggle_thread)

        self.ui.comboBox.currentIndexChanged.connect(self.style_change)
        self.ui.pushButton_2.clicked.connect(exit)
        # Initialize variables for handling window dragging
        self.draggable = False
        self.offset = None

        self.setWindowRounded(True)

    def setWindowRounded(self, rounded: bool):
        if rounded:
            # Create a rounded rectangle shape
            path = QPainterPath()
            rect = QRectF(self.rect())  # Create a QRectF object
            # Adjust the radii for smoother curves
            path.addRoundedRect(rect, 10, 10)  # Adjust the radius as needed
            # Create a region based on the shape
            region = QRegion(path.toFillPolygon().toPolygon())
            # Set the window mask to the rounded region
            self.setMask(region)
        else:
            # Reset the window mask
            self.setMask(QRegion())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Ensure MouseButton is used instead of Button
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:  # Ensure MouseButton is used instead of Button
            self.draggable = False
            self.offset = None

    def style_change(self):
        if self.ui.comboBox.currentIndex() == 0:
            app.setStyleSheet("")
            app.setStyle('Fusion')

        elif self.ui.comboBox.currentIndex() == 1:
            File = open("D:\cupi\gui\ElegantDark.qss", 'r')
            with File:
                qss = File.read()
                app.setStyleSheet(qss)

    def toggle_thread(self):
        # If the thread is running, stop it
        if self.thread_running:
            self.stop_thread()
        # Otherwise, start the thread
        else:
            self.start_thread()

    def start_thread(self):
        self.thread = threading.Thread(target=self.btnstart)
        self.thread.daemon = True
        self.running = True
        self.thread.start()
        self.thread_running = True

    def stop_thread(self):
        if self.thread_running:
            print(self.thread)
            self.running = False
            self.thread.join()
        self.thread_running = False

    def btnstart(self):
        global count
        count = 0
        savedpos = position()
        while self.running:
            try:
                if count > (int(self.ui.time_line.text()) * 20):  # break after 5sec
                    self.bot()
            except:
                break
            curpos = position()
            if savedpos != curpos:
                savedpos = curpos
                count = 0
            else:
                sleep(0.05)
                count += 1

    def bot(self):
        pyautogui.FAILSAFE = False
        global count
        # Radius
        R = 400
        # measuring screen size
        (x, y) = pyautogui.size()
        # locating center of the screen
        (X, Y) = pyautogui.position(x / 2, y / 2)
        # offsetting by radius
        pyautogui.moveTo(X + R, Y)
        stop_check = 0
        start = time()
        self.count = count
        while self.count > 0 and self.running:
            if self.ui.checkBox.isChecked():  # If mouse movment is checked
                for i in range(360):
                    # setting pace with a modulus
                    if pos_check_instance.StopCheck():
                        self.count = 0
                        while stop_check == 0 and self.running:
                            if pos_check_instance.ContinueCheck():
                                stop_check += 1
                        break
                    elif i % 6 == 0:
                        pyautogui.moveTo(X + R * cos(radians(i)), Y + R * sin(radians(i)))
                        if time() - start > 60:
                            pyautogui.press('volumedown')
                            # sleep(1)
                            pyautogui.press('volumeup')
                            # sleep(1)
                            start = time()
            else:
                if time() - start > 60:
                    pyautogui.press('volumedown')
                    # sleep(1)
                    pyautogui.press('volumeup')
                    # sleep(1)
                    start = time()


class PosCheck:
    def __init__(self):
        self.STOP_POINTS = [(0, 0)]
        self.CONTINUE_POINTS = [(0, 1079)]

    def StopCheck(self):
        if tuple(position()) in self.STOP_POINTS:
            return True

    def ContinueCheck(self):
        if tuple(position()) in self.CONTINUE_POINTS:
            return True


if __name__ == "__main__":
    app = QApplication(argv)
    app.setStyle('Fusion')
    control_window = Control()
    pos_check_instance = PosCheck()
    exit(app.exec())
