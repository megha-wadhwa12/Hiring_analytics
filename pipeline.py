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

def move_candidate(candidate_id, new_stage_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stage_id FROM candidate_stage_history
    WHERE candidate_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (candidate_id,))

    row = cursor.fetchone()

    if not row:
        print("❌ Candidate not found")
        conn.close()
        return

    current_stage = row[0]

    # STRICT STATE MACHINE
    if new_stage_id == 6:
        pass
    elif new_stage_id != current_stage + 1:
        print("❌ Invalid stage transition")
        conn.close()
        return

    cursor.execute("""
    INSERT INTO candidate_stage_history (candidate_id, stage_id, updated_at)
    VALUES (?, ?, datetime('now'))
    """, (candidate_id, new_stage_id))

    conn.commit()
    conn.close()

    print("✅ Candidate moved successfully!")
