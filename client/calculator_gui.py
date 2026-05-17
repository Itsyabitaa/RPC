import sys
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_client import RPCClient
from rpc_core.protocol import RPCError
from client.generated_stub import CalculatorStub

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RPC Calculator Framework")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e2e2e")

        # Initialize RPC components
        self.rpc_client = RPCClient('127.0.0.1', 5555)
        self.calculator = CalculatorStub(self.rpc_client)

        self.buttons = []
        self._build_ui()

    def _build_ui(self):
        # Header
        tk.Label(self.root, text="Remote Calculator", font=("Helvetica", 16, "bold"), fg="white", bg="#2e2e2e").pack(pady=15)

        # Inputs Frame
        frame = tk.Frame(self.root, bg="#2e2e2e")
        frame.pack(pady=10)

        tk.Label(frame, text="Value A:", font=("Helvetica", 12), fg="white", bg="#2e2e2e").grid(row=0, column=0, padx=5, pady=5)
        self.entry_a = tk.Entry(frame, font=("Helvetica", 12), width=10)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Value B:", font=("Helvetica", 12), fg="white", bg="#2e2e2e").grid(row=1, column=0, padx=5, pady=5)
        self.entry_b = tk.Entry(frame, font=("Helvetica", 12), width=10)
        self.entry_b.grid(row=1, column=1, padx=5, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#2e2e2e")
        btn_frame.pack(pady=15)

        btn_style = {"font": ("Helvetica", 12, "bold"), "width": 5, "bg": "#4CAF50", "fg": "white"}

        btn_add = tk.Button(btn_frame, text="+", command=lambda: self.start_rpc_thread("add"), **btn_style)
        btn_add.grid(row=0, column=0, padx=10, pady=5)
        
        btn_sub = tk.Button(btn_frame, text="-", command=lambda: self.start_rpc_thread("subtract"), **btn_style)
        btn_sub.grid(row=0, column=1, padx=10, pady=5)
        
        btn_mul = tk.Button(btn_frame, text="*", command=lambda: self.start_rpc_thread("multiply"), **btn_style)
        btn_mul.grid(row=1, column=0, padx=10, pady=5)
        
        btn_div = tk.Button(btn_frame, text="/", command=lambda: self.start_rpc_thread("divide"), **btn_style)
        btn_div.grid(row=1, column=1, padx=10, pady=5)
        
        self.buttons.extend([btn_add, btn_sub, btn_mul, btn_div])

        # Progress and Status
        self.lbl_status = tk.Label(self.root, text="Ready", font=("Helvetica", 10, "italic"), fg="#aaaaaa", bg="#2e2e2e")
        self.lbl_status.pack(pady=(10, 0))

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Result display
        self.lbl_result = tk.Label(self.root, text="Result: -", font=("Helvetica", 16, "bold"), fg="#4CAF50", bg="#2e2e2e", wraplength=350)
        self.lbl_result.pack(pady=15)

    def set_ui_state(self, state):
        """Enable or disable buttons while processing"""
        for btn in self.buttons:
            btn.config(state=state)

    def update_progress(self, text, value):
        """Update progress bar and status text safely from background thread"""
        self.lbl_status.config(text=text)
        self.progress['value'] = value
        self.root.update_idletasks()

    def start_rpc_thread(self, operation):
        """Starts a background thread so the GUI doesn't freeze during time.sleep"""
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        self.set_ui_state(tk.DISABLED)
        self.lbl_result.config(text="", fg="#4CAF50")
        
        # Run the simulated process in a background thread
        thread = threading.Thread(target=self._execute_rpc_with_delays, args=(operation, a, b))
        thread.daemon = True
        thread.start()

    def _execute_rpc_with_delays(self, operation, a, b):
        try:
            # 1. Initiating
            self.root.after(0, self.update_progress, "Initiating RPC Call...", 10)
            time.sleep(0.6)

            # 2. Marshaling
            self.root.after(0, self.update_progress, "Marshaling parameters to JSON...", 30)
            time.sleep(0.8)

            # 3. Sending
            self.root.after(0, self.update_progress, "Sending data over TCP socket...", 50)
            time.sleep(0.6)

            # 4. Waiting / Actual Execution
            self.root.after(0, self.update_progress, "Waiting for Server response...", 70)
            
            # --- ACTUAL RPC CALL ---
            self.rpc_client.connect()
            if operation == "add":
                res = self.calculator.add(a, b)
            elif operation == "subtract":
                res = self.calculator.subtract(a, b)
            elif operation == "multiply":
                res = self.calculator.multiply(a, b)
            elif operation == "divide":
                res = self.calculator.divide(a, b)
            # -----------------------

            # 5. Unmarshaling
            self.root.after(0, self.update_progress, "Unmarshaling response JSON...", 90)
            time.sleep(0.8)

            # 6. Done
            self.root.after(0, self.update_progress, "Process Complete!", 100)
            self.root.after(0, lambda: self.lbl_result.config(text=f"Result: {res}", fg="#4CAF50"))

        except RPCError as e:
            self.root.after(0, self.update_progress, "RPC Error encountered!", 100)
            self.root.after(0, lambda: self.lbl_result.config(text=f"Server Error:\n{e.message}", fg="#F44336"))
        except Exception as e:
            self.root.after(0, self.update_progress, "Connection Failed!", 100)
            self.root.after(0, lambda: self.lbl_result.config(text="Connection Error: Is the server running?", fg="#F44336"))
        finally:
            self.rpc_client.disconnect()
            self.root.after(0, self.set_ui_state, tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
