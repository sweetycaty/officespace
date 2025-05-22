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
        # Clean up date, strip leading apostrophe if present
        raw_date = rec.get("Date")
        if isinstance(raw_date, str):
            date_str = raw_date.lstrip("'")
        else:
            date_str = str(raw_date)
        desk_name = rec.get("Desk")
        user = rec.get("Booked By")
        if date_str and desk_name and user and desk_name in desk_labels:
            idx = desk_labels.index(desk_name) + 1
            key = f"{date_str}_desk{idx}"
            bookings[key] = user
except Exception:
    st.error("Could not load existing bookings from Google S
