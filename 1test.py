
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import os
 
from numerize import numerize
# os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
plt.figure(figsize=(20,10))
G =  nx.DiGraph() 

s_solution =  pd.read_excel("city.xlsx",sheet_name="crop").replace(0, 1)
s_solution=s_solution.dropna()
s_solution=s_solution.replace(0, 1)
s_solution = s_solution.drop(s_solution[s_solution.water ==1].index)

ss_solution = s_solution['city']

xx =ss_solution.drop_duplicates()

s_solution= s_solution.drop_duplicates()




for  row in xx:
    G.add_edge('Egypt',row)
for  row in xx:
    # G.add_edge('Egypt',row['city'])
    # G.add_edge('egypt',row)
    for index, rowi in s_solution.iterrows():
        if rowi['city'] == "Fayoum" or rowi['city'] == "Giza"or rowi['city'] == "Cairo"or rowi['city'] == "Alexandria":
            G.add_edge(rowi['city'],rowi['name'])
            
            G.add_edge(rowi['name'],numerize.numerize(int(rowi['water'])))
           




# nx.draw(G,with_labels=1,edge_cmap=plt.cm.OrRd,pos=nx.random_layout(G, seed=13))




pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
nx.draw(G,pos=pos,with_labels=True,node_size=1000)
plt.show()



