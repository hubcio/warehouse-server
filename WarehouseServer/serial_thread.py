# -*- encoding: utf-8 -*-

import json
from threading import Thread
import logging
import serial
import time

logger = logging.getLogger(__name__)


class WarehouseCommunicator(Thread):
    x = 0
    y = 0
    z = 0

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
                    parsed_line = json.loads(line[-29:])
                    if parsed_line['x'] != self.x or parsed_line['y'] != self.y or parsed_line['z'] != self.z:
                        logger.info("Received: " + line)

                    self.x = parsed_line['x']
                    self.y = parsed_line['y']
                    self.z = parsed_line['z']
                except Exception as exc:
                    logger.error(exc)

    def send(self, command, value=99):
        if value < 0:
            value = 0
            logger.error("Wrong value!" + ':' + str(command).zfill(2) + '-' + str(value).zfill(8))

        command_string = ':' + str(command).zfill(2) + '-' + str(value).zfill(8) + '\r\n'
        logger.debug("Sent: " + command_string)
        self.serial.write(command_string)
        time.sleep(0.01)
