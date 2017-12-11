# -*- encoding: utf-8 -*-

import json
from threading import Thread
import logging
import serial

logger = logging.getLogger(__name__)


class WarehouseCommunicator(Thread):
    x_pos_fdb = 0
    y_pos_fdb = 0
    z_pos_fdb = 0
    x_current = 0
    y_current = 0
    z_current = 0
    state = ''

    def __init__(self, level=logging.INFO, port='/dev/ttyAMA0', baudrate=115200,
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):
        Thread.__init__(self)
        logging.basicConfig()
        logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")
        self.serial = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize,
                                    stopbits=stopbits, parity=parity, timeout=3.0)
        self.daemon = True
        logger.info("STM <--> Raspberry communication started!")

    def run(self):
        while True:
            for line in self.serial:
                try:
                    parsed_line = json.loads(line)
                    self.x_pos_fdb = parsed_line['x']
                    self.y_pos_fdb = parsed_line['y']
                    self.z_pos_fdb = parsed_line['z']
                    self.x_current = parsed_line['cx']
                    self.y_current = parsed_line['cy']
                    self.z_current = parsed_line['cz']
                    logger.debug("Received: " + line)
                except Exception as exc:
                    logger.error(exc)

    def send(self, command, value=99):
        command_string = ':' + str(command).zfill(2) + '-' + str(value).zfill(8) + '\r\n'
        logger.info("Sent: " + command_string)
        self.serial.write(command_string)

    def move_x_absolute(self, value):
        self.send(0, value)

    def move_y_absolute(self, value):
        self.send(1, value)

    def move_z_absolute(self, value):
        self.send(2, value)

    def move_x_relative(self, value):
        self.send(0, value + self.x_pos_fdb)

    def move_y_relative(self, value):
        self.send(1, value + self.y_pos_fdb)

    def move_z_relative(self, value):
        self.send(2, value + self.z_pos_fdb)

    def move_servo(self, value):
        self.send(3, value)

    def reset_stm(self):
        self.send(99)

    def home_x(self):
        self.send(4)

    def home_y(self):
        self.send(5)

    def home_z(self):
        self.send(6)
