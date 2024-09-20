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
    st.write("No emails found with this search term in
