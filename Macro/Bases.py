import pyautogui
from io import BytesIO
from base64 import b64decode, b64encode
from PIL import Image
from Macro import IMG_SAVER, Imaging, MethodIterator, check_event, stoppable_sleep


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

    def run(self):
        # not sure if checking EVENT frequently is good design choice.
        check_event()

        if self.action():

            if self.onSuccess is None:
                return self.next

            return self.onSuccess

        if self.onFail is None:
            return self.next

        return self.onFail

    def action(self):
        return True

    def setArea(self, p1, p2):
        self.screenArea = Imaging.Area.fromPos(p1, p2)

    def serialize(self):
        return self.__dict__

    def deserialize(self):
        pass

    def reset(self):
        self.screenArea = None

    def __iter__(self):
        return MethodIterator(self)


class ClickMixin:
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """

    def __init__(self):
        self.target = Imaging.Pos()
        self.clickCount = 1
        self.clickDelay = 0.01
        self.randomOffset = 0

    @property
    def finalPos(self, target=None):
        if target is None:
            target = self.target

        if self.randomOffset:
            out = Imaging.RandomOffset(target, self.randomOffset)

        else:
            out = target

        return out()

    def clickBase(self, target=None):

        for i in range(self.clickCount):
            stoppable_sleep(self.clickDelay)
            pyautogui.click(self.finalPos(target))
            print(f"Click: {self.finalPos(target)}")


class ImageMixin:
    """
    mixin class of all Macro classes dealing with image.
    """

    def __init__(self):
        super().__init__()

        self._targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.matchPoint = None  # expects pos object
        self.precision = 0.85

    def DumpCaptured(self, name=None):
        IMG_SAVER(self.capturedImage, str(name))

    def DumpTarget(self):
        IMG_SAVER(self.targetImage, self.targetName)

    @property
    def targetImage(self):
        return self._targetImage

    @targetImage.setter
    def targetImage(self, img):
        try:
            img.convert("RGB")

        except AttributeError:
            raise AttributeError("Onl PIL-type images are supported.")

        else:
            if img.format != "PNG":  # Non-png images has trouble with cv2 conversion

                byte_io = BytesIO()
                img.save(byte_io, "PNG")
                self._targetImage = Image.open(byte_io)

            else:
                self._targetImage = img

    def serialize(self):
        try:
            self.target = self.target()
        except AttributeError:
            pass

        buffer = BytesIO()
        self._targetImage.save(buffer, format="PNG")
        string = b64encode(buffer.getvalue())
        self._targetImage = string.decode("utf-8")
        buffer.close()

        return self.__dict__

    def deserialize(self):
        try:
            self.target = Imaging.Pos(*self.target)
        except AttributeError:
            pass
        except TypeError:
            print("Old value found, save file again for update.")
            if isinstance(self.target, dict):
                self.target = Imaging.Pos(self.target["x"], self.target["y"])
            else:
                raise Exception("File is damaged.")

        buffer = BytesIO()
        string = self._targetImage

        buffer.write(b64decode(string))
        self._targetImage = Image.open(buffer).copy()
        buffer.close()

    def reset(self):
        self.capturedImage = None
        self.matchPoint = None
