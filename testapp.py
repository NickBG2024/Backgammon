import streamlit as st
import re
import sqlite3

# Function to create/connect to an SQLite database and table
def create_connection():
    conn = sqlite3.connect("backgammon_matches.db")  # Creates the database file if it doesn't exist
    cursor = conn.cursor()
    
    # Create table for storing match results if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS matches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player_1_points REAL,
                        player_1_length REAL,
                        player_1_pr REAL,
                        player_1_luck REAL,
                        player_2_points REAL,
                        player_2_length REAL,
                        player_2_pr REAL,
                        player_2_luck REAL
                    )''')
    conn.commit()
    return conn

# Function to insert data into the database
def insert_match(conn, p1_stats, p2_stats):
    cursor = conn.cursor()
    
    # Insert match values into the database
    cursor.execute('''INSERT INTO matches 
                      (player_1_points, player_1_length, player_1_pr, player_1_luck,
                       player_2_points, player_2_length, player_2_pr, player_2_luck)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (p1_stats[0], p1_stats[1], p1_stats[2], p1_stats[3],
                       p2_stats[0], p2_stats[1], p2_stats[2], p2_stats[3]))
    
    conn.commit()

# Connect to the database and create table if it doesn't exist
conn = create_connection()

# Sample email subject for testing purposes
subject = "Admin: A league match was played between Rambizzle (3 3 2.541 -1.532) and NickBG (0 3 7.051 0.035) on Heroes!"

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
    player_1_stats = player_1_values.split()  # ['4', '3', '6.741', '2.532']
    player_2_stats = player_2_values.split()  # ['1', '3', '15.054', '1.035']

    # Display the extracted data in the Streamlit app
    st.write(f"Player 1 values: {player_1_stats}")
    st.write(f"Player 2 values: {player_2_stats}")

    # Insert the extracted values into the database
    insert_match(conn, player_1_stats, player_2_stats)
    
    st.success("Match data has been saved to the database!")
else:
    st.write("No match found.")
