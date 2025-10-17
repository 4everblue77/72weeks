import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "demo-user"
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

# Completion status
st.markdown("### Sections")
for section in sections:
    completed_resp = supabase.table("completion").select("completed").eq("user_id", user_id).eq("week", week).eq("day", selected_day).eq("section", section).execute()
    completed = completed_resp.data[0]['completed'] if completed_resp.data else False
    status = "✅" if completed else "❌"
    if st.button(f"{section} {status}"):
        st.session_state['selected_section'] = section

# Details screen
if 'selected_section' in st.session_state:
    section = st.session_state['selected_section']
    st.subheader(f"{section} Details")

    if section == "Warmup":
        st.text(f"{workout['warmup_description']} ({workout['warmup_time_minutes']} min)")
    elif section == "Strength":
        st.text(f"{workout['strength_description']} ({workout['strength_time_minutes']} min, Rest: {workout['strength_rest_seconds']} sec)")
    elif section == "Conditioning":
        st.text(f"{workout['conditioning_description']} ({workout['conditioning_type']}, {workout['conditioning_time_minutes']} min)")
    elif section == "Cooldown":
        st.text(f"{workout['cooldown_description']} ({workout['cooldown_time_minutes']} min)")

    if st.button("Start Timer"):
        st.info("Timer started... (placeholder)")

    if st.button("Complete"):
        supabase.table("completion").upsert({
            "user_id": user_id,
            "week": week,
            "day": selected_day,
            "section": section,
            "completed": True
        }).execute()
        st.success(f"{section} marked complete")
        del st.session_state['selected_section']
