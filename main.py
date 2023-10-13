import tkinter as tk
from tkinter import ttk
import subprocess

# Function to execute a wmic command for a given category
def execute_wmic_command(category):
    try:
        command = f"wmic {category} get /format:list"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")

            headers = []
            values = []

            # Iterate over the data list and split into headers and values
            for item in lines:
                if item:  # Check if the item is not an empty string
                    header, value = item.split('=', 1)  # Split at the "="
                    headers.append(header)
                    values.append(value)

            pairs = dict(zip(headers, values))

            return pairs
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to create a table (Treeview) for a category
def create_table(tab, pairs):
    # Create a Frame to hold the Treeview
    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True)

    # Creating the tree (table)
    tree = ttk.Treeview(frame, columns=["Attributes", "Values"], show="headings")

    # Adding columns
    columns = ["Attributes", "Values"]

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    # Adding the rows to the tree
    for att, value in pairs.items():
        tree.insert("", "end", values=(att, value))

    tree.pack(fill="both", expand=True)
    return tree

# Create the main application window
def main():
    app = tk.Tk()
    app.title("System Information Viewer")
    app.geometry("800x400")  # Fixed window size

    # Create tabs for different categories
    tabs = ttk.Notebook(app)

    categories = ["OS", "CPU", "DiskDrive", "LogicalDisk", "MemoryChip", "Baseboard", "BIOS"]    

    # Retrieve data for all categories when the program starts
    category_data = {}
    for category in categories:
        data = execute_wmic_command(category)
        if data:
            category_data[category] = data

    for category in categories:
        tab = ttk.Frame(tabs)
        tabs.add(tab, text=category)

        pairs = category_data.get(category, {})

        table = create_table(tab, pairs)
        
    # Make the tabs expand to fill the window
    tabs.pack(fill="both", expand=True)  

    app.mainloop()

if __name__ == "__main__":
    main()
