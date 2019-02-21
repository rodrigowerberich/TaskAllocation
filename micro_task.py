from functools import reduce

class MuTask:
    def __init__(self, name, mu_task_type, position, previous=None):
        self.name = name
        self.type = mu_task_type
        self.position = position
        self.previous = previous

    def __str__(self):
        if self.previous:
            return '[Mu'+str(self.name)+','+str(self.position)+','+str([ 'Mu'+task.name for task in self.previous])+']'
        else:
            return '[Mu'+str(self.name)+','+str(self.position)+']'

    def __repr__(self):
        return str(self)

    def get_all_pre_requisites(self):
        pre_requisites = []
        if self.previous is not None and self.previous is not []:
            pre_requisites += self.previous
            pre_requisites = reduce(lambda pre, task: pre+task.get_all_pre_requisites(), self.previous, pre_requisites)
        return pre_requisites

    def add_task_as_previous(self, mu_task):
        if self.previous is None:
            self.previous = []
        self.previous.append(mu_task)

    def add_tasks_as_previous(self, mu_tasks):
        if self.previous is None:
            self.previous = []
        self.previous += mu_tasks