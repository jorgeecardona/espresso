from providers import PackageProvider, FileProvider


class BaseType(object):
    pass


class Package(BaseType):

    provider = PackageProvider()

    def __init__(self, name, ensure='installed'):
        self.name = name
        self.ensure = ensure

    def apply(self):
        " Apply the tag."

        if self.ensure == 'installed':
            self.provider.install(self.name)

        elif self.ensure == 'purged':
            self.provider.purge(self.name)


class File(BaseType):

    provider = FileProvider()

    def __init__(self, path, content=None, owner=None, group=None):
        self.path = path
        self.content = content
        self.owner = owner
        self.group = group

    def __repr__(self):
        msg = " - File on %s" % (self.path, )

        if self.content:
            msg += ", set content"

        if self.owner:
            msg += ", set owner to '%s'" % (self.owner, )

        if self.group:
            msg += ", set group to '%s'" % (self.group, )

        return msg

    def apply(self):
        " Apply a file tag is to set the content and permissions."

        # If content set the try to set it.
        if self.content != None:
            self.provider.set(path=self.path, content=self.content)

        # If owner and group set then try to chown,
        if self.owner != None or self.group != None:
            self.provider.chown(
                path=self.path, owner=self.owner, group=self.group)
