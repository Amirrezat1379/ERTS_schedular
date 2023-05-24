from task_set import TaskSet
from task import Task
from scheduler import Scheduler
import printer, csv


if __name__ == '__main__':
    with open("tasks_interrupts.csv", 'r') as file:
        csvFile = csv.reader(file)
        taskSet = TaskSet()
        for row in csvFile:
            priority, name, state, type, act_time, period, wcet, deadline = row
            if name != 'name':
                task = Task(
                    priority=int(priority),
                    name=name,
                    state=int(state),
                    type=int(type),
                    act_time=int(act_time),
                    period=int(period),
                    wcet=int(wcet),
                    deadline=int(deadline)
                )
                taskSet.set_tasks(task)
        file.close()
    sets = Scheduler(taskSet, 100)
    # sets.monotonic("R")
    # sets.monotonic("D")
    # sets.EDF("preemptive")
    sets.EDF("non_preemptive")
    printer.printer(sets)
