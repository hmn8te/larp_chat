from sx127x import SX127x
from sx127x import MODE, BANDWIDTH, SPREADING_FACTOR, CODING_RATE

# LoRa radio configuration
frequency = 433E6  # 433 MHz frequency band
tx_power_level = 14  # max power
signal_bandwidth = BANDWIDTH.BW_125KHZ
spreading_factor = SPREADING_FACTOR.SF7
coding_rate = CODING_RATE.CR_4_5
preamble_length = 8
implicit_header_mode = False

# Initialize LoRa radios
lora1 = SX127x(frequency=frequency, tx_power_level=tx_power_level, signal_bandwidth=signal_bandwidth,
               spreading_factor=spreading_factor, coding_rate=coding_rate, preamble_length=preamble_length,
               implicit_header_mode=implicit_header_mode, sync_word=None, dio0_pin=25, reset_pin=17, spi_bus=0, spi_device=0)
lora2 = SX127x(frequency=frequency, tx_power_level=tx_power_level, signal_bandwidth=signal_bandwidth,
               spreading_factor=spreading_factor, coding_rate=coding_rate, preamble_length=preamble_length,
               implicit_header_mode=implicit_header_mode, sync_word=None, dio0_pin=25, reset_pin=17, spi_bus=0, spi_device=1)

# Connect to LoRa radios and start receiving messages
lora1.start()
lora2.start()

# Callback function to handle incoming messages
def on_receive(lora, payload):
    print(f"Received message: {payload.decode()}")

# Set callback function for incoming messages
lora1.set_receive_handler(on_receive)
lora2.set_receive_handler(on_receive)

# Main loop to send chat messages
while True:
    message = input("Type a message to send: ")
    lora1.send(bytes(message, 'utf-8'))
    print(f"Sent message: {message}")
