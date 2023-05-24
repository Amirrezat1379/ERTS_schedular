# Minimal RTOS 

This is a minimal RTOS based on Python. It is a simple implementation of a EDF, RM, DM scheduler. It is a good starting point for learning how to implement a RTOS.

## How to use

At first run this command:
```bash
pip install -r requirements.txt
```
If you are using linux or macOS and it does not work, run command by using pip3.

Run main.py by using this command:

Unix base OS (Linux/MacOS):
```bash
python3 main.py
```

Windows:
```bash
python main.py
```

## Documentation

you need CSV file to import your tasks

### Task

It has many parameters to show its situation.
```python
RUNNING   = 0   # Currently executing on the processor
READY     = 1   # Ready to run but task of higher or equal priority is currently running
BLOCKED   = 2   # Task is waiting for some condition to be met to move to READY state
SUSPENDED = 3   # Task is waiting for some other task to unsuspend

INTERRUPT =0  # Task type is interrupt
PERIODIC  =1  # Task type is periodic
APERIODIC =2  # Task type is aperiodic
SPORADIC  =3  # Task type is sporadic
```

### Taskset

You need Taskset to save your task and schedul them
