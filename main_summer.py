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

    
    st.header('Compare Solution')
    st.subheader('Select')

    df1 = pd.read_csv('output\\summer\\summary_to_power_pi.csv',skip_blank_lines=True, na_filter=True)
    df2 = pd.read_csv('output\\summer\\final_table_percentage.csv',skip_blank_lines=True, na_filter=True)
    df3 = pd.read_csv('output\\summer\\summary.csv',skip_blank_lines=True, na_filter=True)

    df2=df2.loc[df2['Labels']=='water']
    df2 = df2[['sol_index','Labels','Total']]

    merged_table1 = pd.merge(df1, df2, on=["sol_index"])

    df3["sol_index"] = df3["sol_index"].astype(str)
    merged_table2 = pd.merge(df3, df2, on=["sol_index"])

    def catValue(row):
        if row['Total'] >= 0.95 and row['Total'] <= 1:
            return int('95')
        elif row['Total'] >= 0.90 and row['Total'] < 0.95:
            return int('90')
        elif row['Total'] >= 0.85  and row['Total'] < 0.90:
            return int('85')
        elif row['Total'] >= 0.80  and row['Total'] < 0.85:
            return int('80')
        elif row['Total'] >= 0.75  and row['Total'] < 0.80:
            return int('75')
        return int('70')

    merged_table1['value'] = merged_table1.apply(lambda row: catValue(row), axis=1)
    merged_table1 = merged_table1.drop(merged_table1[merged_table1.Crop_Name =='X'].index)
    merged_table2['value'] = merged_table2.apply(lambda row: catValue(row), axis=1)
    select_W_S = st.selectbox('Select Water Saturation',merged_table1['value'].drop_duplicates() )

    xlen = len(merged_table1.loc[merged_table1['value']==select_W_S])
    st.write("you have "+str(int(xlen/16)) +" solutions")
    # print(totalData)
    solutions = merged_table2.loc[merged_table2['value']==select_W_S]

    solutions = solutions[['sol_index','Water','Area','Production','city skip','value']]
    dfx = pd.DataFrame({"sol_index":['Orginal'], "Water":[12645859000], "Area":[5915686.76908405],"Production":[72641081.731879],"city skip":[0],"value":[95] })

    solutions = pd.concat([solutions, dfx], ignore_index = True, axis = 0)

    st.dataframe(solutions)

    select_S = st.selectbox('select solution',solutions.loc[solutions['value']==select_W_S]) 



    sol =merged_table1.loc[merged_table1['sol_index'] ==select_S]
    original =merged_table1.loc[merged_table1['sol_index'] =="Orginal"]
    def chart(data , yData ,tit ,nn):

        chart1 = px.bar(data,x="Crop_Name",y= yData , text=yData
        ,orientation="v",
        title="<b>"+nn+" difference of solution "+str(tit) +"</b>",
        color_discrete_sequence=["#008388"] * len(df1),
        template="plotly_white"
        )
        chart1.update_layout(
            
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False)))

        st.plotly_chart(chart1)


    def defrance(data2,sol1,name,TT ,wiz):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
        go.Bar(x=original['Crop_Name'], y=original[wiz], name="Orginal",text =original['Water']),
        secondary_y=False)
        fig.add_trace(
        go.Bar(x=data2, y=sol1, name=name,text = sol1),
        secondary_y=True,)
        fig.update_layout(
        title_text=TT
        )



        st.plotly_chart(fig)

    inner_merged_total = pd.merge(original, sol, on=["Crop_Name"])
    dd=inner_merged_total
    dd['water_def'] = (dd["Water_y"] - dd["Water_x"])

    totalWaterO =solutions.loc[solutions['sol_index'] =="Orginal"]
    totalWaterS =solutions.loc[solutions['sol_index'] ==select_S]

    with st.container():
        st.header("Water Difference ")
        x,y = st.columns(2)
        with x:
            st.write("Orginal ="+str(numerize.numerize(int(totalWaterO['Water'])))+' m3')
        with y:
            st.write("Solution "+str(select_S)+" ="+str(numerize.numerize(int(totalWaterS['Water'])))+' m3')



    defrance(sol["Crop_Name"],sol["Water"],select_S,"Compare Water ","Water")
    
    st.write("Difference "+str(select_S)+" ="+str(numerize.numerize(int(totalWaterS['Water'])-int(totalWaterO['Water'])))+' m3')
    chart(dd,dd["water_def"],select_S,"water")




    dd['Production_def'] = (dd["Production_y"] - dd["Production_x"])

    totalWaterO =solutions.loc[solutions['sol_index'] =="Orginal"]
    totalWaterS =solutions.loc[solutions['sol_index'] ==select_S]

    with st.container():
        st.header("Production Difference ")
        x,y = st.columns(2)
        with x:
            st.write("Orginal ="+str(numerize.numerize(int(totalWaterO['Production'])))+'Ton')
        with y:
            st.write("Solution "+str(select_S)+" ="+str(numerize.numerize(int(totalWaterS['Production'])))+'Ton')



    defrance(sol["Crop_Name"],sol["Production"],select_S,"Compare Production ","Production")

    numerize.numerize(int(totalWaterS['Production'])-int(totalWaterO['Production']))
    st.write("Difference "+str(select_S)+" ="+str(   numerize.numerize(int(totalWaterS['Production'])-int(totalWaterO['Production'])))+'Ton')
    chart(dd,dd["Production_def"],select_S,"Production")

