from Edge import *
from GraphAlgo import *

if __name__ == '__main__':
    n1 = Node(0, (1,2,3))
    # n2 = Node(2,(3,4,5))
    # e = Edge(0,1,1.1)
    # graph = DiGraph()
    # graph.add_node(0 ,(1,2,3))
    # graph.add_node(1 ,(1,2,3))
    # graph.add_node(2,(0,1,2))
    # graph.add_edge(0,2,3)
    # graph.add_edge(2,1,2)
    gw = GraphAlgo()
    gw.load_from_json('A3.json')
    # gw.TSP([1 ,3 ,5 ,45])
    # print(gw.centerPoint())
    gw.plot_graph()
    # print(gw.centerPoint())
    # g_algo.plot_graph()
    # graph.add_node(n2.getId(), n2.getLocation())
    # graph.add_edge(0,2)
    # print(graph.get_all_v())
#
