import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

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
  else
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
#take the json version of the response and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
  
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruitlist contains:")
streamlit.dataframe(my_data_rows)

#Allow end user to add a fruit
fruit_choice = streamlit.text_input('What fruit would you like to add?', 'Fruit here')
streamlit.write('The user entered',fruit_choice)
my_cur.execute("insert into fruit_load_list values ('from streamlit')");
