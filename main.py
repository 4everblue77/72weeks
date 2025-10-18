import streamlit as st

from supabase import create_client
from datetime import datetime, timedelta
## from config import SUPABASE_URL, SUPABASE_KEY




# Supabase credentials
SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

user_id = "123e4567-e89b-12d3-a456-426614174000"

st.set_page_config(page_title="OpenPrep Tracker", layout="wide", initial_sidebar_state="collapsed")

# Fixed start date
START_DATE = datetime(2025, 10, 13)
today = datetime.today()

# Calculate current week
days_since_start = (today - START_DATE).days
default_week = max(1, (days_since_start // 7) + 1)

# Initialize session state
if "selected_week" not in st.session_state:
    st.session_state.selected_week = default_week

# Week navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Previous Week"):
        st.session_state.selected_week = max(1, st.session_state.selected_week - 1)
with col3:
    if st.button("➡️ Next Week"):
        st.session_state.selected_week += 1

selected_week = st.session_state.selected_week

# Week range display
week_start_date = START_DATE + timedelta(weeks=selected_week - 1)
week_end_date = week_start_date + timedelta(days=6)
week_range = f"Week {selected_week}: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d')}"
st.markdown(f"### 📅 {week_range}")

# Fetch workouts and completion data
workouts_resp = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").execute()
workouts = workouts_resp.data

completion_resp = supabase.table("completion").select("*").eq("user_id", user_id).eq("week", f"Week {selected_week}").execute()
completion_data = completion_resp.data

# Build maps
workout_map = {w['day']: w for w in workouts}
completion_lookup = {
    (c["day"], c["section"]): c["completed"]
    for c in completion_data
}

# Day status
sections = ["Warmup", "Strength", "Conditioning", "Cooldown"]
day_status = {
    day: all(completion_lookup.get((day, section), False) for section in sections)
    for day in workout_map
}

# Day selector
weekday_map = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
all_days = list(range(1, 8))

if workouts:
    with st.form("day_selector_form"):
        selected_day = st.radio("Select a day", options=all_days, format_func=lambda x: weekday_map[x])
        submitted = st.form_submit_button("Go")

    if submitted:
        st.session_state.selected_day = selected_day
else:
    st.warning("No workouts available for this week.")

# Show selected day workout
if "selected_day" in st.session_state:
    selected_day = st.session_state.selected_day
    st.subheader(f"{weekday_map[selected_day]} (Day {selected_day})")

    if selected_day not in workout_map:
        st.info("🛌 Rest Day – No workout scheduled.")
    else:
        st.markdown("### Sections")
        for section in sections:
            completed = completion_lookup.get((selected_day, section), False)
            button_label = f"{section} {'✔️' if completed else '❌'}"

            with st.form(f"{section}_form"):
                submitted = st.form_submit_button(button_label)
                if submitted:
                    st.success(f"You selected: {section}")
                    st.session_state.selected_section = section
                    # Navigation logic can be added here if needed
