import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget,QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, pyqtSlot, QFile, QTextStream, QTimer, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QColor,QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5 import QtGui,QtCore,QtSvg

import cv2
from threadGUI import ThreadGUI
import numpy as np

from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI, qfi_VSI, qfi_TC
import math

from sidebar import Ui_MainWindow as Ui_Mainwindow_sidebar
from splash import Ui_MainWindow

from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
## ==> GLOBALS

counter = 0



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui1 = Ui_Mainwindow_sidebar()
        self.ui1.setupUi(self)
        self.setWindowTitle("GRAVITEAM")

        #self.ui1.adi.setRoll(10)
        #self.ui1.adi.setPitch(20)

        # ADD ADI
        self.adi = qfi_ADI.qfi_ADI(self)
        self.adi.resize(240, 240)
        self.adi.reinit()
        self.adi.setParent(self.ui1.ADI_frame)

        # ADD HSI
        self.hsi = qfi_HSI.qfi_HSI(self)
        self.hsi.resize(240, 240)
        self.hsi.reinit()
        self.hsi.setParent(self.ui1.HSI_frame)

        # ADD SI
        self.si = qfi_SI.qfi_SI(self)
        self.si.resize(240, 240)
        self.si.reinit()
        self.si.setParent(self.ui1.SI_frame)

        #loadJsonStyle(self, self.ui)
        self.ui1.full_menu_widget.hide()
        self.ui1.profile_widget.hide()
        self.ui1.stackedWidget.setCurrentIndex(0)
        self.ui1.homeBtn.setChecked(True)
        self.vertical_scrollbar = self.ui1.console_home.verticalScrollBar()

        # Dikey kaydırma çubuğunu en aşağıya taşı
        self.vertical_scrollbar.setValue(self.vertical_scrollbar.maximum())

        self.disply_width = 640
        self.display_height = 480
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.ui1.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    

    def on_homeBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(0)
        self.vertical_scrollbar.setValue(self.vertical_scrollbar.maximum())

    def on_mapsBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(1)

    def on_terminalBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(5)
    
    def on_settingsBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(2)
    
    def on_infoBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(3)

    def on_helpBtn_toggled(self):
        self.ui1.stackedWidget.setCurrentIndex(4)



class SplashScreen(QMainWindow):
    def __init__(self):
        super(SplashScreen,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #REMOVE TITLE BAR

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #DROP SHADOW EFECT

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 90))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
    
        #QTIMER ==> START
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

         # Initial Text
        self.ui.label_2_description.setText("<strong>WELCOME</strong> TO MY APPLICATION")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_2_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_2_description.setText("<strong>LOADING</strong> USER INTERFACE"))


    def progress(self):
        global counter


        #SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        #CLOSE SPLASH SCREEN AND OPEN APP
        if counter >100:
            #STOP TIMER
            self.timer.stop()
            self.window=MainWindow()
            self.window.show()
            #CLOSE SPLASH SCREEN
            self.close()

        counter +=1


if __name__=="__main__":
    app = QApplication(sys.argv)

    window=SplashScreen()
    window.show()
    sys.exit(app.exec())