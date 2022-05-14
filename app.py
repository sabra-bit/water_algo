import main 

import Tool_refactor_main_3 
import best_country 

import streamlit as st
st.set_page_config(layout="wide")
PAGES = {
    
    "Calculate": Tool_refactor_main_3,
    "Dash Board" :best_country,
    
    "Rusult ": main,
   
    
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

page.app()

