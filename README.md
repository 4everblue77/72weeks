
# OpenPrep Tracker

This is a Streamlit app for tracking the 7-week Open Prep Program using Supabase as the backend.

## 📦 Project Structure

```
openprep_tracker/
├── app/                  # Streamlit app code
├── data/                 # JSON data files
├── sql/                  # SQL scripts for Supabase setup
└── README.md             # Setup instructions
```

## 🚀 Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/openprep_tracker.git
cd openprep_tracker
```

2. Install dependencies:
```bash
pip install streamlit supabase
```

3. Add your Supabase credentials to `app/config.py`:
```python
url = "https://your-project.supabase.co"
key = "your-anon-key"
```

4. Run the app:
```bash
streamlit run app/main.py
```

## 🗄️ Supabase Setup
- Use `sql/insert_workouts.sql` to populate the `workouts` table.
- Use the schema provided in documentation to create the `completion` table.

## 📁 Data Files
- `data/open_prep_program_weeks_1_to_7.json`: Full workout plan

