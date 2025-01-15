### OSN Mini-Project-2 

# xv6 Scheduler and Syscall Implementation

This project involves implementing new system calls, alarm mechanisms, and two different process scheduling algorithms in the xv6 operating system: Lottery-Based Scheduling (LBS) and Multi-Level Feedback Queue (MLFQ). Below are detailed explanations of each part, along with instructions on how to build, test, and use the new features.

## Table of Contents
1. [Part A: Syscall and Alarm Implementation](#part-a-syscall-and-alarm-implementation)
   - Implementation of `syscount` Syscall
   - Implementation of `sigalarm` and `sigreturn` Mechanisms
2. [Part B: Scheduling Algorithms](#part-b-scheduling-algorithms)
   - Lottery-Based Scheduling (LBS)
   - Multi-Level Feedback Queue (MLFQ)
3. [Testing Instructions](#testing-instructions)
4. [Building xv6](#building-xv6)
5. [How to Run and Test the New Features](#how-to-run-and-test-the-new-features)

## Part A: Syscall and Alarm Implementation

### 1. Implementation of `syscount` Syscall
- A new system call `syscount()` has been implemented, which returns the total number of system calls made by the current process since its creation.
- The syscall count is tracked in the `proc` structure by adding a new field `syscall_count`, which is incremented each time a system call is made.
- The system call is defined in `sysproc.c` and registered in the system call table (`syscall.c`).

### 2. Implementation of Alarm Mechanism (`sigalarm` and `sigreturn`)
- **`sigalarm(int ticks, void (*handler)())`**:
  - This system call sets an alarm for the process, causing the specified handler function to be called after the given number of ticks (timer interrupts). It enables the process to execute a user-defined handler periodically.
  - Implementation details:
    - Two new fields were added to the `proc` structure: `alarmticks` and `handler`.
    - `alarmticks` stores the number of ticks after which the handler is invoked, while `handler` is a pointer to the function that should be executed.
    - During each timer interrupt, the alarm mechanism checks if the specified number of ticks has passed and invokes the handler if it has.

- **`sigreturn()`**:
  - Restores the process state after a handler execution, allowing the process to resume normal execution as if it was never interrupted.
  - This mechanism saves the trap frame state before executing the handler and restores it when `sigreturn()` is called.

## Part B: Scheduling Algorithms

### 1. Lottery-Based Scheduling (LBS)
- **Overview**: In Lottery-Based Scheduling, processes are assigned a certain number of "tickets," and during each scheduling decision, a random ticket is selected to determine which process runs. The more tickets a process has, the higher its chance of being selected.
- **Implementation Details**:
  - Added new fields to the `proc` structure: `tickets` and `arrival_time`.
  - Created a system call `settickets(int value)` that allows any process to set its ticket count. By default, each process is assigned `1` ticket in `allocproc()`.
  - The `scheduler()` function was modified to perform a "lottery" by calculating the total number of tickets for runnable processes and randomly selecting a process based on its ticket count.
  - When processes have identical ticket counts, the tie is broken using the `arrival_time`, with preference given to the older process.

### 2. Multi-Level Feedback Queue (MLFQ)
- **Overview**: MLFQ prioritizes processes based on their behavior (CPU-bound vs. I/O-bound), dynamically adjusting process priorities based on CPU usage. Processes that have used up their time slice are moved down in priority, while long-waiting or I/O-bound processes are moved up.
- **Implementation Details**:
  - Added fields to `proc.h` to store a process's priority (`priority`), the process index within the priority queue (`pvalue`), the start time (`pstart`), and the end time (`pend`).
  - Created structures for managing the number of processes at each priority level and the maximum time allowed for each priority.
  - Implemented functions to find the highest-priority runnable process (`high_priority_process`) and to periodically reset all process priorities (`reset`).
  - The `scheduler()` was modified to execute processes based on their priority and dynamically adjust their priority based on their execution characteristics.

## Testing Instructions

### Syscall Testing
- **`syscount`**:
  - Create a user program that makes several system calls and then calls `syscount()` to verify that the number of system calls is correctly counted.
- **`sigalarm` and `sigreturn`**:
  - Write a test program that sets an alarm using `sigalarm()` with a specific tick count and a handler function. Check if the handler is called after the specified number of ticks.
  - Ensure that after the handler executes, the process resumes its normal flow.

### Scheduler Testing
- **Lottery-Based Scheduling (LBS)**:
  - Use the `settickets()` system call to assign different ticket values to various processes and observe whether processes with more tickets get scheduled more often.
  - Run the `schedulertest` command to measure the average waiting and running times.
- **Multi-Level Feedback Queue (MLFQ)**:
  - Run a mix of CPU-bound and I/O-bound processes to observe how their priorities change over time.
  - Use `schedulertest` to compare performance metrics with the other scheduling algorithms.

## Building xv6
To build xv6 with the new system calls and scheduling algorithms, follow these steps:

1. Clone the xv6 repository.
2. Apply your changes for syscalls and scheduling policies.
3. Set the `SCHEDULER` macro in the `Makefile`:
   ```bash
   # Example: To build with Lottery-Based Scheduling
   make clean
   make SCHEDULER=LBS
   ```
   ```bash
   # Example: To build with Multi-Level Feedback Queue
   make clean
   make SCHEDULER=MLFQ
   ```
   If no scheduler is specified, the default will be Round-Robin (RR).

4. Run xv6:
   ```bash
   make qemu
   ```

## How to Run and Test the New Features
1. **Syscall Tests**:
   - Run the syscall test programs to verify `syscount()`, `sigalarm()`, and `sigreturn()` functionality.

2. **Testing Scheduling Policies**:
   - Set the desired scheduling policy using the `SCHEDULER` macro.
   - Run multiple processes and observe the scheduling behavior.
   - Use the `schedulertest` command to generate performance data for comparison:
     ```bash
     schedulertest
     ```

3. **Example Commands for Testing**:
   - Set tickets for a process in LBS:
     ```c
     settickets(5); // Set 5 tickets for the current process
     ```
   - Set an alarm with `sigalarm`:
     ```c
     sigalarm(10, handler); // Set an alarm to execute handler every 10 ticks
     ```

4. **Logs and Debugging**:
   - Use `printf` statements in the kernel to print debug information about system calls, scheduling decisions, and priority changes.
   - Review the output in the QEMU console to understand the behavior.

---

This `README` provides a comprehensive overview of the project, ensuring that all implemented features can be tested and evaluated effectively.