from PySide2.QtCore import QObject, Signal, Slot, Property


class Controller(QObject):
    boldChanged = Signal(bool)
    italicChanged = Signal(bool)
    underlineChanged = Signal(bool)
    sizeChanged = Signal(int)

    def __init__(self):
        QObject.__init__(self)
        self._color = "Black"
        self._italic = False
        self._bold = False
        self._underline = False
        self._size = 16

    @Property(int, notify=sizeChanged)
    def size(self):
        return self._size

    @size.setter
    def setSize(self, value):
        if self._size != value:
            self._size = value
            self.sizeChanged.emit(self._size)

    @Property(bool, notify=boldChanged)
    def bold(self):
        return self._bold

    @bold.setter
    def setBold(self, value):
        if self._bold != value:
            self._bold = value
            self.boldChanged.emit(self._bold)

    @Property(bool, notify=italicChanged)
    def italic(self):
        return self._italic

    @italic.setter
    def setItalic(self, value):
        if self._italic != value:
            self._italic = value
            self.italicChanged.emit(self._italic)

    @Property(bool, notify=underlineChanged)
    def underline(self):
        return self._underline

    @underline.setter
    def setUnderline(self, value):
        if self._underline != value:
            self._underline = value
            self.underlineChanged.emit(self._underline)

    @Slot()
    def toggleBold(self):
        self.setBold(not self.bold)

    @Slot()
    def toggleItalic(self):
        self.setItalic(not self.italic)

    @Slot()
    def toggleUnderline(self):
        self.setUnderline(not self.underline)

    @Slot()
    def clearStyle(self):
        self.setBold(False)
        self.setItalic(False)
        self.setUnderline(False)

    # The slot decorator takes the argument's type and the return type
    @Slot(str, result=str)
    def getColor(self, color_name):
        if color_name.lower() == "red":
            return "#ef9a9a"
        elif color_name.lower() == "green":
            return "#a5d6a7"
        elif color_name.lower() == "blue":
            return "#90caf9"
        else:
            return "Black"
