import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QStackedWidget, QToolButton, QMessageBox
from animated_toggle import AnimatedToggle
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QColor, QFont, QCursor, QIcon

# Set the global font
font = QFont("Brown Pro Light", 20)

# Define Logitech-inspired colors
blue = QColor("#04A5E5")
light_gray = QColor("#F4F3F4")
black = QColor("#080608")
lighter_black = QColor("#141214")
gray = QColor("#211F21")


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

        def Submit():
            camera_value = camera.isChecked()
            keyboard_value = keyboard.isChecked()
            mouse_value = mouse.isChecked()
            print(camera_value, keyboard_value, mouse_value)

        # Create the Submit button and connect it to the Submit function
        submit = QPushButton("Submit")
        submit.setStyleSheet(f"""
            QPushButton {{
                background-color: {blue.name()};
            }}
            QPushButton:hover {{
                color:rgba(244,243,244,0.5);
            }}
        """)

        submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        submit.clicked.connect(Alert)

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


def Alert():
    # Create a new instance of QMessageBox
    alert_box = QMessageBox()

    # Set the alert properties
    alert_box.setWindowTitle("Alert")
    alert_box.setText("Alert message")
    alert_box.setIcon(QMessageBox.Icon.Warning)
    alert_box.addButton("Got it", QMessageBox.ButtonRole.AcceptRole)

    # Apply styling to the alert box
    alert_box.setStyleSheet(f"""
        QMessageBox {{
            background-color: {black.name()};
            font-size: 20px;
            color: {light_gray.name()};
        }}
        QPushButton {{
            background-color: {blue.name()};
        }}
        QPushButton:hover {{
            color: rgba(244, 243, 244, 0.5);
        }}
    """)

    # Get the screen dimensions
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()

    # Calculate the position for the bottom-right corner
    alert_width = alert_box.width()
    alert_height = alert_box.height()
    x = screen_geometry.width() - alert_width
    y = screen_geometry.height() - alert_height

    # Set the alert box position
    alert_box.setGeometry(QRect(x, y, alert_width, alert_height))

    # Show the alert box
    alert_box.exec()


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
    sys.exit(app.exec())
