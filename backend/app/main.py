import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-18/food_consumption.csv'
food_consumption = pd.read_csv(url)

rice_consumption = food_consumption[food_consumption['food_category'] == 'Rice']


# plt.hist(rice_consumption['co2_emmission'], color='red')
# plt.show()

rice_consumption['co2_emmission'].hist(color='green')
plt.show()

rice_consumption['consumption'].hist(color='red')
plt.show()

