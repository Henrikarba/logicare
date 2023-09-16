from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from animated_toggle import AnimatedToggle

app = QApplication([])

window = QWidget()

camera = AnimatedToggle()

camera.setFixedSize(camera.sizeHint())

keyboard = AnimatedToggle()

keyboard.setFixedSize(keyboard.sizeHint())

window.setLayout(QVBoxLayout())
window.layout().addWidget(QLabel("Toggle Camera"))
window.layout().addWidget(camera)
window.layout().addWidget(QLabel("Toggle Keyboard"))
window.layout().addWidget(keyboard)

camera_value = camera.isChecked()
keyboard_value = keyboard.isChecked()

print(keyboard_value, camera_value)

window.show()
app.exec()
