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
    mail = imaplib.IMAP4_SSL('mail.sabga.co.za', 993)
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

            # Extract the sender's email address
            sender = msg['from']
            st.write(f"From: {sender}")
                    
            # Extract the recipient's email address
            recipient = msg['to']
            st.write(f"To: {recipient}")
                    
            # Extract CC if available
            cc = msg.get('cc', 'None')  # CC might not always be present
            st.write(f"Cc: {cc}")
                    
            # Extract the email's date and time
            email_date = msg['date']
            st.write(f"Date: {email_date}")
            
            # Extract the body (plain text or HTML)
            if msg.is_multipart():
              for part in msg.walk():
                  if part.get_content_type() == "text/plain":  # Extract plain text
                      body = part.get_payload(decode=True).decode('utf-8')
                      st.write(f"Body (text): {body}")
                  elif part.get_content_type() == "text/html":  # Extract HTML if needed
                      html_body = part.get_payload(decode=True).decode('utf-8')
                      st.write(f"Body (HTML): {html_body}")
            else:
            # For non-multipart messages (single-part emails)
            body = msg.get_payload(decode=True).decode('utf-8')
            st.write(f"Body: {body}")

            # Clean up subject to remove any 'Fwd:' or 'Re:' prefixes
            cleaned_subject = re.sub(r"^(Fwd:|Re:)\s*", "", subject).strip()
            st.write(f"Cleaned Subject: {repr(cleaned_subject)}")  # Debugging: Show cleaned subject line
            cleaned_subject = cleaned_subject.replace("\r\n", " ")  # Replace any \r\n with a space
            st.write(f"Cleaned Subject: {repr(cleaned_subject)}")  # Debugging line

            # Updated regex to account for spaces or newlines between the first player and the word 'and'
            match = re.search(r"\(([^)]+)\)\s*and\s*[^\(]+\(([^)]+)\)", cleaned_subject)

            # Check if the match was successful
            if match:
                st.write(f"Match found for email {email_id}")
                player_1_values = match.group(1)  # Values for Player 1
                player_2_values = match.group(2)  # Values for Player 2
    
                # Split the values to get individual stats
                player_1_stats = player_1_values.split()
                player_2_stats = player_2_values.split()

                # Display the extracted data in the Streamlit app
                st.write(f"Player 1 values: {player_1_stats}")
                st.write(f"Player 2 values: {player_2_stats}")

                # Store in match_results
                match_results.append({
                    "Player 1 Points": player_1_stats[0],
                    "Player 1 Match Length": player_1_stats[1],
                    "Player 1 PR": player_1_stats[2],
                    "Player 1 Luck": player_1_stats[3],
                    "Player 2 Points": player_2_stats[0],
                    "Player 2 Match Length": player_2_stats[1],
                    "Player 2 PR": player_2_stats[2],
                    "Player 2 Luck": player_2_stats[3]
                })
            else:
                st.write(f"No match found for email {email_id}")  # Add this check to avoid errors

# Logout from the email server
mail.logout()

# If match results were found, display them in a table
if match_results:
    st.write("Match Results:")
    st.write(match_results)
else:
    st.write("No match results were extracted.")
