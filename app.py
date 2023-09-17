import sys
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QStackedWidget, QToolButton, QDialog, QSystemTrayIcon, QMenu
from animated_toggle import AnimatedToggle
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject, QProcess
from PyQt6.QtGui import QColor, QFont, QCursor, QIcon, QGuiApplication, QAction, QKeyEvent
from pynput import keyboard

# Set the global font
font = QFont("Brown Pro Light", 20)

# Define Logitech-inspired colors
blue = QColor("#04A5E5")
light_gray = QColor("#F4F3F4")
black = QColor("#080608")
lighter_black = QColor("#141214")
gray = QColor("#211F21")


def minimize_to_system_tray():
    # Allow clicking the system tray icon to restore the window
    app.setActiveWindow(None)
    main_window.hide()
    tray_icon.show()


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(window_width, window_height)
        self.setWindowTitle("LogiCare")
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {black.name()};
                font-size: 20px;
                color: {light_gray.name()};
            }}
        """)

        # Create a stacked widget to manage layouts
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Main Layout
        ToSettings = QToolButton()
        ToSettings.setIcon(QIcon("settings.png"))
        ToSettings.setIconSize(QSize(24, 24))
        ToSettings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout1 = QVBoxLayout()
        label1 = QLabel("This is Layout 1")
        ToSettings.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(1))
        layout1.addWidget(
            ToSettings, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        layout1.addWidget(label1)

        widget1 = QWidget()
        widget1.setLayout(layout1)

        # Create Layout 2
        camera = AnimatedToggle(checked_color=QColor(blue))
        camera.setFixedSize(camera.sizeHint())
        keyboard = AnimatedToggle(checked_color=QColor(blue))
        keyboard.setFixedSize(keyboard.sizeHint())
        mouse = AnimatedToggle(checked_color=QColor(blue))
        mouse.setFixedSize(mouse.sizeHint())

        camera.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        keyboard.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        mouse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Create the Submit button and connect it to the Submit function
        submit = QPushButton("Submit")
        submit.setStyleSheet(f"""
            QPushButton {{
                background-color: {blue.name()};
            }}
            QPushButton:hover {{
                color: rgba(244,243,244,0.5);
            }}
        """)

        submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # submit.clicked.connect()

        # Create a QVBoxLayout for the main window
        layout2 = QVBoxLayout()

        # labels
        label_main = QLabel("Choose Options")
        label_camera = QLabel("Toggle Camera")
        label_keyboard = QLabel("Toggle Keyboard")
        label_mouse = QLabel("Toggle Mouse")

        # label styling
        label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # layouts
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(label_camera)
        camera_layout.addWidget(camera)

        keyboard_layout = QHBoxLayout()
        keyboard_layout.addWidget(label_keyboard)
        keyboard_layout.addWidget(keyboard)

        mouse_layout = QHBoxLayout()
        mouse_layout.addWidget(label_mouse)
        mouse_layout.addWidget(mouse)

        backButton = QToolButton()
        backButton.setIcon(QIcon("arrow.png"))
        backButton.setIconSize(QSize(24, 24))
        backButton.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0))
        backButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Add labels, AnimatedToggle widgets, and the Submit button to the layout
        layout2.addWidget(
            backButton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout2.addWidget(label_main)
        layout2.addLayout(camera_layout)
        layout2.addLayout(keyboard_layout)
        layout2.addLayout(mouse_layout)
        layout2.addWidget(submit)

        widget2 = QWidget()
        widget2.setLayout(layout2)

        # Add both layouts to the stacked widget
        self.stacked_widget.addWidget(widget1)
        self.stacked_widget.addWidget(widget2)

        self.init_processes()

    def init_processes(self):
        self.tracking_p = QProcess()
        self.tracking_p.readyReadStandardOutput.connect(self.handle_stdout)
        self.tracking_p.readyReadStandardError.connect(self.handle_stdout)
        self.tracking_p.start("python", ["background_processes\\tracking.py"])

        self.webcam_p = QProcess()
        self.webcam_p.readyReadStandardOutput.connect(self.handle_stdout)
        self.webcam_p.readyReadStandardError.connect(self.handle_stdout)
        self.webcam_p.start("python", ["background_processes\\blink_yawn_detection.py"])

        self.analysis_p = QProcess()
        self.analysis_p.readyReadStandardOutput.connect(self.handle_stdout)
        self.analysis_p.start("python", ["background_processes\\analysis.py"])

    def handle_stdout(self):
        print(bytes(self.tracking_p.readAllStandardOutput()).decode("utf8"))
        print(bytes(self.tracking_p.readAllStandardError()).decode("utf8"))
        print(bytes(self.webcam_p.readAllStandardOutput()).decode("utf8"))
        print(bytes(self.webcam_p.readAllStandardError()).decode("utf8"))

        command = bytes(self.analysis_p.readAllStandardOutput()).decode("utf8")
        if command:
            show_custom_alert('Please take a break!')

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            # The delete button (Del) was pressed
            show_custom_alert("Delete button was pressed")
        else:
            # Handle other key events
            super().keyPressEvent(event)


class Alert(QDialog):
    def __init__(self, message, duration=30000):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint)

        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        self.setLayout(layout)

        self.setStyleSheet(f"""
            background-color: {black.name()};
            color: {light_gray.name()};
            font-size: 20px;
        """)

        self.setFixedHeight(100)  # Adjust the height as needed
        self.setFixedWidth(200)  # Adjust the width as needed

        # Move the alert to the bottom right corner
        self.move_to_bottom_right()

        # Automatically close the alert after a certain duration
        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.close)
        self.close_timer.start(duration)

    def move_to_bottom_right(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        self.setGeometry(
            screen_geometry.width() - self.width(),
            screen_geometry.height() - self.height(),
            self.width(),
            self.height(),
        )


def show_custom_alert(message="Error: No call message"):
    alert = Alert(message)
    alert.exec()


class KeyPressSignal(QObject):
    key_pressed = pyqtSignal()


key_press_signal = KeyPressSignal()


def key_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


def on_key_press(key):
    if key == keyboard.Key.delete:
        key_press_signal.key_pressed.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(font)

    # Set the window size (width, height)
    screen = app.primaryScreen()
    # Calculate the size for the window (half the screen size)
    window_width = int(screen.size().width() / 2)
    window_height = int(screen.size().height() / 2)

    main_window = MyMainWindow()
    main_window.show()

    # Store the main window reference in the app
    app.main_window = main_window

    # Minimize the application to the system tray
    main_window.hide()

    # Create the system tray icon after creating the main window
    tray_icon = QSystemTrayIcon(QIcon("icon.png"))
    tray_icon.setToolTip("LogiCare")

    # Create a menu for the system tray icon
    tray_menu = QMenu()

    # Add an action to restore the main window
    restore_action = QAction("Restore", tray_icon)
    restore_action.triggered.connect(
        lambda: main_window.showNormal())  # Corrected connection
    tray_menu.addAction(restore_action)

    # Add an action to exit the application
    exit_action = QAction("Exit", tray_icon)
    exit_action.triggered.connect(app.quit)
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)

    tray_icon.show()

    # Create a separate thread for keypress monitoring
    key_listener_thread = threading.Thread(target=key_listener)
    # This allows the thread to exit when the main program exits
    key_listener_thread.daemon = True
    key_listener_thread.start()

    # Connect the custom signal to the alert function
    key_press_signal.key_pressed.connect(
        lambda: show_custom_alert("Please consider taking a break or getting some rest"))

    sys.exit(app.exec())
