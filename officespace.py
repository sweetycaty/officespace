import streamlit as st
import calendar
from datetime import datetime
import pandas as pd

# === Configuration ===
st.set_page_config(page_title="Desk Booking – May 2025", layout="wide")
month = 5
year = 2025
desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]
cal = calendar.monthcalendar(year, month)

# === Header Section ===
st.title("📅 Office Desk Booking – May 2025")
st.markdown("Use the dropdowns to assign a team member to each desk per day.")

# === Initialize Session State ===
if "bookings" not in st.session_state:
    st.session_state.bookings = {}

# === Determine Today's Date ===
today = datetime.today()
scroll_to_date = None
if today.year == year and today.month == month:
    scroll_to_date = f"{year}-{month:02d}-{today.day:02d}"

# === Scroll to Today's Date Using JS ===
if scroll_to_date:
    st.markdown(
        f"""
        <script>
            window.onload = function() {{
                var el = document.getElementsByName("{scroll_to_date}")[0];
                if (el) {{
                    el.scrollIntoView({{ behavior: "smooth" }});
                }}
            }};
        </script>
        """,
        unsafe_allow_html=True
    )

# === Calendar Rendering ===
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.markdown(" ")
            else:
                day_str = f"{year}-{month:02d}-{day:02d}"
                st.markdown(f'<a name="{day_str}"></a>', unsafe_allow_html=True)  # anchor for scrolling
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

# === CSV Export ===
st.markdown("---")
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
    st.download_button("Download CSV", csv, "bookings_may2025.csv", "text/csv")
