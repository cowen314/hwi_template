from PySide2 import QObject, Signal, Slot, Property


class LoginController(QObject):
    loginSucceeded = Signal()
    loginFailed = Signal()

    def __init__(self):
        QObject.__init__(self)

    @Slot
    def loginRequested(self, username):
        # check the username. normally we'd want to call into the model but for the sake of simplicity, we'll do
        # everything in the controller
        if username == "cowen":



