
n = 12

class Job:
    def __init__(self, job_number):
        # self.joblist = []
        self.job_number = job_number % n
        self.start_time = 0
        self.Pj = 0
        self.Cj = 0
        
        
