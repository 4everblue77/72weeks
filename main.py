import streamlit as st
from supabase import create_client
## from config import SUPABASE_URL, SUPABASE_KEY

SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
user_id = "123e4567-e89b-12d3-a456-426614174000"

st.set_page_config(page_title="OpenPrep Tracker", layout="wide", initial_sidebar_state="collapsed"
                   
week = "Week 1"

st.set_page_config(page_title="OpenPrep Tracker", layout="centered")
st.title("OpenPrep Tracker - Week 1")

# Fetch workouts
response = supabase.table("workouts").select("*").eq("week", week).execute()
workouts = response.data

days = [w['day'] for w in workouts]
selected_day = st.selectbox("Select Day", days)
workout = next(w for w in workouts if w['day'] == selected_day)

st.subheader(f"Day {selected_day}")
sections = ["Warmup", "Strength", "Conditioning", "Cooldown"]

st.markdown("### Sections")

# Store selection in session state
if "pending_navigation" not in st.session_state:
    st.session_state.pending_navigation = None

for section in sections:
    completed_resp = supabase.table("completion").select("completed").eq("user_id", user_id).eq("week", week).eq("day", selected_day).eq("section", section).execute()
    completed = completed_resp.data[0]['completed'] if completed_resp.data else False
    status = "✅" if completed else "❌"



    if st.button(f"{section} {status}"):
        st.session_state.selected_day = selected_day
        st.session_state.selected_section = section
        st.switch_page("pages/details.py")

