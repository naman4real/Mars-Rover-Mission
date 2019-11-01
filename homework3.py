#def findOptimalPath(sr,sc,dr,dc,came_from):

from math import sqrt
from queue import PriorityQueue

import timeit


def heuristic(new_c,new_r,dc,dr):
    d=abs(sqrt(((new_c-dc)*10)**2+ ((new_r-dr)*10)**2))
    h=abs(TheMap[new_r][new_c]-TheMap[dr][dc])
    estimated_dist=abs(sqrt(d**2 + h**2))
    return estimated_dist



def findOptimalPath(dr,dc,came_from):
    steps = 0
    the_path = []
    a, b = dc, dr
    while len(came_from):
        if (a, b) == (SC, SR):
            the_path.append((a, b))
            the_path.reverse()
            print(steps)
            return the_path
        the_path.append((a, b))
        if (a,b) in came_from:
            (a, b) = came_from[(a, b)]
            steps += 1
        else:
            return 'FAIL'



def explore_neighbours_Astar(r, c,dc,dr ,cost):
    temp_cost=0
    for i in range(8):
        new_r = r + rdv[i]
        new_c = c + cdv[i]
        if new_r < 0 or new_c < 0:
            continue
        if new_r >= H or new_c >= W:
            continue
        if (new_c,new_r) in Astar_came_from:
            continue
        if abs(TheMap[new_r][new_c] - TheMap[r][c]) > ElevationDifference:
            continue
        if abs(new_c-c)==1 and abs(new_r-r)==1:
            temp_cost = (cost + 14) + heuristic(new_c, new_r,dc,dr) + abs(TheMap[new_r][new_c] - TheMap[r][c])
            Astar_queue.put( [temp_cost , (new_c,new_r)] )
        else:
            temp_cost = (cost + 10) + heuristic(new_c, new_r,dc,dr) + abs(TheMap[new_r][new_c] - TheMap[r][c])
            Astar_queue.put( [temp_cost  , (new_c,new_r)] )

        for m in range(len(Astar_queue.queue)):
            if Astar_queue.queue[m][1]==(new_c, new_r) and Astar_queue.queue[m][0]!=temp_cost:
                Astar_queue.queue[m][0]=min(Astar_queue.queue[m][0],temp_cost)

        Astar_came_from[(new_c, new_r)] = (c, r)


def explore_neighbours_UCS(r, c, cost):
    for i in range(8):
        new_r = r + rdv[i]
        new_c = c + cdv[i]

        if new_r < 0 or new_c < 0:
            continue
        if new_r >= H or new_c >= W:
            continue
        if (new_c,new_r) in came_from:
            continue
        if abs(TheMap[new_r][new_c] - TheMap[r][c]) > ElevationDifference:
            continue
        if abs(new_c-c)==1 and abs(new_r-r)==1:
            rqueue.put([cost + 14, (new_c,new_r)])
            temp=cost+14

        else:
            rqueue.put([cost + 10, (new_c,new_r)])
            temp=cost+10
        for m in range(len(rqueue.queue)):
            if rqueue.queue[m][1]==(new_c, new_r) and rqueue.queue[m][0]!=temp:
                #print("again!!!!!! now replace")
                rqueue.queue[m][0]=min(rqueue.queue[m][0],temp)

        came_from[(new_c, new_r)] = (c, r)

def explore_neighbours_BFS(r,c):
    for i in range(8):
        new_r=r+rdv[i]
        new_c=c+cdv[i]
        #print(new_c,new_r,end=" ")
        if new_r<0 or new_c<0:
            continue
        if new_r>=H or new_c>=W:
            continue
        if (new_c,new_r) in came_from:
            continue
        if abs(TheMap[new_r][new_c]-TheMap[r][c])>ElevationDifference:
            continue

        CellQueue.append((new_c, new_r))
        came_from[(new_c, new_r)] = (c, r)


def Astar(dc,dr):
    global target_reached
    r, c = 0, 0
    final_cost=0

    Astar_queue.put([0, (SC,SR)])
    Astar_came_from[(SC, SR)] = (-1, -1)
    while not Astar_queue.empty():
        cost, cell = Astar_queue.get()
        c=cell[0]
        r=cell[1]
        if r == dr and c == dc:
            final_cost=cost
            target_reached = True
            break
        explore_neighbours_Astar(r, c, dc,dr, cost)
    if target_reached:
        path = findOptimalPath(r, c, Astar_came_from)  #change ths
        # print("----------------------------")
        #print(final_cost)
        return path
    return 'FAIL'



