import smbus2  # Import SMBus for I2C communication
import bme280  # Import BME280 library for sensor data
import bluetooth  # Import Bluetooth library
import time  # Import time library for delays

# Function to sample sensor data using BME280
def sample_sensor_data():
    # Use BME280 library to sample data from the sensor
    data = bme280.sample(bus, address, bme280_params)
    return f'Temperature: {data.temperature:.2f} °C\nPressure: {data.pressure:.2f} hPa\nHumidity: {data.humidity:.2f} %'

# I2C setup for BME280 sensor
i2c_port = 1
address = 0x76  # Default I2C address, use 0x77 if your sensor has a different address

# Initialize I2C bus and load calibration parameters for BME280
bus = smbus2.SMBus(i2c_port)
bme280_params = bme280.load_calibration_params(bus, address)

# Bluetooth setup
bt_port = 1  # Use any available port
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket = None  # Initialize client_socket to avoid NameError

try:
    # Bind the server socket to the specified port and start listening
    server_socket.bind(("", bt_port))
    server_socket.listen(1)
    print(f"Waiting for connection on RFCOMM channel {bt_port}...")

    # Accept an incoming Bluetooth connection
    client_socket, client_info = server_socket.accept()
    print(f"Accepted connection from {client_info}")

    while True:
        # Sample sensor data
        data_to_send = sample_sensor_data()

        # Send data over Bluetooth
        client_socket.send(data_to_send)
        
        # Wait for 1 minute before sampling again
        time.sleep(60)

except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")
finally:
    # Close the Bluetooth connections if they are defined
    if client_socket:
        client_socket.close()
    server_socket.close()
