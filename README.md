# frix-mvp
frix-mvp


# Smart Date Picker for Event Organizers
Frix helps event organizers avoid scheduling conflicts by analyzing thousands of public events and recommending the best possible dates.

🚀 What It Does
Organizers input:
    Event name
    Location
    Tentative date(s)
    Event theme

Frix responds with:
    A conflict score
    A list of overlapping events
    A set of recommended low-conflict dates

📦 Tech Stack
    Frontend: Next.js + TailwindCSS
    Backend: Python (FastAPI)
    Data Sources: Ticketmaster, PredictHQ, Open Data
    Conflict Engine: Clustering + Scoring logic (custom)

✨ Core Features
    ✅ Date conflict detection via real event data
    📊 Conflict score based on overlapping audience & timing
    📅 Smart date recommendations
    📄 Optional PDF export
    🔒 Optional user signup (for saving results)


📁 API Overview
POST /api/analyze-date
json
Copy
Edit
{
  "eventName": "Tech Summit",
  "city": "Brno",
  "dateRange": ["2025-09-10", "2025-09-20"],
  "theme": "technology"
}
Returns:

json
Copy
Edit
{
  "conflictScore": 10.0,
  "overlappingEvents": [{ "name": "...", "date": "..." }],
  "recommendedDates": ["2025-09-15", "2025-09-19"]
}

🛠️ Setup Notes
    Get API keys for PredictHQ, etc.
    Store them in .env.local
    .env
        PREDICT_HQ_API=your_token



# For clarity (made by ChatGPT)
| Folder/File     | Purpose                                               |
| --------------- | ----------------------------------------------------- |
| `app/api/`      | Define FastAPI routes (e.g. `/api/v1/analyze-date`)   |
| `app/core/`     | Centralized config (CORS, env settings, secrets)      |
| `app/models/`   | Define request and response data structures           |
| `app/services/` | Business logic like conflict score, API calls         |
| `app/utils/`    | Tiny utilities for reusable logic (e.g., time ranges) |
| `tests/`        | Test files for logic, routes, and edge cases          |
| `.env`          | Store secrets like API keys securely                  |
| `run.py`        | Starts the app using `uvicorn`                        |
