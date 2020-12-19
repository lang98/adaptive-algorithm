class Evaluator:
    def __init__(self, order, case_number):
        self.order = order
        if self.order == 6:
            self.names = ['a0', 'a1', 'd0', 'd1', 'd2', 'd3']
        elif self.order == 11:
            self.names = ["a0", "a1", "a2", "d0", "d1", "d2", "d3", "d4", "d5", "d6", "d7"]
        else:
            self.names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        self.values = [False] * order

        i = order - 1
        while case_number > 0 and i >= 0:
            self.values[i] = (case_number % 2 == 1)
            i -= 1
            case_number /= 2

    def value(self, name):
        return self.values[self.names.index(name)]

    def expected(self):
        if self.order == 6:
            return self._six_mux()

    def _six_mux(self):
        if self.values[0] and self.values[1]:
            return self.values[5]
        elif self.values[0]:
            return self.values[3]
        elif self.values[1]:
            return self.values[4]
        else:
            return self.values[2]
