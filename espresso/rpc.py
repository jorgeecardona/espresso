import pkg_resources

class TaskProxy(object):

    def __init__(self, module_name):
		" Create a proxy to the task function or class."

        # Import object
		obj = __import__(module_name)

		# check if obj is callable.
		if callable(obj):
			self.fn = obj

	def run(self, args, kwargs):
		" Run the code."

        if self.fn is not None:
			res = self.fn(*args, **kwargs)


class TaskManager(object):

	tasks = {}

    def update_tasks(self):
		# Check for new tasks.

        reload(pkg_resources)

        for entry_point in pkg_resources.iter_entry_points('espresso.tasks'):

            if entry_point.name not in self.tasks:

                # Add the task.
                self.tasks[entry_point.name] = {
					'version': entry_point.dist.version,
					'task': TaskProxy(entry_point.module_name)
					}

			elif entry_point.dist.version != self.tasks[name]['version']:

                # Add the task.
                self.tasks[entry_point.name] = {
					'version': entry_point.dist.version,
					'task': TaskProxy(entry_point.module_name)
					}


	def run(self, name, args, kwargs):

        if name in self.tasks:
			return self.tasks[name]['task'].run(args, kwargs)

        raise Exception("Task not registered in espresso daemon.")
