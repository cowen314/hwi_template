import sys
import os.path
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QUrl
import controller

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    qml_engine = QQmlApplicationEngine()

    ctlr = controller.Controller()
    context = qml_engine.rootContext()
    context.setContextProperty("controller", ctlr)

    qml_file = os.path.join(os.path.dirname(__file__), "view.qml")
    qml_engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if not qml_engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
