import tkinter as tk
from tkinter import ttk
import random

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TechThemedBinaryTreeVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dynamic Tree Size Binary Tree Visualizer")
        self.window.geometry("1200x800")
        self.window.configure(bg='#1e1e1e')

        self.root = None
        self.setup_ui()
        self.setup_tree()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.window, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for tree visualization
        self.canvas = tk.Canvas(main_frame, width=1200, height=650, bg='#2d2d2d', highlightthickness=0)
        self.canvas.pack(pady=10)

        # Control frame
        control_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=10)

        # Tree size slider
        ttk.Label(control_frame, text="Tree Size:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.tree_size = tk.IntVar(value=7)
        self.size_slider = ttk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.tree_size, length=300, style='Dark.Horizontal.TScale', command=self.update_tree_size)
        self.size_slider.pack(side=tk.LEFT)

        # Tree size display
        self.size_display = ttk.Label(control_frame, text="7", style='TargetValue.TLabel')
        self.size_display.pack(side=tk.LEFT, padx=10)

        # Target value input
        ttk.Label(control_frame, text="Target Value:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(20, 10))
        self.target_value = tk.StringVar(value="50")
        self.target_entry = ttk.Entry(control_frame, textvariable=self.target_value, width=5, style='Dark.TEntry')
        self.target_entry.pack(side=tk.LEFT)

        # Search buttons
        self.linear_button = ttk.Button(control_frame, text="Linear Search", command=self.linear_search, style='Accent.TButton')
        self.linear_button.pack(side=tk.LEFT, padx=10)

        self.binary_button = ttk.Button(control_frame, text="Binary Search", command=self.binary_search, style='Accent.TButton')
        self.binary_button.pack(side=tk.LEFT)

        # Info display
        self.info_display = ttk.Label(main_frame, text="Welcome to the Dynamic Tree Size Binary Tree Visualizer!", style='Info.TLabel', wraplength=1180)
        self.info_display.pack(pady=10)

        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e1e')
        style.configure('Dark.TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('Dark.TButton', background='#3c3c3c', foreground='#ffffff')
        style.map('Dark.TButton', background=[('active', '#4c4c4c')])
        
        style.configure('Accent.TButton', background='#007acc', foreground='#ffffff')
        style.map('Accent.TButton', background=[('active', '#005999')])
        
        style.configure('TargetValue.TLabel', background='#1e1e1e', foreground='#00ff00', font=('Arial', 14, 'bold'))
        style.configure('Info.TLabel', background='#1e1e1e', foreground='#00ff00', font=('Arial', 12))
        
        style.configure('Dark.Horizontal.TScale', background='#1e1e1e', troughcolor='#3c3c3c')
        
        style.configure('Dark.TEntry', fieldbackground='#3c3c3c', foreground='#ffffff')

    def setup_tree(self):
        self.update_tree_size()

    def update_tree_size(self, event=None):
        size = self.tree_size.get()
        self.size_display.config(text=str(size))
        values = list(range(1, 101))
        random.shuffle(values)
        self.root = self._build_balanced_tree(values[:size])
        self.draw_tree()
        self.info_display.config(text=f"Tree size updated to {size} nodes. Try searching for a value!")

    def _build_balanced_tree(self, values):
        if not values:
            return None
        mid = len(values) // 2
        root = Node(values[mid])
        root.left = self._build_balanced_tree(values[:mid])
        root.right = self._build_balanced_tree(values[mid+1:])
        return root

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.root:
            return
        
        def get_depth(node):
            if not node:
                return 0
            return 1 + max(get_depth(node.left), get_depth(node.right))
        
        depth = get_depth(self.root)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.vertical_spacing = canvas_height / (depth + 1)
        self.node_radius = min(self.vertical_spacing / 4, 20)
        
        self._draw_node(self.root, canvas_width / 2, self.vertical_spacing, canvas_width / 2)

    def _draw_node(self, node, x, y, x_offset):
        if node:
            node_id = self.canvas.create_oval(x-self.node_radius, y-self.node_radius, x+self.node_radius, y+self.node_radius, fill="#007acc", outline="#ffffff")
            text_id = self.canvas.create_text(x, y, text=str(node.value), font=("Arial", int(self.node_radius/2), "bold"), fill="#ffffff")
            node.node_id = node_id
            node.text_id = text_id
            
            if node.left:
                next_x = x - x_offset
                next_y = y + self.vertical_spacing
                self.canvas.create_line(x, y+self.node_radius, next_x, next_y-self.node_radius, fill="#ffffff")
                self._draw_node(node.left, next_x, next_y, x_offset/2)
            if node.right:
                next_x = x + x_offset
                next_y = y + self.vertical_spacing
                self.canvas.create_line(x, y+self.node_radius, next_x, next_y-self.node_radius, fill="#ffffff")
                self._draw_node(node.right, next_x, next_y, x_offset/2)

    def linear_search(self):
        self._clear_highlight()
        target = self._get_target_value()
        if target is None:
            return
        self.info_display.config(text="Performing Linear Search for value: " + str(target))
        found = self._linear_search(self.root, target)
        if not found:
            self.info_display.config(text=f"Value {target} not found in the tree.")

    def _linear_search(self, node, target):
        if not node:
            return False
        
        self._highlight_node(node, "#ffa500")  # Orange for visited nodes
        self.window.update()
        self.window.after(100)

        if node.value == target:
            self._highlight_node(node, "#00ff00")  # Green for found node
            self.info_display.config(text=f"Value {target} found!")
            return True

        return self._linear_search(node.left, target) or self._linear_search(node.right, target)

    def binary_search(self):
        self._clear_highlight()
        target = self._get_target_value()
        if target is None:
            return
        self.info_display.config(text="Performing Binary Search for value: " + str(target))
        found = self._binary_search(self.root, target)
        if not found:
            self.info_display.config(text=f"Value {target} not found in the tree.")

    def _binary_search(self, node, target):
        if not node:
            return False
        
        self._highlight_node(node, "#ffa500")  # Orange for visited nodes
        self.window.update()
        self.window.after(100)

        if node.value == target:
            self._highlight_node(node, "#00ff00")  # Green for found node
            self.info_display.config(text=f"Value {target} found!")
            return True
        elif target < node.value:
            return self._binary_search(node.left, target)
        else:
            return self._binary_search(node.right, target)

    def _highlight_node(self, node, color):
        self.canvas.itemconfig(node.node_id, fill=color)

    def _clear_highlight(self):
        self._reset_node_color(self.root)

    def _reset_node_color(self, node):
        if node:
            self.canvas.itemconfig(node.node_id, fill="#007acc")
            self._reset_node_color(node.left)
            self._reset_node_color(node.right)

    def _get_target_value(self):
        try:
            return int(self.target_value.get())
        except ValueError:
            self.info_display.config(text="Please enter a valid integer for the target value.")
            return None

    def run(self):
        self.window.mainloop()

# Example usage:
visualizer = TechThemedBinaryTreeVisualizer()
visualizer.run()