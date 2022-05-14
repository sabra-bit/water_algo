from operator import index
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import os
import streamlit as st
from numerize import numerize


# crop =crop.loc[crop['season'] =="Winter"] 




crop = pd.read_excel('data_reset.xls')
# crop =crop.loc[crop['season'] =="Winter"] 

xx = crop[['crop_name','priority']].drop_duplicates().dropna()
st.dataframe(crop)
cropx = st.selectbox('Select crop',xx['crop_name'].drop_duplicates() )
with st.form(key="formTest"):
   

    v1 =xx.loc[xx['crop_name'] ==cropx] 
    v1 =v1.iloc[0]['priority']
    n1 = st.slider(cropx,min_value=1,max_value=16 , value=int(v1))
    ss= st.form_submit_button()

if ss:
    crop.loc[crop['crop_name'] == cropx, 'priority'] = float(n1)


    datatoexcel = pd.ExcelWriter('data_final.xls')
  
    # write DataFrame to excel
    crop.to_excel(datatoexcel,index=False)
    
    # save the excel
    datatoexcel.save()
    # crop.to_excel("data_final.xls" ,index=False)
    st.write("updated")
# xx = crop[['crop_name','priority']].drop_duplicates().dropna()
# st.dataframe(crop)
# with st.form(key="formTest"):
#    ]
#     n1 = st.slider("Wheat",min_value=1,max_value=16 

#     v1 =xx.loc[xx['crop_name'] =="Barley"] 
#     v1=v1.iloc[0]['priority']
#     n2 = st.slider("Barley",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Forestation Alfalfa"] 
#     v1=v1.iloc[0]['priority']
#     n3 = st.slider("Forestation Alfalfa",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Sustains Alfalfa"] 
#     v1=v1.iloc[0]['priority']
#     n4 = st.slider("Sustains Alfalfa",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="vegetables"] 
#     v1=v1.iloc[0]['priority']
#     n5 = st.slider("vegetables",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Medical and Aromatic plants"] 
#     v1=v1.iloc[0]['priority']
#     n6 = st.slider("Medical and Aromatic plants",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="fully grown Beans"] 
#     v1=v1.iloc[0]['priority']
#     n7 = st.slider("fully grown Beans",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="lentils"] 
#     v1=v1.iloc[0]['priority']
#     n8 = st.slider("lentils",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Fenugreek"] 
#     v1=v1.iloc[0]['priority']
#     n9 = st.slider("Fenugreek",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="chickpeas"] 
#     v1=v1.iloc[0]['priority']
#     n10 = st.slider("chickpeas",min_value=1,max_value=16 ,value=int(v1))


#     v1 =xx.loc[xx['crop_name'] =="Lupine"] 
#     v1=v1.iloc[0]['priority']
#     n11 = st.slider("Lupine",min_value=1,max_value=16 ,value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="sugar Beet"] 
#     v1=v1.iloc[0]['priority']
#     n12 = st.slider("sugar Beet",min_value=1,max_value=16 , value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Fully grown Onions"] 
#     v1=v1.iloc[0]['priority']
#     n13 = st.slider("Fully grown Onions",min_value=1,max_value=16 ,  value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Garlic"] 
#     v1=v1.iloc[0]['priority']
#     n14 = st.slider("Garlic",min_value=1,max_value=16 ,  value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Lfax"] 
#     v1=v1.iloc[0]['priority']
#     n15 = st.slider("Lfax",min_value=1,max_value=16 ,  value=int(v1))

#     v1 =xx.loc[xx['crop_name'] =="Others"] 
#     v1=v1.iloc[0]['priority']
#     n16 = st.slider("Others",min_value=1,max_value=16 , value=int(v1))
    
    
    
#     sbmb = st.form_submit_button(label="set value")

