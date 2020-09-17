import sys
from pathlib import Path
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QUrl
from source.ui.qml.controllers.simple_daq_controllers import LoginController
from source.backend.application_parameters.application_parameters import LocalFileParameters
from source.backend.engines.user_workflow_engine import UserWorkflowEngine


if __name__ == '__main__':
    # load up the model (which consists of a number of engines)
    # LocalFileParameters.initialize()
    workflow_engine = UserWorkflowEngine(LocalFileParameters)

    # initialize the controllers
    app = QGuiApplication(sys.argv)
    qml_engine = QQmlApplicationEngine()
    ctlr = LoginController(workflow_engine)
    context = qml_engine.rootContext()
    context.setContextProperty("controller", ctlr)

    # load up view(s)?
    # qml_file = Path("../ui/qml_views/simple_login_screen.qml").resolve()
    qml_file = Path("../ui/qml_views/simple_daq_app_example.qml").resolve()
    qml_engine.load(QUrl.fromLocalFile(str(qml_file.absolute())))

    if not qml_engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
