import streamlit as st
import calendar
from datetime import date

# Configuration
st.set_page_config(page_title="Desk Booking – May 2025", layout="wide")
st.title("📅 Office Desk Booking – May 2025")

month = 5
year = 2025
num_desks = 5
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# Get calendar for the month
cal = calendar.monthcalendar(year, month)

# Initialize session state
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

# Render the calendar
for week in cal:
    cols = st.columns(7)  # 7 days in a week
    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.markdown(" ")
            else:
                day_str = f"{year}-{month:02d}-{day:02d}"
                st.markdown(f"### {calendar.day_abbr[i]} {day}")

                for desk in range(1, num_desks + 1):
                    key = f"{day_str}_desk{desk}"
                    st.session_state.bookings.setdefault(key, "")

                    st.selectbox(
                        label=f"Desk {desk}",
                        options=team_members,
                        index=team_members.index(st.session_state.bookings[key]),
                        key=key,
                        label_visibility="visible"
                    )

# Optional download
st.markdown("---")
if st.button("📥 Download Booking Summary"):
    import pandas as pd
    data = []
    for key, user in st.session_state.bookings.items():
        if user:
            date_str, desk = key.split("_")
            data.append({"Date": date_str, "Desk": desk, "Booked By": user})
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "bookings_may2025.csv", "text/csv")