# print()
# crop.loc[crop['crop_name'] == 'Wheat', 'priority'] = float(n1)
# crop.loc[crop['crop_name'] == 'Barley', 'priority'] = float(n2)
# crop.loc[crop['crop_name'] == 'Forestation Alfalfa', 'priority'] = float(n3)
# crop.loc[crop['crop_name'] == 'Sustains Alfalfa', 'priority'] = float(n4)
# crop.loc[crop['crop_name'] == 'vegetables', 'priority'] = float(n5)
# crop.loc[crop['crop_name'] == 'Medical and Aromatic plants', 'priority'] = float(n6)
# crop.loc[crop['crop_name'] == 'fully grown Beans', 'priority'] = float(n7)
# crop.loc[crop['crop_name'] == 'lentils', 'priority'] = float(n8)
# crop.loc[crop['crop_name'] == 'Fenugreek', 'priority'] = float(n9)
# crop.loc[crop['crop_name'] == 'chickpeas', 'priority'] = float(n10)
# crop.loc[crop['crop_name'] == 'Lupine', 'priority'] = float(n11)
# crop.loc[crop['crop_name'] == 'sugar Beet', 'priority'] = float(n12)
# crop.loc[crop['crop_name'] == 'Fully grown Onions', 'priority'] = float(n13)
# crop.loc[crop['crop_name'] == 'Garlic', 'priority'] = float(n14)
# crop.loc[crop['crop_name'] == 'Lfax', 'priority'] = float(n15)
# crop.loc[crop['crop_name'] == 'Others', 'priority'] = float(n16)
# st.dataframe(crop)


#


# # df1 = pd.read_csv('output/winter/summary_to_power_pi.csv',skip_blank_lines=True, na_filter=True)
# # df1 = df1['sol_index']
# # df1 = df1.astype(str)
# # df1 = df1.drop_duplicates()


# # st.header('Compare Solution')
# # st.subheader('Select')

# # select_S = st.selectbox('select solution',df1) 




# # if select_S != "Orginal":
        
# #     s_solution = pd.read_csv('output/winter/crops_solution_'+str(select_S)+'.csv',skip_blank_lines=True, na_filter=True)

# #     st.write("distribution of crops over the contry in sol: "+str(select_S))
    
# #     # .drop_duplicates()
# #     s_solution = s_solution[['water','area','prod','city','name']]
    
# #     s_solution=s_solution.dropna()
# #     s_solution=s_solution.replace(0, 1)
# #     s_solution = s_solution.drop(s_solution[s_solution.water ==1].index)
# #     print(s_solution)
# #     G =  nx.DiGraph()
# #     city = s_solution['city']
# #     city = city.drop_duplicates()
# #     for  row in city:
# #         G.add_edge('Egypt',row[:4])

# #     pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
# #     nx.draw(G,pos=pos,with_labels=True,node_size=1000)
# #     plt.show()
#     # st.plotly_chart(plt.show())
#     # st.plotly_chart(dd)
#     # for index, rowi in s_solution.iterrows():
#     #     if row == rowi['city']:
#     #         G.add_edge(rowi['city'][:4],rowi['name'][:4])
#     #         G.add_edge(rowi['name'][:4],numerize.numerize(int(rowi['water'])))




# s_solution =  pd.read_excel("city.xlsx",sheet_name="crop")
# sisson =  pd.read_excel("city.xlsx",sheet_name="region")

# sisson = sisson[['city','region_name']]


# sisson = sisson.drop_duplicates()


# print(sisson)


# s_solution=s_solution.dropna()
# s_solution=s_solution.replace(0, 1)
# s_solution = s_solution.drop(s_solution[s_solution.water ==1].index)


# cs_solution = s_solution['city']


# cs_solution =cs_solution.drop_duplicates()

# s_solution= s_solution.drop_duplicates()

# merged = pd.merge(s_solution, sisson, on=["city"])

# merged = merged.loc[merged['region_name']=="Middle Egypt"]
# merged = merged['city']
# merged=merged.drop_duplicates()
# print(merged)
# plt.figure(figsize=(20,10))
# G =  nx.MultiGraph()
# for  row in merged:
#     G.add_edge('Middle Egypt',row[:4])
#     for index, rowi in s_solution.iterrows():
#         if row == rowi['city']:
#             G.add_edge(rowi['city'][:4],rowi['name'][:4])
           


# pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
# nx.draw(G,pos=pos,with_labels=True,node_size=1000)
# plt.show()