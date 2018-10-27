import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QLineEdit, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap
from detect import detect, TOTAL
from detect_drowsiness import detect_drowsiness
from real_time_object_detection import  find_the_distance
import cv2
import flask
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db import find_user

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('login.ui', self)
        username = QLineEdit()
        username.show()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        password.show()
        self.loginButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        
        username = str(self.username.text())
        password = str(generate_password_hash(str(self.password.text())))

        print(self.username.text(), password)
        results = find_user(username, password)
        print(results)
        if results != None:
            self.close()
            self.child_win = Sharingan(username)
            self.child_win.setWindowTitle('Sharingan')
            self.child_win.show()
        else:
            self.child_win = Popup('incorrect password/username. Please Check it again !')
            self.child_win.setWindowTitle('Alert')
            self.child_win.show()    

class Popup(QMainWindow):
    def __init__(self, message):
        super(Popup, self).__init__()
        loadUi('popup.ui', self)
        self.messagePanel = self.messagePanel.setText(message)
        self.okButton.clicked.connect(self.okHandler)
        self.notOkButton.clicked.connect(self.notOkHandler)

    def okHandler(self):
        self.close()
    
    def notOkHandler(self):
        self.close()

class Sharingan(QMainWindow):
    def __init__(self, username):
        super(Sharingan, self).__init__()
        loadUi('sharingan.ui',self)
        self.username = self.username.setText("Hello " + username + ' . Hope you are as healthy as ever !')
        self.image = None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.actionLogout.triggered.connect(self.logout)

        ## Blink Detection
        self.blinkDetect.setCheckable(True)
        self.blinkDetect.toggled.connect(self.detect_webcam_blink)
        self.blink_detect = False

        ## Drowsiness Detection
        self.drowsinessDetect.setCheckable(True)
        self.drowsinessDetect.toggled.connect(self.detectDrowsiness)
        self.drowsiness_detect = False

        ## Posture Detection
        self.postureDetect.setCheckable(True)
        self.postureDetect.toggled.connect(self.detect_posture)
        self.posture_detect = False        

    def logout(self):
        self.close()
        self.child_win = Login()
        self.child_win.setWindowTitle('Sharingan')
        self.child_win.show()

    def detect_webcam_blink(self, status):
        if status:
            self.blinkDetect.setText('Stop Detection')
            self.blink_detect = True
        else :
            self.blinkDetect.setText('Blink Detect')
            self.blink_detect = False

    def detectDrowsiness(self, status):
        if status:
            self.drowsinessDetect.setText('Stop Detection')
            self.drowsiness_detect = True
        else:
            self.drowsinessDetect.setText('Drowsiness Detect')
            self.drowsiness_detect = False

    def detect_posture(self, status):
        if status:
            self.postureDetect.setText('Stop Detection')
            self.posture_detect = True
        else:
            self.postureDetect.setText('Posture Detect')
            self.posture_detect = False

    def start_webcam(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

        ## timer for the images
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(.01)

    def update_frame(self):
        ret, self.image = self.capture.read()
        self.image = cv2.flip(self.image, 1)

        if self.blink_detect:
            detected_image = detect(self.image)
            self.displayImage(detected_image, 1)
        else:
            self.displayImage(self.image, 1)

        if self.drowsiness_detect:
            detected_image = detect_drowsiness(self.image)
            self.displayImage(detected_image, 1)
        else:
            self.displayImage(self.image, 1)

        if self.posture_detect:
            detected_image = find_the_distance(self.image)
            self.displayImage(detected_image, 1)
        else:
            self.displayImage(self.image, 1)

    def stop_webcam(self):
        self.timer.stop()

    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

            outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            outImage = outImage.rgbSwapped()

            if window == 1:
                self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
                self.imgLabel.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.setWindowTitle('Sharingan')
    window.show()
    sys.exit( app.exec_() )
