import re

# Streamlit title
st.title("Mazaltov, you've found the test printing")

test_subject = "Admin: A league match was played between MikeHagg (4 3 6.741 2.532) and NickBG (1 3 15.054 1.035) on Heroes!"

# Adjusted regex to match the format correctly
test_match = re.search(r"\(([^)]+)\)\s*and\s*\(([^)]+)\)", test_subject)

if test_match:
    test_player_1_values = test_match.group(1)  # Values for Player 1
    test_player_2_values = test_match.group(2)  # Values for Player 2
    
    print(f"Player 1 values: {test_player_1_values}")
    print(f"Player 2 values: {test_player_2_values}")
else:
    print("No match found.")

