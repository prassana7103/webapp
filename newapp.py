import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Constants
DATA_FILE = 'data.csv'

# Load existing data from CSV if it exists
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.session_state['months'] = df['Month'].tolist()
    st.session_state['values'] = df['Value'].tolist()
else:
    df = pd.DataFrame(columns=['Month', 'Value'])
    st.session_state['months'] = []
    st.session_state['values'] = []

# Streamlit title
st.title('Interactive Line Graph')

# User inputs for months and values
st.write('## Enter Data for the Graph')

# Input fields
month = st.text_input('Month (e.g., Jan, Feb, Mar, etc.)')
value = st.number_input('Value', min_value=0, value=0)

# Add button
if st.button('Add Data'):
    if month and value is not None:
        st.session_state['months'].append(month)
        st.session_state['values'].append(value)
        # Update the DataFrame
        df = pd.DataFrame({
            'Month': st.session_state['months'],
            'Value': st.session_state['values']
        })
        # Save to CSV
        df.to_csv(DATA_FILE, index=False)

# Remove data section
st.write('## Remove Data from the Graph')

if st.session_state['months']:
    selected_entry = st.selectbox(
        'Select entry to remove', 
        [f'{m}: {v}' for m, v in zip(st.session_state['months'], st.session_state['values'])]
    )

    if st.button('Remove Selected Data'):
        index_to_remove = st.session_state['months'].index(selected_entry.split(':')[0])
        st.session_state['months'].pop(index_to_remove)
        st.session_state['values'].pop(index_to_remove)
        # Update the DataFrame
        df = pd.DataFrame({
            'Month': st.session_state['months'],
            'Value': st.session_state['values']
        })
        # Save to CSV
        df.to_csv(DATA_FILE, index=False)

# Display the data
st.write('## Sample Data', df)

# Plotting the data if there is any
if not df.empty:
    fig, ax = plt.subplots()
    ax.plot(df['Month'], df['Value'], marker='o')
    ax.set_title('Monthly Values')
    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    st.pyplot(fig)
else:
    st.write('No data to display. Please add some data.')
