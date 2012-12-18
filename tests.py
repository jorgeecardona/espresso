from unittest import TestCase
import os
import tempfile
import shutil


class ImportTestCase(TestCase):
    
    def test_import(self):

        __import__('espresso')


class StorageTestCase(TestCase):

    def tearDown(self):

        # Delete any tempdir.
        for tempdir in getattr(self, '_delete_temporary_dirs', []):
            shutil.rmtree(tempdir)

    def test_directory_storage(self):
        " Test the directory storage."

        from espresso.storage import DirectoryStorage

        # Create a pair of tempfile.
        tempdir_1, tempdir_2 =  tempfile.mkdtemp(), tempfile.mkdtemp()
        
        # Remove this at the end.
        self._delete_temporary_dirs = [tempdir_1, tempdir_2]

        storage = DirectoryStorage([tempdir_1, tempdir_2])

        # Fail a lookup.
        with self.assertRaises(ValueError):
            storage['file']

        # Create file.
        fd = open(tempdir_2 + '/file', 'w')
        fd.write('content')
        fd.close()

        # Now lookup must work.
        self.assertEqual(storage['file'], 'content')

        # Create file.
        fd = open(tempdir_1 + '/file', 'w')
        fd.write('content in 1')
        fd.close()

        # Now lookup must work.
        # Respect order in lookup.
        self.assertEqual(storage['file'], 'content in 1')

        # Lookup of directory.
        os.mkdir(tempdir_1 + '/dir')
        self.assertEqual(storage['dir'], tempdir_1 + '/dir')

        
class StageTestCase(TestCase):

    def test_meta(self):

        from espresso.stage import Stage

        global checkpoint

        class MyStage(Stage):

            class Meta(object):
                name = 'my-stage'

            def run(self):
                global checkpoint
                checkpoint = 2
                return self._meta['name']

        class MySecondStage(Stage):
            
            class Meta(object):
                name = 'second'
                requires = MyStage()

            def run(self):
                return 1

        
        self.assertEqual(MyStage().run(), 'my-stage')

        checkpoint = 1
        self.assertEqual(MySecondStage().run(), 1)
        self.assertEqual(checkpoint, 2)

class HelpersTestCase(TestCase):

    def test_ensure_file(self):

        from espresso.helpers import fs

        fs.ensure_file('/tmp/espresso')

    def test_ensure_tree(self):

        # Create source tree.

        # Create a pair of tempfile.
        tempdir_1, tempdir_2 = tempfile.mkdtemp(), tempfile.mkdtemp()

        with open(tempdir_1 + '/file1', 'w') as fd:
            fd.write('content1')

        os.mkdir(tempdir_1 + '/dir')
        with open(tempdir_1 + '/dir/file2', 'w') as fd:
            fd.write('content2')

        from espresso.helpers import fs

        # Ensure tree.
        fs.ensure_tree(tempdir_2, tempdir_1)

        # Assert for existence of paths.
        self.assertTrue(os.path.exists(tempdir_2 + '/dir'))
        self.assertTrue(os.path.exists(tempdir_2 + '/file1'))
        self.assertTrue(os.path.exists(tempdir_2 + '/dir/file2'))

        # Asssert files and dirs
        self.assertTrue(os.path.isdir(tempdir_2 + '/dir'))
        self.assertTrue(os.path.isfile(tempdir_2 + '/file1'))
        self.assertTrue(os.path.isfile(tempdir_2 + '/dir/file2'))

        # Assert for content in files.
        with open(tempdir_2 + '/file1') as fd:
            self.assertEqual(fd.read(), 'content1')

        with open(tempdir_2 + '/dir/file2') as fd:
            self.assertEqual(fd.read(), 'content2')
