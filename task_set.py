class TaskSet:
    """Task Set Class
    
    Attributes:
        tasks (list): List of Task objects
        utility (float): Utility of the task set
        self.feasible (bool): Whether the task set is feasible
    """
    def __init__(self):
        self.tasks = []

    def set_tasks(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks
    

