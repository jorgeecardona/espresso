from unittest import TestCase
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

        
class StageTestCase(TestCase):

    def test_meta(self):

        from espresso.stage import Stage

        global variable

        class MyStage(Stage):

            class Meta(object):
                name = 'my-stage'

            def run(self):
                global variable
                variable = 2
                return self._meta['name']

        class MySecondStage(Stage):
            
            class Meta(object):
                name = 'second'
                requires = MyStage()

            def run(self):
                return 1

        
        self.assertEqual(MyStage().run(), 'my-stage')

        variable = 1
        self.assertEqual(MySecondStage().run(), 1)
        self.assertEqual(variable, 2)
