import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.drawing.nx_pydot import graphviz_layout

    
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        pass
        #raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)



def draw_graph(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="neato")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()

def draw_graph_tree(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="dot")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()

def draw_graph_neato(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="neato")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()


def draw_graph_circo(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="circo")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()

def draw_graph_twopi(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="twopi")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()

def draw_graph_fdp(list,sol_no,graph_color):
    print(graph_color)
    G=nx.DiGraph()
    G.add_edges_from(list)
    G.edges(data=True)
    #pos = hierarchy_pos(G,1.1)
    #graph type circo , dot , twopi ,neato ,fdp 
        
    #pos = nx.spring_layout(G, k=0.15, iterations=20)
    pos = graphviz_layout(G, prog="fdp")
    #edge_labels = nx.get_edge_attributes(G,'Area')
    d = dict(G.degree)
    values = [graph_color.get(node, 0.25) for node in G.nodes()]
    nx.draw(G, pos=pos,with_labels=True,node_size=1000,node_color=values)
    #nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
    #nx.draw(G, with_labels=True)
    text = 'Selected Solution: '+str(sol_no) 
    plt.text(50,50,s=text, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()
