import copy
import time
class graph:
    def __init__(self):
        self.graph={}
        self.visited={}        

    def append(self,vertexid,edge,weight):
        if vertexid not in self.graph.keys():          
            self.graph[vertexid]={}
            self.visited[vertexid]=0
        self.graph[vertexid][edge]=weight

    def reveal(self):
        return self.graph
    
    def vertex(self):
        return list(self.graph.keys())

    def edge(self,vertexid):
        return list(self.graph[vertexid].keys())
    
    def weight(self,vertexid,edge):
        
        return (self.graph[vertexid][edge])
    
    def size(self):
        return len(self.graph)
    
    def visit(self,vertexid):
        self.visited[vertexid]=1
    
    def go(self,vertexid):
        return self.visited[vertexid]
    
    def route(self):
        return self.visited
    
    def degree(self,vertexid):
        return len(self.graph[vertexid])
    
    def mat(self):
        self.matrix=[]
        for i in self.graph:
            self.matrix.append([0 for k in range(len(self.graph))])
            for j in self.graph[i].keys():        
                self.matrix[i-1][j-1]=1
        return self.matrix

    def remove(self,node):
        for i in self.graph[node].keys():
            self.graph[i].pop(node)
        self.graph.pop(node)

df=graph()
df.append(1,2,0)
df.append(1,3,0)
df.append(1,4,0)
df.append(1,6,0)
df.append(2,1,0)
df.append(3,1,0)
df.append(4,1,0)
df.append(6,1,0)

df.append(2,3,0)
df.append(2,4,0)
df.append(2,6,0)
df.append(3,2,0)
df.append(4,2,0)
df.append(6,2,0)

df.append(3,4,0)
df.append(3,7,0)
df.append(4,3,0)
df.append(7,3,0)

df.append(4,5,0)
df.append(5,4,0)

df.append(5,6,0)
df.append(6,5,0)

def sort_by_degree(df):   #sorting in ascending order
    
    dic={}
    for i in df.vertex():
        dic[i]=df.degree(i)
    
    output=[i[0] for i in sorted(dic.items(), key=lambda x:x[1])]
    return output[::-1]

def find_kcore(core,df):     #
    start_time = time.time()
    subset=copy.deepcopy(df)
    queue=sort_by_degree(subset)
    node=queue.pop()
    priority=set([])
    
    
    while queue:
        if len(subset.vertex())<core+1:   
            return {}

        if subset.degree(node)<core:
            if priority.intersection(set(subset.edge(node))):
                priority=priority.intersection(set(subset.edge(node)))
            else:
                priority=priority.union(set(subset.edge(node)))

            priority=set([i for i in sort_by_degree(subset) if i in priority])
            subset.remove(node)

        if priority:
            node=priority.pop()
            try:
                queue.remove(node)
            except ValueError:
                pass
        else:
            node=queue.pop()       
    print("--- %s seconds ---" % (time.time() - start_time))
    return subset.reveal()

def get_degree_list(df):
    D={}
    for i in df.vertex():
        try:
            D[df.degree(i)].append(i)

        except KeyError:
            D[df.degree(i)]=[i]
    D=dict(sorted(D.items()))
    
    return D

def matula_beck(df):
    start_time = time.time()
    subset=copy.deepcopy(df)
    k=0
    L=[]
    output={}
    output[1]=df.vertex()
    D=get_degree_list(subset)
    i=0

    while D:
        j=i
        i=list(D.keys())[0]
        if j<i:
            output[i]=[j for i in D.values() for j in i ]
        
    
        k=max(k,i)
        v=D[i].pop(0)
        L.append(v)
        subset.remove(v)
        D=get_degree_list(subset)  

    missing=[i for i in range(1,max(output.keys())) if i not in output.keys()]
    for i in missing:
        output[i]=output[i-1]
    print("--- %s seconds ---" % (time.time() - start_time))
    return output

def vladimir(k,df):   
    start_time = time.time()
    subset=copy.deepcopy(df)
    D={}
    for i in subset.vertex():
        D[i]=subset.degree(i)
    queue=sort_by_degree(subset)
    while queue:
        i=queue.pop()
        subset.visit(i)
    
        if D[i]<k:
            for j in subset.edge(i):
                D[j]-=1

        queue=[]
        for key,_ in sorted(D.items(),reverse=True,key=lambda x:x[1]):
            if subset.go(key)==0:
                queue.append(key)

    print("--- %s seconds ---" % (time.time() - start_time))
    return [i for i in D if D[i]>=k]

print('brute force')
print(find_kcore(3,df))
print('Matula & Beck')
print(matula_beck(df))
print('Vladimir')
print(vladimir(3,df))