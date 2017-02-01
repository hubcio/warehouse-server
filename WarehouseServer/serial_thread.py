# -*- encoding: utf-8 -*-

import json
import threading
import logging
import serial

logger = logging.getLogger(__name__)


class SerialThread(threading.Thread):
    _state = None

    def __init__(self, *args, **kwargs):
        super(SerialThread, self).__init__(name=self.__class__.__name__)
        self.serial = serial.Serial(*args, **kwargs)
        print('SerialThread running!')

    def run(self):
        while True:
            for line in self.serial:
                try:
                    self._state = json.loads(line)
                except Exception as exc:
                    logger.error(exc)

    def get_state(self):
        return self._state

    def send_command(self, command):
        self.serial.write(command)


class WarehouseCommunicator(SerialThread):
    position_x = 0
    position_y = 0
    position_z = 0
    current_x = 0
    current_y = 0
    current_z = 0

    def run(self):
        while True:
            for line in self.serial:
                try:
                    self._state = json.loads(line)
                    self.position_x = self._state['x']
                    self.position_y = self._state['y']
                    self.position_z = self._state['z']
                    self.current_x = self._state['cx']
                    self.current_y = self._state['cy']
                    self.current_z = self._state['cz']
                except Exception as exc:
                    logger.error(exc)
