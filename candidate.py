from db import get_connection
from datetime import datetime

def add_candidate(name, email, role):
    conn = get_connection()
    cursor = conn.cursor()

    applied_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
        INSERT INTO candidates (name, email, role, applied_date)
        VALUES (?, ?, ?, ?)
        """, (name, email, role, applied_date))

        candidate_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO candidate_stage_history (candidate_id, stage_id, updated_at)
        VALUES (?, ?, ?)
        """, (candidate_id, 1, applied_date))

        conn.commit()
        print(f"✅ Candidate added successfully! (ID: {candidate_id})")
        return candidate_id   # 🔥 RETURN ID

    except Exception as e:
        print("❌ Error adding candidate:", e)
        return None

    finally:
        conn.close()

