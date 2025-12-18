from flask import Flask, render_template, request, jsonify
from utils.fetcher import fetch_url
from utils.parser import parse_html
import database

app = Flask(__name__)

# Initialize DB
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch-score', methods=['POST'])
def fetch_score():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "message": "URL is required"}), 400

    # 1. Fetch
    html_content = fetch_url(url)
    
    # In a real production environment, we should NOT fallback to sample data if fetch fails.
    # The user should receive an error if their specific URL cannot be accessed.
    # (The previous mock fallback logic has been removed for production readiness)

    if not html_content:
        return jsonify({"success": False, "message": "Could not fetch content from URL. Please check the link or try again."}), 400

    # 2. Parse
    try:
        parsed_data = parse_html(html_content)
        candidate_info = parsed_data['candidate_info']
        score_summary = parsed_data['score_summary']
        
        # 3. Save to DB & Get Rank
        if 'Roll Number' in candidate_info:
            database.save_score(
                candidate_info['Roll Number'],
                candidate_info.get('Candidate Name', 'Unknown'),
                score_summary['total_score'],
                score_summary['correct'],
                score_summary['wrong']
            )
            
            rank, total = database.get_rank(score_summary['total_score'])
            leaderboard = database.get_leaderboard()
            
            return jsonify({
                "success": True,
                "data": parsed_data,
                "rank": rank,
                "total_participants": total,
                "leaderboard": leaderboard
            })
        else:
             return jsonify({"success": False, "message": "Could not parse candidate details from the link."}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Parsing Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
