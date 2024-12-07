import sys
from tracker import PhoneNumberTracker
import tkinter as tk
from tkinter import messagebox

class TrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Number Tracker")

        self.api_key = "39838ca6d8b04ac085ad44e0f400ca6a"  # Replace with your OpenCage API key
        self.tracker = PhoneNumberTracker(self.api_key)

        # GUI Components
        self.label = tk.Label(root, text="Enter Phone Number (with country code):")
        self.label.pack(pady=10)

        self.phone_entry = tk.Entry(root, width=30)
        self.phone_entry.pack(pady=5)

        self.track_button = tk.Button(root, text="Track", command=self.track_number)
        self.track_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="blue")
        self.result_label.pack(pady=10)

    def track_number(self):
        phone_number = self.phone_entry.get().strip()
        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number.")
            return

        try:
            self.tracker.process_number(phone_number)
            self.tracker.get_approx_coordinates()
            self.tracker.draw_map(phone_number)

            self.result_label.config(text=f"Tracking complete. Map saved for {phone_number}")
            messagebox.showinfo("Success", f"Tracking complete. Map saved for {phone_number}.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackerApp(root)
    root.mainloop()
