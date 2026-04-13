import streamlit as st
import requests  
import pandas as pd

# Connectie
cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# ✅ Gebruik pure SQL en converteer DIRECT naar Pandas
# Geen Snowpark DataFrame objecten bewaren!
fruit_df = session.sql("SELECT FRUIT_NAME FROM smoothies.public.fruit_options").to_pandas()

# Toon de dataframe
#st.dataframe(data=fruit_df, use_container_width=True)
#st.stop()

pd_df= dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

# Haal lijst op uit Pandas DataFrame
fruit_options = fruit_df['FRUIT_NAME'].tolist()

# Multiselect met gewone Python lijst
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list) + ' '
    #st.subheader(ingredients_list + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        # ✅ Gebruik ook hier pure SQL
        session.sql(
            f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
            """
        ).collect()
        
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")


