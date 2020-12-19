import copy
import random
from abc import abstractmethod, ABC


class Node(ABC):
    def __init__(self, order):
        self.order = order

    def generate_random_child(self, depth):
        from and_node import AndNode
        from if_node import IfNode
        from not_node import NotNode
        from or_node import OrNode
        from terminal_node import TerminalNode
        if depth == 0:
            return TerminalNode(self.order)

        if random.randint(0, 1):
            return TerminalNode(self.order)
        else:
            r = random.randint(0, 3)
            m = {
                0: AndNode(self.order),
                1: OrNode(self.order),
                2: NotNode(self.order),
                3: IfNode(self.order)
            }
            if depth > 1:
                m[r].build(depth - 1)
            return m[r]

    def clone(self):
        return copy.deepcopy(self)

    @abstractmethod
    def build(self, depth):
        pass

    @abstractmethod
    def nonT_list(self):
        pass

    @abstractmethod
    def T_list(self):
        pass

    @abstractmethod
    def height(self):
        pass

    @abstractmethod
    def value(self, evaluator):
        pass

    @abstractmethod
    def swap_child(self, target, new_node):
        pass

    @abstractmethod
    def show(self):
        pass
