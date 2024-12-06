import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import time

class MemoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Memory Management Simulation")
        self.root.geometry("900x1000")

 
        self.memory_blocks = [50, 30, 100, 20, 70, 10]
        self.processes = [None] * len(self.memory_blocks)
        self.original_memory = self.memory_blocks.copy()
        
        
        self.process_list = []
        self.terminated_processes = []   

       
        self.sort_memory_blocks()
 
        self.block_labels = []
        for i, block in enumerate(self.memory_blocks):
            label = tk.Label(self.root, text=f"Block {i+1}: {block}KB - Free", bg="lightgreen", width=40)
            label.grid(row=i, column=0, padx=10, pady=5)
            label.bind("<Enter>", lambda e, i=i: self.show_memory_block_details(i))  # Memory Block Details Tooltip
            self.block_labels.append(label)

  
        self.process_size_var = tk.StringVar()
        tk.Label(self.root, text="Process Size (KB):").grid(row=len(self.memory_blocks), column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_size_var).grid(row=len(self.memory_blocks), column=1, padx=10, pady=5)
 
        self.process_priority_var = tk.StringVar()
        tk.Label(self.root, text="Process Priority (1-10):").grid(row=len(self.memory_blocks)+1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_priority_var).grid(row=len(self.memory_blocks)+1, column=1, padx=10, pady=5)
 
        self.algorithm = tk.StringVar(value="First Fit")
        tk.Label(self.root, text="Choose Algorithm:").grid(row=len(self.memory_blocks)+2, column=0, padx=10, pady=5)
        tk.Radiobutton(self.root, text="First Fit", variable=self.algorithm, value="First Fit").grid(row=len(self.memory_blocks)+2, column=1)
        tk.Radiobutton(self.root, text="Best Fit", variable=self.algorithm, value="Best Fit").grid(row=len(self.memory_blocks)+2, column=2)
        tk.Radiobutton(self.root, text="Worst Fit", variable=self.algorithm, value="Worst Fit").grid(row=len(self.memory_blocks)+2, column=3)
 
        tk.Button(self.root, text="Allocate", command=self.allocate_memory).grid(row=len(self.memory_blocks)+3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Deallocate", command=self.deallocate_memory).grid(row=len(self.memory_blocks)+3, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Visualize Memory", command=self.visualize_memory).grid(row=len(self.memory_blocks)+3, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Defragment Memory", command=self.defragment_memory).grid(row=len(self.memory_blocks)+3, column=3, padx=10, pady=10)
 
        tk.Button(self.root, text="Rename Process", command=self.rename_process).grid(row=len(self.memory_blocks)+4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Suspend Process", command=self.suspend_process).grid(row=len(self.memory_blocks)+4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Resume Process", command=self.resume_process).grid(row=len(self.memory_blocks)+4, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Terminate Process", command=self.terminate_process).grid(row=len(self.memory_blocks)+4, column=3, padx=10, pady=10)
 
        self.process_num_var = tk.StringVar()
        tk.Label(self.root, text="Process to Deallocate (ID):").grid(row=len(self.memory_blocks)+5, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_num_var).grid(row=len(self.memory_blocks)+5, column=1, padx=10, pady=5)
 
        self.fragmentation_label = tk.Label(self.root, text="Fragmentation: None", fg="blue")
        self.fragmentation_label.grid(row=len(self.memory_blocks)+6, column=0, columnspan=2, padx=10, pady=10)
 
        self.statistics_label = tk.Label(self.root, text="Memory Statistics: None", fg="blue")
        self.statistics_label.grid(row=len(self.memory_blocks)+7, column=0, columnspan=2, padx=10, pady=10)
 
        self.process_info_label = tk.Label(self.root, text="Running Processes: None", fg="blue")
        self.process_info_label.grid(row=len(self.memory_blocks)+8, column=0, columnspan=2, padx=10, pady=10)
 
        self.search_var = tk.StringVar()
        tk.Label(self.root, text="Search Process:").grid(row=len(self.memory_blocks)+9, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.search_var).grid(row=len(self.memory_blocks)+9, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Search", command=self.search_process).grid(row=len(self.memory_blocks)+9, column=2, padx=10, pady=5)
 
        tk.Button(self.root, text="Memory Usage Graph", command=self.memory_usage_graph).grid(row=len(self.memory_blocks)+10, column=0, padx=10, pady=10)

    def sort_memory_blocks(self):
        self.memory_blocks.sort(reverse=True)

    def sort_process_list_by_priority(self):
        self.process_list.sort(key=lambda x: x['Priority'], reverse=True)

    def show_memory_block_details(self, index):
        block_info = f"Block {index+1}: {self.memory_blocks[index]}KB - "
        block_info += "Free" if self.processes[index] is None else f"Allocated to P{self.processes[index]}"
        messagebox.showinfo("Memory Block Details", block_info)

    def search_process(self):
        search_query = self.search_var.get().lower()
        found_processes = [f"P{proc['ID']} ({proc['Size']}KB, Priority: {proc['Priority']}, Status: {proc['Status']})"
                           for proc in self.process_list if proc and (str(proc['ID']) == search_query or search_query in proc.get('Name', '').lower())]
        if found_processes:
            messagebox.showinfo("Search Results", "Found Processes: " + ", ".join(found_processes))
        else:
            messagebox.showinfo("Search Results", "No processes found.")

    def allocate_memory(self):
        try:
            process_size = int(self.process_size_var.get())
            process_priority = int(self.process_priority_var.get())
            process_id = len(self.process_list) + 1

            if process_priority < 1 or process_priority > 10:
                messagebox.showerror("Error", "Priority must be between 1 and 10!")
                return

            if self.algorithm.get() == "First Fit":
                allocated = self.first_fit(process_size, process_id)
            elif self.algorithm.get() == "Best Fit":
                allocated = self.best_fit(process_size, process_id)
            elif self.algorithm.get() == "Worst Fit":
                allocated = self.worst_fit(process_size, process_id)

            if allocated:
                start_time = time.time()  # Simulate process start time
                self.process_list.append({"ID": process_id, "Size": process_size, "Priority": process_priority, "Status": "Running", "StartTime": start_time})
                self.sort_process_list_by_priority()  # Sort by priority after allocation
                self.update_process_info()
                messagebox.showinfo("Success", f"Process P{process_id} allocated successfully!")
            else:
                messagebox.showerror("Error", "No suitable block found for the process!")

            self.calculate_fragmentation()
            self.show_statistics()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process size and priority!")

    def first_fit(self, process_size, process_id):
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and self.processes[i] is None:
                self.processes[i] = process_id
                self.memory_blocks[i] -= process_size
                self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - P{process_id}", bg="red")
                return True
        return False

    def best_fit(self, process_size, process_id):
        best_index = -1
        best_size = float('inf')
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and self.processes[i] is None and block_size < best_size:
                best_index = i
                best_size = block_size
        if best_index != -1:
            self.processes[best_index] = process_id
            self.memory_blocks[best_index] -= process_size
            self.block_labels[best_index].config(text=f"Block {best_index+1}: {self.memory_blocks[best_index]}KB - P{process_id}", bg="red")
            return True
        return False

    def worst_fit(self, process_size, process_id):
        worst_index = -1
        worst_size = -1
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and self.processes[i] is None and block_size > worst_size:
                worst_index = i
                worst_size = block_size
        if worst_index != -1:
            self.processes[worst_index] = process_id
            self.memory_blocks[worst_index] -= process_size
            self.block_labels[worst_index].config(text=f"Block {worst_index+1}: {self.memory_blocks[worst_index]}KB - P{process_id}", bg="red")
            return True
        return False

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
            self.calculate_fragmentation()
            self.show_statistics()

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

    def calculate_fragmentation(self):
        free_blocks = [self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None]
        total_fragmentation = sum(free_blocks)
        self.fragmentation_label.config(text=f"Fragmentation: {total_fragmentation}KB")

    def show_statistics(self):
        total_memory = sum(self.original_memory)
        used_memory = sum(self.original_memory[i] - self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is not None)
        free_memory = total_memory - used_memory
        self.statistics_label.config(text=f"Memory Statistics - Total: {total_memory}KB, Used: {used_memory}KB, Free: {free_memory}KB")

    def update_process_info(self):
        running_processes = [f"P{proc['ID']} ({proc['Size']}KB, Priority: {proc['Priority']}, Status: {proc['Status']})"
                             for proc in self.process_list if proc['Status'] == "Running"]
        self.process_info_label.config(text="Running Processes: " + (", ".join(running_processes) if running_processes else "None"))

    def rename_process(self):
        try:
            process_id = int(self.process_num_var.get())
            new_name = simpledialog.askstring("Rename Process", "Enter new process name:")
            for proc in self.process_list:
                if proc['ID'] == process_id:
                    proc['Name'] = new_name
                    messagebox.showinfo("Rename Process", f"Process P{process_id} renamed to {new_name}")
                    break
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def suspend_process(self):
        try:
            process_id = int(self.process_num_var.get())
            for proc in self.process_list:
                if proc['ID'] == process_id and proc['Status'] == "Running":
                    proc['Status'] = "Suspended"
                    messagebox.showinfo("Suspend Process", f"Process P{process_id} has been suspended.")
                    self.update_process_info()
                    break
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def resume_process(self):
        try:
            process_id = int(self.process_num_var.get())
            for proc in self.process_list:
                if proc['ID'] == process_id and proc['Status'] == "Suspended":
                    proc['Status'] = "Running"
                    messagebox.showinfo("Resume Process", f"Process P{process_id} has been resumed.")
                    self.update_process_info()
                    break
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def terminate_process(self):
        try:
            process_id = int(self.process_num_var.get())
            for proc in self.process_list:
                if proc['ID'] == process_id:
                    proc['Status'] = "Terminated"
                    end_time = time.time()
                    total_time = round(end_time - proc['StartTime'], 2)
                    messagebox.showinfo("Terminate Process", f"Process P{process_id} has been terminated.\nExecution time: {total_time}s")
                    self.update_process_info()
                    break
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def visualize_memory(self):
        labels = [f"Block {i+1}" for i in range(len(self.memory_blocks))]
        sizes = [self.memory_blocks[i] for i in range(len(self.memory_blocks))]
        colors = ['lightgreen' if self.processes[i] is None else 'red' for i in range(len(self.memory_blocks))]

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Memory Usage")
        plt.show()

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

if __name__ == "__main__":
    root = tk.Tk()
    MemoryManager(root)
    root.mainloop()
