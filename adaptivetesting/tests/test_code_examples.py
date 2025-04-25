import unittest


class TestCodeExamples(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_default_example(self):
        # read file
        with open("code_examples/example_default.py", "r") as file:
            content = file.read()
            file.close()

        exec(content)

    def test_semi_adaptive_example(self):
        # read file
        with open("code_examples/example_semi.py", "r") as file:
            content = file.read()
            file.close()

        exec(content)
