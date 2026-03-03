import streamlit as st
from langchain_helper import *

st.title("Restaurant_Name_Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine" , ("Indian","Italian","Mexican","Chinese","Arabic"))


if cuisine:
    response = get_restaurant_name_and_items(cuisine)
    lines = response.strip().split("\n")
    restaurant_name = lines[0]
    st.header(restaurant_name)
    food_items = [item.strip() for item in lines[1].split(",")]
    st.write("Menu Items")
    for item in food_items:
        st.write("-" , item)
        
    
