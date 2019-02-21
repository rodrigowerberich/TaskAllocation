from functools import reduce

class Task:
    def __init__(self, name, mu_tasks, priority, deadline):
        self.name = name
        self.mu_tasks = mu_tasks
        self.priority = priority
        self.deadline = deadline

    def __str__(self):
        return 'T'+str(self.name)

    def __repr__(self):
        return str(self)