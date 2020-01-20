from PySide2.QtCore import QObject, Signal, Slot, Property


class LoginController(QObject):
    loginSucceeded = Signal(bool)  # true if succeeded, false otherwise
    stateChanged = Signal()
    testSignal = Signal()

    def __init__(self, user_workflow_engine):
        print("login controller init")
        QObject.__init__(self)
        self._user_workflow_engine = user_workflow_engine

    @Slot(str)
    def log(self, message):
        print("From QML: " + message)

    @Slot(str)
    def loginRequested(self, username):
        # check the username. normally we'd want to call into the model but for the sake of simplicity, we'll do
        # everything in the controller
        if self._user_workflow_engine.try_login(username):
            # TODO switch to other view? Not sure what the best way to do this is...
            self.loginSucceeded.emit(True)
            self.stateChanged.emit()
            # for now, just update some text
            # we can also just switch to another page on a tab control... but it might be nice to have separate view
            # files for readability purposes
        else:
            self.loginSucceeded.emit(False)

    @Slot()
    def testSlot(self):
        self.testSignal.emit()

    @Property(str, notify=stateChanged)
    def statusText(self):
        return str(self._user_workflow_engine.state)

