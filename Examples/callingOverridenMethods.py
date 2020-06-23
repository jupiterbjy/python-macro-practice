# Demonstration of calling same methods in all superclasses.


class Base:
    def __init__(self):
        self.x = 10

    def add_it(self):
        print('running in Base!')
        self.x += 1


class Mixer:
    def add_it(self):
        print('running in Mixer!')
        self.x += 100


class Child(Base, Mixer):
    def __init__(self):
        super().__init__()
        self.x = 10

    def add_it(self):
        print('running in Child!')
        self.x += 10

    def all_add_it(self):
        self.add_it()
        for bases in Child.__bases__:
            try:
                bases.add_it(self)
            except AttributeError:
                pass


source = Child()
source.all_add_it()
print(source.x)
