import time
import serial
import threading
import keyboard as k
import os
import subprocess
from pathlib import Path
import tkinter as tk
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, filedialog

# Implementation flags
stop_threads = False
ser = None
activation = False
connect = 0
indicator = None
config_mode_flag = True
study_mode_flag = False


# Function to read serial port
def read_serial_port(arduino):
    global activation, stop_threads
    try:
        while not stop_threads and activation is True:
            data = arduino.readline().decode().strip()
            if data:
                print(data)
            time.sleep(0.03)  # Short delay to avoid saturating the processor
    except Exception as e:
        print("Error reading the serial port ", e)
        stop_threads = True


# Function to send data by the serial port
def send_data(arduino):
    global arduino_lock, activation, stop_threads
    try:
        while not stop_threads and activation is True:
            if k.is_pressed('e'):
                cadena = 'e'
                arduino_lock.acquire()  # Disable serial port reading
                time.sleep(0.02)
                arduino.write(cadena.encode('ascii'))  # Send data
                time.sleep(0.02)
                arduino_lock.release()  # Enable serial port reading
            elif k.is_pressed('a'):
                cadena = 'a'
                arduino_lock.acquire()  # Disable serial port reading
                time.sleep(0.02)
                arduino.write(cadena.encode('ascii'))  # Send data
                time.sleep(0.02)
                arduino_lock.release()  # Enable serial port reading
            time.sleep(0.03)

    except Exception as e:
        print("Error sending data ", e)
        stop_threads = True


