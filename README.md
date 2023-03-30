# LoRaWAN Chat Application

This is a peer-to-peer chat application that uses LoRaWAN technology to allow communication between devices. The application is designed to work on Raspberry Pi devices equipped with LoRa radio modules.

## Installation

Before running the application, you'll need to install some dependencies:

1. Install the `spidev` library: `sudo apt-get install python-spidev`
2. Install the `RPi.GPIO` library: `sudo apt-get install python-rpi.gpio`
3. Install the `pycryptodome` library: `sudo pip install pycryptodome`

## Configuration

The application can be configured by editing the `config.py` file. Here are the available options:

- `frequency`: The LoRa radio frequency in Hz (default: 868000000)
- `tx_power`: The transmit power in dBm (default: 17)
- `spreading_factor`: The spreading factor (default: 7)
- `bandwidth`: The bandwidth in Hz (default: 125000)
- `coding_rate`: The coding rate (default: 5)
- `preamble_length`: The preamble length (default: 8)
- `implicit_header`: Whether to use implicit or explicit header mode (default: False)
- `sync_word`: The synchronization word (default: 0x12)
- `encryption_key`: The encryption key (default: "0123456789ABCDEF0123456789ABCDEF")

## Usage

To start the application, run the `main.py` file. You can optionally specify a device ID as a command-line argument:

```bash
python main.py --id 1
```

This will start the application with device ID 1. If no ID is specified, the application will assign a random ID to the device.

Once the application is running, you can send messages by typing them into the console and pressing enter. The messages will be sent to all other devices within range.


## Troubleshooting
If you encounter any issues while running the application, here are a few things to check:

Make sure the LoRa radio modules are properly connected to the Raspberry Pi.
Check the wiring of the LoRa radio modules to make sure they are connected correctly.
Check the configuration settings in the config.py file to make sure they match your hardware.
Make sure the devices are within range of each other.
Check the console output for any error messages.


## Code Overview
The code is split into two main parts: the LoRaDevice class and the TDMA scheduler.

## The LoRaDevice Class
The LoRaDevice class represents a single LoRa device and provides methods for sending and receiving messages. When you create an instance of the LoRaDevice class, it initializes a LoRa radio and sets up a receive window for incoming messages. The start_receive() method sets up the receive window, and the receive() method handles incoming messages.

To send a message, call the send(message) method during the device's designated send window. The send() method checks the current time and only sends the message if the device is within its send window.

## The TDMA Scheduler
The TDMA scheduler is responsible for managing the time slots for each device. The SLOT_LENGTH constant is calculated as the receive window divided by the number of devices. The my_slot property of each LoRaDevice instance is calculated as (device_id - 1) * SLOT_LENGTH. The TDMA scheduler loops over each device and checks if it's within its designated time slot, then calls the send() method if it is.


## Credits
This application was developed by Nathaniel Fisher. It is based on the SX127x library by Thomas Telkamp and the LoRaWAN protocol specification by the LoRa Alliance.