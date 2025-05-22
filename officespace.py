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
    scopes=["https://www.googleapis.com/auth/spreadsheets"],
)
gc = gspread.authorize(creds)

# Retrieve spreadsheet ID from secrets
SPREADSHEET_ID = st.secrets["gcp_service_account"]["spreadsheet_id"]
try:
    sh = gc.open_by_key(SPREADSHEET_ID)
    worksheet = sh.sheet1
except Exception:
    st.error(
        "Could not open Google Sheet.\n"
        "- Check `spreadsheet_id` in secrets.toml.\n"
        "- Service account needs Editor access."
    )
    st.stop()

# === Desk & Team Setup ===
desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# === Load existing bookings into session state on first run ===
if "loaded" not in st.session_state:
    st.session_state.loaded = True
    try:
        records = worksheet.get_all_records()
        for rec in records:
            date_str = rec.get("Date", "")
            desk_name = rec.get("Desk", "")
            user = rec.get("Booked By", "")
            if date_str and desk_name and user and desk_name in desk_labels:
                idx = desk_labels.index(desk_name) + 1
                key = f"{date_str}_desk{idx}"
                st.session_state[key] = user
    except Exception:
        pass

# === Prepare keys list for this run ===
all_keys = []

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
                            all_keys.append(key)
                            default = st.session_state.get(key, "")
                            # Selectbox tied to session_state[key]
                            st.selectbox(
                                label=desk_name,
                                options=team_members,
                                index=team_members.index(default) if default in team_members else 0,
                                key=key,
                                label_visibility="visible"
                            )
                    else:
                        st.markdown(" ")

# === Action Buttons ===
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Download Booking Summary"):
        data = []
        for key in all_keys:
            user = st.session_state.get(key, "")
            if user:
                date_str, desk = key.split("_")
                idx = int(desk.replace("desk", ""))
                data.append({"Date": date_str, "Desk": desk_labels[idx-1], "Booked By": user})
        df = pd.DataFrame(data)
        st.download_button("Download CSV", df.to_csv(index=False), "bookings_2025.csv", "text/csv")

with col2:
    if st.button("💾 Save to Google Sheets"):
        rows = []
        for key in all_keys:
            user = st.session_state.get(key, "")
            if user:
                date_str, desk = key.split("_")
                idx = int(desk.replace("desk", ""))
                rows.append([date_str, desk_labels[idx-1], user])
        if rows:
            worksheet.clear()
            worksheet.append_row(["Date", "Desk", "Booked By"])
            worksheet.append_rows(rows)
            st.success("Bookings saved to Google Sheets!")
        else:
            st.info("No bookings to save.")
