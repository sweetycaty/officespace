import streamlit as st
import calendar
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === App Setup ===
st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking – 2025")

# === Google Sheets Setup ===
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
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

# === Callback to write a single booking to Google Sheets ===
def write_booking(key):
    # When a dropdown changes, push that one booking
    val = st.session_state[key]
    if not val:
        return
    date_str, desk = key.split("_")
    idx = int(desk.replace("desk", ""))
    worksheet.append_row([date_str, desk_labels[idx-1], val])
    st.success(f"Booked {val} for {desk_labels[idx-1]} on {date_str}")

# === Auto-load existing bookings if needed (optional) ===
# If you want to clear sheet each run, skip this

# === Calendar Rendering & Dropdowns ===
today = datetime.today()
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
                            # each selectbox writes immediately on change
                            st.selectbox(
                                label=desk_name,
                                options=team_members,
                                key=key,
                                on_change=write_booking,
                                args=(key,),
                                label_visibility="visible"
                            )
                    else:
                        st.markdown(" ")
