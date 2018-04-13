from threading import Thread
from collections import deque
import logging
from WarehouseServer import com, servo
import time

import os

logger = logging.getLogger(__name__)


class SinglePoint:
    def __init__(self, x, y, z, move_type):
        self.x = x
        self.y = y
        self.z = z
        self.move_type = move_type


class WarehousePathfinder(Thread):
    movesQueue = deque()

    def __init__(self, level=logging.INFO):
        Thread.__init__(self)
        logging.basicConfig()
        logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")

    def run(self):
        while True:
            if len(self.movesQueue) > 0:
                self.go_to_point()
            time.sleep(0.1)

    def add_absolute_point(self, x, y, z):
        point = SinglePoint(x, y, z, "absolute")
        self.add_point_to_move(point)

    def add_relative_point(self, x, y, z):
        point = SinglePoint(x, y, z, "relative")
        self.add_point_to_move(point)

    def add_point_to_move(self, single_point):
        self.movesQueue.append(single_point)

    def go_to_point(self):
        point = self.movesQueue.popleft()

        if point.move_type == "relative":
            self.move_relative(point.x, point.y, point.z)

        if point.move_type == "absolute":
            self.move_absolute(point.x, point.y, point.z)

    @staticmethod
    def move_x_absolute(value, blocking=False):
        com.send(0, value)
        if blocking:
            while (com.x - 5 > value) or (com.x + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_y_absolute(value, blocking=False):
        com.send(1, value)
        if blocking:
            while (com.y - 5 > value) or (com.y + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_z_absolute(value, blocking=False):
        com.send(2, value)
        if blocking:
            while (com.z - 5 > value) or (com.z + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_x_relative(value, blocking=False):
        com.send(0, com.x + value)
        value += com.x
        if blocking:
            while (com.x - 5 > value) or (com.x + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_y_relative(value, blocking=False):
        com.send(1, com.y + value)
        value += com.y
        if blocking:
            while (com.y - 5 > value) or (com.y + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_z_relative(value, blocking=False):
        com.send(2, com.z + value)
        value += com.z
        if blocking:
            while (com.z - 5 > value) or (com.z + 5 < value):
                time.sleep(0.1)

    @staticmethod
    def move_servo(value):
        servo.move_percent(value)

    def move_relative(self, x, y, z):
        self.move_x_relative(x)
        self.move_y_relative(y)
        self.move_z_relative(z)
        wx = x + com.x
        wy = y + com.y
        wz = z + com.z
        while (abs(com.x - wx) > 2) or (abs(com.y - wy) > 2) or (abs(com.z - wz) > 2):
            time.sleep(0.1)
        print ("relative move done!")

    def move_absolute(self, x, y, z):
        self.move_x_absolute(x)
        self.move_y_absolute(y)
        self.move_z_absolute(z)
        while (abs(com.x - x) > 2) or (abs(com.y - y) > 2) or (abs(com.z - z) > 2):
            time.sleep(0.1)
        print ("absolute move done!")

    def go_to_transition_a(self):
        self.move_absolute(1350, 8900, 3500)

    def sequence(self):
        self.move_absolute(2280, 2975, 5000)
        self.move_relative(0, 0, 400)
        self.move_relative(0, 370, 0)
        self.move_relative(0, 0, -2500)
        self.move_absolute(1370, 8900, 2900)
        os.system("echo 4=%d%% > /dev/servoblaster" % 18)
        self.move_absolute(1972, 6500, 400)
        self.move_relative(0, -1350, 0)
        self.move_relative(0, 0, -250)
        self.move_relative(0, 2500, 0)
        self.move_relative(0, 0, 3000)
        os.system("echo 4=%d%% > /dev/servoblaster" % 85.6)
        self.move_absolute(1970, 5150, 3300)
        self.move_absolute(1970, 5150, 2912)
        self.move_relative(0, 2500, 0)
        self.move_absolute(1350, 8700, 2000)
        self.move_absolute(1350, 7000, 50)
        time.sleep(5)
        self.move_absolute(1350, 8900, 3500)

    def sequence_backward(self):
        self.move_absolute(1350, 7000, 50)
        time.sleep(5)
        self.move_relative(0, 0, -1000)
        self.move_absolute(1978, 7000, 3000)

        self.move_relative(0, -1500, 0)
        self.move_relative(0, 0, -250)
        self.move_relative(0, 1500, 0)
        os.system("echo 4=%d%% > /dev/servoblaster" % 18)

        self.move_absolute(1975, 7000, 200)


        self.move_relative(0, -2500, 0)
        # self.move_absolute(1950, 5150, 2912)
        # self.move_absolute(1950, 5150, 3300)
        # self.move_relative(0, 0, -3000)
        # self.move_relative(0, -2500, 0)


        # os.system("echo 4=%d%% > /dev/servoblaster" % 85.6)



        # self.move_absolute(1350, 8900, 3500)



    @staticmethod
    def reset_stm():
        com.send(99)

    def home_x(self):
        com.send(4)

    def home_y(self):
        com.send(5)

    def home_z(self):
        com.send(6)

    def home_all(self):
        self.home_y()
        while True:
            time.sleep(0.5)
            if com.y == 0:
                time.sleep(0.5)
                if com.y == 0:
                    break

        self.move_absolute(0, 8900, 0)

        self.home_z()
        while True:
            time.sleep(0.5)
            if com.z == 0:
                time.sleep(0.5)
                if com.z == 0:
                    break

        self.home_x()
        while True:
            time.sleep(0.5)
            if com.x == 0:
                time.sleep(0.5)
                if com.x == 0:
                    break

        time.sleep(0.5)

        self.go_to_transition_a()
