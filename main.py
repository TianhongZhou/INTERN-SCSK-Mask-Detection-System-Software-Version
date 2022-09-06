import sys
import ui
import logging
import datetime
import detectFace
import detectMask
import cv2
import tkinter as tk
from tkinter import filedialog
from logging import handlers
from PyQt5.QtWidgets import QApplication, QMainWindow


# global variables:
# count_time -- used for waiting for next detection
# index -- used for writing file
global count_time
count_time = 0
global index
index = 1
global api
cap = cv2.VideoCapture()

# level relations of log
level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}


# function to write log
def log(message, level='info'):
    # set basic log information
    filename = './logs/' + str(datetime.date.today()) + '.log'
    logger = logging.getLogger(filename)
    logger.setLevel(level_relations.get(level))
    fmt = logging.Formatter('%(asctime)s %(thread)d %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    # output to file
    file_handler = handlers.TimedRotatingFileHandler(filename=filename, when='D', backupCount=1, encoding='utf-8')
    file_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.info(message)
    logger.removeHandler(file_handler)


# function to select file
def select_file():
    root = tk.Tk()
    root.withdraw()
    filePath = filedialog.askopenfilename()
    return filePath


# detect using chosen API and show result
def detect_and_show_result(inputUI, address):
    global index
    if api == "Baidu":
        result = detectMask.baidu_API_fingMask(address)
    elif api == "JD":
        result = detectMask.jd_API_fingMask(address)
    elif api == "SNN":
        result = detectMask.snn_API_fingMask(address)

    inputUI.label_4.setText(result)
    inputUI.label_4.repaint()
    index += 1
    if index > 50:
        index = 1

    log(result, 'info')


# function to take photo manually
def take_photo(inputUI):
    global index
    ret, frame = cap.read()
    address = "./" + "manual_" + str(index) + ".jpg"
    cv2.imwrite(address, frame)

    detect_and_show_result(inputUI, address)


# function to open the camera and take photo manually
def open_camera_photo_manual(inputUI):
    # open camera
    cap.open(0)

    while 1:
        # read camera and show it on the screen
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Capture_Photo", frame)
            cv2.waitKey(1) & 0xFF
        else:
            break


# function to open the camera and take photo automatically
def open_camera_photo_auto(inputUI):
    # open camera
    cap.open(0)

    while 1:
        # read camera and show it on the screen
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Capture_Photo", frame)
            cv2.waitKey(1) & 0xFF
        else:
            break

        global count_time, api

        # if it is time to detect then detect face and save it
        if count_time % 50 == 0:
            detectFace.saveFaces(frame, inputUI, api)

        count_time += 1


# function to run
def run_all(inputUI):
    global api
    # choose API option
    if ui.comboBox_2.currentText() == "Baidu":
        api = "Baidu"
    elif ui.comboBox_2.currentText() == "SNN":
        api = "SNN"
    elif ui.comboBox_2.currentText() == "JD":
        api = "JD"

    # choose input option
    if ui.comboBox.currentText() == "Select file to detect":
        path = select_file()
        detect_and_show_result(inputUI, path)
    elif ui.comboBox.currentText() == "Open camera and Photo manually":
        open_camera_photo_manual(inputUI)
    elif ui.comboBox.currentText() == "Open camera and Photo automatically":
        open_camera_photo_auto(inputUI)


# function to close
def end_all():
    cv2.destroyAllWindows()
    cap.release()


# main function
if __name__ == '__main__':
    # initialization and set up
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = ui.Ui_faceDetect()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # pushButton to start and end
    ui.pushButton.clicked.connect(lambda: run_all(ui))
    ui.pushButton_2.clicked.connect(end_all)
    ui.pushButton_3.clicked.connect(lambda: take_photo(ui))

    sys.exit(app.exec())
