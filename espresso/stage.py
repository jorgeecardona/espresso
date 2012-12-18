
class StageType(type):

    def __new__(cls, name, bases, attrs):
        
        # Check for meta-data in the Stage.
        meta = {}

        if 'Meta' in attrs:
            # Extract all data from the class and accept just the keys
            # that don't start with _.
            data = attrs.pop('Meta').__dict__.items()
            meta.update(dict((k,v) for k,v in data if not k.startswith('_')))
    
        # Add meta to the stage itself.
        attrs['_meta'] = attrs.get('_meta', {})
        attrs['_meta'].update(meta)

        # Decorate the run method.
        def run_decorator(method):
            def new_run(self, *args, **kwargs):
                
                # Ensure run all the requires.
                try:
                    requires = list(self._meta.get('requires', []))
                except TypeError:
                    requires = [self._meta.get('requires')]

                for require in requires:
                    require.run(*args, **kwargs)

                return method(self, *args, **kwargs)

            return new_run
            
        attrs['run'] = run_decorator(attrs.pop('run'))

        return super(StageType, cls).__new__(cls, name, bases, attrs)


class Stage(object):
    """
    Stage
    =====

    A stage will be the way to group different components in a description.

    It will help later to group components and to force a description.

    """

    __metaclass__ = StageType

    def run(self):
        raise NotImplementedError("This stage hasn't been implemented yet.")
    
