import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine

# Optional: Force Material style globally
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"

app = QApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.load("ui.qml")  # Must be in the same directory

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
