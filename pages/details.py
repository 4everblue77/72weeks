import streamlit as st
from supabase import create_client
## from config import SUPABASE_URL, SUPABASE_KEY



params = st.query_params
st.write("DEBUG: Received query params →", params)

selected_day = params.get("day", "")
section = params.get("section", "")

st.write(f"DEBUG: Parsed Day: {selected_day}")
st.write(f"DEBUG: Parsed Section: {section}")


SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "123e4567-e89b-12d3-a456-426614174000"
week = "Week 1"

params = st.query_params
selected_day = params.get("day", "")
section = params.get("section", "")

if not selected_day or not section:
    st.error("Missing day or section. Please return to the main page.")
    st.stop()

# Fetch workout
response = supabase.table("workouts").select("*").eq("week", week).eq("day", selected_day).execute()
workout = response.data[0]

st.title(f"{section} Details - {selected_day}")

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
    st.query_params()
    st.switch_page("main.py")
