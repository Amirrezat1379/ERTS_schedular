import matplotlib.pyplot as plt

def printer(sets):
    print('**************************************')
    print('CPU Utility: ', 1- (sets.free_time/100))
    print('Number of missing tasks: ', sets.miss_task)
    if sets.miss_task != 0:
        print('Feasibility: NOT Feasible!')
    else:
        print('Feasibility: Feasible!')

    x = list(sets.time.keys())
    y = list(sets.time.values())
    for i in range(len(x)):
        if y[i] == "Task1":
            plt.scatter(x[i], "CPU", color="blue")
            plt.scatter(x[i], "Task1", color="blue")
        elif y[i] == "Task2":
            plt.scatter(x[i], "CPU", color="red")
            plt.scatter(x[i], "Task2", color="red")
        elif y[i] == "Task3":
            plt.scatter(x[i], "CPU", color="green")
            plt.scatter(x[i], "Task3", color="green")
        elif y[i] == "Task4":
            plt.scatter(x[i], "CPU", color="yellow")
            plt.scatter(x[i], "Task4", color="yellow")
        elif y[i] == "Task5":
            plt.scatter(x[i], "CPU", color="cyan")
            plt.scatter(x[i], "Task5", color="cyan")
        elif y[i] == "ISR1":
            plt.scatter(x[i], "CPU", color="black")
            plt.scatter(x[i], "ISR1", color="black")
        elif y[i] == "ISR2":
            plt.scatter(x[i], "CPU", color="magenta")
            plt.scatter(x[i], "ISR2", color="magenta")
    plt.title(sets.algorithm)
    plt.show()