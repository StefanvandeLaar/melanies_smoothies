# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


# ✅ Direct converteren naar Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options") \
    .select(col('FRUIT_NAME')) \
    .to_pandas()

# ✅ Werkt nu want my_dataframe is een Pandas DataFrame
st.dataframe(data=my_dataframe, use_container_width=True)

# ✅ Werkt nu want my_dataframe is een Pandas DataFrame
fruit_list = my_dataframe['FRUIT_NAME'].tolist()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , fruit_list
    , max_selections=5
    )

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" +name_on_order + """')"""

 import requests
 smoothiefroot_response =requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
 st.text(smoothiefroot_response)
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered, '+ name_on_order+ '!', icon="✅")
