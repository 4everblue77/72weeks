import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "123e4567-e89b-12d3-a456-426614174000"
week = "Week 1"

st.set_page_config(page_title="OpenPrep Tracker", layout="centered")
st.title("OpenPrep Tracker - Week 1")

# Fetch workouts
response = supabase.table("workouts").select("*").eq("week", week).execute()
workouts = response.data

# Weekly calendar
days = [w['day'] for w in workouts]
selected_day = st.selectbox("Select Day", days)

# Get workout for selected day
workout = next(w for w in workouts if w['day'] == selected_day)

# Section selection
st.subheader(f"Day {selected_day}")
sections = ["Warmup", "Strength", "Conditioning", "Cooldown"]

st.markdown("### Sections")
for section in sections:
    completed_resp = supabase.table("completion").select("completed").eq("user_id", user_id).eq("week", week).eq("day", selected_day).eq("section", section).execute()
    completed = completed_resp.data[0]['completed'] if completed_resp.data else False
    status = "✅" if completed else "❌"
    if st.button(f"{section} {status}"):
        st.query_params(day=selected_day, section=section)
        st.switch_page("details.py")

