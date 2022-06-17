import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

#create function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
#take the json version of the response and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)
my_fruit_list= my_fruit_list.set_index('Fruit')

#list so clients can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display table on page
streamlit.dataframe(my_fruit_list)

streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error('Please sleect a fruit to display information')
  else:
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
  
streamlit.stop()

def insert_row_snowflake(new_fruit): 
    with my_cnx.cursor() as my_cur: 
        my_cur.execute("insert into fruit_load_list values ('from streamlit')") 
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?') 

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
        return "Thanks for adding" + new_fruit
fruit_choice = streamlit.text_input('What fruit would you like to add?', 'Fruit here')

if streamlit.button('Add a Fruit to the List'): 
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
    back_from_function = insert_row_snowflake(add_my_fruit) 	
    streamlit.text(back_from_function)
    

#streamlit.write('The user entered',fruit_choice)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')");
