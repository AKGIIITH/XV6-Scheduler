import matplotlib.pyplot as plt
import csv

# Step 1: Read the file
file_path = 'mlfq.txt'
data = []

with open(file_path, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        data.append([int(priority) for priority in row if priority])

# Step 2: Plot the data
plt.figure(figsize=(10, 6))

# Assuming each process is represented by its index in the list
for process_index, process_data in enumerate(zip(*data)):
    plt.plot(process_data, label=f'Process {process_index}', marker='o')

plt.xlabel('Ticks')
plt.ylabel('Priority Level')
plt.title('Process Priority Levels Over Time')
plt.legend()
plt.grid(True)
plt.show()