import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)


df1 = pd.read_csv('output\\winter\\summary_to_power_pi.csv',skip_blank_lines=True, na_filter=True)
df1 = df1['sol_index']
df1 = df1.astype(str)
df1 = df1.drop_duplicates()


st.header('Compare Solution')
st.subheader('Select')

select_S = st.selectbox('select solution',df1) 




if select_S != "Orginal":
        
    s_solution = pd.read_csv('output\\winter\\crops_solution_'+str(select_S)+'.csv',skip_blank_lines=True, na_filter=True)

    st.write("distribution of crops over the contry in sol: "+str(select_S))

    # .drop_duplicates()
    s_solution = s_solution[['water','area','prod','city','name']]

    s_solution=s_solution.dropna()
    s_solution=s_solution.replace(0, 1)
    s_solution = s_solution.drop(s_solution[s_solution.water ==1].index)


        # Create networkx graph object from pandas dataframe
    G =  nx.MultiGraph()
    city = s_solution['city']
    city = city.drop_duplicates()
    for  row in city:
            G.add_edge('Egypt',row[:4])
            for index, rowi in s_solution.iterrows():
                if row == rowi['city']:
                    G.add_edge(rowi['city'][:4],str(rowi['name'][:4]+" :"+rowi['city'][:4]))

    # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
    # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

        # Initiate PyVis network object
    drug_net = Network(height='565px', bgcolor='#222222', font_color='white')

        # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

        # Generate network with specific layout settings
    drug_net.repulsion(node_distance=420, central_gravity=0.33,
                        spring_length=110, spring_strength=0.10,
                        damping=0.95)

        # Save and read graph as HTML file (on Streamlit Sharing)
    try:
            path = 'img'
            drug_net.save_graph(f'{path}\\pyvis_graph.html')
            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
    except:
            path = 'html_files'
            drug_net.save_graph(f'{path}\\pyvis_graph.html')
            HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=435)
