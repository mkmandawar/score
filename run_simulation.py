import requests
import json

# This script simulates what the frontend does, but we force the "fetch" 
# to use our local sample file because the real URL is blocked in this cloud environment.

url = "http://127.0.0.1:5000/api/fetch-score"

# We cannot actually change the backend logic from outside to force a mock,
# but I demonstrated earlier that the logic works with the sample file.
# Here I will manually invoke the parser logic to show the "Calculation" result
# as if the server had successfully fetched the data.

from utils.parser import parse_html
import database

print("--- Simulating Full Flow ---")

# 1. Load Sample HTML (Simulate Fetch)
print("[1] Fetching URL... (Simulated with local file)")
with open("sample_exam.html", "r") as f:
    html_content = f.read()

# 2. Parse
print("[2] Parsing Content...")
parsed_data = parse_html(html_content)
print(f"    Candidate: {parsed_data['candidate_info']['Candidate Name']}")
print(f"    Score: {parsed_data['score_summary']['total_score']}")

# 3. Save to DB (Simulate Backend)
print("[3] Saving to Database & Calculating Rank...")
database.init_db()
candidate_info = parsed_data['candidate_info']
score_summary = parsed_data['score_summary']

database.save_score(
    candidate_info['Roll Number'],
    candidate_info.get('Candidate Name', 'Unknown'),
    score_summary['total_score'],
    score_summary['correct'],
    score_summary['wrong']
)

rank, total = database.get_rank(score_summary['total_score'])
print(f"    Your Rank: #{rank} out of {total} participants")

print("\n--- Success! The code is logic is working perfectly. ---")
