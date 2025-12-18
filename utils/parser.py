from bs4 import BeautifulSoup

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Extract Candidate Info
    info_table = soup.find('div', class_='main-info-pnl').find('table')
    info = {}
    if info_table:
        for row in info_table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                info[key] = value
    
    # 2. Extract Questions & Calculate Score
    questions = []
    total_score = 0
    correct_count = 0
    wrong_count = 0
    unattempted_count = 0

    question_panels = soup.find_all('div', class_='question-pnl')
    
    for q_idx, panel in enumerate(question_panels):
        # Extract Question ID and Chosen Option
        menu_tbl = panel.find('table', class_='menu-tbl')
        chosen_option = None
        question_id = None
        
        if menu_tbl:
            for row in menu_tbl.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 2:
                    label = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    if "Chosen Option" in label:
                        chosen_option = val
                    if "Question ID" in label:
                        question_id = val

        # Extract Correct Option
        q_row_tbl = panel.find('table', class_='questionRowTbl')
        correct_option_index = None
        
        if q_row_tbl:
            rows = q_row_tbl.find_all('tr')
            option_rows = []
            for r in rows:
                if r.find('td', class_='rightAns') or r.find('td', class_='wrngAns'):
                     option_rows.append(r)
            
            for idx, r in enumerate(option_rows):
                if r.find('td', class_='rightAns'):
                    correct_option_index = idx + 1 # 1-based index
                    break
        
        # Calculate Marks
        status = "Unattempted"
        marks = 0
        
        if chosen_option and chosen_option != "--" and chosen_option.isdigit():
            chosen_option = int(chosen_option)
            if chosen_option == correct_option_index:
                status = "Correct"
                marks = 1
                correct_count += 1
            else:
                status = "Wrong"
                marks = -1/3
                wrong_count += 1
        else:
            unattempted_count += 1

        total_score += marks
        
        questions.append({
            "id": question_id,
            "correct_option": correct_option_index,
            "chosen_option": chosen_option,
            "status": status,
            "marks": marks
        })

    return {
        "candidate_info": info,
        "score_summary": {
            "total_score": round(total_score, 2),
            "correct": correct_count,
            "wrong": wrong_count,
            "unattempted": unattempted_count,
            "total_questions": len(questions)
        }
    }
