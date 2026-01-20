from db import get_connection
from datetime import datetime
from pipeline import get_current_stage, move_candidate

INTERVIEW_STAGE = 3
OFFER_STAGE = 4
REJECTED_STAGE = 6

def schedule_interview(candidate_id, interviewer, score, feedback):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stage_id FROM candidate_stage_history
    WHERE candidate_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (candidate_id,))

    row = cursor.fetchone()

    if not row or row[0] != 3:
        print("❌ Candidate is not in Interview stage")
        conn.close()
        return

    cursor.execute("""
    INSERT INTO interviews (candidate_id, interviewer, score, feedback)
    VALUES (?, ?, ?, ?)
    """, (candidate_id, interviewer, score, feedback))

    conn.commit()
    conn.close()

    print("✅ Interview recorded successfully!")

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
