import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt

class MemoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Memory Management ")
        self.root.geometry("900x1000")

        # Memory blocks (initially free, represented in KB)
        self.memory_blocks = [372,225,179,409,290,100]
        self.processes = [None] * len(self.memory_blocks)
        self.original_memory = self.memory_blocks.copy()
        
        # Process details (ID, Size, Priority, Status)
        self.process_list = []

        # Sorting memory blocks by size (descending)
        self.sort_memory_blocks()

        # Create memory block labels
        self.block_labels = []
        for i, block in enumerate(self.memory_blocks):
            label = tk.Label(self.root, text=f"Block {i+1}: {block}KB - Free", bg="lightgreen", width=40)
            label.grid(row=i, column=0, padx=10, pady=5)
            label.bind("<Enter>", lambda e, i=i: self.show_memory_block_details(i))  # Memory Block Details Tooltip
            self.block_labels.append(label)

        # Process size input
        self.process_size_var = tk.StringVar()
        tk.Label(self.root, text="Process Sizes (KB):").grid(row=len(self.memory_blocks), column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_size_var).grid(row=len(self.memory_blocks), column=1, padx=10, pady=5)


        # Priority input
        self.process_priority_var = tk.StringVar()
        tk.Label(self.root, text="Process Priority (1-10):").grid(row=len(self.memory_blocks)+1, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_priority_var).grid(row=len(self.memory_blocks)+1, column=1, padx=10, pady=5)

        # Algorithm selection
        self.algorithm = tk.StringVar(value="First Fit")
        tk.Label(self.root, text="Choose Algorithm:").grid(row=len(self.memory_blocks)+2, column=0, padx=10, pady=5)
        tk.Radiobutton(self.root, text="First Fit", variable=self.algorithm, value="First Fit").grid(row=len(self.memory_blocks)+2, column=1)
        tk.Radiobutton(self.root, text="Best Fit", variable=self.algorithm, value="Best Fit").grid(row=len(self.memory_blocks)+2, column=2)
        tk.Radiobutton(self.root, text="Worst Fit", variable=self.algorithm, value="Worst Fit").grid(row=len(self.memory_blocks)+2, column=3)

        # Allocate, Deallocate, Visualize, Defragmentation buttons
        tk.Button(self.root, text="Allocate", command=self.allocate_memory).grid(row=len(self.memory_blocks)+3, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Deallocate", command=self.deallocate_memory).grid(row=len(self.memory_blocks)+3, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Visualize Memory", command=self.visualize_memory).grid(row=len(self.memory_blocks)+3, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Defragment Memory", command=self.defragment_memory).grid(row=len(self.memory_blocks)+3, column=3, padx=10, pady=10)

        # Process renaming, suspension, and termination
        tk.Button(self.root, text="Rename Process", command=self.rename_process).grid(row=len(self.memory_blocks)+4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Suspend Process", command=self.suspend_process).grid(row=len(self.memory_blocks)+4, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Resume Process", command=self.resume_process).grid(row=len(self.memory_blocks)+4, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Terminate Process", command=self.terminate_process).grid(row=len(self.memory_blocks)+4, column=3, padx=10, pady=10)

        # Process to deallocate input
        self.process_num_var = tk.StringVar()
        tk.Label(self.root, text="Process to Deallocate (ID):").grid(row=len(self.memory_blocks)+5, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.process_num_var).grid(row=len(self.memory_blocks)+5, column=1, padx=10, pady=5)


        # Fragmentation display
        self.fragmentation_label = tk.Label(self.root, text="Fragmentation: None", fg="blue")
        self.fragmentation_label.grid(row=len(self.memory_blocks)+6, column=0, columnspan=2, padx=10, pady=10)

        # Memory statistics display
        self.statistics_label = tk.Label(self.root, text="Memory Statistics: None", fg="blue")
        self.statistics_label.grid(row=len(self.memory_blocks)+7, column=0, columnspan=2, padx=10, pady=10)

        # Process Information display
        self.process_info_label = tk.Label(self.root, text="Running Processes: None", fg="blue")
        self.process_info_label.grid(row=len(self.memory_blocks)+8, column=0, columnspan=2, padx=10, pady=10)

        # Search bar for process search
        self.search_var = tk.StringVar()
        tk.Label(self.root, text="Search Process:").grid(row=len(self.memory_blocks)+9, column=0, padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.search_var).grid(row=len(self.memory_blocks)+9, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Search", command=self.search_process).grid(row=len(self.memory_blocks)+9, column=2, padx=10, pady=5)

        # Graph button
        tk.Button(self.root, text="Memory Usage Graph", command=self.memory_usage_graph).grid(row=len(self.memory_blocks)+10, column=0, padx=10, pady=10)

    def sort_memory_blocks(self):
        # Sort memory blocks in descending order based on size
        self.memory_blocks.sort(reverse=True)

    def sort_process_list_by_priority(self):
        # Sort the process list by priority in descending order
        self.process_list.sort(key=lambda x: x['Priority'], reverse=True)

    def show_memory_block_details(self, index):
        block_info = f"Block {index+1}: {self.memory_blocks[index]}KB - "
        block_info += "Free" if self.processes[index] is None else f"Allocated to P{self.processes[index]}"

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
            process_sizes = list(map(int, self.process_size_var.get().split()))   
            process_priority = int(self.process_priority_var.get())

            if process_priority < 1 or process_priority > 10:
                messagebox.showerror("Error", "Priority must be between 1 and 10!")
                return

            for process_size in process_sizes:
                process_id = len(self.process_list) + 1

                if self.algorithm.get() == "First Fit":
                    allocated = self.first_fit(process_size, process_id)
                elif self.algorithm.get() == "Best Fit":
                    allocated = self.best_fit(process_size, process_id)
                elif self.algorithm.get() == "Worst Fit":
                    allocated = self.worst_fit(process_size, process_id)

                if allocated:
                    self.process_list.append({"ID": process_id, "Size": process_size, "Priority": process_priority, "Status": "Running"})
                else:
                    messagebox.showerror("Error", f"No suitable block found for process size {process_size}KB!")

            self.sort_process_list_by_priority()  # Sort by priority after allocation
            self.update_process_info()
            messagebox.showinfo("Success", "Processes allocated successfully!")
            self.calculate_fragmentation()
            self.show_statistics()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid process sizes and priority!")


    def first_fit(self, process_size, process_id):
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and self.processes[i] is None:
                self.processes[i] = process_id
                self.memory_blocks[i] -= process_size
                self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Allocated to P{process_id}", bg="lightcoral")
                return True
        return False

    def best_fit(self, process_size, process_id):
        best_block = -1
        best_size = float('inf')
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and block_size < best_size and self.processes[i] is None:
                best_block = i
                best_size = block_size

        if best_block != -1:
            self.processes[best_block] = process_id
            self.memory_blocks[best_block] -= process_size
            self.block_labels[best_block].config(text=f"Block {best_block+1}: {self.memory_blocks[best_block]}KB - Allocated to P{process_id}", bg="lightcoral")
            return True
        return False

    def worst_fit(self, process_size, process_id):
        worst_block = -1
        worst_size = float('-inf')
        for i, block_size in enumerate(self.memory_blocks):
            if block_size >= process_size and block_size > worst_size and self.processes[i] is None:
                worst_block = i
                worst_size = block_size

        if worst_block != -1:
            self.processes[worst_block] = process_id
            self.memory_blocks[worst_block] -= process_size
            self.block_labels[worst_block].config(text=f"Block {worst_block+1}: {self.memory_blocks[worst_block]}KB - Allocated to P{process_id}", bg="lightcoral")
            return True
        return False

    def deallocate_memory(self):
        try:
            process_id = int(self.process_num_var.get())
            for i, allocated_process in enumerate(self.processes):
                if allocated_process == process_id:
                    self.memory_blocks[i] += self.original_memory[i] - self.memory_blocks[i]  # Restores original block size
                    self.processes[i] = None
                    self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Free", bg="lightgreen")

                    # Remove process from process list
                    self.process_list = [proc for proc in self.process_list if proc['ID'] != process_id]

                    self.update_process_info()
                    self.calculate_fragmentation()
                    self.show_statistics()

                    messagebox.showinfo("Success", f"Process P{process_id} deallocated successfully!")
                    return

            messagebox.showerror("Error", "Process not found!")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def rename_process(self):
        try:
            process_id = int(self.process_num_var.get())
            new_name = simpledialog.askstring("Rename Process", "Enter the new process name:")
            if new_name:
                for proc in self.process_list:
                    if proc["ID"] == process_id:
                        proc["Name"] = new_name
                        self.update_process_info()
                        messagebox.showinfo("Success", f"Process P{process_id} renamed to {new_name}!")
                        return
                messagebox.showerror("Error", "Process not found!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def suspend_process(self):
        try:
            process_id = int(self.process_num_var.get())
            for proc in self.process_list:
                if proc["ID"] == process_id and proc["Status"] == "Running":
                    proc["Status"] = "Suspended"
                    self.update_process_info()
                    messagebox.showinfo("Success", f"Process P{process_id} suspended successfully!")
                    return
            messagebox.showerror("Error", "Process not found or already suspended!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def resume_process(self):
        try:
            process_id = int(self.process_num_var.get())
            for proc in self.process_list:
                if proc["ID"] == process_id and proc["Status"] == "Suspended":
                    proc["Status"] = "Running"
                    self.update_process_info()
                    messagebox.showinfo("Success", f"Process P{process_id} resumed successfully!")
                    return
            messagebox.showerror("Error", "Process not found or not suspended!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid process ID!")

    def terminate_process(self):
        self.deallocate_memory()

    def defragment_memory(self):
        for i, allocated_process in enumerate(self.processes):
            if allocated_process is None:
                # Find next allocated block to shift left
                for j in range(i+1, len(self.processes)):
                    if self.processes[j] is not None:
                        self.processes[i] = self.processes[j]
                        self.memory_blocks[i] = self.memory_blocks[j]
                        self.memory_blocks[j] = self.original_memory[j]  # Reset the right block to original size
                        self.processes[j] = None

                        # Update labels
                        self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Allocated to P{self.processes[i]}", bg="lightcoral")
                        self.block_labels[j].config(text=f"Block {j+1}: {self.memory_blocks[j]}KB - Free", bg="lightgreen")
                        break

        messagebox.showinfo("Success", "Memory defragmentation completed!")
        self.calculate_fragmentation()

    def calculate_fragmentation(self):
        total_free = sum(self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None)
        self.fragmentation_label.config(text=f"Fragmentation: {total_free}KB")

    def show_statistics(self):
        total_memory = sum(self.original_memory)
        total_free = sum(self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None)
        total_used = total_memory - total_free
        self.statistics_label.config(text=f"Memory Statistics - Total: {total_memory}KB, Used: {total_used}KB, Free: {total_free}KB")

    def update_process_info(self):
        process_info = ", ".join([f"P{proc['ID']} ({proc['Size']}KB, Priority: {proc['Priority']}, Status: {proc['Status']})" for proc in self.process_list])
        self.process_info_label.config(text=f"Running Processes: {process_info}" if process_info else "Running Processes: None")

    def visualize_memory(self):
        labels = [f"Block {i+1}" for i in range(len(self.memory_blocks))]
        sizes = [self.memory_blocks[i] if self.processes[i] is None else self.original_memory[i] - self.memory_blocks[i] for i in range(len(self.memory_blocks))]
        colors = ["lightgreen" if self.processes[i] is None else "lightcoral" for i in range(len(self.memory_blocks))]

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title("Memory Usage Visualization")
        plt.show()

    def memory_usage_graph(self):
        process_ids = [proc["ID"] for proc in self.process_list]
        process_sizes = [proc["Size"] for proc in self.process_list]
        process_priorities = [proc["Priority"] for proc in self.process_list]

        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Process ID')
        ax1.set_ylabel('Size (KB)', color='tab:blue')
        ax1.bar(process_ids, process_sizes, color='tab:blue', alpha=0.6, label="Size")
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Priority', color='tab:red')
        ax2.plot(process_ids, process_priorities, color='tab:red', marker='o', label="Priority")
        ax2.tick_params(axis='y', labelcolor='tab:red')

        plt.title("Process Size and Priority Comparison")
        fig.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManager(root)
    root.mainloop()
