import pyautogui
from io import BytesIO
from base64 import b64decode, b64encode
from PIL import Image
from Macro import MethodIterator, stoppable_sleep, EnvVariables
from Macro.Imaging import Pos, Area, RandomOffset


class VariableMixin:
    # just a placeholder.
    variables = {}


class Protocol:
    def serialize(self):
        pass
        # raise NotImplementedError

    def deserialize(self):
        pass
        # raise NotImplementedError

    def reset(self):
        pass


class Base(Protocol):
    """
    Defines minimum interfaces that subclasses need to function.
    Override action, reset, serialize and deserialize when necessary.
    """

    env_var = EnvVariables()

    # https://stackoverflow.com/questions/30849383/
    # meaning-of-the-super-keyword-in-the-parent-class-python

    def __init__(self):
        super(Base, self).__init__()  # Refer above link for this call
        self.name = ""
        self.next = None  # Assign next object here when running.
        self.onSuccess = None
        self.onFail = None

    def __repr__(self):
        msg = f"{type(self).__name__} instance <{self.name}>\n"
        properties = [f"┠─{k}: {v}" for k, v in self.__dict__.items()]

        return msg + "\n".join(properties) + "\n"

    def run(self):
        # not sure if checking EVENT frequently is good design choice or not.
        self.env_var.check_event()

        if self.action():

            if self.onSuccess is None:
                return self.next

            return self.onSuccess

        if self.onFail is None:
            return self.next

        return self.onFail

    def action(self):
        return True

    def serialize(self):
        pass

    def deserialize(self):
        pass

    def reset(self):
        pass

    def __iter__(self):
        return MethodIterator(self)


class ScreenAreaMixin(Protocol):
    """
    Only adds screen info, for relative coordination.
    """
    env_var: EnvVariables

    @property
    def screenArea(self):
        return self.env_var.screen_area

    def reset(self):
        self.screenArea.set()

    # no need to serialize as class variable is not in __dict__

    @classmethod
    def set_pos_area(cls, p1: Pos, p2: Pos):
        cls.env_var.screen_area.from_pos(p1, p2)

    @classmethod
    def set_tuple_area(cls, x1, y1, x2, y2):
        cls.env_var.screen_area.set(x1, y1, x2, y2)


class ClickMixin(Protocol):
    """
    Super class for click operation.
    Separated from click object to prevent diamond inherit.
    """
    env_var: EnvVariables

    def __init__(self):
        super(ClickMixin, self).__init__()
        self.target = Pos()  # runtime-set value.
        self.hard_target = Pos()  # fixed, pre-set value.
        self.clickCount = 1
        self.clickDelay = 0.01
        self.randomOffset = 0

    @property
    def final_pos(self):
        target = self.hard_target if self.hard_target else self.target

        if self.randomOffset:
            out = RandomOffset(target, self.randomOffset)
        else:
            out = target

        return out.val

    def clickBase(self):

        for i in range(self.clickCount):
            pyautogui.click(self.final_pos)
            print(f"Click: {self.final_pos}")

            if i != self.clickCount - 1:
                stoppable_sleep(self.clickDelay, self.env_var.event)

    def serialize(self):
        self.hard_target = repr(self.hard_target)

    def deserialize(self):
        self.hard_target = Pos.from_string(self.hard_target)

    def reset(self):
        self.target.set()


class ImageMixin(Protocol):
    """
    mixin class of all Macro classes dealing with image.
    """
    env_var: EnvVariables

    def __init__(self):
        super(ImageMixin, self).__init__()

        self._targetImage = None
        self.targetName = None
        self.capturedImage = None
        self.precision = 0.85

    def DumpCaptured(self, name=None):
        self.env_var.img_saver(self.capturedImage, str(name))

    def DumpTarget(self):
        self.env_var.img_saver(self.targetImage, self.targetName)

    def set_target_image(self, img):
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

    @property
    def targetImage(self):
        return self._targetImage

    @targetImage.setter
    def targetImage(self, img):
        # Depreciated
        self.set_target_image(img)

    def serialize(self):

        buffer = BytesIO()
        self._targetImage.save(buffer, format="PNG")
        string = b64encode(buffer.getvalue())
        self._targetImage = string.decode("utf-8")
        buffer.close()

    def deserialize(self):

        buffer = BytesIO()
        string = self._targetImage

        buffer.write(b64decode(string))
        self._targetImage = Image.open(buffer).copy()
        buffer.close()

    def reset(self):
        self.capturedImage = None
