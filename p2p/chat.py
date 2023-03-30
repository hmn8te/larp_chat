from sx127x import SX127x
from sx127x import MODE, BANDWIDTH, SPREADING_FACTOR, CODING_RATE
from Crypto.Cipher import AES
import hashlib
import time

# LoRa radio configuration
frequency = 433E6  # 433 MHz frequency band
tx_power_level = 14  # max power
signal_bandwidth = BANDWIDTH.BW_125KHZ
spreading_factor = SPREADING_FACTOR.SF7
coding_rate = CODING_RATE.CR_4_5
preamble_length = 8
implicit_header_mode = False

# Encryption key (16, 24, or 32 bytes long)
encryption_key = b'secretkey1234567'

# Configure send and receive time windows (in seconds)
send_window = 5
receive_window = 10

# Initialize LoRa radio
lora = SX127x(frequency=frequency, tx_power_level=tx_power_level, signal_bandwidth=signal_bandwidth,
               spreading_factor=spreading_factor, coding_rate=coding_rate, preamble_length=preamble_length,
               implicit_header_mode=implicit_header_mode, sync_word=None, dio0_pin=25, reset_pin=17, spi_bus=0, spi_device=0)

# Connect to LoRa radio and start receiving messages
lora.start()

# Callback function to handle incoming messages
def on_receive(lora, payload):
    # Decrypt the incoming message
    cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=payload[:16])
    decrypted_message = cipher.decrypt(payload[16:])
    print(f"Received message: {decrypted_message.decode()}")

# Set callback function for incoming messages
lora.set_receive_handler(on_receive)

# Main loop to send chat messages during the send time window
while True:
    start_time = time.time()
    end_time = start_time + send_window
    while time.time() < end_time:
        # Encrypt the chat message
        cipher = AES.new(encryption_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(input("Type a message to send: "), 'utf-8'))
        nonce = cipher.nonce
        encrypted_message = nonce + ciphertext

        # Send the encrypted message
        lora.send(encrypted_message)
        print(f"Sent message: {ciphertext.decode()}")

    time.sleep(receive_window)
