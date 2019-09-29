from PySide2.QtCore import QObject, Signal, Slot, Property


class LoginController(QObject):
    loginSucceeded = Signal()
    loginFailed = Signal()

    def __init__(self, user_workflow_engine):
        print("login controller init")
        QObject.__init__(self)
        self._user_workflow_engine = user_workflow_engine

    @Slot()
    def loginRequested(self, username):
        # check the username. normally we'd want to call into the model but for the sake of simplicity, we'll do
        # everything in the controller
        if self._user_workflow_engine.try_login(username):
            # TODO switch to other view? Not sure what the best way to do this is...
            # we can also just switch to another page on a tab control... but it might be nice to have separate view
            # files for readability purposes
            pass



