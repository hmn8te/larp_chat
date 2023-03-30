import time
from sx127x import SX127x
from sx127x import ModemConfig
from sx127x import RegConfig


class LoRaDevice:
    def __init__(self, device_id, frequency, bandwidth, spreading_factor, coding_rate,
                 output_power, send_window, receive_window, encryption_key):
        self.device_id = device_id
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.spreading_factor = spreading_factor
        self.coding_rate = coding_rate
        self.output_power = output_power
        self.send_window = send_window
        self.receive_window = receive_window
        self.encryption_key = encryption_key
        
        # Calculate TDMA parameters
        self.slot_length = receive_window / NUM_DEVICES
        self.my_slot = (self.device_id - 1) * self.slot_length
        self.slot_start_time = 0

        # Initialize LoRa radio
        self.lora = SX127x(
            name=f'LoRa-{self.device_id}',
            parameters={
                'frequency': self.frequency,
                'bandwidth': self.bandwidth,
                'spreading_factor': self.spreading_factor,
                'coding_rate': self.coding_rate,
                'output_power': self.output_power,
            },
            on_recv=lambda lora, payload: self.receive(payload),
        )

        # Configure modem
        modem_config = ModemConfig.Bw125Cr45Sf128
        self.lora.set_modem_config(modem_config)
        self.lora.set_pa_config(pa_select=1, max_power=self.output_power, output_power=self.output_power)

        # Configure registers
        self.lora.set_reg(RegConfig.LNA_GAIN, 0b00100000)
        self.lora.set_reg(RegConfig.PA_DAC, 0b00001111)

        # Start listening for messages
        self.start_receive()

    def start_receive(self):
        """
        Set up receive window and start listening for messages.
        """
        self.lora.start_implicit_rx(self.slot_start_time + self.my_slot, self.receive_window)

    def send(self, message):
        """
        Send a message during the device's assigned send window.
        """
        if time.monotonic() >= (self.slot_start_time + self.my_slot + self.send_window):
            self.lora.send(message, encryption_key=self.encryption_key)

    def receive(self, payload):
        """
        Handle a received message.
        """
        print(f"Received by device {self.device_id}: {payload.decode()}")


# Constants
FREQUENCY = 915000000
BANDWIDTH = 125000
SPREADING_FACTOR = 7
CODING_RATE = 5
OUTPUT_POWER = 14
SEND_WINDOW = 1.0  # seconds
RECEIVE_WINDOW = 3.0  # seconds
NUM_DEVICES = 100

# Encryption key
encryption_key = b'supersecretkey'

# Create LoRa devices
devices = []
for device_id in range(1, NUM_DEVICES + 1):
    device = LoRaDevice(device_id, FREQUENCY, BANDWIDTH, SPREADING_FACTOR, CODING_RATE,
                        OUTPUT_POWER, SEND_WINDOW, RECEIVE_WINDOW, encryption_key)
    devices.append(device)

# Run TDMA scheme
SLOT_LENGTH = RECEIVE_WINDOW / NUM_DEVICES
SLOT_START_TIME = 0
while True:
    current_time = time.monotonic()
    for device in devices:
        if (current_time >= (SLOT_START_TIME + device.my_slot)) and \
                (current_time < (SLOT_START_TIME
