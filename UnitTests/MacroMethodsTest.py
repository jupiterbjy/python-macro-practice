import MacroMethods
import unittest


def TestCaseGenerate():
    out = []
    for method in MacroMethods.class_dict.values():
        out.append(method())

    MacroMethods.SetNext(out)
    return out


class BaseInterfaceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_case = TestCaseGenerate()

    def test_IterationTest(self):
        result = [i for i in self.test_case[0]]
        self.assertEqual(self.test_case, result)

    # def test_reset(self):
    #     origial = [i.__dict__ for i in self.test_case]
    #     reset = [i.reset()]


if __name__ == '__main__':
    unittest.main()
