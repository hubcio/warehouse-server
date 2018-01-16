from threading import Thread
from collections import deque
import logging
from WarehouseServer import com

logger = logging.getLogger(__name__)

class SinglePoint:
    x=0
    y=0
    z=0
    force=False

    def __init__(self, x, y, z, force=False):
        self.x = x
        self.y = y
        self.z = z
        self.force = force

class WarehousePathfinder(Thread):
    movesQueue = deque()
    x_fdb = com.x_pos_fdb
    y_fdb = com.y_pos_fdb
    z_fdb = com.z_pos_fdb

    def __init__(self, level=logging.INFO):
        Thread.__init__(self)
        logging.basicConfig()
        logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

    def run(self):
        while True:
            if self.movesQueue.len() > 0:
                goto_point()
                sleep(0.1)

    def add_point_to_move(self, single_point):
        self.movesQueue.append(single_point)

    def print_points(self):

    def goto_point(self):
        point = movesQueue.
        movesQueue.remove(point)

    def move_x_absolute(self, value, blocking=False):
        self.send(0, value)
        if blocking:
            while (self.x_pos_fdb-5 > value) or (self.x_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_y_absolute(self, value, blocking=False):
        self.send(1, value)
        if blocking:
            while (self.y_pos_fdb-5 > value) or (self.y_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_z_absolute(self, value, blocking=False):
        self.send(2, value)
        if blocking:
            while (self.z_pos_fdb-5 > value) or (self.z_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_x_relative(self, value, blocking=False):
        self.send(0, self.x_pos_fdb + value)
        value += self.x_pos_fdb
        if blocking:
            while (self.x_pos_fdb-5 > value) or (self.x_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_y_relative(self, value, blocking=False):
        self.send(1, self.y_pos_fdb + value)
        value += self.y_pos_fdb
        if blocking:
            while (self.y_pos_fdb-5 > value) or (self.y_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_z_relative(self, value, blocking=False):
        self.send(2, self.z_pos_fdb + value)
        value += self.z_pos_fdb
        if blocking:
            while (self.z_pos_fdb-5 > value) or (self.z_pos_fdb+5 < value):
                time.sleep(0.1)

    def move_servo(self, value):
        self.send(3, value)

    def move_relative(self, x, y, z):
        self.move_x_relative(x)
        self.move_y_relative(y)
        self.move_z_relative(z)

    def move_absolute(self, x, y, z):
        self.move_x_absolute(x)
        self.move_y_absolute(y)
        self.move_z_absolute(z)

    def reset_stm(self):
        self.send(99)

    def home_x(self):
        self.move_x_relative(200)
        time.sleep(1)
        self.send(4)
        while not (self.x_pos_fdb == 0):
            time.sleep(0.1)
        self.move_x_relative(1600)


    def home_y(self):
        self.move_y_relative(200)
        time.sleep(1)
        self.send(5)

    def home_z(self):
        self.move_z_relative(200)
        time.sleep(1)
        self.send(6)
