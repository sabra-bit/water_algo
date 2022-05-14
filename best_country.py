from matplotlib.pyplot import axes, text
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from numerize import numerize
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components


def app():
    press_button = st.checkbox("Summer")
    st.header('Crop Water Print')
    
    if not press_button:
            
        
        st.subheader('Table Data Winter')
        # select_W_S = st.selectbox('Select city',df1['city'].drop_duplicates() )
        # select_W_S = st.selectbox('Select crop',df1['name'].drop_duplicates() )

        priorty = pd.read_excel('data_final.xls', na_filter=True)
        priorty = priorty[['crop_name','season','priority']]
        priorty = priorty.rename({'crop_name': 'name'}, axis='columns')
        priorty =priorty.loc[priorty['season'] =="Winter"] 
        
        df1 = pd.read_csv('sorted_winter.csv',skip_blank_lines=True, na_filter=True)
        df1 = df1.loc[df1['water'] >0]


        xx = pd.merge(df1, priorty, on=["name"])
        
        
        # merged_table1 = merged_table1.reset_index(drop=True)

    
        xx = xx[['water','area','prod','city','name','priority','Rank']].drop_duplicates() 
        xx = xx.reset_index(drop=True)
        st.dataframe(xx)


        city1 = st.selectbox('Select city',xx['city'].drop_duplicates() )
    

        dfxx = xx.loc[xx['city'] ==city1]
        
        st.dataframe(dfxx)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
        go.Bar(x=dfxx['name'], y=dfxx['priority'], name="priority",text =dfxx['priority']),
        secondary_y=False)
        fig.add_trace(
        go.Bar(x=dfxx['name'], y=dfxx['Rank'], name='Rank',text = dfxx['Rank']),
        secondary_y=True,)
        fig.update_layout(
        title_text=city1
        )



        st.plotly_chart(fig)
        
        crop1 = st.selectbox('Select crop',xx['name'].drop_duplicates() )
        dfyy = xx.loc[xx['name'] ==crop1]
        st.dataframe(dfyy)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
        go.Bar(x=dfyy['city'], y=dfyy['Rank'], name="Rank",text =dfyy['Rank']),
        secondary_y=False)
        
       
        fig.update_layout(
        title_text=crop1
        )



        st.plotly_chart(fig)



        st.subheader('Table Data')
        df = df1.loc[df1['Rank'] ==1]

                        # Create networkx graph object from pandas dataframe
        
        G =  nx.MultiGraph()
        city = df1['city']
        city = city.drop_duplicates()
        for  row in city:
                G.add_edge('Egypt',row)
                dfx = df1.loc[df1['city'] ==row]
                dfx = dfx.sort_values(by='Rank')
                # for index, rowi in dfx.iterrows():
                #     if row == rowi['city']:
                G.add_edge(dfx['city'].iloc[0],str(dfx['name'].iloc[0]+" :"+dfx['city'].iloc[0]))

        # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
        # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

            # Initiate PyVis network object
        drug_net = Network(height='665px', width='665px',directed=True, bgcolor='#222222', font_color='white',)

            # Take Networkx graph and translate it to a PyVis graph format
        drug_net.from_nx(G)

            # Generate network with specific layout settings
        drug_net.repulsion(node_distance=420, central_gravity=0.33,
                            spring_length=110, spring_strength=0.10,
                            damping=0.95)

            # Save and read graph as HTML file (on Streamlit Sharing)
        try:
                path = 'img'
                drug_net.save_graph(f'{path}/pyvis_graph.html')
                HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

            # Save and read graph as HTML file (locally)
        except:
                path = 'html_files'
                drug_net.save_graph(f'{path}/pyvis_graph.html')
                HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        components.html(HtmlFile.read(), height=835 ,width=835,scrolling=True)


    else:
            
        st.subheader('Table Data Summer')
        # select_W_S = st.selectbox('Select city',df1['city'].drop_duplicates() )
        # select_W_S = st.selectbox('Select crop',df1['name'].drop_duplicates() )

        priorty = pd.read_excel('data_final.xls', na_filter=True)
        priorty = priorty[['crop_name','season','priority']]
        priorty = priorty.rename({'crop_name': 'name'}, axis='columns')
        priorty =priorty.loc[priorty['season'] =="Summer"] 
        
        df1 = pd.read_csv('sorted_Summer.csv',skip_blank_lines=True, na_filter=True)
        df1 = df1.loc[df1['water'] >0]


        xx = pd.merge(df1, priorty, on=["name"])
        
        
        # merged_table1 = merged_table1.reset_index(drop=True)

    
        xx = xx[['water','area','prod','city','name','priority','Rank']].drop_duplicates() 
        xx = xx.reset_index(drop=True)
        st.dataframe(xx)

        city1 = st.selectbox('Select city',xx['city'].drop_duplicates() )
    

        dfxx = xx.loc[xx['city'] ==city1]
        
        st.dataframe(dfxx)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
        go.Bar(x=dfxx['name'], y=dfxx['priority'], name="priority",text =dfxx['priority']),
        secondary_y=False)
        fig.add_trace(
        go.Bar(x=dfxx['name'], y=dfxx['Rank'], name='Rank',text = dfxx['Rank']),
        secondary_y=True,)
        fig.update_layout(
        title_text=city1
        )



        st.plotly_chart(fig)
        
        crop1 = st.selectbox('Select crop',xx['name'].drop_duplicates() )
        dfyy = xx.loc[xx['name'] ==crop1]
        st.dataframe(dfyy)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
        go.Bar(x=dfyy['city'], y=dfyy['Rank'], name="Rank",text =dfyy['Rank']),
        secondary_y=False)
        
       
        fig.update_layout(
        title_text=crop1
        )



        st.plotly_chart(fig)





        st.subheader('Table Data')
        df = df1.loc[df1['Rank'] ==1]

                        # Create networkx graph object from pandas dataframe
        
        G =  nx.MultiGraph()
        city = df1['city']
        city = city.drop_duplicates()
        for  row in city:
                G.add_edge('Egypt',row)
                dfx = df1.loc[df1['city'] ==row]
                dfx = dfx.sort_values(by='Rank')
                # for index, rowi in dfx.iterrows():
                #     if row == rowi['city']:
                G.add_edge(dfx['city'].iloc[0],str(dfx['name'].iloc[0]+" :"+dfx['city'].iloc[0]))

        # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
        # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

            # Initiate PyVis network object
        drug_net = Network(height='665px', width='665px',directed=True, bgcolor='#222222', font_color='white',)

            # Take Networkx graph and translate it to a PyVis graph format
        drug_net.from_nx(G)

            # Generate network with specific layout settings
        drug_net.repulsion(node_distance=420, central_gravity=0.33,
                            spring_length=110, spring_strength=0.10,
                            damping=0.95)

            # Save and read graph as HTML file (on Streamlit Sharing)
        try:
                path = 'img'
                drug_net.save_graph(f'{path}/pyvis_graph.html')
                HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

            # Save and read graph as HTML file (locally)
        except:
                path = 'html_files'
                drug_net.save_graph(f'{path}/pyvis_graph.html')
                HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        components.html(HtmlFile.read(), height=835 ,width=835,scrolling=True)


