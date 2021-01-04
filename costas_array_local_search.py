import numpy as np
import random
import time
import math

def get_all_vecs(dots):
    vecs = []
    for i in range(len(dots)):
        for j in range(len(dots)):
            if j>=i: break
            vecs.append(np.array([i-j,dots[i]-dots[j]]))
    return np.array(vecs)

def compute_costs(dots):
    n = dots.shape[0]
    # Make list of the vectors between all dots and their start/end positions
    vecs = []
    vids = []
    for i in range(n):
        for j in range(n):
            if j>=i: break
            vecs.append([i-j,dots[i]-dots[j]])
            vids.append([i,j])
    # Count occurance of vecotrs and add costs accordingly
    costs = np.zeros(n)
    for vec,ids in zip(vecs,vids):
        cnt = vecs.count(vec)
        if cnt>1:
            costs[ids[0]]+=cnt-1
            costs[ids[1]]+=cnt-1
    return np.sum(costs), costs

def import_previous_solutions(n):
    sols=[]
    file = open("data/solitions_"+str(n-1)+".txt","r")
    for ln in file.readlines():
        sols.append(np.array([int(item) for item in ln.split(",")]))
    file.close()
    return sols


def get_bad_except_tabu(costs,tabu):
    n = len(costs)
    ids = list(range(n))
    adjusted_costs = np.copy(costs)
    for i in range(len(adjusted_costs)): adjusted_costs[i]+=random.uniform(0.01,0.10)
    for id in tabu: adjusted_costs[id]=0.0
    ids = [x for _,x in sorted(zip(adjusted_costs,ids))]
    ids.reverse()
    return ids

start_n = 18
no_steps = 2
no_sols = 10
init_policy = 1 #0: random, 1: based on previous successful solution of a N-1 array
max_time = 60*2
save = False
duration=0
save = True

for steps in range(no_steps):
    n=start_n+steps
    max_iter = 1000
    max_restarts = 100
    pre_solutions = import_previous_solutions(n)
    solutions = []
    durations = []
    print("-------------------- Size",n,"*",n,"--------------------")
    while len(solutions)<no_sols:

        start_time = time.time()
        restart_no = 0
        new_solution_found = False

        while restart_no<max_restarts and not new_solution_found:

            restart_no+=1

            # Initiate a random array of dots
            if init_policy==0:
                dots = np.random.permutation(n)
            elif init_policy==1:
                dots = random.choice(pre_solutions)
                dots = np.insert(dots, random.randint(0,n-1), n-1)
            tabu = []
            cost = 999
            iter = 0

            while iter<max_iter and cost>0 and max_time>(time.time()-start_time):

                iter+=1
                cost, costs = compute_costs(dots)
                better_dots = []

                # Swap worst cell with others (all others or alternatively (later) other bad ones)
                bad_ids_sorted = get_bad_except_tabu(costs,tabu)
                for i in bad_ids_sorted:
                    for j in bad_ids_sorted:
                        if i==j: continue
                        new_dots = np.copy(dots)
                        new_dots[i], new_dots[j] = new_dots[j], new_dots[i]
                        new_cost, _ = compute_costs(new_dots)
                        if new_cost<cost:
                            cost = new_cost
                            better_dots = new_dots
                            #break
                    if i>1 and len(better_dots)>0: break

                if len(better_dots)>0: dots = better_dots # you found sometihng better!
                else: # you are trapped in a local minima
                    bad_ids_sorted = get_bad_except_tabu(costs,tabu)
                    test_samples = n
                    num_swaps = 2
                    cost = 9999999
                    for _ in range(test_samples):
                        new_dots = np.copy(dots)
                        for j in range(len(bad_ids_sorted),num_swaps):
                            bad_id = bad_ids_sorted[j]
                            id = random.choice(bad_ids_sorted[num_swaps:])
                            new_dots[bad_id], new_dots[id] = new_dots[id], new_dots[bad_id]
                        new_cost, _ = compute_costs(new_dots)
                        if new_cost<cost:
                            cost = new_cost
                            better_dots = new_dots

            # If you have found a new solution
            """
            if cost==0:
                unique_solition=True
                for sol in solutions:
                    if (sol==dots).all():
                        unique_solition=False
                        break
            """
            if cost==0: # and unique_solition==True:
                new_solution_found=True
                solutions.append(dots)
                duration = round(time.time()-start_time,4)
                durations.append(duration)
                verified_costas_array = False #double checking validity of list
                vecs = get_all_vecs(dots)
                if np.unique(vecs, axis=0).shape[0]==vecs.shape[0]: verified_costas_array=True
                print("Finished in", format(duration, '.2f'), "s. Array:",dots,"N:",n,"Prog:",str(len(solutions))+"/"+str(no_sols),". Ver:",verified_costas_array)

        if duration>=max_time: break
    if duration>=max_time: break
    if save:
        file = open("data_ls/solitions_"+str(n)+".txt","w")
        for sol in solutions:
            for item in sol:
                if item==sol[-1]: file.write("%s\n" % item)
                else: file.write("%s," % item)
        file.close()
        file = open("data_ls/durations_"+str(n)+".txt","w")
        for dur in durations: file.write(str(format(dur, '.4f'))+"\n")
        file.close()
