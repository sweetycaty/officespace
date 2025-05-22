import streamlit as st
import calendar
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Google Sheets Setup ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("DeskBookings2025").sheet1  # open the first worksheet

# === Constants ===
desk_labels = [
    "Bianca's Office",
    "Manuel's Desk",
    "Ioana's Desk",
    "Ecaterina's Desk",
    "Dana's Desk"
]
team_members = ["", "Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# === Load Existing Data from Google Sheet ===
existing_records = sheet.get_all_records()
bookings = {f"{r['Date']}_desk{r['Desk']}": r['Booked By'] for r in existing_records}

# === Today & Scroll Logic ===
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

st.set_page_config(page_title="Desk Booking – 2025", layout="wide")
st.title("📅 Office Desk Booking P&P – 2025")

# === Month View (May to Dec) ===
new_entries = []
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
    new_value = st.selectbox(
        label=desk_name,
        options=team_members,
        index=team_members.index(current_value) if current_value in team_members else 0,
        key=key,
        label_visibility="visible"
    )
    if new_value != current_value:
        bookings[key] = new_value
        new_entries.append({
            "Date": day_str,
            "Desk": desk_index,
            "Booked By": new_value
        })


    # Update the live tracking of booked people for the day
    if current_value:
        booked_people.discard(current_value)  # remove old if changed
    if new_value:
        booked_people.add(new_value)          # add new


# === Update Google Sheet (overwrite changed rows) ===
if new_entries:
    # Remove duplicates from existing sheet
    df = pd.DataFrame(existing_records)
    for entry in new_entries:
        df = df[~((df['Date'] == entry["Date"]) & (df['Desk'] == entry["Desk"]))]

    df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
    df = df.sort_values(by=["Date", "Desk"])
    sheet.clear()
    sheet.append_row(["Date", "Desk", "Booked By"])
    sheet.append_rows(df.values.tolist())

# === CSV Export ===
st.markdown("---")
if st.button("📥 Download Booking Summary"):
    df = pd.DataFrame([
        {"Date": key.split("_")[0], "Desk": desk_labels[int(key.split("_")[1].replace("desk", "")) - 1], "Booked By": user}
        for key, user in bookings.items() if user
    ])
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "bookings_2025.csv", "text/csv")
