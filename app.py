from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from animated_toggle import AnimatedToggle
from PyQt6.QtGui import QColor, QFont

# Create the application instance
app = QApplication([])

# Create the main window
window = QWidget()

# Set the window size (width, height)
window.resize(400, 300)

# Set the global font
font = QFont("Brown Pro Light", 20)
app.setFont(font)


# Define Logitech-inspired colors
blue = QColor("#04A5E5")
light_gray = QColor("#F4F3F4")
black = QColor("#080608")
lighter_black = QColor("#141214")
gray = QColor("#211F21")

window.setStyleSheet(
    f"background-color: {black.name()}; font-size: 20px; color: {light_gray.name()}")

# Create AnimatedToggle widgets
camera = AnimatedToggle(checked_color=QColor(blue))
camera.setFixedSize(camera.sizeHint())
keyboard = AnimatedToggle(checked_color=QColor(blue))
keyboard.setFixedSize(keyboard.sizeHint())

# Define the Submit function


def Submit():
    camera_value = camera.isChecked()
    keyboard_value = keyboard.isChecked()
    print(camera_value, keyboard_value)


# Create the Submit button and connect it to the Submit function
submit = QPushButton("Submit")
submit.setStyleSheet(
    f"background-color: {blue.name()};")
submit.clicked.connect(Submit)

# Create a QVBoxLayout for the main window
layout = QVBoxLayout()

# Add labels, AnimatedToggle widgets, and the Submit button to the layout
layout.addWidget(QLabel("Toggle Camera"))
layout.addWidget(camera)
layout.addWidget(QLabel("Toggle Keyboard"))
layout.addWidget(keyboard)
layout.addWidget(submit)

# Set the layout for the main window
window.setLayout(layout)

# Show the main window
window.show()

# Start the application event loop
app.exec()
