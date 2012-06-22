import pbs
import os
from functools import partial


class BaseProvider(object):
    """
    A provider has all the mechanism to make the type work, and the type has
    the 'policies' to use it.

    This should be also stateless.
    """


class PackageProvider(BaseProvider):
    " Provides the basic structure to install packages."

    aptitude = pbs.Command('aptitude')
    aptitude_install = partial(aptitude, '-y', 'install')
    aptitude_purge = partial(aptitude, '-y', 'purge')

    def install(self, name):
        " Install a package."
        self.aptitude_install(name)

    def purge(self, name):
        " Purge a package."
        self.aptitude_purge(name)


class FileProvider(BaseProvider):
    """
    Set the content, owner, and mode of files.
    """

    class PathIsDirectory(Exception):
        def __init__(self, path):
            Exception.__init__(
                self, "The path %s belongs to a directory." % (path, ))

    class FileDoesNotExists(Exception):
        def __init__(self, path):
            Exception.__init__(
                self, "The file at %s does not exists" % (path, ))

    def assert_existing_file(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                raise self.PathIsDirectory(path)
        else:
            raise self.FileDoesNotExists(path)

    def set(self, path, content, mode=None, owner=None):
        " Set the content of a file."

        self.assert_existing_file(path)

        with open(path, 'w') as fd:
            fd.write(content)

    def chown(self, path, owner=None, group=None):
        " Change owner of a path."

        owner = -1 if owner is None else owner
        group = -1 if group is None else group

        # We need an previously existing file.
        self.assert_existing_file(path)

        # Change owner.
        print owner, group
        os.chown(path, owner, group)


class TemplateProvider(BaseProvider):
    """

    We can add templates to a provider, then this provider must be alive
    during all the application process, since we can define templates and use
    them in the configuration or maybe we can search templates on a standard
    path.

    """

    templates = {}

    class DuplicatedTemplate(Exception):
        pass

    def register(self, name, content):
        " Register a template."

        if name in self.templates:
            raise self.DuplicatedTemplate(
                "The template %s was already defined." % (name, ))

        self.templates[name] = content
