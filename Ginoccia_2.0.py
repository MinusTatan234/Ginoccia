import time
import serial
import threading
import keyboard as k


# Function to set serial connection
def set_connection():
    while True:
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
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print(data)
            time.sleep(0.03)  # Short delay to avoid saturating the processor
    except Exception as e:
        print("Error reading the serial port ", e)


# Function to send data by the serial port
def send_data(arduino):
    try:
        while True:
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


# Create serial connection
ser = set_connection()

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
