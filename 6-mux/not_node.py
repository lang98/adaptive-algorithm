from node import Node


class NotNode(Node):
    def __init__(self, order, x=None):
        Node.__init__(self, order)
        self.x = x

    def build(self, depth):
        self.x = self.generate_random_child(depth)
        if depth > 0:
            self.x.build(depth - 1)

    def nonT_list(self):
        return self.x.nonT_list() + [self]

    def T_list(self):
        return self.x.T_list()

    def height(self):
        return 1 + self.x.height()

    def value(self, evaluator):
        return not self.x.value(evaluator)

    def swap_child(self, target, new_node):
        if self.x == target:
            self.x = new_node
        else:
            self.x.swap_child(target, new_node)

    def show(self):
        return '(!{})'.format(self.x.show())
