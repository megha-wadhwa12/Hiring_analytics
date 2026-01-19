from db import get_connection
from datetime import datetime
from pipeline import get_current_stage, move_candidate

INTERVIEW_STAGE = 3
OFFER_STAGE = 4
REJECTED_STAGE = 6

def schedule_interview(candidate_id, interviewer, score, feedback):
    current_stage = get_current_stage(candidate_id)

    if current_stage != INTERVIEW_STAGE:
        print("❌ Candidate is not in Interview stage")
        return

    conn = get_connection()
    cursor = conn.cursor()

    interview_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO interviews (candidate_id, interviewer, score, feedback, interview_date)
    VALUES (?, ?, ?, ?, ?)
    """, (candidate_id, interviewer, score, feedback, interview_date))

    conn.commit()
    conn.close()

    print("✅ Interview recorded successfully!")

    # Decision logic (simple & realistic)
    if score >= 7:
        move_candidate(candidate_id, OFFER_STAGE)
    else:
        reject_candidate(candidate_id, "Low interview score")

def reject_candidate(candidate_id, reason):
    conn = get_connection()
    cursor = conn.cursor()

    rejected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO rejections (candidate_id, reason, rejected_at)
    VALUES (?, ?, ?)
    """, (candidate_id, reason, rejected_at))

    conn.commit()
    conn.close()

    move_candidate(candidate_id, REJECTED_STAGE)

    print("❌ Candidate rejected:", reason)
