import pyautogui
from copy import deepcopy
from collections import deque

from Toolset import MemberLoader
from Macro import Imaging, Bases, stoppable_sleep, DUMP


class Click(Bases.Base, Bases.ClickMixin):
    """
    Interface of Simple Click method.
    """

    def __init__(self):
        super().__init__()

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.clickBase(self.absPos)
        return True

    def serialize(self):
        self.target = self.target()
        return self.__dict__

    def deserialize(self):
        self.target = Imaging.Pos(*self.target)


class LoopStart(Bases.Base):
    """
    Placeholder for Loop. No special functionality is needed for loop start.
    """

    def __init__(self):
        super().__init__()

        self.name = ""
        self.next = None

    def action(self):
        return True


class LoopEnd(Bases.Base):
    """
    Implements Loop via setting next/onSuccess to LoopStart Object.
    Not for standalone usage.
    """

    def __init__(self):
        super().__init__()

        self.name = ""
        self.next = None
        self.loopCount = 3
        self.loopTime = 0
        self.idx = None  # Convenient variable

    def action(self):
        self.loopTime += 1
        return self.loopTime > self.loopCount

    def reset(self):
        self.screenArea = None
        self.loopTime = 0


class Wait(Bases.Base):
    """
    Using Asynchronous sleep for Qt.
    but will default to normal time.sleep in case this is used on CLI.
    """

    def __init__(self):
        super().__init__()
        self.delay = 0

    def action(self):
        stoppable_sleep(self.delay)
        return True


class Variable(Bases.Base, Bases.VariableMixin):
    """
    Class that trying to mimic what makes fRep different from plain macros.
    Creating Same-name Variable will overwrite existing variable.
    """

    _created_instances = 0
    _deleted_instances = 0

    def __init__(self):
        super().__init__()
        Variable._created_instances += 1
        self.name = "variable-" + str(type(self)._created_instances)
        self.value = 0

    def __del__(self):
        Bases.VariableMixin.variables.pop(self.name, None)

    def setValue(self, text):

        try:
            value = int(text)
        except ValueError:
            print("int failed, Passing to float")
            pass
        else:
            self.value = value
            return

        try:
            value = float(text)
        except ValueError:
            raise AttributeError("String is not convertible.")
        else:
            self.value = value

    def action(self):
        if self.name in Bases.VariableMixin.variables.keys():
            self.name += str(self._created_instances)

        Bases.VariableMixin.variables[self.name] = self.value
        return True


class ImageSearch(Bases.Base, Bases.ClickMixin, Bases.ImageMixin):
    """
    Find Image on given screen area.
    Can decide whether to click or not, or how much trials before fail.
    """

    def __init__(self):

        super().__init__()
        self.loopDelay = 0.2
        self.trials = 5

    def ImageSearch(self):
        self.matchPoint, self.capturedImage = Imaging.imageSearch(
            self.targetImage, self.screenArea.region, self.precision
        )

    def ImageSearchMultiple(self):
        for i in range(self.trials):
            self.ImageSearch()
            if self.matchPoint:
                break

            stoppable_sleep(self.loopDelay)

        if DUMP:
            self.DumpCaptured(bool(self.matchPoint))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint + Imaging.Pos(w // 2, h // 2)

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ImageSearchMultiple()

        if self.matchPoint:
            self.target.set(*self.ImageCenter)
            self.clickBase(self.absPos)

        return bool(self.matchPoint)

    def reset(self):
        self.screenArea = None
        self.target = Imaging.Pos()
        self.capturedImage = None


class SearchOccurrence(Bases.Base, Bases.ClickMixin, Bases.ImageMixin):
    """
    Counts occurrences of target image.
    Not solid about what then I should do.
    Expecting variable assign or clicking each occurrences.
    """

    def __init__(self):

        super().__init__()
        self.matchPoints = []
        self.matchCount = 0
        self.threshold = 0

    def ScanOccurrence(self):
        (
            self.matchCount,
            self.capturedImage,
            self.matchPoints,
        ) = Imaging.scanOccurrence(
            self.targetImage, self.screenArea.region, self.precision, self.threshold
        )

        if DUMP:
            self.DumpCaptured(bool(self.matchCount))

    @property
    def ImageCenter(self):
        w, h = self.targetImage.size
        return self.matchPoint + Imaging.Pos(w // 2, h // 2)

    @property
    def absPos(self):
        return self.screenArea.p1 + self.target

    def action(self):
        self.ScanOccurrence()
        if state := self.matchCount > 0:
            for p in self.matchPoints:
                self.matchPoint = p
                self.target.set(*self.ImageCenter)
                self.clickBase(self.absPos)

        return state

    def reset(self):
        self.screenArea = None
        self.matchCount = 0
        self.matchPoints = []
        self.capturedImage = None


class Drag(Bases.Base):
    """
    Drag from p1 to p2.
    """

    def __init__(self):
        super().__init__()

        self.p1 = Imaging.Pos()
        self.p2 = Imaging.Pos()

    @property
    def From(self):
        return self.p1 + self.screenArea.p1

    @property
    def To(self):
        return self.p2 + self.screenArea.p1

    def set(self, x1, y1, x2, y2):
        self.p1.set(x1, y1)
        self.p2.set(x2, y2)

    def action(self):
        pyautogui.moveTo(*self.From)
        pyautogui.dragTo(*self.To, button="left")
        return True

    def serialize(self):
        self.p1 = self.p1()
        self.p2 = self.p2()
        return self.__dict__

    def deserialize(self):
        self.p1 = Imaging.Pos(*self.p1)
        self.p2 = Imaging.Pos(*self.p2)


def Serializer(obj_list):
    """
    Manage serialization of objects and return serialized string.
    No serialization other than pickle works with object references.
    Therefore, I'm adding reference_list to map references of each objects.
    """
    obj_type = []
    out = []
    reference_list = [[] for _ in range(len(obj_list))]

    for idx, element in enumerate(obj_list):
        element.next = None
        obj_type.append(type(element).__name__)

        try:
            index = obj_list.index(element.onSuccess)
        except ValueError:
            reference_list[idx].append(None)
        else:
            reference_list[idx].append(index)

        try:
            index = obj_list.index(element.onFail)
        except ValueError:
            reference_list[idx].append(None)
        else:
            reference_list[idx].append(index)

        bak = (element.onFail, element.onSuccess)
        element.onFail, element.onSuccess = None, None

        out.append(deepcopy(element.serialize()))

        element.onFail, element.onSuccess = bak

    return {"type": obj_type, "data": out, "reference": reference_list}


def Deserializer(baked):
    """
    Deserialize given json-serialized file.
    error handling should happen outside of this function, where it is called.
    """
    out = []
    inject = deque(baked["data"])
    ref = baked["reference"]
    type_list = baked["type"]

    for obj in type_list:
        obj = class_dict[obj]()
        dict_source = inject.popleft()
        obj.__dict__.update(
            (k, dict_source[k]) for k in dict_source.keys() & obj.__dict__.keys()
        )
        out.append(obj)

    for obj in out:
        success_idx, fail_idx = ref.pop(0)

        try:
            obj.onSuccess = out[success_idx]
        except TypeError:
            obj.onSuccess = None

        try:
            obj.onFail = out[fail_idx]
        except TypeError:
            obj.onFail = None

        obj.deserialize()

    return out


blacklist = {"_", "Ex", "Abort", "deque", "Mixin"}
__all__ = MemberLoader.ListClass(__name__, blacklist=blacklist)
class_dict = MemberLoader.ListClass(__name__, blacklist=blacklist, return_dict=True)
