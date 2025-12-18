from flask import Flask, render_template, request, jsonify
import os
from utils.fetcher import fetch_stealth
from utils.parser import parse_html
import database

app = Flask(__name__)
database.init_db() #

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_request():
    data = request.json
    url = data.get('url')
    
    # 1. Stealth Fetch
    html_content = fetch_stealth(url)
    if not html_content:
        return jsonify({"success": False, "message": "Access Denied by Exam Server (403). Try again later."}), 403

    # 2. Parse Content
    try:
        parsed = parse_html(html_content)
        cand_info = parsed['candidate_info']
        score_info = parsed['score_summary']
        
        # 3. Save and Get Rank
        database.save_score(
            cand_info.get('Roll Number', 'Unknown'),
            cand_info.get('Candidate Name', 'Unknown'),
            score_info['total_score'],
            score_info['correct'],
            score_info['wrong']
        )
        
        rank, total = database.get_rank(score_info['total_score'])
        
        return jsonify({
            "success": True,
            "score": score_info['total_score'],
            "rank": rank,
            "total": total
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Data Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Use port 10000 for Render compatibility
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
