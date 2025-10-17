
import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "demo-user"

st.title("OpenPrep Tracker - Week 1")

# Fetch workouts
response = supabase.table("workouts").select("*").eq("week", "Week 1").execute()
workouts = response.data

selected_day = st.selectbox("Select Day", [w['day'] for w in workouts])
workout = next(w for w in workouts if w['day'] == selected_day)

st.subheader(f"Day {selected_day} Details")
st.text(f"Warmup: {workout['warmup_description']} ({workout['warmup_time_minutes']} min)")
st.text(f"Strength: {workout['strength_description']} ({workout['strength_time_minutes']} min, Rest: {workout['strength_rest_seconds']} sec)")
st.text(f"Conditioning: {workout['conditioning_description']} ({workout['conditioning_type']}, {workout['conditioning_time_minutes']} min)")
st.text(f"Cooldown: {workout['cooldown_description']} ({workout['cooldown_time_minutes']} min)")
st.text(f"Total Estimated Time: {workout['expected_total_time_minutes']} min")

if st.button("Mark Complete"):
    for section in ["Warmup", "Strength", "Conditioning", "Cooldown"]:
        supabase.table("completion").upsert({
            "user_id": user_id,
            "week": "Week 1",
            "day": selected_day,
            "section": section,
            "completed": True
        }).execute()
    st.success("Workout marked complete")
