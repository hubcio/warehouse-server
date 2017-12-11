from WarehouseServer import db
import shortest_path

from serial_thread import WarehouseCommunicator
from shortest_path import Graph
from models import Drawer


class WarehouseLogic(Graph):
    x_pos_ref = 0
    y_pos_ref = 0
    z_pos_ref = 0
    x_pos_fdb = WarehouseCommunicator.x_pos_fdb
    y_pos_fdb = WarehouseCommunicator.y_pos_fdb
    z_pos_fdb = WarehouseCommunicator.z_pos_fdb
    currentNode = {}

    def __init__(self):
        # Create graph and get all drawers from database
        Graph.__init__(self)
        drawers = Drawer.query.all()

        # Add drawers nodes
        for drawer in drawers:
            self.add_node(drawer)

        # Add other nodes
        # self.add_node(transA)
        # self.add_node(transB)
        # self.add_node(out)

        # Add edges to drawers
        # for drawer in drawers:
        #     if drawer.drawer_id.get_range() == 'transA':
        #         self.add_edge(drawer, transA, get_distance(drawer, transA))
        #     if drawer.drawer_id.get_range() == 'transB':
        #
        # Add edges between trans points

        return

    def sequential_move(self, start, end):
        self.dijsktra()
        return
