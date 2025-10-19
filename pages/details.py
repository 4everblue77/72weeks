import streamlit as st
import pandas as pd
import time
from supabase import create_client
from streamlit.components.v1 import html

# --- Supabase Setup ---
SUPABASE_URL = "https://vsujjsdbwrcjgyqymjcq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzdWpqc2Rid3Jjamd5cXltamNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NTY4OTgsImV4cCI6MjA3NjIzMjg5OH0.bIUQ4am5pO2MoEJqmyhrwFxTWh1P6C_hdYoM_ttoJZY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Session State ---
if "selected_day" not in st.session_state or "selected_week" not in st.session_state or "selected_section" not in st.session_state:
    st.error("Missing day or section. Please return to the main page.")
    st.stop()

selected_day = st.session_state["selected_day"]
selected_week = st.session_state["selected_week"]
selected_section = st.session_state["selected_section"]

st.write(selected_week)

# --- Fetch Workout ---
workout_resp = supabase.table("workouts").select("*").eq("week", f"Week {selected_week}").eq("day", selected_day).execute()
if not workout_resp.data:
    st.error("Workout not found.")
    st.stop()

workout = workout_resp.data[0]
workout_id = workout["id"]

# --- Fetch Section ---
section_resp = supabase.table("sections").select("*").eq("workout_id", workout_id).eq("section_type", selected_section).execute()
if not section_resp.data:
    st.warning("No section found.")
    st.stop()

section = section_resp.data[0]
section_id = section["id"]

# --- Fetch Exercises ---
exercise_resp = supabase.table("exercises").select("*").eq("section_id", section_id).order("order_index").execute()
exercises = exercise_resp.data

# --- Page Header ---
st.title(f"{selected_section} Details")
st.markdown(f"**Week:** {selected_week} | **Day:** {selected_day}")
st.markdown(f"**Estimated Time:** {section.get('time_minutes', 'N/A')} minutes")
st.divider()

# --- Section Description ---
st.subheader(f"{selected_section} Description")
st.write(section.get("description", "No details available"))


async def countdown_timer(seconds, placeholder):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_str = f"{mins:02d}:{secs:02d}"
        placeholder.markdown(
            f"<h1 style='text-align:center; color:#ec5953;'>{timer_str}</h1>",
            unsafe_allow_html=True
        )
        await asyncio.sleep(1)
    placeholder.markdown(
        "<h1 style='text-align:center; color:green;'>✅ Done!</h1>",
        unsafe_allow_html=True
    )


# --- Display Exercises ---
if exercises:
    expanded_rows = []
    for ex in exercises:
        sets = int(ex.get("sets", 1)) if ex.get("sets", "").isdigit() else 1
        reps = ex.get("reps", "")
        weight = ex.get("weight", "")
        name = ex.get("name", "")
        rest = section.get("rest_seconds", 60)

        if selected_section == "Strength":
            for s in range(1, sets + 1):
                expanded_rows.append({
                    "Set": s,
                    "Exercise": name,
                    "Reps": reps,
                    "Weight": weight,
                    "Rest": rest
                })
        else:
            expanded_rows.append({
                "Exercise": name,
                "Sets": ex.get("sets", ""),
                "Reps": reps,
                "Weight": weight
            })

    # --- Strength Section Interactive Display ---
    if selected_section == "Strength":
        st.subheader("Strength Sets")
        for i, row in enumerate(expanded_rows):
            cols = st.columns([3, 1, 1, 1, 2])
            cols[0].write(row["Exercise"])
            cols[1].write(f'Set {row["Set"]}')
            cols[2].write(f'{row["Reps"]} reps')
            cols[3].write(f'{row["Weight"]} kg')

            if cols[4].button("✅ Set Complete", key=f"set_complete_{i}"):
                
                timer_placeholder = st.empty()
                asyncio.run(countdown_timer(int(row.get("Rest", 60)), timer_placeholder))


    # --- Non-Strength Section Static Table ---
    else:
        df_display = pd.DataFrame(expanded_rows)
        st.dataframe(df_display, use_container_width=True)

else:
    st.warning("No exercises found.")

# --- Action Buttons ---
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
