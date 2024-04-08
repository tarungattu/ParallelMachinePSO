import random
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from particle import Particle
from machine import Machine
from job import Job

m = 3
n = 12
N = 200
ptimes = [14, 52, 10, 19, 50, 80, 40, 45, 15, 25, 75, 95]

T = 200
t = 0

w = 0.3   #inertia
c1 = 2    #cognitive
c2 = 1.5    #social

penalty = 99999

if len(sys.argv) > 1:
    print_out = sys.argv[1].lower() == 'true'
else:
    # Default value if no command-line argument is provided
    print_out = False

if len(sys.argv) > 1:
    print_out1 = sys.argv[1].lower() == 'true1'
else:
    # Default value if no command-line argument is provided
    print_out1 = False

        
def assign_jobs_to_machines(particle, jobs):
    job = particle.position
    # empty the machines schedule before new assignment.
    for machine in particle.machine_list:
        machine.joblist = []
        
    for num,jobnum in zip(job, range(n)) :
        j, i = math.modf(num)
        i = int(i)
        j = round(j, 2)
        
        for index in range(m):
            if index == i:
                particle.machine_list[index].joblist.append( (j, jobs[jobnum]) ) 
                   
    for machine in particle.machine_list:
        machine.joblist = sorted(machine.joblist, key = lambda x : x[0])
        
                

def assignMachinesToParticles(swarm, machines):
    num_particles = len(swarm)
    num_machines_per_particle = m
    
    # Assign three machine objects to each swarm object
    for particle, machine in zip(swarm, [machines[i:i+num_machines_per_particle] for i in range(0, len(machines), num_machines_per_particle)]):
        particle.assign_machines(machine)
    
    
def assign_processing_times(jobs, ptimes):
    n = len(jobs)
    N = len(ptimes)
    
    for i in range(n):
        pindex = i % N
        jobs[i].Pj = ptimes[pindex]
    
    # for job, index in zip(jobs, range(n)):
    #     job.Pj = ptimes[index]
        
def calculate_makespan(swarm):
    for particle in swarm:
        particle.get_last_job_completiontime(particle.machine_list)
        mlist = particle.machine_list
        Cmax = mlist[0].lastJobCompTime
        for m in mlist:
            if Cmax < m.lastJobCompTime:
                Cmax = m.lastJobCompTime
        
        particle.Cmax = Cmax
        
def getinduv_makespan(particle):
    particle.get_last_job_completiontime(particle.machine_list)
    mlist = particle.machine_list
    Cmax = mlist[0].lastJobCompTime
    for m in mlist:
        if Cmax < m.lastJobCompTime:
            Cmax = m.lastJobCompTime
        
    particle.Cmax = Cmax
    
            
def PlotGanttChar (particle):
        # ------------------------------
        # Figure and set of subplots
        
    Cmax = particle.Cmax
    fig, ax = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # ylim and xlim of the axes
    ax.set_ylabel('Machine', fontweight ='bold', loc='top', color='magenta', fontsize=16)
    ax.set_ylim(-0.5, m-0.5)
    ax.set_yticks(range(m), minor=False)
    ax.tick_params(axis='y', labelcolor='magenta', labelsize=16)
        
    ax.set_xlabel('Time', fontweight ='bold', loc='right', color='red', fontsize=16)
    ax.set_xlim(0, Cmax+2)
        
    ax.tick_params(axis='x', labelcolor='red', labelsize=16)
        
    ax.grid(True)
        
    tmpTitle = 'Flow Shop Scheduling (m={:02d}; n={:03d}; Utilization={:04d})'.format(m, n, Cmax)
    plt.title(tmpTitle, size=24, color='blue')
        
    colors = ['orange', 'deepskyblue', 'indianred', 'limegreen', 'slateblue', 'gold', 'violet', 'grey', 'red', 'magenta','blue','green','silver']
        
        
    for i in range (m):
        joblen = len(particle.machine_list[i].joblist)
        for k in range(joblen):
            j = particle.machine_list[i].joblist[k]
            ST = j[1].start_time
            cIndx = 0
            # cIndx = k%(n*N)
            ax.broken_barh([(ST, j[1].Pj)], (-0.3+i, 0.6), facecolor=random.choice(colors), linewidth=1, edgecolor='black')
            ax.text((ST + (j[1].job_number/2-0.3)), (i+0.03), '{}'.format(j[1].job_number), fontsize=18)
        
