 # prompt: Present a calendar of May 2025 for people to book desks in the office every day. with 5 desks and 6 people names. For each day is possible for a team member to book a desk with a dropdown list.

import calendar
import ipywidgets as widgets
from IPython.display import display

def create_booking_widgets(month, year, num_desks, team_members):
  """Creates booking widgets for each day of a month."""
  cal = calendar.monthcalendar(year, month)
  output_widgets = []

  for week in cal:
    week_widgets = []
    for day in week:
      if day == 0:
        # Day 0 represents padding in the calendar, not a real day
        week_widgets.append(widgets.Label(value=" "))
      else:
        day_str = f"{month:02d}/{day:02d}/{year}"
        desk_bookings = [widgets.Dropdown(
            options=[''] + team_members,
            value='',
            description=f"Desk {i+1}:",
            disabled=False
        ) for i in range(num_desks)]
        day_box = widgets.VBox([widgets.Label(value=f"Day {day}:")] + desk_bookings)
        week_widgets.append(day_box)
    output_widgets.append(widgets.HBox(week_widgets))

  return widgets.VBox(output_widgets)

# Define parameters
month = 5
year = 2025
num_desks = 5
team_members = ["Bianca", "Barry", "Manuel", "Catarina", "Ecaterina", "Dana", "Audun"]

# Create and display the booking calendar
booking_calendar = create_booking_widgets(month, year, num_desks, team_members)
display(booking_calendar)

