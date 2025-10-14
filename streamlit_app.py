# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input box for name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    #.select(col('FRUIT_NAME')) limits what is returned to specified column instead of the whole table
# st.dataframe(data=my_dataframe, use_container_width=True) # put the data in my_dataframe on the screen


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    # ["Green", "Yellow", "Red", "Blue"],   # Manually provided list
    my_dataframe,                            # my_dataframe is a list
    max_selections=5,
    # default=["Apples", "Figs"],
    # default=my_dataframe[0],
)

if ingredients_list:                        # test if ingredients_list is not null
    ingredients_string = ''
    
    # st.write("You selected:", ingredients_list)  
    # st.text(ingredients_list)   

    for fruit_chosen in ingredients_list:   # build up a string by concatenating each item in ingredients_list
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        
    # st.write(ingredients_string)  
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredients_string + "', '" + name_on_order + """')"""  # using triple double quotes to enclose multiline string          
    
    # my_insert_stmt = "insert into smoothies.public.orders(ingredients) values ('" + ingredients_string + "')"
        # Simple single line string using single double quotes
    
    # st.write(my_insert_stmt)
    # st.stop

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")


