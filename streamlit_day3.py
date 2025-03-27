import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import seaborn as sns

st.header('st.button')

if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')
    
    
#create a Dataframe and calculate the probabilities of dice rolls
dice_df = pd.DataFrame({
    'roll': [1, 2, 3, 4, 5, 6],
    'probability': [1/6] * 6
})

st.write(dice_df)
Iterations : int = 100000

#simulate dice rolls
dice_roll1 : np.ndarray = np.random.randint(1, 7, Iterations)
dice_roll2 : np.ndarray = np.random.randint(1, 7, Iterations)

dice_roll_df : pd.DataFrame = pd.DataFrame({
    'roll1': dice_roll1,
    'roll2': dice_roll2,
    'sum': dice_roll1 + dice_roll2
})

#count the number of times each sum occurs
sum_counts = dice_roll_df['sum'].value_counts().sort_index()
#now we can calculate the probability of each sum
sum_counts = sum_counts.reset_index()
st.write(sum_counts)
sum_counts.columns = ['sum', 'count']
sum_counts['probability'] = sum_counts['count'] / sum_counts['count'].sum() * 100


#st.write(dice_roll_df)
st.write(sum_counts)
#plot a graph of the probabilities in relation to the sum of the dice rolls
fig = px.bar(sum_counts, x='sum', y='probability', text='probability')
st.plotly_chart(fig)

fig2 = px.histogram(sum_counts, x='sum', y='probability', histfunc='sum', nbins=11)
st.plotly_chart(fig2)

fig2 = ff.create_distplot([sum_counts['sum'], sum_counts['probability']], group_labels=['sum', 'probability'])
st.plotly_chart(fig2)

plot = sns.histplot(sum_counts, x='sum', y='probability', bins=11, kde=True)
st.pyplot(plot.figure)

