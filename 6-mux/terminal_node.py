import random

from node import Node


class TerminalNode(Node):

    def __init__(self, order):
        Node.__init__(self, order)
        r = random.randint(0, 5)
        if self.order == 6:
            self.values = ['a0', 'a1', 'd0', 'd1', 'd2', 'd3']
        elif self.order == 11:
            self.values = ["a0", "a1", "a2", "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7"]
        else:
            self.values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        self.v = self.values[r]

    def build(self, depth):
        pass

    def nonT_list(self):
        return []

    def T_list(self):
        return [self]

    def height(self):
        return 1

    def value(self, evaluator):
        return evaluator.value(self.v)

    def swap_child(self, target, new_node):
        pass

    def show(self):
        return self.v
