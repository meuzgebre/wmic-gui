import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import json

# Function to execute a wmic command for a given category and return the output
def execute_wmic_command(category):
    """
    Execute a WMIC command to retrieve system information for a given category.
    
    Args:
        category (str): The category for which to fetch system information.
    
    Returns:
        dict: A dictionary containing the retrieved system information.
    """
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
    """
    Load system information data from a local cache.
    
    Args:
        category (str): The category for which to load system information.
    
    Returns:
        dict: A dictionary containing the cached system information.
    """
    try:
        cache_file = f"{category}.json"
        with open(cache_file, "r") as cache:
            data = json.load(cache)
            return data
    except FileNotFoundError:
        return None

# Function to create a table (Treeview) for a category
def create_table(tab, pairs):
    """
    Create a table (Treeview) for a category and populate it with system information.
    
    Args:
        tab (ttk.Frame): The tab where the table should be created.
        pairs (dict): A dictionary containing system information.
    
    Returns:
        ttk.Treeview: The created Treeview widget.
    """
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
    """
    Fetch system information data and update the Treeview for a specific category.

    Args:
        tab (ttk.Frame): The tab where the Treeview should be created.
        category (str): The category for which to fetch system information.
    """
    pairs = load_data_from_cache(category)
    if pairs is None:
        pairs = execute_wmic_command(category)

    if pairs:
        table = create_table(tab, pairs)

# Create the main application window
def main():
    app = tk.Tk()
    
    # Get the screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculate the X and Y coordinates for centering the window
    x = (screen_width - 800) // 2
    y = (screen_height - 600) // 2

    app.title("System Information Viewer")
    app.geometry(f"800x600+{x}+{y}")  # Fixed window size

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
