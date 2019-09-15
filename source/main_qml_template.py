import sys
from pathlib import Path
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QUrl
from source.ui.controllers.controller_template import TemplateController
from source.application_parameters.application_parameters import LocalFileParameters
from .engines.user_workflow_engine import UserWorkflowEngine


if __name__ == '__main__':
    # load up the model (which consists of a number of engines)
    # TODO find some solid dependency injection framework to place dependencies into the engines
    workflow_engine = UserWorkflowEngine(LocalFileParameters)


    # initialize the controllers
    qml_engine = QQmlApplicationEngine()
    ctlr = TemplateController()
    context = qml_engine.rootContext()
    context.setContextProperty("controller", ctlr)

    # load up view(s)?
    qml_file = Path("./ui/qml_views/simple_daq_application.qml")
    qml_engine.load(QUrl.fromLocalFile(str(qml_file.absolute())))

    if not qml_engine.rootObjects():
        sys.exit(-1)

    app = QGuiApplication(sys.argv)
    sys.exit(app.exec_())
