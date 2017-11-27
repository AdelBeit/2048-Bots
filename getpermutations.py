import numpy as np

#a = [0,0,0]
def getpermutations(a):
    p = [a]
    nextpermutation(a,2**len(a)-1,p)
    return p
    
def nextpermutation(a,i,p):
    if i > 0:
        b = add1(a)
        for o in range(len(p[0])-len(b)):
            b.insert(0,0)
        p.append(b)
        nextpermutation(b,i-1,p)
    return p

def add1(a):
    s = ""
    for i in a:
        s += str(i)
    b = "".join(['0' for i in range(len(a)-1)]) + '1'
    c = bin(int(s,2) + int(b,2))[2:]
    u = [int(i) for i in c]
    return u

#nextpermutation(a,2**len(a)-1)
#print(np.array(getpermutations(a)))
