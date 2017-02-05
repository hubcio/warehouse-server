# -*- encoding: utf-8 -*-

import json
import threading
import logging
import serial

logger = logging.getLogger(__name__)


class WarehouseCommunicator(threading.Thread):
    position_x = 0
    position_y = 0
    position_z = 0
    current_x = 0
    current_y = 0
    current_z = 0
    parsed_line = ''

    def __init__(self):
        super(WarehouseCommunicator, self).__init__(name=self.__class__.__name__)
        self.serial = serial.Serial(
                port='/dev/ttyAMA0',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS)
        print('Warehouse UART running!')

    def run(self):
        while True:
            for line in self.serial:
                try:
                    self.parsed_line = json.loads(line)
                    self.position_x = self.parsed_line['x']
                    self.position_y = self.parsed_line['y']
                    self.position_z = self.parsed_line['z']
                    self.current_x = self.parsed_line['cx']
                    self.current_y = self.parsed_line['cy']
                    self.current_z = self.parsed_line['cz']
                except Exception as exc:
                    logger.error(exc)
