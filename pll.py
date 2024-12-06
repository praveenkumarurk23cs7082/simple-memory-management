    import tkinter as tk
    from tkinter import messagebox, simpledialog
    import matplotlib.pyplot as plt

    class MemoryManager:
        def __init__(self, root):
            self.root = root
            self.root.title("Simple Memory Management Simulation")
            self.root.geometry("900x1000")

            # Memory blocks (initially free, represented in KB)
            self.memory_blocks = [50, 30, 100, 20, 70, 10]
            self.original_memory = self.memory_blocks.copy()
            self.processes = [None] * len(self.memory_blocks)
            
            # Process details (ID, Size, Priority, Status)
            self.process_list = []

            # Create memory block labels
            self.block_labels = []
            for i, block in enumerate(self.memory_blocks):
                label = tk.Label(self.root, text=f"Block {i+1}: {block}KB - Free", bg="lightgreen", width=40)
                label.grid(row=i, column=0, padx=10, pady=5)
                label.bind("<Enter>", lambda e, i=i: self.show_memory_block_details(i))
                self.block_labels.append(label)

            # Process size input
            self.process_size_var = tk.StringVar()
            tk.Label(self.root, text="Process Size (KB):").grid(row=len(self.memory_blocks), column=0, padx=10, pady=5)
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
            self.process_num_var = tk.StringVar()
            tk.Label(self.root, text="Process to Deallocate (ID):").grid(row=len(self.memory_blocks)+4, column=0, padx=10, pady=5)
            tk.Entry(self.root, textvariable=self.process_num_var).grid(row=len(self.memory_blocks)+4, column=1, padx=10, pady=5)

            # Fragmentation display
            self.fragmentation_label = tk.Label(self.root, text="Fragmentation: None", fg="blue")
            self.fragmentation_label.grid(row=len(self.memory_blocks)+5, column=0, columnspan=2, padx=10, pady=10)


            # Memory statistics display
            self.statistics_label = tk.Label(self.root, text="Memory Statistics: None", fg="blue")
            self.statistics_label.grid(row=len(self.memory_blocks)+6, column=0, columnspan=2, padx=10, pady=10)

            # Process Information display
            self.process_info_label = tk.Label(self.root, text="Running Processes: None", fg="blue")
            self.process_info_label.grid(row=len(self.memory_blocks)+7, column=0, columnspan=2, padx=10, pady=10)

            # Search bar for process search
            self.search_var = tk.StringVar()
            tk.Label(self.root, text="Search Process:").grid(row=len(self.memory_blocks)+8, column=0, padx=10, pady=5)
            tk.Entry(self.root, textvariable=self.search_var).grid(row=len(self.memory_blocks)+8, column=1, padx=10, pady=5)
            tk.Button(self.root, text="Search", command=self.search_process).grid(row=len(self.memory_blocks)+8, column=2, padx=10, pady=5)

            # Graph button
            tk.Button(self.root, text="Memory Usage Graph", command=self.memory_usage_graph).grid(row=len(self.memory_blocks)+9, column=0, padx=10, pady=10)

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
                    self.process_list.append({"ID": process_id, "Size": process_size, "Priority": process_priority, "Status": "Running"})
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
            worst_size = -1
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
                found = False
                for i, proc_id in enumerate(self.processes):
                    if proc_id == process_id:
                        self.processes[i] = None
                        self.memory_blocks[i] = self.original_memory[i]  # Restore original block size
                        self.block_labels[i].config(text=f"Block {i+1}: {self.memory_blocks[i]}KB - Free", bg="lightgreen")
                        found = True
                        break

                if found:
                    self.process_list = [proc for proc in self.process_list if proc['ID'] != process_id]
                    messagebox.showinfo("Success", f"Process P{process_id} deallocated successfully!")
                else:
                    messagebox.showerror("Error", "Process not found!")

                self.calculate_fragmentation()
                self.update_process_info()
                self.show_statistics()

            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid process ID!")

        def terminate_process(self):
            # Similar to deallocation, but simulating a process "termination"
            self.deallocate_memory()

        def rename_process(self):
            try:
                process_id = int(self.process_num_var.get())
                for process in self.process_list:
                    if process['ID'] == process_id:
                        new_name = simpledialog.askstring("Rename Process", "Enter new name for the process:")
                        process['Name'] = new_name
                        messagebox.showinfo("Success", f"Process P{process_id} renamed to {new_name}!")
                        return
                messagebox.showerror("Error", "Process not found!")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid process ID!")

        def suspend_process(self):
            try:
                process_id = int(self.process_num_var.get())
                for process in self.process_list:
                    if process['ID'] == process_id:
                        process['Status'] = 'Suspended'
                        messagebox.showinfo("Success", f"Process P{process_id} suspended!")
                        return
                messagebox.showerror("Error", "Process not found!")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid process ID!")

        def resume_process(self):
            try:
                process_id = int(self.process_num_var.get())
                for process in self.process_list:
                    if process['ID'] == process_id:
                        process['Status'] = 'Running'
                        messagebox.showinfo("Success", f"Process P{process_id} resumed!")
                        return
                messagebox.showerror("Error", "Process not found!")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid process ID!")

        def defragment_memory(self):
            # Combines adjacent free blocks into one larger block
            new_memory_blocks = []
            current_block_size = 0
            for i in range(len(self.memory_blocks)):
                if self.processes[i] is None:
                    current_block_size += self.original_memory[i]
                else:
                    if current_block_size > 0:
                        new_memory_blocks.append(current_block_size)
                        current_block_size = 0
                    new_memory_blocks.append(self.original_memory[i])

            if current_block_size > 0:
                new_memory_blocks.append(current_block_size)

            self.memory_blocks = new_memory_blocks
            self.original_memory = self.memory_blocks.copy()
            self.processes = [None] * len(self.memory_blocks)
            self.update_memory_labels()
            messagebox.showinfo("Defragmentation Complete", "Memory blocks have been defragmented.")

        def update_memory_labels(self):
            # Updates memory block labels after defragmentation
            for i, block_size in enumerate(self.memory_blocks):
                self.block_labels[i].config(text=f"Block {i+1}: {block_size}KB - Free", bg="lightgreen")

        def visualize_memory(self):
            allocated = [self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is not None]
            free = [self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None]

            labels = [f"P{proc[' ID']}" for proc in self.process_list]
            plt.pie([sum(allocated), sum(free)], labels=["Allocated", "Free"], autopct='%1.1f%%')
            plt.title("Memory Allocation")
            plt.show()

        def calculate_fragmentation(self):
            fragmentation = sum(self.memory_blocks[i] for i in range(len(self.memory_blocks)) if self.processes[i] is None)
            self.fragmentation_label.config(text=f"Fragmentation: {fragmentation}KB")

        def show_statistics(self):
            total_memory = sum(self.original_memory)
            used_memory = total_memory - sum(self.memory_blocks)
            free_memory = total_memory - used_memory
            self.statistics_label.config(text=f"Total Memory: {total_memory}KB | Used: {used_memory}KB | Free: {free_memory}KB")

        def update_process_info(self):
            if self.process_list:
                running_processes = ", ".join([f"P{proc['ID']} (Priority: {proc['Priority']}, Status: {proc['Status']})" for proc in self.process_list])
            else:
                running_processes = "None"
            self.process_info_label.config(text=f"Running Processes: {running_processes}")

        def memory_usage_graph(self):
            allocated_sizes = [proc['Size'] for proc in self.process_list]
            allocated_labels = [f"P{proc['ID']}" for proc in self.process_list]
            plt.bar(allocated_labels, allocated_sizes, color='orange')
            plt.title("Memory Usage by Processes")
            plt.xlabel("Processes")
            plt.ylabel("Memory Size (KB)")
            plt.show()

    if __name__ == "__main__":
        root = tk.Tk()
        app = MemoryManager(root)
        root.mainloop()