from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt, QTimer, QObject, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QTextEdit, QWidget, QInputDialog, QLineEdit
import pyautogui
from pynput import keyboard


class MousePositionCapture(QObject):
    mouse_position_changed = Signal(int, int)
    capture_key_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self.capture_key = "."
        self.listener = None

    def start_capture(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def set_capture_key(self):
        input_dialog = QInputDialog()
        input_dialog.setInputMode(QInputDialog.TextInput)
        input_dialog.setWindowTitle("Change Key")
        input_dialog.setLabelText("Enter the new capture key:")
        input_dialog.setTextValue(self.capture_key)
        text_line_edit = input_dialog.findChild(QLineEdit)
        text_line_edit.setMaxLength(1)  # Limit input to one character

        if input_dialog.exec():
            new_key = input_dialog.textValue().lower()
            self.capture_key = new_key
            self.capture_key_changed.emit(self.capture_key)
            self.update_label()

    def capture_mouse_position(self):
        x, y = pyautogui.position()
        self.mouse_position_changed.emit(x, y)

    def on_key_press(self, key):
        if key == keyboard.KeyCode.from_char(self.capture_key):
            self.capture_mouse_position()

    def stop_capture(self):
        if self.listener:
            self.listener.stop()

    def update_label(self):
        self.capture_key_changed.emit(self.capture_key)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(250, 200)
        MainWindow.setStyleSheet("background-color:rgb(53,53,53)")
        style="background-color:rgb(200,200,200);color:rgb(0,0,0)"

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(11)
        font.setBold(True)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(30, 120, 180, 70))
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet(style)
        self.textEdit.setAlignment(Qt.AlignCenter)

        font1 = QFont()
        font1.setFamilies([u"Times New Roman"])
        font1.setPointSize(12)
        font1.setBold(True)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(30, 20, 180, 50))
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(style)

        font2 = QFont()
        font2.setFamilies([u"Times New Roman"])
        font2.setPointSize(14)
        font2.setBold(True)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 80, 180, 30))
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color:rgb(255,255,255)")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Change key", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Click (.) to capture", None))

    def update_label(self, capture_key):
        self.label.setText(QCoreApplication.translate("MainWindow", f"Click ({capture_key}) to capture", None))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.mouse_position_capture = MousePositionCapture()
        self.mouse_position_capture.mouse_position_changed.connect(self.update_mouse_position)
        self.mouse_position_capture.capture_key_changed.connect(self.update_label)

        self.ui.pushButton.clicked.connect(self.mouse_position_capture.set_capture_key)

        QTimer.singleShot(1000, self.start_mouse_position_capture)

    def start_mouse_position_capture(self):
        self.mouse_position_capture.start_capture()

    def update_mouse_position(self, x, y):
        self.ui.textEdit.append(f"X , Y = ( {x} , {y} )")

    def update_label(self, capture_key):
        self.ui.update_label(capture_key)

    def stop_mouse_position_capture(self):
        self.mouse_position_capture.stop_capture()

    def closeEvent(self, event):
        self.stop_mouse_position_capture()
        event.accept()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
