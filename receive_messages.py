import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import serial
import time
import queue

# Configuration
SERIAL_PORT = "COM3"  # Change this to your port, e.g., '/dev/ttyUSB0' on Linux/macOS.
BAUD_RATE = 9600      # Adjust if needed

# Create a thread-safe queue to transfer messages from the serial thread to the GUI thread.
message_queue = queue.Queue()

def serial_reader(port, baud_rate, queue_obj):
    """
    Opens the serial port and continuously reads lines. Each complete line is put into the queue.
    """
    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            print(f"Connected to {port} at {baud_rate} baud.")
            # Run an infinite loop to continuously read from the serial port.
            while True:
                try:
                    # Read a line from the serial port (ends with newline).
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        # If we received a message, put it into the queue.
                        queue_obj.put(line)
                except Exception as e:
                    print(f"Error reading from serial port: {e}")
                    break
                time.sleep(0.1)
    except Exception as e:
        print(f"Could not open serial port {port}: {e}")

def update_gui_from_queue(text_widget, queue_obj):
    """
    Periodically checks the queue for new messages and inserts them into the text widget.
    """
    try:
        # Process all messages currently in the queue.
        while not queue_obj.empty():
            message = queue_obj.get_nowait()
            text_widget.insert(tk.END, message + "\n")
            text_widget.see(tk.END)  # Auto-scroll to the end
    except queue.Empty:
        pass
    # Reschedule this function to run again after 100ms.
    text_widget.after(100, update_gui_from_queue, text_widget, queue_obj)

def on_closing(root):
    """
    Handle closing of the GUI window.
    """
    root.destroy()

def main():
    # Create the main window
    root = tk.Tk()
    root.title("XBee Radio Message Display")
    
    # Create a scrolled text widget to display messages
    text_display = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Start the serial reading thread in background
    serial_thread = threading.Thread(target=serial_reader, args=(SERIAL_PORT, BAUD_RATE, message_queue), daemon=True)
    serial_thread.start()

    # Start the periodic GUI update using the after() callback mechanism.
    update_gui_from_queue(text_display, message_queue)

    # Set up the close event handler
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()