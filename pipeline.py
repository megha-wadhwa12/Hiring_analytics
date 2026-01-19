from db import get_connection
from datetime import datetime

# Allowed stage flow
STAGE_FLOW = {
    1: [2, 6],  # Applied -> Screening or Rejected
    2: [3, 6],  # Screening -> Interview or Rejected
    3: [4, 6],  # Interview -> Offer or Rejected
    4: [5, 6],  # Offer -> Hired or Rejected
}

def get_current_stage(candidate_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stage_id
    FROM candidate_stage_history
    WHERE candidate_id = ?
    ORDER BY updated_at DESC
    LIMIT 1
    """, (candidate_id,))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None

def move_candidate(candidate_id, next_stage_id):
    current_stage = get_current_stage(candidate_id)

    if current_stage is None:
        print("❌ Candidate not found")
        return

    if current_stage not in STAGE_FLOW or next_stage_id not in STAGE_FLOW[current_stage]:
        print("❌ Invalid stage transition")
        return

    conn = get_connection()
    cursor = conn.cursor()

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO candidate_stage_history (candidate_id, stage_id, updated_at)
    VALUES (?, ?, ?)
    """, (candidate_id, next_stage_id, updated_at))

    conn.commit()
    conn.close()

    print("✅ Candidate moved successfully!")
