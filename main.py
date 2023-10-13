import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import json

# Function to execute a wmic command for a given category and return the output
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
                    header, value = item.split('=', 1)  # Split at the first "="
                    headers.append(header)
                    values.append(value)

            pairs = dict(zip(headers, values))

            # Cache the data in a local file
            cache_file = f"{category}.json"
            with open(cache_file, "w") as cache:
                json.dump(pairs, cache)

            return pairs
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to load data from cache
def load_data_from_cache(category):
    try:
        cache_file = f"{category}.json"
        with open(cache_file, "r") as cache:
            data = json.load(cache)
            return data
    except FileNotFoundError:
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
        tree.column(col, width=200)  # Adjust the column width as needed

    # Adding the rows to the tree
    for att, value in pairs.items():
        tree.insert("", "end", values=(att, value))

    tree.pack(fill="both", expand=True)
    return tree

# Function to fetch data and update the table
def fetch_data_and_update_tree(tab, category):
    pairs = load_data_from_cache(category)
    if pairs is None:
        pairs = execute_wmic_command(category)

    if pairs:
        table = create_table(tab, pairs)

# Create the main application window
def main():
    app = tk.Tk()
    app.title("System Information Viewer")
    app.geometry("800x400")  # Fixed window size

    # Create tabs for different categories
    tabs = ttk.Notebook(app)

    # categories = ["OS", "CPU", "DiskDrive", "LogicalDisk", "MemoryChip", "Baseboard", "BIOS"]
    categories = ["OS", "CPU", "DiskDrive", "LogicalDisk", "MemoryChip", "Baseboard", "BIOS", "MEMORYCHIP", "NIC"]

    for category in categories:
        tab = ttk.Frame(tabs)
        tabs.add(tab, text=category)

        # Use threading to fetch data in parallel
        thread = threading.Thread(target=fetch_data_and_update_tree, args=(tab, category))
        thread.start()

    tabs.pack(fill="both", expand=True)  # Make the tabs expand to fill the window

    app.mainloop()

if __name__ == "__main__":
    main()
