import streamlit as st
import re

# Sample email subject for testing purposes
subject = "Admin: A league match was played between MikeHagg (4 3 6.741 2.532) and NickBG (1 3 15.054 1.035) on Heroes!"

# Streamlit title
st.title("Backgammon Match Results")

# Print the subject to the Streamlit app for verification
st.write(f"Subject being processed: {subject}")

# Updated regex to match the format
match = re.search(r"\(([^)]+)\) and [^\(]+\(([^)]+)\)", subject)

# Check if the match was successful
if match:
    player_1_values = match.group(1)  # Values for Player 1
    player_2_values = match.group(2)  # Values for Player 2
    
    # Split the values to get individual stats
    player_1_stats = player_1_values.split()  # Example: ['4', '3', '6.741', '2.532']
    player_2_stats = player_2_values.split()  # Example: ['1', '3', '15.054', '1.035']

    # Display the extracted data in the Streamlit app
    st.write(f"Player 1 values: {player_1_stats}")
    st.write(f"Player 2 values: {player_2_stats}")
else:
    # If no match is found, output this message
    st.write("No match found.")