def getVelocity(c1, c2, w, particle):
    
    vel = [v for v in range(n)]
    getrandomnumbers(particle)
    
    for i in range(n):
        vel[i] = w*particle.v[i] + c1*particle.r1 * (particle.local_best[i] - particle.position[i]) + c2*particle.r2 * (particle.global_best[i] - particle.position[i])
        
    rounded_list = [round(num, 2) for num in vel]
    
    particle.v = rounded_list
        
def set_local_best(particle):
    if particle.oldfit > particle.Cmax:
        particle.local_best = particle.position
        particle.oldfit = particle.Cmax
            
def set_global_best(swarm):
    min = swarm[0]
    for particle in swarm:
        if particle.Cmax < min.Cmax:
            min = particle
        
    for particle in swarm:
        particle.global_best = min.position
            
        

def getrandomnumbers(particle):
    particle.r1 = random.uniform(0, 1)
    particle.r2 = random.uniform(0, 1)
        
def checkbounds(particle):
    for i in range(len(particle.position)):
        if particle.position[i] > m:
            particle.position[i] = m - 0.1
                
        if particle.position[i] < 0:
            particle.position[i] = 0

def update_position(particle):
    newpos = [num1 + num2 for num1,num2 in zip(particle.position, particle.v)]
    rounded_list = [round(num, 2) for num in newpos]
    particle.position = rounded_list


def get_best_makespan(swarm):
    min = swarm[0]
    bestCmax = 0
    for particle in swarm:
        if min.Cmax < particle.Cmax:
            min = particle

    bestCmax = min.Cmax
    return min, bestCmax


def get_global_fitness(particle):
    tjobs = [Job(number) for number in range(n)]
    tmachines = [Machine(index) for index in range(m)]
    tparticle = Particle(n,m)
    tparticle.position = particle.global_best
    assign_processing_times(tjobs, ptimes)
    assignMachinesToParticles([tparticle], tmachines)
    assign_jobs_to_machines(tparticle , tjobs)
    getinduv_makespan(tparticle)
    
    return tparticle.Cmax

def get_global_particle(particle):
    tjobs = [Job(number) for number in range(n)]
    tmachines = [Machine(index) for index in range(m)]
    tparticle = Particle(n,m)
    tparticle.position = particle.global_best
    assign_processing_times(tjobs, ptimes)
    assignMachinesToParticles([tparticle], tmachines)
    assign_jobs_to_machines(tparticle , tjobs)
    getinduv_makespan(tparticle)
    
    return tparticle

def check_global_best(swarm, gbest):
    for particle in swarm:
        if particle.Cmax < get_global_fitness(gbest):
            gbest = particle
            
    for particle in swarm:
        particle.global_best = gbest.position

# def generateMjConstraint(m):
    
#     length = random.randint(1, m)  # Random length within the range 1 to m
#     numbers = random.sample(range(0, m), length)  # Sample without replacement from the range 1 to m
#     return numbers

def assignMjConstraints(newjobs):
    # random_lists = [generateMjConstraint(m) for _ in range(n)]
    
    MjConst = [0,2]
    
    # Assign the randomly generated lists to the corresponding elements in each sublist
    for sublist in newjobs:
        sublist[5].Mj = MjConst

def check_Mj_constraint(particle):
    for machine in particle.machine_list:
        for job in machine.joblist:
            if machine.machine_id not in job[1].Mj and len(job[1].Mj) != 0:
                particle.put_penalty()
    
    
# plt.show()

