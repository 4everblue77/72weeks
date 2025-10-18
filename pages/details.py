
import streamlit as st
from supabase import create_client
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

user_id = "123e4567-e89b-12d3-a456-426614174000"

st.set_page_config(page_title="Workout Details", layout="wide")

# Get values from session_state
selected_day = st.session_state.get("selected_day", "")
selected_section = st.session_state.get("selected_section", "")
selected_week = st.session_state.get("selected_week", "")

if not selected_day or not selected_section or not selected_week:
    st.error("Missing day or section. Please return to the main page.")
    st.stop()

# Fetch workout details
response = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").eq("day", selected_day).execute()
workout = response.data[0]

# Calculate date and day name
start_date = datetime(2025, 10, 13) + (selected_day - 1) * datetime.timedelta(days=1)
day_name = start_date.strftime("%A")
date_str = start_date.strftime("%b %d, %Y")

# Header
st.title(f"{selected_section} Details")
st.markdown(f"**Date:** {date_str} ({day_name})")
st.markdown(f"**Week:** {selected_week} | **Day:** {selected_day}")

# Total estimated time
total_time = (
    workout.get("warmup_time_minutes", 0)
    + workout.get("strength_time_minutes", 0)
    + workout.get("conditioning_time_minutes", 0)
    + workout.get("cooldown_time_minutes", 0)
)
st.markdown(f"**Estimated Total Time:** {total_time} minutes")

st.divider()

# Display exercises for the selected section
if selected_section == "Warmup":
    st.subheader("Warmup")
    st.write(workout.get("warmup_description", "No details available"))
elif selected_section == "Strength":
    st.subheader("Strength Exercises")
    exercises = workout.get("strength_exercises", [])
    for ex in exercises:
        st.markdown(f"- **{ex['name']}**: {ex['sets']} sets × {ex['reps']} reps @ {ex['weight']} kg")
elif selected_section == "Conditioning":
    st.subheader("Conditioning")
    st.write(f"{workout.get('conditioning_description', '')} ({workout.get('conditioning_type', '')})")
elif selected_section == "Cooldown":
    st.subheader("Cooldown")
    st.write(workout.get("cooldown_description", "No details available"))

st.divider()

# Action buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Timer"):
        st.info("Timer started... (placeholder)")
with col2:
    if st.button("Mark Complete"):
        supabase.table("completion").upsert({
            "user_id": user_id,
            "week": f"Week {selected_week}",
            "day": selected_day,
            "section": selected_section,
            "completed": True
        }).execute()
        st.success(f"{selected_section} marked complete")
        st.switch_page("main.py")
