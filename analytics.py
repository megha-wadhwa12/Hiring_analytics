from db import get_connection

def funnel_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ps.stage_name, COUNT(DISTINCT csh.candidate_id) AS total_candidates
    FROM pipeline_stages ps
    LEFT JOIN candidate_stage_history csh
    ON ps.stage_id = csh.stage_id
    GROUP BY ps.stage_id
    ORDER BY ps.stage_id
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n📊 Hiring Funnel Report")
    for stage, count in rows:
        print(f"{stage}: {count}")

def hiring_success_ratio():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
      (SELECT COUNT(DISTINCT candidate_id)
       FROM candidate_stage_history
       WHERE stage_id = 5) * 1.0 /
      (SELECT COUNT(*) FROM candidates)
    """)

    ratio = cursor.fetchone()[0]
    conn.close()

    print(f"\n✅ Hiring Success Ratio: {ratio:.2f}")

def interviewer_performance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT interviewer,
           COUNT(*) AS interviews_taken,
           AVG(score) AS avg_score
    FROM interviews
    GROUP BY interviewer
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n🎯 Interviewer Performance")
    for name, count, avg in rows:
        print(f"{name} | Interviews: {count} | Avg Score: {avg:.2f}")

def average_time_to_hire():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(
      JULIANDAY(hired.updated_at) - JULIANDAY(applied.updated_at)
    )
    FROM
      candidate_stage_history applied
    JOIN
      candidate_stage_history hired
    ON applied.candidate_id = hired.candidate_id
    WHERE applied.stage_id = 1
      AND hired.stage_id = 5
    """)

    result = cursor.fetchone()[0]
    conn.close()

    if result is None:
        print("\n⏱ Average Time to Hire: Not enough data (no hired candidates yet)")
    else:
        print(f"\n⏱ Average Time to Hire: {result:.2f} days")


def top_rejection_reasons():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT reason, COUNT(*) AS count
    FROM rejections
    GROUP BY reason
    ORDER BY count DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\n❌ Top Rejection Reasons")
    for reason, count in rows:
        print(f"{reason}: {count}")
