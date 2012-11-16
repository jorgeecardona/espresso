from unittest import TestCase

class ImportTestCase(TestCase):
    
    def test_import(self):

        __import__('espresso')

