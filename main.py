import streamlit as st

from supabase import create_client
from datetime import datetime, timedelta
## from config import SUPABASE_URL, SUPABASE_KEY

SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "123e4567-e89b-12d3-a456-426614174000"

st.set_page_config(page_title="OpenPrep Tracker", layout="wide", initial_sidebar_state="collapsed")



# Scoped CSS for default buttons only
st.markdown("""
<style>
div[data-testid="stButton"][class*="default-btn"] > button {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75em 1em;
    font-size: 1.1rem;
    font-weight: 500;
    background-color: #ffffff;
    border-radius: 8px;
    border: none;
    cursor: pointer;
}
div[data-testid="stButton"][class*="default-btn"] > button:hover {
    background-color: #e0e2e6;
}
</style>
""", unsafe_allow_html=True)

# Scoped CSS for section buttons onl
st.markdown("""
<style>
div[data-testid="stButton"][class*="section-btn"] > button {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75em 1em;
    font-size: 1.1rem;
    font-weight: 500;
    background-color: #ffffff;
    border-radius: 8px;
    border: 10px solid grey;
    cursor: pointer;
}
div[data-testid="stButton"][class*="section-btn"] > button:hover {
    background-color: #e0e2e6;
}
</style>
""", unsafe_allow_html=True)

 
                   

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
    st.markdown('<div class="default-button">', unsafe_allow_html=True)
    if st.button("⬅️ Previous Week",key=f"default-btn-prev"):
        st.session_state.selected_week = max(1, st.session_state.selected_week - 1)
with col3:
    st.markdown('<div class="default-button">', unsafe_allow_html=True)
    if st.button("➡️ Next Week",key=f"default-btn-next"):
        st.session_state.selected_week += 1

selected_week = st.session_state.selected_week


# Calculate week range
week_start_date = START_DATE + timedelta(weeks=selected_week - 1)
week_end_date = week_start_date + timedelta(days=6)


week_range = f"Week {selected_week}: {week_start_date.strftime('%b %d')} - {week_end_date.strftime('%b %d')}"
st.markdown(f"### 📅 {week_range}")

# Determine today's day index (1 = Mon, ..., 7 = Sun)
today_index = today.weekday() + 1  # Python weekday: 0=Mon, so +1 to match your map

# If today is within the selected week and no day is selected yet, default to today
if "selected_day" not in st.session_state:
    if week_start_date <= today <= week_end_date:
        st.session_state.selected_day = today_index


# Determine current day index (0=Mon, 6=Sun)
current_day_index = (today - week_start_date).days if week_start_date <= today <= week_end_date else None


# Fetch workouts
response = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").execute()
workouts = response.data

days = [w['day'] for w in workouts]

# Fetch completion data
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



# Horizontal day selector
##st.markdown("### Select a Day")



# Day selector with buttons
weekday_map = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
all_days = list(range(1, 8))


if workouts:
    st.markdown("### Select a Day")
    cols = st.columns(7)
    icons = {
        "completed": "✔️",
        "incomplete": "⚫",
        "rest": "⚪"
    }

    for i, day in enumerate(all_days):
        day_label = weekday_map[day]
        workout_exists = day in workout_map
        completed = day_status.get(day, False)

        icon = icons["completed"] if completed else icons["incomplete"] if workout_exists else icons["rest"]
        button_text = f"{day_label[0]}\n{icon}"

        with cols[i]:
            st.markdown('<div class="default-button">', unsafe_allow_html=True)
            if st.button(button_text, key=f"day_{day}"):
                st.session_state.selected_day = day
else:
    st.warning("No workouts available for this week.")







# Show selected day workout
if "selected_day" in st.session_state:
    selected_day = st.session_state.selected_day
    st.subheader(f"{weekday_map[selected_day]} (Day {selected_day}) Est. Time: {workout.get('expected_total_time_minutes', 'N/A')} minutes")

    if selected_day not in workout_map:
        st.info("🛌 Rest Day – No workout scheduled.")
    else:
        st.markdown("### Sections")



        for section in sections:
            completed = completion_lookup.get((selected_day, section), False)
            icon = "✔️" if completed else "❌"
            button_label = f"{section} {icon}"


            # Wrap each button in a div with class 'section-button'
            st.markdown('<div class="section-button">', unsafe_allow_html=True)
            if st.button(button_label, key=f"section-btn-{section}", use_container_width = True):
                st.session_state.selected_section = section

                st.session_state.selected_day = selected_day
                st.session_state.selected_week = selected_week
                st.switch_page("pages/details.py")  # Navigate to details page








