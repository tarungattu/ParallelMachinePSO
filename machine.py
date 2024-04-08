#number of machines
m = 3

class Machine:
    def __init__(self, machine_id):
        self.joblist = []
        self.machine_id = machine_id % m #machine number
        self.lastJobCompTime = 0