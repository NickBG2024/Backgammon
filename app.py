import streamlit as st
import imaplib
import email
import re
import pandas as pd

# Streamlit title
st.title("Backgammon Match Results via Email")

# Get email credentials from Streamlit Secrets
EMAIL = st.secrets["imap"]["email"]
PASSWORD = st.secrets["imap"]["password"]

try:
    mail = imaplib.IMAP4_SSL('mail.sabga.co.za', 993)  # Update to correct server
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    st.write("Login successful")
except imaplib.IMAP4.error as e:
    st.error(f"IMAP login failed: {str(e)}")
    
# Connect to custom email
mail = imaplib.IMAP4_SSL('mail.sabga.co.za', 993)
mail.login(EMAIL, PASSWORD)

# Select the inbox
mail.select('inbox')

# Search for emails with a specific subject
status, messages = mail.search(None, '(SUBJECT "A league match was played")')

# Get the list of email IDs
email_ids = messages[0].split()

# Initialize empty list to store match results
match_results = []

# Loop through the emails and extract data
for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    
    # Parse the email
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = msg['subject']
            
            # Use regex to extract the values in the parentheses
            match = re.search(r"\((.*?)\) and \((.*?)\)", subject)
            if match:
                player_1_values = match.group(1)  # Values for Player 1
                player_2_values = match.group(2)  # Values for Player 2
                
                # Split the values and format them into a readable structure
                match_results.append({
                    "Player 1": match.group(0).split()[0],
                    "Player 1 Values": player_1_values,
                    "Player 2": match.group(2).split()[0],
                    "Player 2 Values": player_2_values
                })

# Convert match results into a DataFrame
if match_results:
    df = pd.DataFrame(match_results)
    st.write("### Match Results Table")
    st.write(df)
else:
    st.write("No match emails found.")

# Logout from the email server
mail.logout()