# # ================Graph================ 
# ==================Graph================






    if select_S != "Orginal":
            
        s_solution = pd.read_csv('output\\summer\\crops_solution_'+str(select_S)+'.csv',skip_blank_lines=True, na_filter=True)

        st.write("distribution of crops over the contry in sol: "+str(select_S))

        # .drop_duplicates()
        s_solution = s_solution[['water','area','prod','city','name']]

        s_solution=s_solution.dropna()
        s_solution=s_solution.replace(0, 1)
        s_solution = s_solution.drop(s_solution[s_solution.water ==1].index)

# ==========================================================
            
        s_solutionO = pd.read_excel('data_final.xls', na_filter=True)

        

        # .drop_duplicates()
        s_solutionO = s_solutionO[['crop_footprint_m3','Area','Prod','government_name','crop_name','season']]

        s_solutionO=s_solutionO.dropna()
        s_solutionO=s_solutionO.replace(0, 1)
        s_solutionO=s_solutionO.loc[s_solutionO['season']=='Summer']
        




        with st.container():
            st.header("Crop Distriution")
            x,y = st.columns(2)

            with x:
                st.write("distribution of crops over the contry in sol: "+str(select_S))
                    # Create networkx graph object from pandas dataframe
                G =  nx.MultiGraph()
                city = s_solution['city']
                city = city.drop_duplicates()
                for  row in city:
                        G.add_edge('Egypt',row)
                        for index, rowi in s_solution.iterrows():
                            if row == rowi['city']:
                                G.add_edge(rowi['city'],str(rowi['name']+" :"+rowi['city']))

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
                        drug_net.save_graph(f'{path}\\pyvis_graph.html')
                        HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                    # Save and read graph as HTML file (locally)
                except:
                        path = 'html_files'
                        drug_net.save_graph(f'{path}\\pyvis_graph.html')
                        HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                components.html(HtmlFile.read(), height=835 ,width=835,scrolling=True)

            with y:
                st.write("distribution of crops over the contry in origenal: ")
                G =  nx.MultiGraph()
                city = s_solutionO['government_name']
                city = city.drop_duplicates()
                for  row in city:
                        G.add_edge('Egypt',row)
                        for index, rowi in s_solutionO.iterrows():
                            if row == rowi['government_name']:
                                G.add_edge(rowi['government_name'],str(rowi['crop_name']+" :"+rowi['government_name']))


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
                        drug_net.save_graph(f'{path}\\pyvis_graph.html')
                        HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                    # Save and read graph as HTML file (locally)
                except:
                        path = 'html_files'
                        drug_net.save_graph(f'{path}\\pyvis_graph.html')
                        HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

                components.html(HtmlFile.read(), height=835 ,width=835,scrolling=True)
                

        with st.container():
            st.header("Water Difference ")
            x,y = st.columns(2)
            with x:
                st.write("distribution of crops over the contry in origenal: ")
                st.write("values of water")

                fig = px.treemap(s_solutionO, path=['government_name', 'crop_name', 'crop_footprint_m3'],
                        values='crop_footprint_m3',
                        color='crop_footprint_m3')
        
                st.plotly_chart(fig)
            with y:
                st.write("distribution of crops over the contry in sol: "+str(select_S))
                
                st.write("values of water")
                fig = px.treemap(s_solution, path=['city', 'name', 'water'],
                                values='water',
                                color='water')
                
                st.plotly_chart(fig)




# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        with st.container():
            st.header("Production Difference ")
            x,y = st.columns(2)
            with x:
                st.write("distribution of crops over the contry in origenal: ")
                st.write("values of production")

                fig = px.treemap(s_solutionO, path=['government_name', 'crop_name', 'Prod'],
                        values='Prod',
                        color='Prod')
        
                st.plotly_chart(fig)
            with y:
                st.write("distribution of crops over the contry in sol: "+str(select_S))
                
                st.write("values of production")
                fig = px.treemap(s_solution, path=['city', 'name', 'prod'],
                                values='prod',
                                color='prod')
                
                st.plotly_chart(fig)
        s_solutiona = pd.read_csv('output\\summer\\final_table_numeric.csv',skip_blank_lines=True, na_filter=True)
    
        s_solutiona=s_solutiona.dropna()

        original=s_solutiona.loc[s_solutiona['sol_index']=='orginal']
        sol=s_solutiona.loc[s_solutiona['sol_index']==str(select_S)]
        
        df = original.append(sol)
        
        st.dataframe(df)
        st.write("distribution of crops over the contry in sol: "+str(select_S))
        st.dataframe(s_solution)
        st.write("distribution of crops over the contry in origenal ")
        st.dataframe(s_solutionO)
        
        






