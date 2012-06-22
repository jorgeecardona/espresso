import yaml
from types import File, BaseType


class FileTag(yaml.YAMLObject):
    yaml_tag = u'!File'

    def __new__(cls, path=None, content=None, owner=None, group=None):
        return File(path, content=content, owner=owner, group=group)


class Barista(object):

    def brew(self, stream=None, filename=None):
        " Read a single file and brew it."

        if stream != None:
            data = yaml.load(stream)

        elif filename != None:
            with open(filename) as fd:
                data = yaml.load(fd)

        self.apply(data)

    def apply(self, data):
        " Apply a set of types resolving its dependencies."

        if isinstance(data, BaseType):
            data = [data]

        for item in data:
            item.apply()
