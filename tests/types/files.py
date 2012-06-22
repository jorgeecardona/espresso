import unittest
from mock import patch
from mock import call
from StringIO import StringIO

from espresso.providers import FileProvider


class TestFileType(unittest.TestCase):

    def setUp(self):
        " Mock the basic of the library."

        def assert_existing_file(s, path):
            if path in self.existing_files:
                return True
            raise Exception("File doesn't exists")

        # Create mocks
        self.mock_set = patch.object(FileProvider, 'set')
        self.mock_assert_existing_file = patch.object(
            FileProvider, 'assert_existing_file')
        self.mock_chown = patch.object(FileProvider, 'chown')

        # Start mocks
        self.provider_chown = self.mock_chown.start()
        self.provider_set = self.mock_set.start()
        self.provider_assert_existing_file = \
            self.mock_assert_existing_file.start()

        # Define behavior
        self.provider_assert_existing_file.return_value = True

    def tearDown(self):
        self.mock_set.stop()
        self.mock_assert_existing_file.stop()
        self.mock_chown.stop()

    def test_set_content(self):
        " Set the content of a path."

        from espresso.types import File

        f = File('/tmp/coffee', content='Delicious!')
        f.apply()

        # Check the calls to the provider.
        self.provider_set.assert_called_once_with(
            path='/tmp/coffee', content='Delicious!')

    def test_set_owner(self):
        " Set the owner of a file path."

        from espresso.types import File

        f = File('/tmp/coffee', owner='root')
        f.apply()

        # Check the calls to the provider.
        self.provider_chown.assert_called_once_with(
            path='/tmp/coffee', owner='root', group=None)

    def test_set_group(self):
        " Set the group of a file path."

        from espresso.types import File

        f = File('/tmp/coffee', group='barista')
        f.apply()

        # Check the calls to the provider.
        self.provider_chown.assert_called_once_with(
            path='/tmp/coffee', group='barista', owner=None)

    def test_set_content_with_yaml(self):
        " Set the content of a path."

        stream = StringIO("""
!File
path: /tmp/coffee
content: Delicious!
""")

        from espresso.barista import Barista
        b = Barista()
        b.brew(stream)

        # Check the calls to the provider.
        self.provider_set.assert_called_once_with(
            path='/tmp/coffee', content='Delicious!')

    def test_set_owner_with_yaml(self):
        " Set the ownership of a path with yaml"

        stream = StringIO("""

 - !File
   path: /tmp/coffee1
   owner: root

 - !File
   path: /tmp/coffee2
   group: baristas

""")

        from espresso.barista import Barista
        b = Barista()
        b.brew(stream)

        # Check the calls to the provider.
        self.assertIn(
            call(path='/tmp/coffee1', owner='root', group=None),
            self.provider_chown.call_args_list)

        self.assertIn(
            call(path='/tmp/coffee2', owner=None, group='baristas'),
            self.provider_chown.call_args_list)
