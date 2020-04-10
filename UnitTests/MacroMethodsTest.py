import MacroMethods
import unittest


def testcaseGenerate():
    out = []
    for method in MacroMethods.class_dict.values():
        out.append(method())

    MacroMethods.SetNext(out)
    return out


class BaseInterfaceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_case = testcaseGenerate()

    def test_IterationTest(self):
        result = [i for i in self.test_case[0]]
        self.assertEqual(self.test_case, result)


if __name__ == '__main__':
    unittest.main()
