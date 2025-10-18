
import streamlit as st
from supabase import create_client
import pandas as pd

# Supabase credentials
SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Get session state values
selected_day = st.session_state.get("selected_day", "")
selected_week = st.session_state.get("selected_week", "")
selected_section = st.session_state.get("selected_section", "")

if not selected_day or not selected_week or not selected_section:
    st.error("Missing day or section. Please return to the main page.")
    st.stop()

# Fetch workout
workout_resp = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").eq("day", selected_day).execute()
if not workout_resp.data:
    st.error("Workout not found.")
    st.stop()

workout = workout_resp.data[0]
workout_id = workout["id"]

# Fetch section
section_resp = supabase.table("sections").select("*").eq("workout_id", workout_id).eq("section_type", selected_section).execute()
if not section_resp.data:
    st.warning("No section found.")
    st.stop()

section = section_resp.data[0]
section_id = section["id"]

# Fetch exercises
exercise_resp = supabase.table("exercises").select("*").eq("section_id", section_id).order("order_index").execute()
exercises = exercise_resp.data

# Header
st.title(f"{selected_section} Details")
st.markdown(f"**Week:** {selected_week} | **Day:** {selected_day}")
st.markdown(f"**Estimated Time:** {section.get('time_minutes', 'N/A')} minutes")
st.divider()

# Display section description
st.subheader(f"{selected_section} Description")
st.write(section.get("description", "No details available"))

# Display exercises in table

if exercises:
    expanded_rows = []
    for ex in exercises:
        sets = int(ex.get("sets", 1)) if ex.get("sets", "").isdigit() else 1
        reps = ex.get("reps", "")
        weight = ex.get("weight", "")
        name = ex.get("name", "")
        
        if selected_section == "Strength":
            # Create one row per set
            for s in range(1, sets + 1):
                expanded_rows.append({
                    "Set": s,
                    "Exercise": name,
                    "Reps": reps,
                    "Weight (kg)": weight,
                    "Rest (sec)": section.get("rest_seconds", "")
                })
        else:
            # For non-strength, keep one row per exercise
            expanded_rows.append({
                "Exercise": name,
                "Sets": ex.get("sets", ""),
                "Reps": reps,
                "Weight (kg)": weight
            })

    df_display = pd.DataFrame(expanded_rows)
    st.table(df_display.style.hide(axis="index"))
else:
    st.warning("No exercises found.")


# Action buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Timer"):
        st.info("Timer started... (placeholder)")
with col2:
    if st.button("Mark Complete"):
        supabase.table("completion").upsert({
            "week": f"Week {selected_week}",
            "day": selected_day,
            "section": selected_section,
            "completed": True
        }).execute()
        st.success(f"{selected_section} marked complete")
        st.switch_page("main.py")
