import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_ssd1306
import adafruit_rfm9x
import binascii

# Define the frequency and CS pin for each device
devices = {
    "device1": {
        "frequency": 915.0,
        "cs_pin": DigitalInOut(board.D5),
        "send_window": (0, 5),
        "receive_window": (5, 10)
    },
    "device2": {
        "frequency": 915.0,
        "cs_pin": DigitalInOut(board.D6),
        "send_window": (10, 15),
        "receive_window": (15, 20)
    },
    # Add more devices here...
}

# Define the TDMA slots
tdma_slots = 20

# Initialize the RFM9x devices and create a dictionary of radios
radios = {}
for device_name, device_config in devices.items():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    radios[device_name] = adafruit_rfm9x.RFM9x(spi, device_config["cs_pin"], device_config["frequency"])

# Define the encryption key
encryption_key = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F"

# Initialize the display
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

def encrypt_data(data, key):
    """
    Encrypts the given data using the provided key.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce + ciphertext + tag

def decrypt_data(data, key):
    """
    Decrypts the given data using the provided key.
    """
    nonce = data[:16]
    ciphertext = data[16:-16]
    tag = data[-16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

def send_message(device_name, message):
    """
    Sends the given message from the specified device.
    """
    radio = radios[device_name]
    send_start, send_end = devices[device_name]["send_window"]
    receive_start, receive_end = devices[device_name]["receive_window"]
    
    # Wait until the start of the send window
    while time.monotonic() < send_start:
        pass
    
    # Encrypt the message
    encrypted_message = encrypt_data(message, encryption_key)
    
    # Send the message
    radio.send(encrypted_message)
    
    # Wait until the end of the send window
    while time.monotonic() < send_end:
        pass
    
    # Listen for messages
    radio.listen()
    
    # Wait until the start of the receive window
    while time.monotonic() < receive_start:
        pass
    
    # Receive messages
    messages = []
    while time.monotonic() < receive_end:
        if radio.available():
            received_message = radio.receive()
            # Decrypt the message
            decrypted_message = decrypt_data(received_message, encryption_key)
           
