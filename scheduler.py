import copy
from task import * 
from colorama import Fore

class Scheduler:
    """Scheduler Class
    
    Attributes:
        task_set (TaskSet): Task set to be scheduled
    """
    def __init__(self, task_set, time_limit):
        self.task_set = task_set
        self.algorithm = ""
        self.time_limit = time_limit
        self.time = {}
        self.miss_task = 0
        self.free_time = 0

    def execute_task(self, task, current_time, ready_queue):
        task.state = 0
        task.wcet -= 1
        free = False
        self.time[current_time] = task.name
        if task.wcet == 0:
            ready_queue.remove(task)
        return task, ready_queue, free
        

    def EDF(self, eType):
        self.algorithm = "EDF_" + eType
        ready_queue = [task for task in self.task_set.tasks if task.state == 1]
        # Calculate absolute deadlines
        for task in ready_queue:
            task.deadline += task.act_time

        ready_queue.sort(key=lambda x: x.deadline)
        running = []
        all_tasks = copy.deepcopy(ready_queue)
        for current_time in range(1, self.time_limit):
            free = True
            interrupt = False
            # Add tasks from period time
            for task in all_tasks:
                if task.period != 0 and current_time % task.period == task.act_time and task.period < current_time:
                    add_task = copy.deepcopy(task)
                    add_task.deadline = add_task.deadline - add_task.act_time + current_time
                    add_task.act_time = current_time
                    ready_queue.append(add_task)
                    ready_queue.sort(key=lambda x: x.deadline)
                    print(Fore.BLUE + f'{add_task.name} added in time {current_time}')
                    print(Fore.WHITE)

            # Handle missed tasks
            for task in ready_queue:
                if task.deadline <= current_time:
                    print(Fore.RED + f'MISSED {task.name} in time {current_time}')
                    print(Fore.WHITE)
                    ready_queue.remove(task)
                    self.miss_task += 1
                    if eType == "non_preemptive":
                        if task in running:
                            running.remove(task)

            if eType == "non_preemptive" and running:
                running_task = running[0]
                running_task, ready_queue, free = self.execute_task(running_task, current_time, ready_queue)
                if running_task.wcet == 0:
                    running.pop(0)
            else:
                for task in ready_queue:
                    if task.type == 0 and task.act_time <= current_time:
                        interrupt = True
                        task, ready_queue, free = self.execute_task(task, current_time, ready_queue)
                        if eType == "non_preemptive":
                            running.append(task)
                        break
                if not interrupt:
                    for task in ready_queue:
                        if task.act_time <= current_time:
                            task, ready_queue, free = self.execute_task(task, current_time, ready_queue)
                            if eType == "non_preemptive":
                                running.append(task)
                            break

                # When CPU is FREE and we don't have any ready tasks
                if free:
                    self.free_time += 1


    def monotonic(self, mType):
        self.algorithm = mType + "M"
        periodic_queue = [task for task in list(self.task_set.tasks) if task.state == 1 and task.type == 1]
        aperiodic_queue = [task for task in self.task_set.tasks if task.state == 1 and (task.type == 0 or task.type == 2 or task.type == 3)]
        # Calculate absolute deadlines
        for task in periodic_queue + aperiodic_queue:
            task.deadline += task.act_time
        
        if mType == "R":
            periodic_queue.sort(key=lambda x: x.period)
            aperiodic_queue.sort(key=lambda x: x.period)
        else:
            periodic_queue.sort(key=lambda x: x.deadline)
            aperiodic_queue.sort(key=lambda x: x.deadline)

        all_periodic_tasks = copy.deepcopy(periodic_queue)
        for current_time in range(1, self.time_limit):
            free = True
            interrupt = False

            # Add tasks from period time
            for task in all_periodic_tasks:
                if task.period != 0 and current_time % task.period == task.act_time and task.period < current_time:
                    add_task = copy.deepcopy(task)
                    add_task.deadline = add_task.deadline - add_task.act_time + current_time
                    add_task.act_time = current_time
                    periodic_queue.append(add_task)
                    if mType == "R":
                        periodic_queue.sort(key=lambda x: x.period)
                    else:
                        periodic_queue.sort(key=lambda x: x.deadline)
                    print(Fore.BLUE + f'{add_task.name} added in time {current_time}')
                    print(Fore.WHITE)

            # Handle missed tasks from queues
            missed_periodic_tasks = [task for task in periodic_queue + aperiodic_queue if task.deadline <= current_time]
            for task in missed_periodic_tasks:
                print(Fore.RED + f'{task.name} missed in time {current_time}')
                print(Fore.WHITE)
                self.miss_task += 1
                if task in periodic_queue:
                    periodic_queue.remove(task)
                elif task in aperiodic_queue:
                    aperiodic_queue.remove(task)

            for task in aperiodic_queue:
                if task.act_time <= current_time:
                    interrupt = True
                    task, aperiodic_queue, free = self.execute_task(task, current_time, aperiodic_queue)
                    break

            # Run task
            if not interrupt:
                periodic_priority = next((task for task in periodic_queue if task.act_time <= current_time), None)
                aperiodic_priority = next((task for task in aperiodic_queue if task.act_time <= current_time), None)

                if periodic_priority and aperiodic_priority:
                    if periodic_priority.priority < aperiodic_priority.priority:
                        periodic_priority, periodic_queue, free = self.execute_task(periodic_priority, current_time, periodic_queue)
                    else:
                        aperiodic_priority, aperiodic_queue, free = self.execute_task(aperiodic_priority, current_time, aperiodic_queue)
                elif periodic_priority:
                    periodic_priority, periodic_queue, free = self.execute_task(periodic_priority, current_time, periodic_queue)
                elif aperiodic_priority:
                    aperiodic_priority, aperiodic_queue, free = self.execute_task(aperiodic_priority, current_time, aperiodic_queue)
            

            # When CPU is FREE and we don't have any ready tasks
            if free:
                self.free_time += 1
    
    def sort_queue(self, queue):
        for i in range(len(queue)):
            for j in range(i, len(queue)):
                if queue[i].period > queue[j].period:
                    queue[i], queue[j] = queue[j], queue[i]
        return queue