def UCS():
    dest_path_pair = {}
    tempList = []
    target_cnt = 0
    global target_reached
    r, c = 0, 0
    rqueue.put([0, (SC,SR)])
    came_from[(SC, SR)] = (-1, -1)
    for q in ListOfTargetSites:
        tempList.append(q)
    while not rqueue.empty():
        cost, cell = rqueue.get()
        c=cell[0]
        r=cell[1]
        if [c,r] in tempList:
            path = findOptimalPath(r, c, came_from)
            dest_path_pair[(c,r)]=path
            tempList.remove([c,r])
            target_cnt+=1
        if target_cnt==NumberOfTargetSites:
            return dest_path_pair
        explore_neighbours_UCS(r,c,cost)
    if tempList:
        for unreachable in tempList:
            if tuple(unreachable) in dest_path_pair:
                continue
            dest_path_pair[tuple(unreachable)] = 'FAIL'

    return dest_path_pair

def BFS():
    dest_path_pair={}
    tempList=[]
    target_cnt=0
    CellQueue.append((SC,SR))
    came_from[(SC, SR)]=(-1, -1)
    for q in ListOfTargetSites:
        tempList.append(q)
    while len(CellQueue)>0:
        c,r=CellQueue.pop(0)
        if [c,r] in tempList:
            path = findOptimalPath(r, c, came_from)
            dest_path_pair[(c,r)]=path
            tempList.remove([c,r])
            target_cnt+=1
        if target_cnt==NumberOfTargetSites:
            return dest_path_pair
        explore_neighbours_BFS(r, c)
    if tempList:
        for unreachable in tempList:
            if tuple(unreachable) in dest_path_pair:
                continue
            dest_path_pair[tuple(unreachable)]='FAIL'
    return dest_path_pair

#variables
f=open('input.txt','r')
f.seek(0)
TargetSite=[]
ListOfTargetSites=[]
ColumnValues=[]
TheMap=[]


#file read starts
FirstLine=f.readline()
SecondLine=f.readline()
ThirdLine=f.readline()
FourthLine=int(f.readline())
FifthLine=int(f.readline())



SizeOfMap=[int(n) for n in SecondLine.split()]
LandingSite=[int(n) for n in ThirdLine.split()]
algorithm=FirstLine
algorithm=algorithm.strip()
W , H = SizeOfMap[0] , SizeOfMap[1]
SC , SR = LandingSite[0] , LandingSite[1]
ElevationDifference=FourthLine
NumberOfTargetSites=FifthLine


for i in range(NumberOfTargetSites):
    line=f.readline()
    ListOfTargetSites.append([int(n) for n in line.split()])


for j in range(H):
    line=f.readline()
    TheMap.append([int(n) for n in line.split()])
#file read ends
#variables initialized

CellQueue=[]
came_from={}
DestPathPairs={}
rdv=[-1,1,0,0,-1,1,1,-1]
cdv=[0,0,1,-1,1,1,-1,-1]
rqueue=PriorityQueue()
answer=[]
#last part
if algorithm=='BFS':
    DestPathPairs=BFS()
    for site in ListOfTargetSites:
        #print(DestPathPairs[tuple(site)])
        answer.append(DestPathPairs[tuple(site)])
elif algorithm=='UCS':
    DestPathPairs=UCS()
    for site in ListOfTargetSites:
        #print(DestPathPairs[tuple(site)])
        answer.append(DestPathPairs[tuple(site)])
else:
    DestPathPairs={}
    for i in ListOfTargetSites:
        if tuple(i) in DestPathPairs:
            continue
        Astar_queue = PriorityQueue()
        Astar_came_from={}
        target_reached=False
        path=Astar(i[0],i[1])
        DestPathPairs[tuple(i)]=path
    for site in ListOfTargetSites:
        #print(DestPathPairs[tuple(site)])
        answer.append(DestPathPairs[tuple(site)])
f.close()
f=open('output.txt','w')
for i in answer:
    if i=='FAIL':
        f.write('FAIL')
    else:
        #print(len(i))
        for j in range(len(i)):
            f.write(str(i[j][0]))
            f.write(',')
            f.write(str(i[j][1]))
            f.write(' ')
    f.write('\n')










