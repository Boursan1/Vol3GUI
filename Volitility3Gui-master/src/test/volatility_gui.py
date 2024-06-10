import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Combobox, Style
import subprocess
import sys
import re

class Volatility3GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Volatility3 GUI")
        self.configure(bg='black')
        self.geometry("1000x700")

        self.memory_image = None
        self.volatility_path = None
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
        top_frame = tk.Frame(self, bg='black')
        top_frame.pack(side=tk.TOP, fill=tk.X)

        left_frame = tk.Frame(top_frame, bg='black')
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        right_frame = tk.Frame(top_frame, bg='black')
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Custom Progress Bar Canvas
        self.progress_canvas = tk.Canvas(left_frame, width=500, height=50, bg='black', highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 50, fill='green', outline='white')
        self.progress_text = self.progress_canvas.create_text(250, 25, text="0%", fill="white", font=("Helvetica", 20))

        # Memory Image Loader
        self.load_button = tk.Button(right_frame, text="Load Memory Image", command=self.load_memory_image, bg='orange', fg='white')
        self.load_button.pack(pady=10)

        # Volatility Path Loader
        self.load_vol_button = tk.Button(right_frame, text="Load Volatility3 (vol.py)", command=self.load_volatility, bg='orange', fg='white')
        self.load_vol_button.pack(pady=10)

        # OS Selector
        self.os_label = tk.Label(right_frame, text="Select OS", bg='black', fg='orange')
        self.os_label.pack(pady=5)
        self.os_combo = Combobox(right_frame, values=["Windows", "Linux", "Mac"], state="readonly")
        self.os_combo.bind("<<ComboboxSelected>>", self.update_plugins)
        self.os_combo.pack(pady=5)

        # Plugin Selector
        self.plugin_label = tk.Label(right_frame, text="Select Plugin", bg='black', fg='orange')
        self.plugin_label.pack(pady=5)
        self.plugin_combo = Combobox(right_frame, values=[], state="readonly")
        self.plugin_combo.pack(pady=5)

        # Execute Button
        self.execute_button = tk.Button(right_frame, text="Execute Plugin", command=self.execute_plugin, bg='orange', fg='white')
        self.execute_button.pack(pady=10)

        # Export Button
        self.export_button = tk.Button(right_frame, text="Export Results", command=self.export_results, bg='orange', fg='white')
        self.export_button.pack(pady=10)

        # Output Display
        self.output_text = scrolledtext.ScrolledText(self, width=120, height=20, bg='black', fg='white', insertbackground='white')
        self.output_text.pack(pady=10)

        # Style configuration for Progressbar
        style = Style(self)
        style.configure('orange.Horizontal.TProgressbar', background='orange')

    def load_memory_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Memory Images", "*.img *.mem *.raw")])
        if file_path:
            self.memory_image = file_path
            messagebox.showinfo("Memory Image Loaded", f"Loaded memory image: {file_path}")
        else:
            messagebox.showerror("Error", "No memory image selected.")

    def load_volatility(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.volatility_path = file_path
            messagebox.showinfo("Volatility3 Loaded", f"Loaded Volatility3 script: {file_path}")
        else:
            messagebox.showerror("Error", "No Volatility3 script selected.")

    def update_plugins(self, event):
        selected_os = self.os_combo.get().lower()
        if selected_os in self.plugins:
            self.plugin_combo['values'] = self.plugins[selected_os]
        else:
            self.plugin_combo['values'] = []

    def update_progress(self, value):
        self.progress_canvas.coords(self.progress_rect, 0, 0, value*5, 50)
        self.progress_canvas.itemconfig(self.progress_text, text=f"{int(value)}%")

    def execute_plugin(self):
        if not self.memory_image:
            messagebox.showerror("Error", "Please load a memory image first.")
            return
        if not self.volatility_path:
            messagebox.showerror("Error", "Please load the Volatility3 script (vol.py) first.")
            return
        plugin = self.plugin_combo.get()
        if not plugin:
            messagebox.showerror("Error", "Please select a plugin to execute.")
            return

        self.update_progress(0)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Executing {plugin}...\n")

        try:
            python_executable = sys.executable if sys.executable else 'python3'
            command = [python_executable, self.volatility_path, '-f', self.memory_image, plugin]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            total_lines = 100  # Set a dummy value for total lines
            processed_lines = 0

            for line in process.stdout:
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
