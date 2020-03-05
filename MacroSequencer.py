# python 3.8 add := in if statement
from MacroMethods import Actions

# TODO: convert into coroutine
# TODO: convert into
# Deprecated

class sequence:
    def __init__(self, file=None, undo_max=5):
        self.seq = [[] for i in range(undo_max)]  # [0] will be primary
        self.undo_max = undo_max
        if file:
            self.backup(file)

    def readfile(self, file):

        pass

    def writefile(self):
        for i in self.seq[0]:
            pass

    def run(self):

        def recurser(seq_list):     # not sure how deep this could go..
            current = 0

            for i in seq_list:

                if isinstance(i, Actions.LoopStart):
                    loop_info = i.action()

                    for _ in range(loop_info[2]):
                        recurser(seq_list[current:i.object.endOrder])
                i.action()
                current += 1

        recurser(self.seq[0])

    def backup(self, new):
        self.seq.insert(0, new)
        if self.seq.__len__() >= self.undo_max:
            self.seq.pop()

    def add(self):
        pass

    def Loop(self, start, end, counts):
        pass
