from sx127x import SX127x
from sx127x import MODE, BANDWIDTH, SPREADING_FACTOR, CODING_RATE
from Crypto.Cipher import AES
import hashlib
import time
import getpass


class ChatApp:
    def __init__(self, frequency, tx_power_level, signal_bandwidth, spreading_factor, coding_rate,
                 preamble_length, implicit_header_mode, encryption_key):
        self.frequency = frequency
        self.tx_power_level = tx_power_level
        self.signal_bandwidth = signal_bandwidth
        self.spreading_factor = spreading_factor
        self.coding_rate = coding_rate
        self.preamble_length = preamble_length
        self.implicit_header_mode = implicit_header_mode
        self.encryption_key = encryption_key
        self.lora = None

    def start(self):
        self.lora = SX127x(frequency=self.frequency, tx_power_level=self.tx_power_level,
                           signal_bandwidth=self.signal_bandwidth, spreading_factor=self.spreading_factor,
                           coding_rate=self.coding_rate, preamble_length=self.preamble_length,
                           implicit_header_mode=self.implicit_header_mode, sync_word=None, dio0_pin=25,
                           reset_pin=17, spi_bus=0, spi_device=0)
        self.lora.start()

    def stop(self):
        self.lora.stop()

    def send_message(self, message):
        # Encrypt the chat message
        cipher = AES.new(self.encryption_key.encode(), AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(bytes(message, 'utf-8'))
        nonce = cipher.nonce
        encrypted_message = nonce + ciphertext

        # Send the encrypted message
        self.lora.send(encrypted_message)
        print(f"Sent message: {ciphertext.decode()}")

    def receive_message(self):
        # Wait for incoming messages
        while True:
            payload = self.lora.receive()
            if payload is not None:
                # Decrypt the incoming message
                cipher = AES.new(self.encryption_key, AES.MODE_EAX, nonce=payload[:16])
                decrypted_message = cipher.decrypt(payload[16:])
                print(f"Received message: {decrypted_message.decode()}")
                break


def main():
    # LoRa radio configuration
    frequency = 433E6  # 433 MHz frequency band
    tx_power_level = 14  # max power
    signal_bandwidth = BANDWIDTH.BW_125KHZ
    spreading_factor = SPREADING_FACTOR.SF7
    coding_rate = CODING_RATE.CR_4_5
    preamble_length = 8
    implicit_header_mode = False

    # Configure send and receive time windows (in seconds)
    send_window = 5
    receive_window = 10

    # Read the encryption key securely
    while True:
        encryption_key = getpass.getpass("Enter encryption key (16, 24, or 32 bytes long): ")
        if len(encryption_key) in [16, 24, 32]:
            break
        print("Invalid key length, please try again")

    # Initialize chat apps for up to 100 devices
    chat_apps = []
    for i in range(1, 101):
        chat_app = ChatApp(frequency=frequency, tx_power_level=tx_power_level, signal_bandwidth=signal_bandwidth,
                           spreading_factor=spreading_factor, coding_rate=coding_rate, preamble_length=preamble_length,
                           implicit_header_mode=implicit_header_mode, encryption_key=encryption_key)
