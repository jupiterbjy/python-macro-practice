import Macro


class VariableMixin:
    variables = {}


class Base:
    """
    Defines minimum interfaces that subclasses need to function.
    Override action, reset, serialize and deserialize when necessary.
    """

    # https://stackoverflow.com/questions/30849383/
    # meaning-of-the-super-keyword-in-the-parent-class-python

    def __init__(self):
        super(Base, self).__init__()  # Refer above link for this call
        self.name = ""
        self.next = None  # Assign next object here when running.
        self.onSuccess = None
        self.onFail = None
        self.screenArea = None

    def __repr__(self):
        msg = f"{type(self).__name__} instance <{self.name}>\n"
        properties = [f"┠─{k}: {v}" for k, v in self.__dict__.items()]

        return msg + "\n".join(properties) + "\n"

    def setName(self, text):
        self.name = str(text)

    def run(self):
        Macro.checkAbort()

        if self.action():

            if self.onSuccess is None:
                return self.next

            return self.onSuccess

        if self.onFail is None:
            return self.next

        return self.onFail

    def action(self):
        return True

    def setArea(self, x1, y1, x2, y2):
        self.screenArea = ImageModule.Area(x1, y1, x2, y2)

    def serialize(self):
        return self.__dict__

    def deserialize(self):
        pass

    def reset(self):
        self.screenArea = None

    def __iter__(self):
        return MethodIterator(self)


# --------------------------------------------------------


class ClickMixin:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """

    def __init__(self):
        self.target = ImageModule.Pos()
        self.clickCount = 1
        self.clickDelay = 0.01
        self.randomOffset = 0

    @property
    def finalPos(self, target=None):
        if target is None:
            target = self.target

        if self.randomOffset:
            out = ImageModule.RandomOffset(target, self.randomOffset)

        else:
            out = target

        return out()

    def clickBase(self, target=None):

        for i in range(self.clickCount):
            checkAbort()
            SLEEP_FUNCTION(self.clickDelay)
            pyautogui.click(self.finalPos(target))
            print(f"Click: {self.finalPos(target)}")
