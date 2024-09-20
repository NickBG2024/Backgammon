import re
import streamlit as st

# Streamlit title
st.title("Mazaltov, you've found the test printing")

subject = "Admin: A league match was played between MikeHagg (4 3 6.741 2.532) and NickBG (1 3 15.054 1.035) on Heroes!"

# Adjusted regex to match the format correctly
match = re.search(r"\(([^)]+)\)\s*and\s*\(([^)]+)\)", subject)

if match:
    player_1_values = match.group(1)  # Values for Player 1
    player_2_values = match.group(2)  # Values for Player 2
    
    # You can split the values inside the parentheses if you want to extract individual numbers
    player_1_stats = player_1_values.split()  # ['4', '3', '6.741', '2.532']
    player_2_stats = player_2_values.split()  # ['1', '3', '15.054', '1.035']

    # Example of using this data in a dictionary
    player_data = {
        "Player 1": player_1_stats,
        "Player 2": player_2_stats,
    }
    
st.write(f"Player 1 values: {player_1_stats}")
st.write(f"Player 2 values: {player_2_stats}")
else:
    st.write("No match found.")
