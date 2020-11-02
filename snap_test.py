import snap
import random

f = open("data/US_airports/US_airports.net", "r")
G1 = snap.PUNGraph.New()
nodes = set()
for line in f:
    items = line.split(" ")
    start = int(items[0])
    end = int(items[1])
    weight = int(items[2])
    if start not in nodes:
        nodes.add(start)
        G1.AddNode(start)
    if end not in nodes:
        nodes.add(end)
        G1.AddNode(end)
    G1.AddEdge(start, end)


print("Diameter: "+str(snap.GetBfsFullDiam(G1, G1.GetNodes())))
print("Nodes:" +str(G1.GetNodes()))
print("Edges: "+str(G1.GetEdges()))
print("Clustering coeff: "+str(round(snap.GetClustCf(G1, -1),3)))
#print("Beetweeness cent: "+snap.GetBetweennessCentr(G1, -1))
#snap.GetOutDegCnt(G1)

print("------------------------------------------------------------")
UGraph1 = snap.GenRndGnm(snap.PUNGraph, 300, 1000, False)
print("Diameter: "+str(snap.GetBfsFullDiam(UGraph1, UGraph1.GetNodes())))
print("Nodes:" +str(UGraph1.GetNodes()))
print("Edges: "+str(UGraph1.GetEdges()))
print("Clustering coeff: "+str(round(snap.GetClustCf(UGraph1, -1),3)))
#writeGraphToFile(UGraph1, "Graph-1")
print("")

UGraph2 = snap.GenRndGnm(snap.PUNGraph, 500, 30000, False)
print("Diameter: "+str(snap.GetBfsFullDiam(UGraph2, UGraph2.GetNodes())))
print("Nodes:" +str(UGraph2.GetNodes()))
print("Edges: "+str(UGraph2.GetEdges()))
print("Clustering coeff: "+str(round(snap.GetClustCf(UGraph2, -1),3)))
g1 = snap.TFOut("data/graph2.graph")

print("-------------------------------------------------------------")

f = open("data/facebook_like_forum_network", "r")
G4 = snap.PUNGraph.New()
nodes = set()
for line in f:
    items = line.split(" ")
    start = int(items[0])
    end = int(items[1])
    weight = int(items[2])
    if start not in nodes:
        nodes.add(start)
        G4.AddNode(start)
    if end not in nodes:
        nodes.add(end)
        G4.AddNode(end)
    G4.AddEdge(start, end)


print("Diameter: "+str(snap.GetBfsFullDiam(G4, G4.GetNodes())))
print("Nodes:" +str(G4.GetNodes()))
print("Edges: "+str(G4.GetEdges()))
print("Clustering coeff: "+str(round(snap.GetClustCf(G4, -1),3)))

f = open("data/Graph-1.txt", "w")
for nid in UGraph1.Edges():
    weight = random.randint(1,101)
    print("edge (%d, %d, %d)" % (nid.GetSrcNId(), nid.GetDstNId(), weight))
    f.write("%d %d %d\n" % (nid.GetSrcNId(), nid.GetDstNId(), weight))
f.close()

f = open("data/Graph-2.txt", "w")
for nid in UGraph2.Edges():
    weight = random.randint(1, 1001)
    f.write("%d %d %d\n" % (nid.GetSrcNId(), nid.GetDstNId(), weight))
f.close()
