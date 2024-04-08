class Machine:
    def __init__(self, machine_id):
        self.joblist = []
        self.machine_id = machine_id  #machine number
        self.lastJobCompTime = 0