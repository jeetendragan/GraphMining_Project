import snap

Graph = snap.GenRndGnm(snap.PNGraph, 100, 1000)
snap.PlotKCoreNodes(Graph, "example", "Directed graph - k-core nodes")

UGraph = snap.GenRndGnm(snap.PUNGraph, 100, 1000)
snap.PlotKCoreNodes(UGraph, "example", "Undirected graph - k-core nodes")

Network = snap.GenRndGnm(snap.PNEANet, 100, 1000)
snap.PlotKCoreNodes(Network, "example", "Network - k-core nodes")