import streamlit as st
import calendar
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError

# === App Setup ===
st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking – 2025")

# === Google Sheets Setup ===
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
gc = gspread.authorize(creds)
SPREADSHEET_ID = st.secrets["gcp_service_account"]["spreadsheet_id"]
sh = gc.open_by_key(SPREADSHEET_ID)
worksheet = sh.sheet1

# === Desk & Team Setup ===
desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# === Load all bookings from sheet every run ===
bookings = {}
try:
    for rec in worksheet.get_all_records():
        date_str = rec.get("Date")
        desk_name = rec.get("Desk")
        user = rec.get("Booked By")
        if date_str and desk_name and user and desk_name in desk_labels:
            idx = desk_labels.index(desk_name) + 1
            key = f"{date_str}_desk{idx}"
            bookings[key] = user
except Exception:
    st.error("Could not load existing bookings from Google Sheets.")

# === Callback to write a single booking to Google Sheets ===
def write_booking(key):
    val = st.session_state[key]
    prev = bookings.get(key)
    if not val or val == prev:
        return
    date_str, desk = key.split("_")
    idx = int(desk.replace("desk", ""))
    try:
        worksheet.append_row([date_str, desk_labels[idx-1], val])
        bookings[key] = val
        st.success(f"Booked {val} for {desk_labels[idx-1]} on {date_str}")
    except APIError:
        st.error(
            "Failed to save booking.\n"
            "Ensure service account has edit rights and sheet ID is correct."
        )

# === Calendar Rendering & Dropdowns ===

today = datetime.today()
# Auto-scroll for May–Dec 2025
if 5 <= today.month <= 12 and today.year == 2025:
    today_str = today.strftime("%Y-%m-%d")
    st.markdown(
        f"""
        <script>
            window.onload = function() {{
                var el = document.getElementsByName("{today_str}")[0];
                if (el) el.scrollIntoView({{behavior:'smooth'}});
            }};
        </script>
        """,
        unsafe_allow_html=True,
    )

for month in range(5, 13):
    cal = calendar.monthcalendar(2025, month)
    with st.expander(f"{calendar.month_name[month]} 2025", expanded=(month == today.month)):
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day:
                        date_str = f"2025-{month:02d}-{day:02d}"
                        st.markdown(f'<a name="{date_str}"></a>', unsafe_allow_html=True)
                        st.markdown(f"### {calendar.day_abbr[i]} {day}")
                        for idx, desk_name in enumerate(desk_labels, start=1):
                            key = f"{date_str}_desk{idx}"
                            # sync session state with latest booking from sheet
                            if key not in st.session_state or st.session_state[key] != bookings.get(key, ""):
                                st.session_state[key] = bookings.get(key, "")
                            # dropdown writes to session state and triggers write
                            # determine default index from session state
                            default = st.session_state.get(key, "")
                            idx_default = team_members.index(default) if default in team_members else 0
                            st.selectbox(
                                label=desk_name,
                                options=team_members,
                                index=idx_default,
                                key=key,
                                on_change=write_booking,
                                args=(key,),
                                label_visibility="visible"
                            )
                    else:
                        st.markdown(" ")
