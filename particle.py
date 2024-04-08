import random
import numpy as np
import sys
import math

penalty = 99999

class Particle:
    def __init__(self, n, m):
        self.position = [round(random.uniform(0, m), 2) for _ in range(n)]  # Initialize random position
        self.v = [0 for _ in range(n)]  # Initialize random velocity
        self.local_best = self.position.copy()  # Initialize personal best position
        self.global_best = []
        self.Cmax = 99999
        self.oldfit = self.Cmax  # Initialize personal best value
        self.machine_list = []
        self.r1 = random.uniform(0,1)
        self.r2 = random.uniform(0,1)
        self.penalty_count = 0
        
        # self.joblist = []
        # self.index = []
    def assign_machines(self, machine_list):
        if len(machine_list) < 3:
            raise ValueError("Insufficient number of machines")

            # Assign three machine objects to the swarm
        self.machine_list = machine_list[:3]
        
    def get_last_job_completiontime(self, machine_list):
        for machine in machine_list:
            start_time = 0
            complete_time = 0
            for job in machine.joblist:
                job[1].start_time = start_time
                job[1].Cj = job[1].start_time + job[1].Pj
                start_time = job[1].Cj
                complete_time = job[1].Cj
            machine.lastJobCompTime = complete_time
            
    def put_penalty(self):
        self.Cmax = self.Cmax + penalty
        self.penalty_count += 1