import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Combobox, Style
import subprocess
import sys
import os
from tkinter.font import Font
import threading

class Volatility3GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Volatility3 GUI")
        self.configure(bg='black')
        self.geometry("1200x800")  # Adjust window size for larger output area

        self.memory_image = None
        self.volatility_path = os.path.join(os.path.dirname(sys.argv[0]), 'vol.py')  # Path to the included vol.py
        self.os_selection = None
        self.plugins = {
            'windows': ["windows.pslist", "windows.pstree", "windows.netscan", "windows.dlllist",
                        "windows.filescan", "windows.handles", "windows.hivelist",
                        "windows.info", "windows.malfind", "windows.memmap",
                        "windows.modules", "windows.mutantscan", "windows.privs",
                        "windows.psscan", "windows.sessions", "windows.ssdt",
                        "windows.symlinkscan", "windows.vadinfo", "windows.verinfo"],
            'linux': ["linux.pslist", "linux.pstree"],
            'mac': ["mac.pslist", "mac.pstree"]
        }
        self.create_widgets()

    def create_widgets(self):
        # Create a menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Add a Help menu with a README option
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="README", command=self.show_readme)

        top_frame = tk.Frame(self, bg='black')
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Custom font for the GUI name
        custom_font = Font(family="Helvetica", size=20, weight="bold")

        # GUI name label with bloody red color
        self.gui_name_label = tk.Label(top_frame, text="Volatility3 GUI", font=custom_font, bg='black', fg='#8B0000')
        self.gui_name_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Controls on the right
        controls_frame = tk.Frame(top_frame, bg='black')
        controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Memory Image Loader
        self.load_button = tk.Button(controls_frame, text="Load Memory Image", command=self.load_memory_image, bg='orange', fg='white')
        self.load_button.pack(pady=5, side=tk.LEFT, padx=5)

        # Volatility Path Loader
        self.load_vol_button = tk.Button(controls_frame, text="Load Volatility3 (vol.py)", command=self.load_volatility, bg='orange', fg='white')
        self.load_vol_button.pack(pady=5, side=tk.LEFT, padx=5)

        # OS Selector
        self.os_label = tk.Label(controls_frame, text="Select OS", bg='black', fg='orange')
        self.os_label.pack(pady=5, side=tk.LEFT, padx=5)
        self.os_combo = Combobox(controls_frame, values=["Windows", "Linux", "Mac"], state="readonly")
        self.os_combo.bind("<<ComboboxSelected>>", self.update_plugins)
        self.os_combo.pack(pady=5, side=tk.LEFT, padx=5)

        # Plugin Selector
        self.plugin_label = tk.Label(controls_frame, text="Select Plugin or Enter Custom Plugin", bg='black', fg='orange')
        self.plugin_label.pack(pady=5, side=tk.LEFT, padx=5)
        self.plugin_combo = Combobox(controls_frame, values=[], state="normal")
        self.plugin_combo.pack(pady=5, side=tk.LEFT, padx=5)

        # Execute Button
        self.execute_button = tk.Button(controls_frame, text="Execute Plugin", command=self.execute_plugin, bg='orange', fg='white')
        self.execute_button.pack(pady=5, side=tk.LEFT, padx=5)

        # Export Button
        self.export_button = tk.Button(controls_frame, text="Export Results", command=self.export_results, bg='orange', fg='white')
        self.export_button.pack(pady=5, side=tk.LEFT, padx=5)

        # Custom Progress Bar Canvas (always shown)
        self.progress_canvas = tk.Canvas(self, width=500, height=50, bg='black', highlightthickness=0)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 50, fill='green', outline='white')
        self.progress_text = self.progress_canvas.create_text(250, 25, text="0%", fill="white", font=("Helvetica", 20))
        self.progress_canvas.pack(pady=10, side=tk.TOP, fill=tk.X)

        # Search Field and Button
        search_frame = tk.Frame(self, bg='black')
        search_frame.pack(pady=5, side=tk.TOP, fill=tk.X)
        self.search_label = tk.Label(search_frame, text="Search:", bg='black', fg='orange')
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(search_frame, text="Search", command=self.search_text, bg='orange', fg='white')
        self.search_button.pack(side=tk.LEFT)

        # Output Display
        self.output_text = scrolledtext.ScrolledText(self, width=120, height=30, bg='black', fg='white', insertbackground='white')  # Increased height
        self.output_text.pack(pady=10, expand=True, fill=tk.BOTH)

        # Style configuration for Progressbar
        style = Style(self)
        style.configure('green.Horizontal.TProgressbar', background='orange')

    def show_readme(self):
        readme_window = tk.Toplevel(self)
        readme_window.title("README")
        readme_window.geometry("600x400")
        readme_text = scrolledtext.ScrolledText(readme_window, width=70, height=20, wrap=tk.WORD, bg='black', fg='white')
        readme_text.pack(expand=True, fill=tk.BOTH)
        try:
            script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Get the directory of the executable
            readme_path = os.path.join(script_dir, 'README.txt')
            with open(readme_path, 'r') as file:
                readme_content = file.read()
                readme_text.insert(tk.END, readme_content)
                readme_text.config(state=tk.DISABLED)
        except FileNotFoundError:
            messagebox.showerror("Error", "README.txt file not found.")

    def load_memory_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Memory Images", "*.img *.mem *.raw")])
        if file_path:
            self.memory_image = file_path
            messagebox.showinfo("Memory Image Loaded", f"Loaded memory image: {file_path}")
        else:
            messagebox.showerror("Error", "No memory image selected.")

    def load_volatility(self):
        # This method is now redundant as vol.py is included with the executable.
        self.volatility_path = os.path.join(os.path.dirname(sys.argv[0]), 'vol.py')
        if os.path.exists(self.volatility_path):
            messagebox.showinfo("Volatility3 Loaded", f"Loaded Volatility3 script: {self.volatility_path}")
        else:
            messagebox.showerror("Error", "Volatility3 script not found.")

    def update_plugins(self, event):
        selected_os = self.os_combo.get().lower()
        if selected_os in self.plugins:
            self.plugin_combo['values'] = self.plugins[selected_os]
        else:
            self.plugin_combo['values'] = []

    def update_progress(self, value):
        self.progress_canvas.coords(self.progress_rect, 0, 0, value * 5, 50)
        self.progress_canvas.itemconfig(self.progress_text, text=f"{int(value)}%")

    def execute_plugin(self):
        if not self.memory_image:
            messagebox.showerror("Error", "Please load a memory image first.")
            return
        if not self.volatility_path:
            messagebox.showerror("Error", "Volatility3 script (vol.py) not found.")
            return
        plugin = self.plugin_combo.get()
        if not plugin:
            messagebox.showerror("Error", "Please select a plugin to execute.")
            return

        self.update_progress(0)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Executing {plugin}...\n")

        # Run the plugin execution in a separate thread
        thread = threading.Thread(target=self.run_plugin, args=(plugin,))
        thread.start()

    def run_plugin(self, plugin):
        try:
            command = [sys.executable, self.volatility_path, '-f', self.memory_image, plugin]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

            total_lines = 100  # Set a dummy value for total lines
            processed_lines = 0

            for line in iter(process.stdout.readline, ''):
                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)
                self.update_idletasks()
                processed_lines += 1
                progress_value = (processed_lines / total_lines) * 100
                self.update_progress(min(progress_value, 100))

            self.update_progress(100)
            self.output_text.insert(tk.END, "Execution finished.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to execute plugin {plugin}")
            self.update_progress(0)

    def search_text(self):
        search_term = self.search_entry.get()
        self.output_text.tag_remove('found', '1.0', tk.END)

        if search_term:
            start_pos = '1.0'
            while True:
                start_pos = self.output_text.search(search_term, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.output_text.tag_add('found', start_pos, end_pos)
                start_pos = end_pos
            self.output_text.tag_config('found', background='yellow', foreground='black')

    def export_results(self):
        if not self.output_text.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "No results to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("PDF files", "*.pdf")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.output_text.get("1.0", tk.END))
                messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")

if __name__ == "__main__":
    app = Volatility3GUI()
    app.mainloop()
