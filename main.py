import streamlit as st

from supabase import create_client
from datetime import datetime, timedelta
## from config import SUPABASE_URL, SUPABASE_KEY

SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "123e4567-e89b-12d3-a456-426614174000"

st.set_page_config(page_title="OpenPrep Tracker", layout="wide", initial_sidebar_state="collapsed")
                   
all_days = list(range(1, 8))  # Days 1 to 7 (Mon to Sun)
weekday_map = {
    1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"
}
# Fixed start date
START_DATE = datetime(2025, 10, 13)
today = datetime.today()

# Calculate current week
days_since_start = (today - START_DATE).days
default_week = max(1, (days_since_start // 7) + 1)


# Initialize session state
if "selected_week" not in st.session_state:
    st.session_state.selected_week = default_week


# Week navigation arrows
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Previous Week"):
        st.session_state.selected_week = max(1, st.session_state.selected_week - 1)
with col3:
    if st.button("➡️ Next Week"):
        st.session_state.selected_week += 1

selected_week = st.session_state.selected_week


# Calculate week range
week_start_date = START_DATE + timedelta(weeks=selected_week - 1)
week_end_date = week_start_date + timedelta(days=6)
week_range = f"Week {selected_week}: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d')}"
st.markdown(f"### 📅 {week_range}")

# Determine current day index (0=Mon, 6=Sun)
current_day_index = (today - week_start_date).days if week_start_date <= today <= week_end_date else None


# Fetch workouts
response = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").execute()
workouts = response.data

days = [w['day'] for w in workouts]

# Fetch completion data
completion_resp = supabase.table("completion").select("*").eq("user_id", user_id).eq("week", f"Week {selected_week}").execute()
completion_data = completion_resp.data

# Build completion map



workout_map = {w['day']: w for w in workouts}





day_status = {}
for day in days:
    sections = ["Warmup", "Strength", "Conditioning", "Cooldown"]
    completed_sections = [
        c for c in completion_data
        if c["day"] == day and c["section"] in sections and c["completed"]
    ]
    day_status[day] = len(completed_sections) == len(sections)




# Horizontal day selector
##st.markdown("### Select a Day")


all_days = list(range(1, 8))  # Days 1 to 7 (Mon to Sun)
workout_map = {w['day']: w for w in workouts}
weekday_map = {
    1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"
}


if workouts:
    cols = st.columns(len(all_days))
    selected = False



   
    # Emoji indicators
    icons = {
        "completed": "✔️",   # You can also use "✅" or "✔️"
        "incomplete": "⚫",
        "rest": "⚪"
    }
    
    for i, day in enumerate(all_days):
        day_label = weekday_map[day]
        workout_exists = day in workout_map
        completed = day_status.get(day, False)
    
        with cols[i]:
            # Header with weekday initial
            # st.markdown(f"{day_label[0]}")
    
            # Determine icon
            if workout_exists:
                icon = f"{icons['completed']}" if completed else icons["incomplete"]
            else:
                icon = icons["rest"]
    
            button_key = f"day-{day}"
            highlight_style = ""
            if current_day_index is not None and day == current_day_index + 1:
                highlight_style = "font-weight: bold;"
                st.markdown(f"**{day_label[0]}**")
            else:
                st.markdown(f"{day_label[0]}")

  
            # Inject style
            st.markdown(f"""
                <style>
                button[data-testid="baseButton"][aria-label="{button_key}"] {{
                    background-color: transparent;
                    color: black;
                    border: none;
                    font-size: 1.5em;
                    {highlight_style}
                }}
                </style>
            """, unsafe_allow_html=True)
    
            # Render button
            if st.button(icon, key=button_key):
                st.session_state.selected_day = day
                st.session_state.selected_section = None
                selected = True



    if not selected and "selected_day" not in st.session_state and current_day_index is not None:
        st.session_state.selected_day = current_day_index + 1
else:
    st.warning("No workouts available for this week.")






# Show selected day workout
if "selected_day" in st.session_state:

    selected_day = st.session_state.selected_day

    st.subheader(f"Day {selected_day}")
    sections = ["Warmup", "Strength", "Conditioning", "Cooldown"]

    st.markdown("### Sections")

    if "pending_navigation" not in st.session_state:
        st.session_state.pending_navigation = None

    for section in sections:
        completed_resp = supabase.table("completion").select("completed").eq("user_id", user_id).eq("week", selected_week).eq("day", selected_day).eq("section", section).execute()
        completed = completed_resp.data[0]['completed'] if completed_resp.data else False
        

        # Set color
        button_color = "#4CAF50" if completed else "#F44336"  # Green or Red
    
        # Unique key for each button
        if st.button(section, key=f"{section}-btn"):
            st.session_state.selected_section = section
            st.switch_page("pages/details.py")
    
        # Inject scoped style for that button
        st.markdown(f"""
            <style>
            button[data-testid="baseButton"][aria-label="{section}-btn"] {{
                background-color: {button_color};
                color: white;
                border: none;
                padding: 0.5em 1em;
                border-radius: 5px;
            }}
            </style>
        """, unsafe_allow_html=True)







