import os

class Storage(object):
    """
    Storage
    =======

    This defines an abstract storage it can be a local storage, http, and so on.

    It works basically as a dict with __getitem__.

    """

    def __getitem__(self, name):
        raise ValueError("Storage's backend is not implemented yet.")


class DirectoryStorage(object):
    """
    Directory's storage
    ===================

    Lock for files in a list of directories in order.

    Example::

        from espresso.storage import DirectoryStorage
        import os
        
        storage = DirectoryStorage(['/tmp', '/home/user', os.path.dirname(__file__)])

        print storage['bridge.template']


    """

    def __init__(self, directories=[]):
        self.directories = directories

    def __getitem__(self, name):
        " Look for object."

        for directory in self.directories:
            if os.path.isdir(directory):
                if name in os.listdir(directory):
                    with open(os.path.join(directory, name)) as fd:
                        content = fd.read()
                    return content

        raise ValueError("The object doesn't exists in the storage.")
