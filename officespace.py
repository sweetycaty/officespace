import streamlit as st
import calendar
from datetime import datetime
import pandas as pd

# === App Setup ===
st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking – 2025")

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
                        st.markdown(f'<a name="{d
