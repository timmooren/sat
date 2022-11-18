
from copy import deepcopy

def clean_cnf(cnf, literals, trails_cnf, trails):
    for literal in literals:
        for clause in cnf.copy():
            # remove clauses containing literal 
            # clause[0] contains literal, clause[1] contains clause tag (eg. 'c1')
            if literal in clause[0]:
                #HERE: UPDATE TRAILS
                trail_literal = {literal : trails_cnf[clause[1]]}
                trails.append(trail_literal)
                # removes clause since it evalues to True
                cnf.remove(clause)
            # shorten clauses containing ~literal
            if -literal in clause[0]:
                clause[0].remove(-literal)
            
    return cnf, trails

# numbers each cnf so it can be used for updating trails -> returns list 
def number_cnf_list(cnf):
    numbered_cnf = []
    for i, clause in enumerate(cnf):
        temp = [clause, f'c{i+1}']
        numbered_cnf.append(temp)
    return numbered_cnf

# numbers each cnf so it can be used for updating trails -> returs dict 
def number_cnf_dict(cnf):
    numbered_cnf = {}
    for i, clause in enumerate(cnf):
        numbered_cnf[f'c{i+1}'] = clause
    return numbered_cnf

# mutable ds that will go through DPLL 
cnf = [[-1,-2],[-1,3],[-3,-4],[2,4,5],[-5,6,-7],[2,7,8],[-8,-9],[-8,10],[9,10,11],[-10,-12],[-11,12]]
# keeps an original copy of the cnf 
trails_cnf = number_cnf_dict(deepcopy(cnf))
cnf = number_cnf_list(cnf)

# print(trails_cnf)
# print(cnf)
# make empty trails ds
trails = []

# we make a decision
literals = [1] # l^dec
# update trails w/ l^dec
trails.append({literals[0]:'dec'}) # 
# clean cnf + update trails w/ l^clause
cnf, trails = clean_cnf(cnf, literals, trails_cnf, trails)
print(trails)
print(cnf)
# assign new literals 
literals.extend([-2,3])
# clean cnf + update trails w/ l^clause
cnf, trails = clean_cnf(cnf, literals, trails_cnf, trails)
print(cnf)
print(trails)
literals.extend([-4])
cnf, trails = clean_cnf(cnf, literals, trails_cnf, trails)
print(cnf)
print(trails)
literals.extend([5])
cnf, trails = clean_cnf(cnf, literals, trails_cnf, trails)
print(cnf)
print(trails)

# do this until we hit a contradiction 

l = [[1,2], [1,1],[1,3]]
m = []

if not l:
    print(True)

