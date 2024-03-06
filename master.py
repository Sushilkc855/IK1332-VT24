import bluetooth  # Import Bluetooth library
import firebase_admin  # Import Firebase library
from firebase_admin import credentials, db  # Import specific modules from Firebase library

# Initialize Firebase with provided credentials
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iotrasp-fc960-default-rtdb.europe-west1.firebasedatabase.app/'})

# Bluetooth setup
server_address = "B8:27:EB:3F:E3:D4"  # Bluetooth server's address
port = 1  # The port number to connect to on the server

# Create a Bluetooth socket using RFCOMM protocol
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # Connect to the Bluetooth server using the specified address and port
    client_socket.connect((server_address, port))
    print("Connected to Bluetooth server.")

    while True:
        # Receive data from the server
        received_data = client_socket.recv(1024).decode('utf-8')  # Decode the received data

        # Print and push data to Firebase
        print(f"Received data:\n{received_data}")

        # Split the received data into individual values (temperature, pressure, humidity)
        data_list = received_data.split('\n')
        temperature = float(data_list[0].split(': ')[1].split(' °C')[0])
        pressure = float(data_list[1].split(': ')[1].split(' hPa')[0])
        humidity = float(data_list[2].split(': ')[1].split(' %')[0])

        # Push data to Firebase Realtime Database
        db.reference('/sensor_data').push({
            'temperature': temperature,
            'pressure': pressure,
            'humidity': humidity
        })

except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting...")

finally:
    # Close the Bluetooth connection
    client_socket.close()
