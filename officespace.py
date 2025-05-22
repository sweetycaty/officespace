import streamlit as st
import calendar
from datetime import date

# App configuration
st.set_page_config(page_title="Office Desk Booking – May 2025", layout="wide")

st.title("📅 Office Desk Booking – May 2025")

# Configuration
month = 5
year = 2025
num_desks = 5
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# Get calendar for the month
cal = calendar.monthcalendar(year, month)

# Initialize session state for booking data
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

# Display the calendar
for week_num, week in enumerate(cal):
    cols = st.columns(7)  # 7 columns for the days of the week
    for i, day in enumerate(week):
        with cols[i]:
            i
