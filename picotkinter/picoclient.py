# made by woodycal
# This client is designed only to work on full python, it will not work on Micropython!


import tkinter as tk
from tkinter import ttk
import threading
import time
import socket
import json

HOST = 'changeme' #server host
PORT = 8080
data_payload = 2048
style = 'utf-8'

class ThreadedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pico secure delivery box ")

        # Variable to store submitted data
        self.submitted_data = {}

        # Create and place widgets
        self.setup_widgets()


    def echo_long_task(self):
        # Start a new thread to run the long-running task
        threading.Thread(target=self.echo_state(), daemon=True).start()

    def echo_armed(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        try:
            sock.connect(server_address)
            sock.send("ARMED".encode())
            datamain = sock.recv(data_payload)
            data1main = datamain.decode(style)
            if data1main == "ARMED":
                print("message sent")
        except Exception as e:
            print(f"Error in echo_armed: {e}")
        finally:
            sock.close()
            self.status_label.config(text=f"Box is now: {data1main}")



    def echo_disarmed(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        try:
            sock.connect(server_address)
            sock.send("DISARMED".encode())
            datamain = sock.recv(data_payload)
            data1main = datamain.decode(style)
            if data1main == "DISARMED":
                print("message sent")
        except Exception as e:(
            print(f"Error in echo_disarmed: {e}"))
        finally:
            sock.close()
            self.status_label.config(text=f"Box is now: {data1main}")


    def echo_dropoffmode(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        try:
            sock.connect(server_address)
            sock.send("DROPOFFMODE".encode())
            datamain = sock.recv(data_payload)
            data1main = datamain.decode(style)
            if data1main == "DROPOFFMODE":
                print("message sent")
        except Exception as e:
            print(f"Error in echo_dropoffmode: {e}")
        finally:
            sock.close()
            self.status_label.config(text=f"Box is now: {data1main}")


    def echo_weather_stats(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        try:
            sock.connect(server_address)
            sock.send("getweathervalue".encode())
            datamain = sock.recv(data_payload)
            data1main = datamain.decode(style)
            if data1main == "getweathervalue":
                print("message sent")
        except Exception as e:
            print(f"Error in echo_state: {e}")
        finally:
            sock.close()
            self.status_label.config(text=f"Weather statistics: {data1main}")


    def echo_state(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        try:
            sock.connect(server_address)
            sock.send("GETSTATE".encode())
            datamain = sock.recv(data_payload)
            data1main = datamain.decode(style)
        except Exception as e:
            print(f"Error in echo_state: {e}")
        finally:
            sock.close()
            self.status_label.config(text=f"Box is now: {data1main}")

    def echo_clear_schedule(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        sock.connect(server_address)
        sock.send("CLEARSCHEDULES".encode())
        sock.close()
        self.submitted_data_label.config(text="Schedules Removed")




    def setup_widgets(self):
        # Box 1: Frame with buttons and labels
        box1 = tk.Frame(self.root, bd=2, relief="groove")
        box1.grid(row=0, column=0, padx=10, pady=10)

        # Buttons to start long-running tasks
        btn_armed = tk.Button(box1, text="ARMED", command=self.echo_armed)
        btn_armed.pack(side=tk.TOP, fill=tk.X)
        btn_disarmed = tk.Button(box1, text="DISARMED", command=self.echo_disarmed)
        btn_disarmed.pack(side=tk.TOP, fill=tk.X)
        btn_dropoffmode = tk.Button(box1, text="DROPOFFMODE", command=self.echo_dropoffmode)
        btn_dropoffmode.pack(side=tk.TOP, fill=tk.X)
        btn_weatherstats = tk.Button(box1, text="Weather statistics", command=self.echo_weather_stats)
        btn_weatherstats.pack(side=tk.TOP, fill=tk.X)

        self.status_label = tk.Label(box1, text="Box Status: NOT SET")
        self.status_label.pack(side=tk.TOP, fill=tk.X)
        self.status_label1 = tk.Label(box1, text="Weather statistics:")
        self.status_label1.pack(side=tk.TOP, fill=tk.X)

        btn_update = tk.Button(box1, text="Get Box Status", command=self.echo_long_task)
        btn_update.pack(side=tk.TOP, fill=tk.X)

        # Box 2: Frame with dropdown menus and submit button
        box2 = tk.Frame(self.root, bd=2, relief="groove")
        box2.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown menu for hours
        self.hour_var = tk.StringVar()
        hour_dropdown = ttk.Combobox(box2, textvariable=self.hour_var)
        hour_dropdown['values'] = [f"{h:02}" for h in range(24)]
        hour_dropdown.current(0)  # set the selected item
        hour_dropdown.pack(pady=5)

        # Dropdown menu for minutes
        self.minute_var = tk.StringVar()
        minute_dropdown = ttk.Combobox(box2, textvariable=self.minute_var)
        minute_dropdown['values'] = [f"{m:02}" for m in range(60)]
        minute_dropdown.current(0)  # set the selected item
        minute_dropdown.pack(pady=5)

        # Dropdown menu for state
        self.state_var = tk.StringVar()
        state_dropdown = ttk.Combobox(box2, textvariable=self.state_var)
        state_dropdown['values'] = ["ARMED", "DISARMED", "DROPOFFMODE"]
        state_dropdown.current(0)  # set the selected item
        state_dropdown.pack(pady=5)

        # Dropdown menu for schedule
        self.schedule_var = tk.StringVar()
        schedule_dropdown = ttk.Combobox(box2, textvariable=self.schedule_var)
        schedule_dropdown['values'] = ["Schedule 1", "Schedule 2", "Schedule 3","Schedule 4" ]
        schedule_dropdown.current(0)  # set the selected item
        schedule_dropdown.pack(pady=5)

        def submit():
            self.submitted_data.update({
                'hour': hour_dropdown.get(),
                'minute': minute_dropdown.get(),
                'state': state_dropdown.get(),
                'schedule': schedule_dropdown.get()
            })
            self.display_submitted_data()



        btn_submit = tk.Button(box2, text="Submit", command=submit)
        btn_submit.pack(side=tk.TOP, fill=tk.X)

        # Label to display submitted data
        self.submitted_data_label = tk.Label(box2, text="")
        self.submitted_data_label.pack(side=tk.TOP, fill=tk.X)

        btn_clear_schedules = tk.Button(box2, text="Clear Schedules", command=self.echo_clear_schedule)
        btn_clear_schedules.pack(side=tk.TOP, fill=tk.X)


    def update_status(self, message):
        # Update the status label on the main thread
        self.status_label.config(text=message)

    def display_submitted_data(self):
        data_str = ", ".join([f"{key}: {value}" for key, value in self.submitted_data.items()])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_json = json.dumps(self.submitted_data)
        server_address = (HOST, PORT)
        sock.connect(server_address)
        sock.send(f"schedule{data_json}".encode())
        sock.close()
        self.submitted_data_label.config(text=f"Submitted Data: {self.submitted_data}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ThreadedApp(root)
    root.mainloop()
