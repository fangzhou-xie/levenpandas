import os

module_path = os.path.dirname(__file__)


def testpath():
    return os.path.join(module_path, 'test.csv')
