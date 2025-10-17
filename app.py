import streamlit as st
from supabase import create_client, Client
import datetime

# Supabase credentials
url = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"
supabase: Client = create_client(url, key)

# Simulated user ID
user_id = "demo-user"

# Fetch workout plan
@st.cache_data
def get_workouts(week):
    response = supabase.table("workouts").select("*").eq("week", week).execute()
    return response.data
# Fetch completion status
def get_completion(user_id, week, day):
    response = supabase.table("completion").select("*").eq("user_id", user_id).eq("week", week).eq("day", day).execute()
    return {item['section']: item['completed'] for item in response.data}

# Mark section complete
def mark_complete(user_id, week, day, section):
    supabase.table("completion").upsert({
        "user_id": user_id,
        "week": week,
        "day": day,
        "section": section,
        "completed": True
    }).execute()

# UI
st.title("Open Prep Program Tracker")
selected_week = "Week 1"
workouts = get_workouts(selected_week)

st.subheader(f"{selected_week} Overview")
for workout in workouts:
    day = workout['day']
    st.markdown(f"### Day {day}")
    cols = st.columns(4)
    completion = get_completion(user_id, selected_week, day)
    for i, section in enumerate(["Warmup", "Strength", "Conditioning", "Cooldown"]):
        key = f"{selected_week}_{day}_{section}"
        checked = completion.get(section, False)
        if cols[i].checkbox(section, value=checked, key=key):
            mark_complete(user_id, selected_week, day, section)

# Workout Details
st.sidebar.title("Workout Details")
selected_day = st.sidebar.selectbox("Select Day", [w['day'] for w in workouts])
selected_data = next(w for w in workouts if w['day'] == selected_day)

st.sidebar.subheader(f"Day {selected_day} Details")
st.sidebar.text(f"Strength: {selected_data['strength']}")
st.sidebar.text(f"Conditioning: {selected_data['conditioning']}")

if st.sidebar.button("Start Timer"):
    st.sidebar.write("Timer started (placeholder)")

if st.sidebar.button("Mark Complete"):
    for section in ["Warmup", "Strength", "Conditioning", "Cooldown"]:
        mark_complete(user_id, selected_week, selected_day, section)
    st.sidebar.success("Workout marked complete")
