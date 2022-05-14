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
    if not press_button:
        st.subheader('Winter Data')
        st.header('Compare Solution')
        st.subheader('Select')

        df1 = pd.read_csv('output/winter/summary_to_power_pi.csv',skip_blank_lines=True, na_filter=True)
        df2 = pd.read_csv('output/winter/final_table_percentage.csv',skip_blank_lines=True, na_filter=True)
        df3 = pd.read_csv('output/winter/summary.csv',skip_blank_lines=True, na_filter=True)

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
        select_W_S = st.selectbox('Select Water Saturation',merged_table1['value'].drop_duplicates().sort_values( ascending=True))
        print(select_W_S)
        if int(select_W_S) == 75:
            st.write('75-80')
        elif int(select_W_S) == 80:
            st.write('80-85')
        elif int(select_W_S) == 85:
            st.write('85-90')
        elif int(select_W_S) == 90:
            st.write('90-95')
        elif int(select_W_S) == 95:
            st.write('95-100')
        else:
            st.write('less than 70')


# .sort_values( ascending=True)
        xlen = len(merged_table1.loc[merged_table1['value']==select_W_S])
        st.write("you have "+str(int(xlen/16)) +" solutions")
        # print(totalData)
        solutions = merged_table2.loc[merged_table2['value']==select_W_S]

        solutions = solutions[['sol_index','Water','Area','Production','city skip','Total','value']]
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
        dd['Area_def'] = (dd["Area_y"] - dd["Area_x"])

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


        with st.container():
            st.header("Area Difference ")
            x,y = st.columns(2)
            with x:
                st.write("Orginal ="+str(numerize.numerize(int(totalWaterO['Area'])))+'fetdan')
            with y:
                st.write("Solution "+str(select_S)+" ="+str(numerize.numerize(int(totalWaterS['Area'])))+'fetdan')

        st.write("Difference "+str(select_S)+" ="+str(   numerize.numerize(int(totalWaterS['Area'])-int(totalWaterO['Area'])))+'fetdan')
        defrance(sol["Crop_Name"],sol["Area"],select_S,"Compare Production ","Area")
        chart(dd,dd["Area_def"],select_S,"Area_def")


    # # ================Graph================ 
    # ==================Graph================






        if select_S != "Orginal":
                
            s_solution = pd.read_csv('output/winter/crops_solution_'+str(select_S)+'.csv',skip_blank_lines=True, na_filter=True)

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
            s_solutionO = s_solutionO[s_solutionO['Area'] > 1]
            
            s_solutionO=s_solutionO.loc[s_solutionO['season']=='Winter']



            
            st.header("Crop Distriution")
            

            st.write("distribution of crops over the contry in origenal: ")
            G =  nx.MultiGraph()
            city = s_solutionO['government_name']
            city = city.drop_duplicates()
            for  row in city:
                    G.add_edge('Egypt',row)
                    for index, rowi in s_solutionO.iterrows():
                        if row == rowi['government_name']:
                            G.add_edge(rowi['government_name'],str(rowi['crop_name']+" :"+rowi['government_name']))

            # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
            # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

                # Initiate PyVis network object
            drug_net = Network(height='1050px', width='1050px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=1835 ,width=1835,scrolling=True)

        
        
        
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
            drug_net = Network(height='1050px', width='1050px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=1835 ,width=1835,scrolling=True)
#==============*******************************************************************
            
            selectx = st.selectbox('Select Crop',s_solution['name'].drop_duplicates())
            G =  nx.MultiGraph()
            
            city = s_solution['city']
            city = city.drop_duplicates()
            
            
            for index, rowi in s_solution.iterrows():
                if selectx == rowi['name']:
                    G.add_edge(str(rowi['name']),rowi['city'])

            # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
            # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

                # Initiate PyVis network object
            drug_net = Network(height='500px', width='500px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=600 ,width=600,scrolling=True)
            
                    

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
            s_solutiona = pd.read_csv('output/winter/final_table_numeric.csv',skip_blank_lines=True, na_filter=True)
        
            s_solutiona=s_solutiona.dropna()

            original=s_solutiona.loc[s_solutiona['sol_index']=='orginal']
            sol=s_solutiona.loc[s_solutiona['sol_index']==str(select_S)]
            
            df = original.append(sol)
            
            st.dataframe(df)
            st.write("distribution of crops over the contry in sol: "+str(select_S))
            st.dataframe(s_solution)
            st.write("distribution of crops over the contry in origenal ")
            st.dataframe(s_solutionO)
            # ==================================================================================
        print(dd)

        def difect(row):
            if row['Production_def'] <0 :
                difect = row['Production_def']*row['Water_AVG']*-1
                return int(difect)
            else:
                
                return int(0)


        def increaseArea(row):
            if row['Production_def'] <0 :
            
                return int(0)
            else:
                
                difect = row['Production_def']*row['Area_AVG']
                return int(difect)
        def increase(row):
            if row['Production_def'] <0 :
            
                return int(0)
            else:
                
                difect = row['Production_def']*row['Water_AVG']
                return int(difect)
        def difectArea(row):
            if row['Production_def'] <0 :
                difect = row['Production_def']*row['Area_AVG']*-1
                return int(difect)
            else:
                difect = row['Production_def']*row['Area_AVG']*-1
                return int(0)
        dd['Water_AVG'] = (dd["Water_y"] / dd["Production_y"])
        dd['Area_AVG'] = (dd["Area_y"] / dd["Production_y"])
        # dd['Water_AVGO'] = (dd["Water_x"] / dd["Production_x"])
        # dd['Area_AVGO'] = (dd["Area_x"] / dd["Production_x"])

        dd['water_defict'] = dd.apply(lambda row: difect(row), axis=1)
        dd['Area_defict'] = dd.apply(lambda row: difectArea(row), axis=1)


        dd['water_increase'] = dd.apply(lambda row: increase(row), axis=1)
        dd['Area_increase'] = dd.apply(lambda row: increaseArea(row), axis=1)
        st.subheader('All Data')
        st.dataframe(dd)

        sumWater = dd['water_defict'].sum()   
        sumArea = dd['Area_defict'].sum() 

        WaterIncrease = dd['water_increase'].sum()   
        AreaIncrease = dd['Area_increase'].sum() 


        Waterx = dd['Water_x'].sum()   
        watery = dd['Water_y'].sum()
        water = Waterx - watery
        Areax = dd['Area_x'].sum()   
        Areay = dd['Area_y'].sum()
        area = Areax - Areay
        st.write("sum of water needed in defict "+str(numerize.numerize(int(sumWater)))+" ========= sum of Area needed in defict "+str(numerize.numerize(int(sumArea))))

        st.write(" sum of water saved  "+str(numerize.numerize(int(water)))+" ========= sum of Area saved "+str(numerize.numerize(int(area)))) 
        subWater = water - sumWater
        subArea = area - sumArea
        
        st.write(" sum of water satsfied  "+str(numerize.numerize(int(subWater)))+" ========= sum of Area satsfied "+str(numerize.numerize(int(subArea)))) 
        
        if subWater >=0 and subArea >=0:
            st.write('Allowed')
        else:
            st.write('Not Allowed')
        
        st.write(" sum of water used  "+str(numerize.numerize(int(WaterIncrease)))+" ========= sum of Area used "+str(numerize.numerize(int(AreaIncrease)))) 

        dfDetail = pd.read_csv('output//winter//final_table_details_numeric.csv',skip_blank_lines=True, na_filter=True)

        solD =dfDetail.loc[dfDetail['sol_index'] =='Solution '+select_S]
        solD =solD.loc[solD['Labels'] =='Area']
        

        originalD =dfDetail.loc[dfDetail['sol_index'] =="Orginal"]  
        originalD =originalD.loc[originalD['Labels'] =='Area']

        originalD['sum_x']=originalD.sum(axis=1)
        solD['sum_y']=solD.sum(axis=1)
        
        merged_table2 = pd.merge(originalD, solD, on=["City"])
        merged_table2['Area_Deff'] = merged_table2['sum_x']-merged_table2['sum_y']

        summm = merged_table2['Area_Deff'].sum()
        print(numerize.numerize(summm))
        dd = dd.loc[dd['Production_def'] <0]

        
        
        s_solutionO = pd.read_excel('data_final.xls', na_filter=True)
        s_solutionO = s_solutionO[['crop_name','season','priority']]#.drop_duplicates()
    

        s_solutionO =s_solutionO.loc[s_solutionO['season'] =="Winter"]  
        # s_solutionO = s_solutionO[['crop_name','priority']]
        merged_table1 = pd.concat([s_solutionO, dd], axis=1)
        merged_table1 = merged_table1.drop(merged_table1[merged_table1.crop_name =='X'].index)
        merged_table1 = merged_table1.drop(merged_table1[merged_table1.crop_name =='y'].index)

        xx = merged_table1[['crop_name','priority']].drop_duplicates().dropna()
        xx = xx.astype({'crop_name': 'str', 'priority': 'int'})
        xx = xx.rename({'crop_name': 'Crop_Name'}, axis='columns')
        yy = dd[['Crop_Name','Production_def','water_defict','Area_defict']]
        xx = pd.merge(xx, yy, on=["Crop_Name"])
        st.subheader('Production Defict')
        st.dataframe( xx)
        # ===============================================

        priorty = pd.read_excel('data_final.xls', na_filter=True)
        priorty = priorty[['crop_name','season','priority']]
        priorty = priorty.rename({'crop_name': 'name'}, axis='columns')
        priorty =priorty.loc[priorty['season'] =="Winter"] 
        
        df1 = pd.read_csv('sorted_winter.csv',skip_blank_lines=True, na_filter=True)
        df1 = df1.loc[df1['water'] >0]


        xxz = pd.merge(df1, priorty, on=["name"])

        xxz = xxz[['water','area','prod','city','name','Rank','priority']].drop_duplicates() 
        xxz = xxz.reset_index(drop=True)

        crop1 = st.selectbox('Select crop',xx['Crop_Name'].drop_duplicates() )
        print(crop1)
        dfyy = xxz.loc[xxz['name'] == crop1]
        st.dataframe(dfyy)
# ===============================================
        merged_table2 = merged_table2.loc[merged_table2['Area_Deff'] >=1]
        st.dataframe(merged_table2[['City','sum_x','sum_y','Area_Deff']])

# =============================summer==============================
    else:
        st.subheader('Summer Data')

               
        st.header('Compare Solution')
        st.subheader('Select')

        df1 = pd.read_csv('output/summer/summary_to_power_pi.csv',skip_blank_lines=True, na_filter=True)
        df2 = pd.read_csv('output/summer/final_table_percentage.csv',skip_blank_lines=True, na_filter=True)
        df3 = pd.read_csv('output/summer/summary.csv',skip_blank_lines=True, na_filter=True)

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
        select_W_S = st.selectbox('Select Water Saturation',merged_table1['value'].drop_duplicates().sort_values( ascending=True))
        print(select_W_S)
        if int(select_W_S) == 75:
            st.write('75-80')
        elif int(select_W_S) == 80:
            st.write('80-85')
        elif int(select_W_S) == 85:
            st.write('85-90')
        elif int(select_W_S) == 90:
            st.write('90-95')
        elif int(select_W_S) == 95:
            st.write('95-100')
        else:
            st.write('less than 70')


        xlen = len(merged_table1.loc[merged_table1['value']==select_W_S])
        st.write("you have "+str(int(xlen/16)) +" solutions")
        # print(totalData)
        solutions = merged_table2.loc[merged_table2['value']==select_W_S]

        solutions = solutions[['sol_index','Water','Area','Production','city skip','Total','value']]
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
        dd['Area_def'] = (dd["Area_y"] - dd["Area_x"])

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


        with st.container():
            st.header("Area Difference ")
            x,y = st.columns(2)
            with x:
                st.write("Orginal ="+str(numerize.numerize(int(totalWaterO['Area'])))+'fetdan')
            with y:
                st.write("Solution "+str(select_S)+" ="+str(numerize.numerize(int(totalWaterS['Area'])))+'fetdan')

        st.write("Difference "+str(select_S)+" ="+str(   numerize.numerize(int(totalWaterS['Area'])-int(totalWaterO['Area'])))+'fetdan')
        defrance(sol["Crop_Name"],sol["Area"],select_S,"Compare Production ","Area")
        chart(dd,dd["Area_def"],select_S,"Area_def")


    # # ================Graph================ 
    # ==================Graph================






        if select_S != "Orginal":
                
            s_solution = pd.read_csv('output/summer/crops_solution_'+str(select_S)+'.csv',skip_blank_lines=True, na_filter=True)

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
            s_solutionO = s_solutionO[s_solutionO['Area'] > 1]
            
            s_solutionO=s_solutionO.loc[s_solutionO['season']=='Summer']



            
            st.header("Crop Distriution")
            

            st.write("distribution of crops over the contry in origenal: ")
            G =  nx.MultiGraph()
            city = s_solutionO['government_name']
            city = city.drop_duplicates()
            for  row in city:
                    G.add_edge('Egypt',row)
                    for index, rowi in s_solutionO.iterrows():
                        if row == rowi['government_name']:
                            G.add_edge(rowi['government_name'],str(rowi['crop_name']+" :"+rowi['government_name']))

            # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
            # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

                # Initiate PyVis network object
            drug_net = Network(height='1050px', width='1050px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=1835 ,width=1835,scrolling=True)

        
        
        
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
            drug_net = Network(height='1050px', width='1050px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=1835 ,width=1835,scrolling=True)

            selectx = st.selectbox('Select Crop',s_solution['name'].drop_duplicates())
            G =  nx.MultiGraph()
            
            city = s_solution['city']
            city = city.drop_duplicates()
            
            
            for index, rowi in s_solution.iterrows():
                if selectx == rowi['name']:
                    G.add_edge(str(rowi['name']),rowi['city'])

            # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
            # nx.draw(G,pos=pos,with_labels=True,node_size=1000)

                # Initiate PyVis network object
            drug_net = Network(height='500px', width='500px',directed=True, bgcolor='#222222', font_color='white',)

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

            components.html(HtmlFile.read(), height=600 ,width=600,scrolling=True)
             
                    

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
            s_solutiona = pd.read_csv('output/summer/final_table_numeric.csv',skip_blank_lines=True, na_filter=True)
        
            s_solutiona=s_solutiona.dropna()

            original=s_solutiona.loc[s_solutiona['sol_index']=='orginal']
            sol=s_solutiona.loc[s_solutiona['sol_index']==str(select_S)]
            
            df = original.append(sol)
            
            st.dataframe(df)
            st.write("distribution of crops over the contry in sol: "+str(select_S))
            st.dataframe(s_solution)
            st.write("distribution of crops over the contry in origenal ")
            st.dataframe(s_solutionO)
            # ==================================================================================
        print(dd)

        def difect(row):
            if row['Production_def'] <0 :
                difect = row['Production_def']*row['Water_AVG']*-1
                return int(difect)
            else:
                
                return int(0)


        def increaseArea(row):
            if row['Production_def'] <0 :
            
                return int(0)
            else:
                
                difect = row['Production_def']*row['Area_AVG']
                return int(difect)
        def increase(row):
            if row['Production_def'] <0 :
            
                return int(0)
            else:
                
                difect = row['Production_def']*row['Water_AVG']
                return int(difect)
        def difectArea(row):
            if row['Production_def'] <0 :
                difect = row['Production_def']*row['Area_AVG']*-1
                return int(difect)
            else:
                difect = row['Production_def']*row['Area_AVG']*-1
                return int(0)
        dd['Water_AVG'] = (dd["Water_y"] / dd["Production_y"])
        dd['Area_AVG'] = (dd["Area_y"] / dd["Production_y"])
        # dd['Water_AVGO'] = (dd["Water_x"] / dd["Production_x"])
        # dd['Area_AVGO'] = (dd["Area_x"] / dd["Production_x"])

        dd['water_defict'] = dd.apply(lambda row: difect(row), axis=1)
        dd['Area_defict'] = dd.apply(lambda row: difectArea(row), axis=1)


        dd['water_increase'] = dd.apply(lambda row: increase(row), axis=1)
        dd['Area_increase'] = dd.apply(lambda row: increaseArea(row), axis=1)
        st.subheader('All Data')
        st.dataframe(dd)

        sumWater = dd['water_defict'].sum()   
        sumArea = dd['Area_defict'].sum() 

        WaterIncrease = dd['water_increase'].sum()   
        AreaIncrease = dd['Area_increase'].sum() 


        Waterx = dd['Water_x'].sum()   
        watery = dd['Water_y'].sum()
        water = Waterx - watery
        Areax = dd['Area_x'].sum()   
        Areay = dd['Area_y'].sum()
        area = Areax - Areay
        st.write("sum of water needed in defict "+str(numerize.numerize(int(sumWater)))+" ========= sum of Area needed in defict "+str(numerize.numerize(int(sumArea))))

        st.write(" sum of water saved  "+str(numerize.numerize(int(water)))+" ========= sum of Area saved "+str(numerize.numerize(int(area)))) 
        
        subWater = water - sumWater
        subArea = area - sumArea

        st.write(" sum of water satsfied  "+str(numerize.numerize(int(subWater)))+" ========= sum of Area satsfied "+str(numerize.numerize(int(subArea)))) 
        if subWater >=0 and subArea >=0:
            st.write('Allowed')
        else:
            st.write('Not Allowed')
        
        st.write(" sum of water used  "+str(numerize.numerize(int(WaterIncrease)))+" ========= sum of Area used "+str(numerize.numerize(int(AreaIncrease)))) 

        dfDetail = pd.read_csv('output/summer/final_table_details_numeric.csv',skip_blank_lines=True, na_filter=True)

        solD =dfDetail.loc[dfDetail['sol_index'] =='Solution '+select_S]
        solD =solD.loc[solD['Labels'] =='Area']
        

        originalD =dfDetail.loc[dfDetail['sol_index'] =="Orginal"]  
        originalD =originalD.loc[originalD['Labels'] =='Area']

        originalD['sum_x']=originalD.sum(axis=1)
        solD['sum_y']=solD.sum(axis=1)
        
        merged_table2 = pd.merge(originalD, solD, on=["City"])
        merged_table2['Area_Deff'] = merged_table2['sum_x']-merged_table2['sum_y']

        summm = merged_table2['Area_Deff'].sum()
        print(numerize.numerize(summm))
        dd = dd.loc[dd['Production_def'] <0]

        
        
        s_solutionO = pd.read_excel('data_final.xls', na_filter=True)
        s_solutionO = s_solutionO[['crop_name','season','priority']]#.drop_duplicates()
    

        s_solutionO =s_solutionO.loc[s_solutionO['season'] =="Summer"]  
        # s_solutionO = s_solutionO[['crop_name','priority']]
        merged_table1 = pd.concat([s_solutionO, dd], axis=1)
        merged_table1 = merged_table1.drop(merged_table1[merged_table1.crop_name =='X'].index)
        merged_table1 = merged_table1.drop(merged_table1[merged_table1.crop_name =='y'].index)

        xx = merged_table1[['crop_name','priority']].drop_duplicates().dropna()
        xx = xx.astype({'crop_name': 'str', 'priority': 'int'})
        xx = xx.rename({'crop_name': 'Crop_Name'}, axis='columns')
        yy = dd[['Crop_Name','Production_def','water_defict','Area_defict']]
        xx = pd.merge(xx, yy, on=["Crop_Name"])
        st.subheader('Production Defict')
        st.dataframe( xx)
        # ===============================================

        priorty = pd.read_excel('data_final.xls', na_filter=True)
        priorty = priorty[['crop_name','season','priority']]
        priorty = priorty.rename({'crop_name': 'name'}, axis='columns')
        priorty =priorty.loc[priorty['season'] =="Summer"] 
        
        df1 = pd.read_csv('sorted_Summer.csv',skip_blank_lines=True, na_filter=True)
        df1 = df1.loc[df1['water'] >0]


        xxz = pd.merge(df1, priorty, on=["name"])

        xxz = xxz[['water','area','prod','city','name','Rank','priority']].drop_duplicates() 
        xxz = xxz.reset_index(drop=True)

        crop1 = st.selectbox('Select crop',xx['Crop_Name'].drop_duplicates() )
        print(crop1)
        dfyy = xxz.loc[xxz['name'] == crop1]
        st.dataframe(dfyy)
# ===============================================
        merged_table2 = merged_table2.loc[merged_table2['Area_Deff'] >=1]
        st.dataframe(merged_table2[['City','sum_x','sum_y','Area_Deff']])

        st.dataframe( s_solution)



        
        
        










    