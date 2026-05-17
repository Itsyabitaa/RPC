import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rpc_core.rpc_client import RPCClient
from rpc_core.protocol import RPCError
from client.generated_stub import CalculatorStub

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RPC Calculator Framework")
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e2e2e")

        # Initialize RPC components
        self.rpc_client = RPCClient('127.0.0.1', 5555)
        self.calculator = CalculatorStub(self.rpc_client)

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

        tk.Button(btn_frame, text="+", command=lambda: self.execute_rpc("add"), **btn_style).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="-", command=lambda: self.execute_rpc("subtract"), **btn_style).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="*", command=lambda: self.execute_rpc("multiply"), **btn_style).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="/", command=lambda: self.execute_rpc("divide"), **btn_style).grid(row=1, column=1, padx=10, pady=5)

        # Result display
        self.lbl_result = tk.Label(self.root, text="Result: -", font=("Helvetica", 14), fg="#4CAF50", bg="#2e2e2e", wraplength=300)
        self.lbl_result.pack(pady=20)

    def execute_rpc(self, operation):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        self.lbl_result.config(text="Sending request...", fg="#FFC107")
        self.root.update()

        try:
            self.rpc_client.connect()
            
            # Map operation to stub method
            if operation == "add":
                res = self.calculator.add(a, b)
            elif operation == "subtract":
                res = self.calculator.subtract(a, b)
            elif operation == "multiply":
                res = self.calculator.multiply(a, b)
            elif operation == "divide":
                res = self.calculator.divide(a, b)

            self.lbl_result.config(text=f"Result: {res}", fg="#4CAF50")
            
        except RPCError as e:
            self.lbl_result.config(text=f"RPC Error: {e.message}", fg="#F44336")
        except Exception as e:
            self.lbl_result.config(text=f"Connection Error: Server might be down.", fg="#F44336")
        finally:
            # We don't necessarily need to keep the connection open, 
            # our transport layer handles reconnection if needed.
            self.rpc_client.disconnect()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    
    # Check if user needs instruction on running server
    print("GUI Starting... Ensure you are running 'python server/calculator_server.py' in a separate terminal!")
    
    root.mainloop()
