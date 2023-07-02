# -*- coding: utf-8 -*-
import random
from builtins import len

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

import EventListener
import FileManagement
import tracker


# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        while self._run_flag:
            self.msleep(10)
            if 0 < len(EventListener.EventListener.current_frames) and EventListener.EventListener.index < len(
                    EventListener.EventListener.current_frames):
                img = EventListener.EventListener.current_frames[EventListener.EventListener.index].copy()
                if not EventListener.EventListener.tracked:
                    cv2.rectangle(img, (EventListener.EventListener.x, EventListener.EventListener.y), (
                        EventListener.EventListener.x + EventListener.EventListener.w,
                        EventListener.EventListener.y + EventListener.EventListener.h), (255, 0, 0), 2)
                self.change_pixmap_signal.emit(img)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class Ui_MainWindow(QWidget):
    def setupUi(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.exportBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exportBtn.setGeometry(QtCore.QRect(1080, 600, 180, 80))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        self.exportBtn.setFont(font)
        self.exportBtn.setObjectName("pushButton")
        self.exportBtn.clicked.connect(self.export)
        self.trackBtn = QtWidgets.QPushButton(self.centralwidget)
        self.trackBtn.setGeometry(QtCore.QRect(1080, 500, 180, 80))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        self.trackBtn.setFont(font)
        self.trackBtn.setObjectName("pushButton_3")
        self.trackBtn.clicked.connect(self.track)
        self.selectROI = QtWidgets.QPushButton(self.centralwidget)
        self.selectROI.setGeometry(QtCore.QRect(1080, 400, 180, 80))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        self.selectROI.setFont(font)
        self.selectROI.setObjectName("pushButton_4")
        self.selectROI.clicked.connect(self.roi)
        self.importBtn = QtWidgets.QPushButton(self.centralwidget)
        self.importBtn.setGeometry(QtCore.QRect(20, 10, 200, 680))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        self.importBtn.setFont(font)
        self.importBtn.setObjectName("pushButton_2")
        self.importBtn.clicked.connect(self.import_)
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(1080, 50, 180, 30))
        self.l = QtWidgets.QSpinBox(self.centralwidget)
        self.l.setGeometry(QtCore.QRect(1080, 150, 180, 30))
        self.t = QtWidgets.QSpinBox(self.centralwidget)
        self.t.setGeometry(QtCore.QRect(1080, 200, 180, 30))
        self.w = QtWidgets.QSpinBox(self.centralwidget)
        self.w.setGeometry(QtCore.QRect(1080, 250, 180, 30))
        self.h = QtWidgets.QSpinBox(self.centralwidget)
        self.h.setGeometry(QtCore.QRect(1080, 300, 180, 30))
        self.fps = QtWidgets.QSpinBox(self.centralwidget)
        self.fps.setGeometry(QtCore.QRect(1080, 350, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.valueChanged.connect(self.val)
        self.l.setObjectName("left")
        self.l.valueChanged.connect(self.val_x)
        self.t.setObjectName("top")
        self.t.valueChanged.connect(self.val_y)
        self.w.setObjectName("width")
        self.w.valueChanged.connect(self.val_w)
        self.h.setObjectName("height")
        self.h.valueChanged.connect(self.val_h)
        self.fps.setObjectName("fps")
        self.fps.valueChanged.connect(self.val_fps)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1080, 25, 181, 30))
        self.label.setObjectName("label")
        self.label_l = QtWidgets.QLabel(self.centralwidget)
        self.label_l.setGeometry(QtCore.QRect(1080, 125, 181, 30))
        self.label_t = QtWidgets.QLabel(self.centralwidget)
        self.label_t.setGeometry(QtCore.QRect(1080, 175, 181, 30))
        self.label_w = QtWidgets.QLabel(self.centralwidget)
        self.label_w.setGeometry(QtCore.QRect(1080, 225, 181, 30))
        self.label_h = QtWidgets.QLabel(self.centralwidget)
        self.label_h.setGeometry(QtCore.QRect(1080, 275, 181, 30))
        self.label_fps = QtWidgets.QLabel(self.centralwidget)
        self.label_fps.setGeometry(QtCore.QRect(1080, 325, 181, 30))
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        main_window.show()

        self.videoThread = VideoThread()
        # connect its signal to the update_image slot
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.videoThread.start()

    def closeEvent(self, event):
        self.videoThread.stop()

    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MotionTrackrr"))
        self.exportBtn.setText(_translate("MainWindow", "Exporter la vidéo"))
        self.trackBtn.setText(_translate("MainWindow", "Tracker"))
        self.selectROI.setText(_translate("MainWindow", "Selectionner un ROI"))
        self.importBtn.setText(_translate("MainWindow", "Importer une vidéo"))
        self.label.setText(_translate("MainWindow", "Numéro de l\'image"))
        self.label_l.setText(_translate("MainWindow", "X"))
        self.label_t.setText(_translate("MainWindow", "Y"))
        self.label_w.setText(_translate("MainWindow", "largeur"))
        self.label_h.setText(_translate("MainWindow", "hauteur"))
        self.label_fps.setText(_translate("MainWindow", "fps"))

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        self.image_label.setGeometry(QtCore.QRect(230, 10, 850, 700))
        self.image_label.alignment()
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(850, 700, QtCore.Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def val(self):
        self.setIndex(self.spinBox.value())

    def val_x(self):
        EventListener.EventListener.x = self.l.value()
        self.update_pos()

    def val_y(self):
        EventListener.EventListener.y = self.t.value()
        self.update_pos()

    def val_w(self):
        EventListener.EventListener.w = self.w.value()
        self.update_pos()

    def val_h(self):
        EventListener.EventListener.h = self.h.value()
        self.update_pos()

    def val_fps(self):
        EventListener.EventListener.fps = self.fps.value()

    def update_pos(self):
        self.l.setMaximum(EventListener.EventListener.max_x - EventListener.EventListener.w)
        self.t.setMaximum(EventListener.EventListener.max_y - EventListener.EventListener.h)
        img = EventListener.EventListener.current_frames[EventListener.EventListener.index].copy()
        cv2.rectangle(img, (EventListener.EventListener.x, EventListener.EventListener.y), (
            EventListener.EventListener.x + EventListener.EventListener.w,
            EventListener.EventListener.y + EventListener.EventListener.h), (255, 0, 0), 2)
        self.update_image(img)

    @pyqtSlot()
    def import_(self):
        file = openFileNameDialog()
        EventListener.EventListener.tracked = False
        if file != "":
            FileManagement.FileManagement.files.clear()
            FileManagement.FileManagement.files.append(file)
            EventListener.EventListener.current_frames.clear()
            EventListener.EventListener.current_frames, fps = FileManagement.get_frames()
            EventListener.EventListener.fps = fps
            self.fps.setValue(fps)
            self.spinBox.setMaximum(len(EventListener.EventListener.current_frames))
            h, w, _ = cv2.cvtColor(EventListener.EventListener.current_frames[0], cv2.COLOR_BGR2RGB).shape
            EventListener.EventListener.max_x = w
            EventListener.EventListener.max_y = h
            EventListener.EventListener.max_w = w
            EventListener.EventListener.max_h = h
            self.l.setMaximum(w)
            self.t.setMaximum(h)
            self.w.setMaximum(w)
            self.h.setMaximum(h)

    @pyqtSlot()
    def track(self):
        tracker.track(EventListener.EventListener.current_frames[EventListener.EventListener.index], (
            EventListener.EventListener.x, EventListener.EventListener.y, EventListener.EventListener.w,
            EventListener.EventListener.h
        ))
        for index, frame in enumerate(EventListener.EventListener.current_frames):
            bbox = EventListener.EventListener.current_bbox[index]
            print(bbox)
            EventListener.EventListener.current_frames[index] = frame[bbox[1]:(bbox[1] + bbox[3]), bbox[0]:(bbox[0] + bbox[2])]
        EventListener.EventListener.tracked = True

    def roi(self):
        roi = cv2.selectROI(EventListener.EventListener.current_frames[EventListener.EventListener.index], True)
        EventListener.EventListener.x = roi[0]
        self.l.setValue(roi[0])
        EventListener.EventListener.y = roi[1]
        self.t.setValue(roi[1])
        EventListener.EventListener.w = roi[2]
        self.w.setValue(roi[2])
        EventListener.EventListener.h = roi[3]
        self.h.setValue(roi[3])

    @pyqtSlot()
    def export(self):
        dire = openDirNameDialog()
        if dire != "":
            rand = random.Random()
            FileManagement.extract(dire, rand.randint(100, 10000))
            QMessageBox.about(None, "Extraction", "Extraction terminée !")

    @pyqtSlot()
    def setIndex(self, index_):
        EventListener.EventListener.index = index_


def openFileNameDialog():
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                              "Vidéo Files (*.mp4 *.mov *.avi);;All Files (*)", options=options)
    return fileName


def openDirNameDialog():
    options = QFileDialog.Options()
    direr = QFileDialog.getExistingDirectory(None, "QFileDialog.getOpenFileName()", "", options=options)
    return direr


def openFileNamesDialog():
    options = QFileDialog.Options()
    files, _ = QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileNames()", "",
                                            "Vidéo Files (*.mp4 *.mov *.avi);;All Files (*)", options=options)
    return files