import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import matplotlib.pyplot as plt
import json

class MemoryManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Management System")

        # Set up initial memory blocks
        self.memory_blocks = [100, 200, 300, 400, 500]
        self.original_memory = self.memory_blocks.copy()
        self.processes = [None] * len(self.memory_blocks)
        self.process_list = []
        self.terminated_processes = []

        # GUI Labels for each memory block
        self.block_labels = []
        for i, block in enumerate(self.memory_blocks):
            label = tk.Label(self.master, text=f"Block {i+1}: {block}KB - Free", bg="lightgreen", width=40)
            label.grid(row=i, column=0)
            self.block_labels.append(label)

        # Input for process number and size
        tk.Label(self.master, text="Process ID:").grid(row=6, column=0)
        self.process_num_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.process_num_var).grid(row=6, column=1)

        tk.Label(self.master, text="Process Size:").grid(row=7, column=0)
        self.process_size_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.process_size_var).grid(row=7, column=1)

        tk.Label(self.master, text="Process Priority:").grid(row=8, column=0)
        self.process_priority_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.process_priority_var).grid(row=8, column=1)

        # Buttons
        tk.Button(self.master, text="Allocate Memory (First Fit)", command=self.allocate_first_fit).grid(row=9, column=0)
        tk.Button(self.master, text="Deallocate Memory", command=self.deallocate_memory).grid(row=9, column=1)
        tk.Button(self.master, text="Defragment Memory", command=self.defragment_memory).grid(row=10, column=0)
        tk.Button(self.master, text="Show Memory Usage", command=self.memory_usage_graph).grid(row=10, column=1)

        # Fragmentation & Statistics
        self.fragmentation_label = tk.Label(self.master, text="Fragmentation: 0KB", fg="blue")
        self.fragmentation_label.grid(row=11, column=0)

        self.statistics_label = tk.Label(self.master, text="Memory Statistics", fg="blue")
        self.statistics_label.grid(row=11, column=1)

        # Process Information Label
        self.process_info_label = tk.Label(self.master, text="Running Processes: None")
        self.process_info_label.grid(row=12, column=0, columnspan=2)

        # New Feature: Compact View, Aging, Swapping, and Execution
        tk.Button(self.master, text="Compact Memory View", command=self.compact_memory_view).grid(row=13, column=0)
        tk.Button(self.master, text="Simulate Process Execution", command=self.simulate_execution).grid(row=13, column=1)
        tk.Button(self.master, text="Apply Aging", command=self.apply_aging).grid(row=14, column=0)
        tk.Button(self.master, text="Swap Processes", command=self.swap_processes).grid(row=14, column=1)

        self.load_saved_state()  # Load saved process state on startup

    def allocate_first_fit(self):
        try:
            process_id = int(self.process_num_var.get())
            process_size = int(self.process_size_var.get())
            process_priority = int(self.process_priority_var.get())
            allocated = False

            for i in range(len(self.memory_blocks)):
                if self.memory_blocks[i] >= process_size and self.processes[i] is None:
                    self.processes[i] = process_id
                    self.memory_blocks[i] -= process_size
                    self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - P{process_id} (Priority: {process_priority})", bg="red")

                    # Store the process details
                    self.process_list.append({
                        "ID": process_id,
                        "Size": process_size,
                        "Priority": process_priority,
                        "StartTime": time.time(),
                        "Status": "Running"
                    })
                    allocated = True
                    break

            if not allocated:
                messagebox.showwarning("Allocation Failed", "Not enough memory for this process!")
            else:
                self.calculate_fragmentation()
                self.show_statistics()
                self.update_process_info()
                self.save_state()  # Save the process state

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid process details!")

    def deallocate_memory(self):
        try:
            process_id = int(self.process_num_var.get())
            found = False

            for i, proc_id in enumerate(self.processes):
                if proc_id == process_id:
                    self.memory_blocks[i] += self.original_memory[i]
                    self.processes[i] = None
                    self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Free", bg="lightgreen")
                    found = True
                    self.terminated_processes.append({"ID": process_id, "EndTime": time.time()})
                    messagebox.showinfo("Deallocation", f"Process P{process_id} deallocated successfully!")
                    break

            if not found:
                messagebox.showwarning("Not Found", "Process not found!")
            else:
                self.calculate_fragmentation()
                self.show_statistics()
                self.save_state()  # Save the process state

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def defragment_memory(self):
        free_memory = sum(self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None)
        self.memory_blocks = [self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is not None]
        self.memory_blocks.append(free_memory)

        for i, label in enumerate(self.block_labels):
            if i < len(self.memory_blocks):
                if self.processes[i] is None:
                    label.config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Free", bg="lightgreen")
                else:
                    label.config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - P{self.processes[i]}", bg="red")
            else:
                label.config(text=f"Block {i+1}: N/A", bg="lightgrey")

        messagebox.showinfo("Defragmentation", "Memory successfully defragmented!")
        self.save_state()  # Save the process state

    def calculate_fragmentation(self):
        free_blocks = [self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None]
        total_fragmentation = sum(free_blocks)
        self.fragmentation_label.config(text=f"Fragmentation: {total_fragmentation}KB")

    def show_statistics(self):
        total_memory = sum(self.original_memory)
        used_memory = sum(self.original_memory[i] - self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is not None)
        free_memory = total_memory - used_memory
        self.statistics_label.config(text=f"Memory Statistics - Total: {total_memory}KB, Used: {used_memory}KB, Free: {free_memory}KB")

    def memory_usage_graph(self):
        used_memory = [self.original_memory[i] - self.memory_blocks[i] for i in range(len(self.memory_blocks))]
        free_memory = [self.memory_blocks[i] for i in range(len(self.memory_blocks))]

        labels = [f"Block {i+1}" for i in range(len(self.memory_blocks))]
        plt.bar(labels, used_memory, label='Used Memory', color='red')
        plt.bar(labels, free_memory, bottom=used_memory, label='Free Memory', color='green')

        plt.xlabel('Memory Blocks')
        plt.ylabel('Memory Size (KB)')
        plt.title('Memory Usage Breakdown')
        plt.legend()
        plt.show()

    def compact_memory_view(self):
        compact_view = "\n".join([f"Block {i+1}: {self.memory_blocks[i]}KB" for i in range(len(self.memory_blocks))])
        messagebox.showinfo("Compact Memory View", compact_view)

    def apply_aging(self):
        for proc in self.process_list:
            proc['Priority'] += 1  # Increase priority as process ages
        messagebox.showinfo("Aging", "Process priorities increased due to aging.")
        self.save_state()  # Save the process state

    def swap_processes(self):
        messagebox.showinfo("Swapping", "Feature under development! This will swap lower priority processes.")

    def simulate_execution(self):
        for i in range(len(self.process_list)):
            if self.process_list[i]['Status'] == "Running":
                self.process_list[i]['Size'] -= 10  # Simulate size reduction
                if self.process_list[i]['Size'] <= 0:
                    self.process_list[i]['Status'] = "Terminated"
        self.save_state()  # Save the process state

    def update_process_info(self):
        if self.process_list:
            process_info = "\n".join([f"P{proc['ID']} (Priority: {proc['Priority']}, Size: {proc['Size']}KB, Status: {proc['Status']})" for proc in self.process_list])
        else:
            process_info = "No Running Processes"
        self.process_info_label.config(text=process_info)

    def save_state(self):
        with open("process_state.json", "w") as f:
            json.dump(self.process_list, f)

    def load_saved_state(self):
        try:
            with open("process_state.json", "r") as f:
                self.process_list = json.load(f)
            self.update_process_info()
        except FileNotFoundError:
            pass


# Main Application
root = tk.Tk()
app = MemoryManager(root)
root.mainloop()