if __name__ == '__main__':
    t = 0
    
    machines = [Machine(index) for index in range(n*N)]
    swarm = [Particle(n, m) for _ in range(N)]
    
    
    jobs = [Job(number) for number in range(n*N)]
    #assign the data to the jobs
    assign_processing_times(jobs, ptimes)
    
    
    # assign machines to particles
    assignMachinesToParticles(swarm, machines)

    times = n

    # Split the list into sublists of size N
    newjobs = [jobs[i:i+times] for i in range(0, len(jobs), times)]
    
    # generateMjConstraint(m)
    assignMjConstraints(newjobs)
    
    if print_out1:
        for sublist in newjobs:
            for obj in sublist:
                print(f"{obj.job_number} Random List: {obj.Mj}")
    
    # assign jobs to machines in each particle
    for particle,i in zip(swarm, range(0, len(newjobs))):
        assign_jobs_to_machines(particle , newjobs[i])   

    
    # calculate_makespan(swarm)

    # for particle in swarm:
    #     PlotGanttChar(particle)

    # print(jobs[11].Pj)

    if print_out:
        print(swarm[0].position)
        # print(swarm[0].machine_list)
        # for particle in swarm:
        #     print(f" Machines: {[machine.machine_id for machine in particle.machine_list]}")
            
        # if print_out:
        #     for job in jobs:
        #         print(f'job number - {job.job_number} pj - {job.Pj}')
            
        print(swarm[0].machine_list[0].joblist)
        print(swarm[0].machine_list[1].joblist)
        print(swarm[0].machine_list[2].joblist)
        print(jobs[2].start_time)

        for i in range(len(swarm[1].machine_list[0].joblist)):
            print(f'job number: {swarm[1].machine_list[0].joblist[i][1].job_number}, job processing times: {swarm[1].machine_list[0].joblist[i][1].Pj} \t')
            
        print('\n')
        for i in range(len(swarm[1].machine_list[1].joblist)):
            print(f'job number: {swarm[1].machine_list[1].joblist[i][1].job_number}, job processing times: {swarm[1].machine_list[1].joblist[i][1].Pj}\t')
            
        print('\n')
        for i in range(len(swarm[1].machine_list[2].joblist)):
            print(f'job number: {swarm[1].machine_list[2].joblist[i][1].job_number}, job processing times: {swarm[1].machine_list[2].joblist[i][1].Pj} \t')

        print('\n')
        # print('Completion of last job in machine 0 ', swarm[0].machine_list[0].lastJobCompTime)
        # print('Completion of last job in machine 1 ', swarm[0].machine_list[1].lastJobCompTime)
        # print('Completion of last job in machine 2 ', swarm[0].machine_list[2].lastJobCompTime)
        print('Makespan of machine: ',swarm[0].Cmax)
        print('\n')
        print('Start time of first job ', swarm[0].machine_list[0].joblist[0][1].start_time)
        print('Completion of first job ', swarm[0].machine_list[0].joblist[0][1].Cj)
        print('Start time of first job ', swarm[0].machine_list[0].joblist[1][1].start_time)
        print('Completion of first job ', swarm[0].machine_list[0].joblist[1][1].Cj)


        print(len(swarm[0].machine_list[0].joblist))
        
    
    ypoints = []
    
    set_global_best(swarm)
    bestlist = []
    counter = 0
    history = 0
    
    # start of generation loop
    while t < T:
        
        # set_global_best(swarm)
        gbest = get_global_particle(swarm[0])
        checkbounds(gbest)
       
        for particle, i in zip(swarm, range(0,len(newjobs))):
            getVelocity(c1= c1, c2= c2, w= w, particle = particle)
            update_position(particle)
            checkbounds(particle)
            assign_jobs_to_machines(particle, newjobs[i])
            getinduv_makespan(particle)
            check_Mj_constraint(particle)
            set_local_best(particle)
            
        check_global_best(swarm, gbest)
        
        bestCmax, value = get_best_makespan(swarm)
        checkbounds(bestCmax)
        
        # count no of times same Cmax
        if counter >= 3:
           break 
        
        
        bestlist.append(bestCmax)
        
        
        # check if previous Cmax is same
        if history == value:
            counter += 1
        else:
            counter = 0
            
        # set new history for next gen
        history = value
        
        t += 1
        
            
    bestlist = sorted(bestlist, key = lambda x : x.Cmax)
    ypoints = [particle.Cmax for particle in reversed(bestlist)]
    
    
    print(ypoints[-1], t)
    
    # plot line graph
    
    xpoints = [x for x in range(1, t+ 1)]
    plt.plot(xpoints, ypoints,  color= 'b')
    plt.show()
    
    
    # plot gantt chart
    
    PlotGanttChar(bestlist[0])
    plt.show()
    
print('done')
    
            
    