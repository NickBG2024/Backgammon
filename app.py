import streamlit as st
import imaplib
import email
import re

# Streamlit title
st.title("SANDBOX: Backgammon Match Details parsing, via Email - subject: Admin: A league match was played")

# Get email credentials from Streamlit Secrets
EMAIL = st.secrets["imap"]["email"]
PASSWORD = st.secrets["imap"]["password"]

# Try connecting to the email server
try:
    mail = imaplib.IMAP4_SSL('mail.sabga.co.za', 993)  # Update to correct server
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    st.write("Login successful")
except imaplib.IMAP4.error as e:
    st.error(f"IMAP login failed: {str(e)}")

# Search for emails with "Admin: A league match was played" in the subject
status, messages = mail.search(None, '(SUBJECT "Admin: A league match was played")')

# Check the number of emails found
email_ids = messages[0].split()

# Display how many emails were found
if email_ids:
    st.write(f"Found {len(email_ids)} emails with 'Admin: A league match was played' in the subject.")
else:
    st.write("No emails found with this search term in the subject.")

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
            st.write(f"Subject: {subject}")

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
            else:
                st.write("No match found in this email.")

# Logout from the email server
mail.logout()
