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

def compute_costs(dots, return_local=True):
    n = dots.shape[0]

    # Make list of the vectors between all dots and their start/end positions
    vecs = []
    vids = []
    for i in range(n):
        for j in range(n):
            if j>=i: break
            vecs.append([i-j,dots[i]-dots[j]])
            vids.append([i,j])

    # Calculate total cost
    unique, counts = np.unique(np.array(vecs), axis=0, return_counts=True)
    cost = (np.sum(counts)-len(counts))

    # Calculate local costs if necessary
    if return_local:
        costs = np.zeros(n)
        for vec,ids in zip(vecs,vids):
            cnt = vecs.count(vec)
            if cnt>1:
                costs[ids[0]]+=cnt-1
                costs[ids[1]]+=cnt-1
        return cost, costs
    else:
        return cost

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

start_n = 19
no_steps = 1 #5 to 16, 8 to 19
no_sols = 10
init_policy = 0 #0: random, 1: based on previous successful solution of a N-1 array
save = False
duration=0
save = True
max_shuffle_cnt = 50

for steps in range(no_steps):
    n=start_n+steps
    max_iter = 1000
    max_restarts = 100
    pre_solutions = import_previous_solutions(n)
    solutions = []
    durations = []
    start_time = time.time()
    print("-------------------- Size",n,"*",n,"--------------------")
    while len(solutions)<no_sols:

        restart_no = 0
        new_solution_found = False

        while restart_no<max_restarts and not new_solution_found:

            restart_no+=1
            shuffle_cnt=0

            # Initiate a random array of dots
            if init_policy==0:
                dots = np.random.permutation(n)

            elif init_policy==1:
                # Take a random solution of n-1, insert a random column and row to this solution
                dots = np.copy(random.choice(pre_solutions))
                rcol, rrow = random.randint(0,n-1), random.randint(0,n-1)
                dots[dots>=rcol]+=1
                dots = np.insert(dots, rrow, rcol)

            tabu = []
            cost = 999
            iter = 0

            while iter<max_iter and cost>0:

                iter+=1
                cost, costs = compute_costs(dots)
                better_dots = []

                # Swap worst cell with others
                bad_id = get_bad_except_tabu(costs,tabu)[0]

                for i in range(n):
                    if i==bad_id: continue
                    new_dots = np.copy(dots)
                    new_dots[i], new_dots[bad_id] = new_dots[bad_id], new_dots[i] #swap
                    new_cost = compute_costs(new_dots, return_local=False)
                    if new_cost<cost:
                        cost = new_cost
                        better_dots = new_dots

                if len(better_dots)>0: # you found sometihng better!
                    dots = better_dots
                    #if len(tabu)>0: tabu.pop(0)
                #elif len(tabu)<3: tabu.append(bad_id)
                else: iter=max_iter #restart
                #
                # Baseline option
                #iter=max_iter #restart

                """
                # Try swapping more... Restart policy B
                if shuffle_cnt<max_shuffle_cnt:
                    bad_ids = get_bad_except_tabu(costs,tabu)[:int(n/3)]
                    bad_dots = []
                    for id in bad_ids: bad_dots.append(dots[id])
                    random.shuffle(bad_dots)
                    for i,id in enumerate(bad_ids): dots[id] = bad_dots[i]
                    shuffle_cnt+=1
                else: iter=max_iter #restart

                # Try swapping more... Restart policy A
                bad_ids = get_bad_except_tabu(costs,tabu)
                bad_id1 = bad_ids[0]
                bad_id2 = bad_ids[1]
                for i in range(n):
                    for j in range(n):
                        if i==bad_id1 or j==bad_id1: continue
                        if i==bad_id2 or j==bad_id2: continue
                        if i==j: continue
                        new_dots = np.copy(dots)
                        new_dots[i], new_dots[bad_id1] = new_dots[bad_id1], new_dots[i] #swap
                        new_dots[j], new_dots[bad_id2] = new_dots[bad_id2], new_dots[j] #swap
                        new_cost = compute_costs(new_dots, return_local=False)
                        if new_cost<cost:
                            cost = new_cost
                            better_dots = new_dots
                if len(better_dots)>0: dots = better_dots # you found sometihng better!
                else: iter=max_iter #restart
                """

            if cost==0:
                new_solution_found=True
                solutions.append(dots)
                duration = round(time.time()-start_time,4)
                durations.append(duration)
                verified_costas_array = False #double checking validity of list
                vecs = get_all_vecs(dots)
                if np.unique(vecs, axis=0).shape[0]==vecs.shape[0]: verified_costas_array=True
                #if len(solutions)%10==0:
                print("Finished in", format(duration, '.2f'), "s. Array:",dots,"N:",n,"Prog:",str(len(solutions))+"/"+str(no_sols),". Ver:",verified_costas_array)
                start_time = time.time()

    median_duration = list(durations)
    median_duration.sort()
    mid_index = int(len(durations)/2)
    median_duration = median_duration[mid_index]
    print("-")
    print("Finished", n, "sized array in median time", format(median_duration, '.2f'), "s.")
    print("-")
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