def interface():
    global indicator

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(fr"{str(OUTPUT_PATH)}\assets\frame0")

    def on_window_close():
        global stop_threads
        stop_threads = True
        window.destroy()

    def on_enter_pressed(event):
        text = entry_1.get()
        print("Texto ingresado:", text)

    def show_selected_option(event):
        selected_option = combo_box_leg.get()
        print("Opción seleccionada:", selected_option)

    def on_slider_changed(value):
        print("Valor seleccionado:", value)

    # Function to set serial connection
    def connect_btn():
        global connect
        connect = 1

    def close_btn():
        global connect, ser, activation
        connect = 2
        indicator.config(bg="gray")
        if ser is not None:
            ser.close()
            ser = None
            activation = False

    def config_mode_btn():
        global config_mode_flag, study_mode_flag, ser, activation, connect
        config_mode_flag = True
        study_mode_flag = False
        button_3.config(state="disabled")  # close btn disable
        button_4.config(state="disabled")  # config btn disable
        button_5.config(state="disabled")  # config btn disable
        button_6.config(state="normal")  # study btn enable
        button_7.config(state="disabled")  # Export to excel btn disable
        entry_1.config(state="normal")  # Entry text box enable
        slider.config(state="disabled")  # slider disable
        connect = 2
        indicator.config(bg="gray")
        if ser is not None:
            ser.close()
            ser = None
            activation = False

    def study_mode_btn():
        global config_mode_flag, study_mode_flag
        config_mode_flag = False
        study_mode_flag = True
        button_3.config(state="normal")  # close btn enable
        button_4.config(state="normal")  # config btn enable
        button_5.config(state="normal")  # config btn enable
        button_6.config(state="disabled")  # study btn disable
        button_7.config(state="normal")  # Export to excel btn enable
        entry_1.config(state="disabled")  # Entry text box disable
        slider.config(state="normal")  # slider enable

    def open_folder():
        # get the directory within the current script
        path = os.path.dirname(__file__)
        # Open the files explorer in the same project path
        rute = filedialog.askopenfilename(initialdir=path, title="Select archive")
        # If a file is selected
        if rute:
            subprocess.Popen(["start", "", rute], shell=True)

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Tk()
    window.geometry("1574x915")
    window.protocol("WM_DELETE_WINDOW", on_window_close)

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=915,
        width=1574,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        334.0,
        351.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        983.0,
        728.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        983.0,
        351.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        334.0,
        728.0,
        image=image_image_4
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=open_folder,
        relief="flat"
    )
    button_1.place(
        x=1329.0,
        y=848.0,
        width=230.0,
        height=60.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=1329.0,
        y=698.0,
        width=230.0,
        height=60.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=close_btn,
        relief="flat",
        state="disabled"
    )
    button_3.place(
        x=1000.0,
        y=90.0,
        width=230.0,
        height=60.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=connect_btn,
        relief="flat",
        state="disabled"
    )
    button_4.place(
        x=1000.0,
        y=9.0,
        width=230.0,
        height=60.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=config_mode_btn,
        relief="flat",
        state="disabled"
    )
    button_5.place(
        x=23.0,
        y=9.0,
        width=230.0,
        height=60.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=study_mode_btn,
        relief="flat",
        state="normal"
    )
    button_6.place(
        x=23.0,
        y=90.0,
        width=230.0,
        height=60.0
    )
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat",
        state="disabled"
    )
    button_7.place(
        x=1330.0,
        y=773.0,
        width=230.0,
        height=60.0
    )
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        1445.0,
        224.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        state="normal"
    )
    entry_1.bind('<Return>', on_enter_pressed)
    entry_1.place(
        x=1350.0,
        y=194.0,
        width=190.0,
        height=58.0
    )

    canvas.create_text(
        1338.0,
        171.0,
        anchor="nw",
        text="Name of patient",
        fill="#000000",
        font=("Inter Black", 13 * -1)
    )

    canvas.create_text(
        420.0,
        12.0,
        anchor="nw",
        text="Maximum configured angle of the left leg",
        fill="#000000",
        font=("Inter Black", 13 * -1)
    )

    canvas.create_text(
        707.0,
        14.0,
        anchor="nw",
        text="Maximum configured angle of the right leg",
        fill="#000000",
        font=("Inter Black", 13 * -1)
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        516.0,
        83.0,
        image=image_image_5
    )

    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        798.0,
        83.0,
        image=image_image_6
    )

    canvas.create_text(
        727.0,
        73.0,
        anchor="nw",
        text="0",
        fill="#000000",
        font=("Inter Black", 24 * -1)
    )

    canvas.create_text(
        448.0,
        66.0,
        anchor="nw",
        text="0",
        fill="#000000",
        font=("Inter Black", 24 * -1)
    )

    canvas.create_text(
        1338.0,
        300.0,
        anchor="nw",
        text="Choose Leg Side",
        fill="#000000",
        font=("Inter Black", 13 * -1)
    )

    canvas.create_text(
        1338,
        425,
        anchor="nw",
        text="Strength",
        fill="#000000",
        font=("Inter Black", 13 * -1)
    )
    indicator = tk.Label(
        window,
        width=5,
        height=2,
        bg="gray"
    )
    indicator.place(x=1250, y=60)
    # Add ComboBox
    options = ["Right", "Left"]
    combo_box_leg = ttk.Combobox(
        window,
        values=options,
        state="readonly",
    )
    combo_box_leg.place(
        x=1338,
        y=320,
        width=220.0,
        height=60.0
    )

    # Bind function show_selected_option to event <<ComboboxSelected>>
    combo_box_leg.bind("<<ComboboxSelected>>", show_selected_option)

    combo_box_leg.configure(
        font=(
            "Inter",
            24,
            "bold"
        ),
        justify="center",
    )

    # Add a slider from 0 to 12
    slider = tk.Scale(
        window,
        from_=0,
        to=12,
        tickinterval=1,
        orient=tk.HORIZONTAL,
        command=on_slider_changed,
        state="disabled"
    )

    slider.place(
        x=1338.0,
        y=450.0,
        width=220,
        height=60
    )

    window.resizable(False, False)
    window.mainloop()


# Starting the interface
interface_thread = threading.Thread(target=interface)
interface_thread.start()

# Create serial connection
while not stop_threads:
    if ser is None and connect == 1:
        while not stop_threads and connect == 1:
            try:
                ser = serial.Serial('COM4', 9600)
                if ser is not None:
                    connect = 0
                    indicator.config(bg="green")

            except Exception as e:
                print("The connection was not established ", e)
                print("Reconnecting...")
                time.sleep(1)
    elif connect == 2:
        print("Connection close")
        connect = 0

    # time.sleep(0.1)
    if ser is not None:
        activation = True
        arduino_lock = threading.Lock()  # Lock to ensure mutual exclusion between sending and receiving data

        # Starting the reading thread
        reading_thread = threading.Thread(target=read_serial_port, args=(ser,))
        reading_thread.start()

        # Starting the sending thread
        sending_thread = threading.Thread(target=send_data, args=(ser,))
        sending_thread.start()

        # Wait up to all threads end
        reading_thread.join()
        sending_thread.join()

        if activation is True:
            # Close connection
            ser.close()
            print("Serial connection closed")

    elif ser is None:
        print("Serial connection could not be established")
    time.sleep(0.2)

interface_thread.join()