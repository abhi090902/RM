import os
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import matplotlib.pyplot as plt

# Initialize session state for the pop-up visibility
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False

# Function to load local CSV file
def load_local_csv(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

# Streamlit UI
st.title("AI Content Rating Analysis")

# Load and Handle CSV Data
csv_file_path = "RM LIVE_RM - Dec2024_Table - Sheet1.csv"  # Replace with your actual CSV file
df = load_local_csv(csv_file_path)

if df is not None:
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d %Y', errors='coerce')

    # Date Selection
    start_date_input = st.date_input("Start Date", value=df['Date'].min().date())
    end_date_input = st.date_input("End Date", value=(df['Date'].min() + timedelta(days=1)).date())

    start_date = pd.to_datetime(start_date_input)
    end_date = pd.to_datetime(end_date_input)

    # Display selected date range
    st.markdown(f"**Selected Date Range:** {start_date} to {end_date}")

    # Filter DataFrame by the date range
    df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    rating_counts = df_filtered['vSp Rating'].value_counts().sort_index()

    # Plot the ratings graph
    fig, ax = plt.subplots()
    bars = ax.bar(rating_counts.index, rating_counts.values, color='skyblue')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom', fontsize=10)

    ax.set_xlabel('vSp Rating')
    ax.set_ylabel('Count')
    ax.set_title('vSp Rating Counts')
    st.pyplot(fig)

    # Email input
    #email = st.text_input("Enter your email to receive the report")
    if st.button("Analyze"):
          # Display the predefined summary data
          st.write("Overall Summary for Dec 1 to Dec 31 Reviews")
          summary_data = {
              "Metric": [
                  "Total Reviews",
                  "NA",
                  "Correct Reviews",
                  "Overrated Reviews",
                  "2 Ratings should have been 1",
                  "4 Ratings should have been 3",
                  "Underrated Reviews",
                  "3 Ratings should have been 4"
              ],
              "Count": [
                  724,
                  3,
                  710,
                  10,
                  1,
                  9,
                  1,
                  1
              ]
          }
          st.table(pd.DataFrame(summary_data))

          # Option to download the summary as CSV
          output = StringIO()
          summary_df = pd.DataFrame(summary_data)
          summary_df.to_csv(output, index=False)
          st.download_button(
              label="Download Summary as CSV",
              data=output.getvalue(),
              file_name='summary_results.csv',
              mime='text/csv'
          )

