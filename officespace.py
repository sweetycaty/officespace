import streamlit as st
import calendar
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === App Setup ===
st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking – 2025")

# === Google Sheets Setup ===
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
gc = gspread.authorize(creds)
SPREADSHEET_NAME = "DeskBookings2025"
sh = gc.open(SPREADSHEET_NAME)
worksheet = sh.sheet1

desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# === Session State Init ===
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

# === Today for Scroll Logic ===
today = datetime.today()
today_str = f"{today.year}-{today.month:02d}-{today.day:02d}"

# === Scroll to Today with JS if in May–Dec 2025 ===
if 5 <= today.month <= 12 and today.year == 2025:
    st.markdown(
        f'''
        <script>
            window.onload = function() {{
                var el = document.getElementsByName("{today_str}")[0];
                if (el) {{
                    el.scrollIntoView({{ behavior: "smooth" }});
                }}
            }};
        </script>
        ''',
        unsafe_allow_html=True
    )

# === Generate Calendar for May–Dec 2025 ===
for month in range(5, 13):
    cal = calendar.monthcalendar(2025, month)
    month_name = calendar.month_name[month]
    expand_default = (month == today.month and today.year == 2025)

    with st.expander(f"{month_name} 2025", expanded=expand_default):
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.markdown(" ")
                    else:
                        day_str = f"2025-{month:02d}-{day:02d}"
                        st.markdown(f'<a name="{day_str}"></a>', unsafe_allow_html=True)
                        st.markdown(f"### {calendar.day_abbr[i]} {day}")

                        for desk_index, desk_name in enumerate(desk_labels, start=1):
                            key = f"{day_str}_desk{desk_index}"
                            st.session_state.bookings.setdefault(key, "")
                            st.selectbox(
                                label=desk_name,
                                options=team_members,
                                index=team_members.index(st.session_state.bookings[key]),
                                key=key,
                                label_visibility="visible"
                            )

# === Action Buttons ===
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Download Booking Summary"):
        data = []
        for key, user in st.session_state.bookings.items():
            if user:
                date_str, desk = key.split("_")
                desk_index = int(desk.replace("desk", ""))
                data.append({
                    "Date": date_str,
                    "Desk": desk_labels[desk_index - 1],
                    "Booked By": user
                })
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "bookings_2025.csv", "text/csv")

with col2:
    if st.button("💾 Save to Google Sheets"):
        data_rows = []
        for key, user in st.session_state.bookings.items():
            if user:
                date_str, desk = key.split("_")
                desk_index = int(desk.replace("desk", ""))
                data_rows.append(
                    [date_str, desk_labels[desk_index - 1], user]
                )
        if data_rows:
            # Clear existing sheet and reset headers
            worksheet.clear()
            headers = ["Date", "Desk", "Booked By"]
            worksheet.append_row(headers)
            # Append new booking rows
            for row in data_rows:
                worksheet.append_row(row)
            st.success("Bookings saved to Google Sheets!")
        else:
            st.info("No bookings to save.")
