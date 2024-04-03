import time
import serial
import threading
import keyboard as k
from pathlib import Path
import tkinter as tk
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk

stop_threads = False


# Function to set serial connection
def set_connection():
    while not stop_threads:
        try:
            serial_connection = serial.Serial('COM4', 9600)
            return serial_connection

        except Exception as e:
            print("The connection was not established ", e)
            print("Reconnecting...")
            time.sleep(1)


# Function to read serial port
def read_serial_port(arduino):
    try:
        while not stop_threads:
            data = arduino.readline().decode().strip()
            if data:
                print(data)
            time.sleep(0.03)  # Short delay to avoid saturating the processor
    except Exception as e:
        print("Error reading the serial port ", e)


# Function to send data by the serial port
def send_data(arduino):
    try:
        while not stop_threads:
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
            time.sleep(0.02)

    except Exception as e:
        print("Error sending data ", e)


def interface():

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

    '''
    def on_spinbox_modified():
        selected_value = Slider.get()
        print("Valor seleccionado:", selected_value)
    '''

    def on_slider_changed(value):
        print("Valor seleccionado:", value)

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
        command=lambda: print("button_1 clicked"),
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
        command=lambda: print("button_3 clicked"),
        relief="flat"
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
        command=lambda: print("button_4 clicked"),
        relief="flat"
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
        command=lambda: print("button_5 clicked"),
        relief="flat"
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
        command=lambda: print("button_6 clicked"),
        relief="flat"
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
        relief="flat"
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
        highlightthickness=0
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
        command=on_slider_changed)

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
ser = None

if ser is not None:
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

    # Close connection
    ser.close()
    print("Serial connection closed")

else:
    print("Serial connection could not be established")

interface_thread.join()
