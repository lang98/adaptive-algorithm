from node import Node


class OrNode(Node):

    def __init__(self, order, x=None, y=None):
        Node.__init__(self, order)
        self.x = x
        self.y = y

    def build(self, depth):
        self.x = self.generate_random_child(depth)
        self.y = self.generate_random_child(depth)
        if depth > 0:
            self.x.build(depth - 1)
            self.y.build(depth - 1)

    def nonT_list(self):
        return self.x.nonT_list() + self.y.nonT_list() + [self]

    def T_list(self):
        return self.x.T_list() + self.y.T_list()

    def height(self):
        x = self.x.height()
        y = self.y.height()
        return 1 + max(x, y)

    def value(self, evaluator):
        return self.x.value(evaluator) or self.y.value(evaluator)

    def swap_child(self, target, new_node):
        if self.x == target:
            self.x = new_node
        elif self.y == target:
            self.y = new_node
        else:
            self.x.swap_child(target, new_node)
            self.y.swap_child(target, new_node)

    def show(self):
        return '({} || {})'.format(self.x.show(), self.y.show())
