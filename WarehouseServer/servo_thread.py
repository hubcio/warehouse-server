from threading import Thread
import logging
import time
import os

logger = logging.getLogger(__name__)


class ServoController(Thread):
    positionPercentDesired = 0
    positionPercentCurrent = 0

    def __init__(self, level=logging.INFO):
        Thread.__init__(self)
        self.daemon = True
        logging.basicConfig()
        logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")
        logger.info("Servo task started!")

    def run(self):
        if self.positionPercentCurrent > self.positionPercentDesired:
            self.positionPercentCurrent -= 1

        if self.positionPercentDesired < self.positionPercentCurrent:
            self.positionPercentCurrent += 1

        os.system("echo 4=%d%% > /dev/servoblaster" % self.positionPercentCurrent)
        time.sleep(0.05)

    def move_percent(self, value):
        self.positionPercentDesired = value

    def get_position(self):
        return self.positionPercentCurrent
