import numpy as np
import random
import time
import math

class Node:
    def __init__(self, id, parent, n=None):
        self.id = id
        self.parent = parent  # previous node
        if parent==None: # the first node
            self.dots = []
            self.vecs = np.array([[0,0]])
            self.n=n
        else: # following nodes
            self.n = self.parent.n
            self.vecs = np.concatenate((self.parent.vecs, get_vecs(id,self.parent.dots)), axis=0)
            self.dots = list(self.parent.dots) + [id]
        self.depth = len(self.dots)
        self.get_children()        # potential next ids

    def get_children(self):
        children_ids = list(set(list(range(self.n)))-set(self.dots)) #all minus previous dots
        if len(self.dots)==0: self.children = children_ids #root
        else:
            self.children = []
            for cid in children_ids:
                child_vecs = get_vecs(cid,self.dots)  #get all vectors between previous dots and new dot
                all_vecs = np.concatenate((self.vecs,child_vecs))
                all_unique_vecs = np.unique(all_vecs, axis=0)
                if all_vecs.shape[0]==all_unique_vecs.shape[0]:
                    self.children.append(cid)

    def select_child(self):
        #if in the top or bottom: random
        ratio = self.depth/self.n
        if ratio<0.2 or ratio>0.7: #0.25, 0.50
            cid = random.choice(self.children)
        else:
            #CHOSE A HEURISTIC
            #1. Random
            cid = random.choice(self.children)
            #2. Choose the child that with longest sum of vectors
            """
            sums = []
            for child in self.children:
                next_vecs = get_vecs(child,self.dots)
                sum = 0
                for vec in next_vecs: sum+=np.linalg.norm(vec)
                sums.append(sum)
                children = [x for _,x in sorted(zip(sums,self.children))]
                cid = children[0]
            """
            #3. Choose the child that is the furthest from the center column
            """
            dists = []
            for child in self.children: dists.append(abs(child-0.5*self.n))
            children = [x for _,x in sorted(zip(dists,self.children))]
            cid = children[0]
            """

        return cid

#integrate the 2 functions below. make get vecs a subfucntion of get all vecs
def get_vecs(id,dots):
    if len(dots)==0:
        vecs = [[0,id]]
    else:
        a = np.flip(np.arange(len(dots)))+1
        b = id-np.copy(dots)
        vecs = np.column_stack((a,b))
    return vecs

def get_all_vecs(dots):
    vecs = []
    for i in range(len(dots)):
        for j in range(len(dots)):
            if j>=i: break
            vecs.append(np.array([i-j,dots[i]-dots[j]]))
    return np.array(vecs)

start_n = 10
no_steps = 10
no_sols = 1000
save = True

init_poliy = 1 #0: random, 1: based on previous valid solution for N-1

for steps in range(no_steps):
    n=start_n+steps
    solutions = []
    durations = []
    print("-------------------- Size",n,"*",n,"--------------------")
    for no_sol in range(no_sols):
        nodes = [Node(-1, None, n=n)] # start node to coonect the tree at the origin
        start_time = time.time()
        while nodes[-1].depth<n and (time.time()-start_time)<60*60:
            if len(nodes[-1].children)!=0:
                next_id = nodes[-1].select_child()
                nodes.append(Node(next_id,nodes[-1]))
            else: #there are no children
                last_node = nodes[-1]
                for back_track in range(nodes[-1].depth):
                    last_node.parent.children.remove(last_node.id) # remove "bad" child
                    if len(last_node.parent.children)>0: #if there is another porential child
                        next_id = last_node.parent.select_child()
                        nodes.append(Node(next_id,last_node.parent))
                        nodes.remove(last_node)
                        break
                    else:
                        nodes.remove(last_node)
                        last_node = last_node.parent # if there is no other porential child, backtrack further

        # Finish up
        solutions.append(nodes[-1].dots)
        duration = round(time.time()-start_time,4)
        if duration>=60*60: break
        durations.append(duration)
        verified_costas_array = False #double checking validity of list
        vecs = get_all_vecs(nodes[-1].dots)
        if np.unique(vecs, axis=0).shape[0]==vecs.shape[0]: verified_costas_array=True
        #if no_sol%10==0:
    mid_index = int(len(durations)/2)
    median_duration = list(durations)
    median_duration.sort()
    median_duration = median_duration[mid_index]
    print("Finished in mediam time", format(median_duration, '.2f'), "s. Array:",nodes[-1].dots,"N:",n,"Prog:",str(no_sol+1)+"/"+str(no_sols),". Ver:",verified_costas_array)
    if duration>=60*60: break
    if save:
        file = open("data_laptop_tree_random/solitions_"+str(n)+".txt","w")
        for sol in solutions:
            for item in sol:
                if item==sol[-1]: file.write("%s\n" % item)
                else: file.write("%s," % item)
        file.close()
        file = open("data_laptop_tree_random/durations_"+str(n)+".txt","w")
        for dur in durations: file.write(str(format(dur, '.4f'))+"\n")
        file.close()
