import streamlit as st
import calendar
import json
import os
from datetime import datetime
import pandas as pd

# === Setup ===
st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking P&P – 2025")

# === Settings ===
desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]
data_file = "bookings.json"

# === Load Persistent Data ===
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        bookings = json.load(f)
else:
    bookings = {}

# === Helper to Save to File ===
def save_bookings():
    with open(data_file, "w") as f:
        json.dump(bookings, f)

# === Determine Today's Date for Scroll ===
today = datetime.today()
today_str = f"{today.year}-{today.month:02d}-{today.day:02d}"

if 5 <= today.month <= 12 and today.year == 2025:
    st.markdown(
        f"""
        <script>
            window.onload = function() {{
                var el = document.getElementsByName("{today_str}")[0];
                if (el) {{
                    el.scrollIntoView({{ behavior: "smooth" }});
                }}
            }};
        </script>
        """,
        unsafe_allow_html=True
    )

# === Calendar from May to Dec 2025 ===
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
                            current_value = bookings.get(key, "")

                            selected = st.selectbox(
                                label=desk_name,
                                options=team_members,
                                index=team_members.index(current_value) if current_value in team_members else 0,
                                key=key
                            )

                            if selected != current_value:
                                bookings[key] = selected
                                save_bookings()

# === Download Button ===
st.markdown("---")
if st.button("📥 Download Booking Summary"):
    data = []
    for key, user in bookings.items():
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
