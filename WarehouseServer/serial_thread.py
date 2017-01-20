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
