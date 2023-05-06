"""
Programmer: David Evans
CS230: Jennifer Xu
Data Set: United States Cities

Description: This program summarizes necessary information a person would need to know
when learning more about cities and states that would best suite there preferences utilizing visuals
and features that help illustrate this data in a concise and easily understood manner.

Extra Credit
Streamlit Cloud Link:
"""

import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

st.title("The Great Cities and States of America")
st.write("Hello friend! This website will provide you with important information, regarding cities and states across America, to assit you in determing where you would like to move or visit.")
from PIL import Image
image = Image.open('states_pic.png')
st.image(image, caption= 'American States')

st.write("\n\n")

st.subheader("Looking for a Consultation 🤔")

first_name = st.text_input('Enter your first name')
last_name = st.text_input('Enter your last name')
email = st.text_input('Enter your email')

if first_name and last_name and email != '':
    with open('consultation.py', 'a') as f:
        f.writelines(f'{first_name},{last_name},{email}, \n')
st.write(f'Thank you {first_name} {last_name} for submitting your contact information')

st.button("Submit")

def read_data():
    return pd.read_csv("uscities.csv").set_index("id")

st.write("#")

#Pivot Table
def make_pivot():
    st.subheader("City & State Attributes")
    df = read_data()
    columns = ['city','state_name','population','density','ranking']
    pivot_table = pd.pivot_table(df[columns], index=['ranking','city', 'state_name'])
    st.write(pivot_table)
    st.markdown("*With a ranking of 1 representing 'popular location' any person looking for a new adventure will love these destinations. Often being highly populated, prepare to meet tons of new folxs and rejuvinize your social life. Nevertheless, if you are more of a reserved person, you may feel more at home at a location ranked 3 or higher.*")

make_pivot()

from PIL import Image
image = Image.open('travel_pic.png')
st.image(image, caption= 'Travelling the States')

#Default Values
default_states = ["New York", "California", "Massachusetts", "Texas"]
default_population = 100000
default_ranking = 3

def all_states():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['state_name'] not in lst:
            lst.append(row['state_name'])

    return lst

#filter data
def filter_data(sel_state, high_population, high_rank):
    df = read_data()
    df = df.loc[df['state_name'].isin(sel_state)]
    df = df.loc[df['population'] > high_population]
    df = df.loc[df['ranking'] < high_rank]


    st.pyplot(plt)

#bar chart
def state_pop(df):
    population = [row['population'] for ind, row in df.iterrows()]
    state_name = [row['state_name'] for ind, row in df.iterrows()]

    dict = {}
    for state_name in state_name:
        dict[state_name] = []
    for i in range(len(population)):
        dict[state_name[i]].append(population[i])

    return dict

#dictonary averages
def state_name_avg(dict_population):
    dict = {}
    for key in dict_population.keys():
        dict[key] = np.mean(dict_population[key])

    return(dict)

#bar chart #1
def make_bar(dict_averages):
    plt.figure()
    x = dict_averages.keys()
    y = dict_averages.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.title(f"Average population for States: {', '.join(dict_averages.keys())}")
    plt.xlabel("State Name")
    plt.ylabel("Population")
    return plt

#barchart#2
def make_barchart():
    st.title("Population by City")
    df = pd.read_csv('uscities.csv')
    cities = df['city']
    plt.bar(cities, df['population'], align="center", alpha=0.5)
    plt.ylabel("Population")
    plt.xlabel("Cities")
    plt.title("Cities by Population")
    plt.xticks(rotation=45)
    return plt

#map
def make_map(df):
    if df is not None:
        map_df = df.filter(['city', 'state_name', 'lat', 'lng'])

    view_state = pdk.ViewState(latitude=map_df['lat'].mean(),
                               longitude=map_df['lng'].mean(),
                               zoom=10)
    layer = pdk.layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[lng, lat]',
                      get_radius = 500,
                      get_color = [70, 52, 235],
                      pickable=True)

    tool_tip = {'html': 'City&State:<br><b>{city},{state}</b>',
                'style': {'backgroundColor':'steelblue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state,
                   layers=[layer],
                   tooltip=tool_tip)

    map.to_html()
    st.pydeck_chart(map)

#count the frequency of states
def count_states(state_names, df):
    lst = [df.loc[df['state_name'].isin([state_name])].shape[0] for state_name in default_states]
    return lst

#pie chart
def make_pie(counts, sel_state):
    plt.figure()
    explodes = [0 for i in range(len(counts))]
    maximum = counts.index(np.max(counts))
    explodes[maximum] = .20

    plt.pie(counts, labels=sel_state, explode=explodes, autopct = "%.2f")
    plt.title(f" Comparison of State size according to respective number of cities: {', '.join(sel_state)}")
    return plt

def main():
    # Sidebar Widget
    st.sidebar.title("Welcome!")
    st.sidebar.write("Please select an option to display the data" )
    states = st.sidebar.multiselect("Select a state: ", all_states())
    population = st.sidebar.slider("Max population: ", 1, 18975000)
    ranking = st.sidebar.slider("Ranking (1=high | 5=low): ", 1,5)

    data = filter_data(states, population, ranking)
    series = count_states(states, data)

    if len(states) > 0 and population > 0 and ranking > 0:
        st.write("View map of states and their information")
        make_map(data)

        st.write("View Pie Chart")
        st.pyplot(make_pie(series, states))

        st.write("View Bar Chart")
        st.pyplot(make_bar(series, states))

        st.write("Bar: Chart Population by City")
        st.pyplot(make_barchart())

main()

