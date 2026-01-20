from candidate import add_candidate
from pipeline import move_candidate
from interview import schedule_interview

def seed_candidates():

    # ================================
    # Candidate 1 – HIRED (Happy Path)
    # ================================
    c1 = add_candidate(
        "Rahul Sharma",
        "rahul.seed1@gmail.com",
        "Backend Engineer"
    )

    move_candidate(c1, 2)   # Applied → Screening
    move_candidate(c1, 3)   # Screening → Interview
    schedule_interview(
        c1,
        interviewer="Ankit",
        score=8,
        feedback="Strong backend fundamentals"
    )
    move_candidate(c1, 4)   # Interview → Offer
    move_candidate(c1, 5)   # Offer → Hired


    # ==================================
    # Candidate 2 – REJECTED IN INTERVIEW
    # ==================================
    c2 = add_candidate(
        "Priya Verma",
        "priya.seed2@gmail.com",
        "Frontend Engineer"
    )

    move_candidate(c2, 2)   # Applied → Screening
    move_candidate(c2, 3)   # Screening → Interview
    schedule_interview(
        c2,
        interviewer="Neha",
        score=5,
        feedback="Weak JavaScript fundamentals"
    )
    move_candidate(c2, 6)   # Interview → Rejected


    # ==================================
    # Candidate 3 – REJECTED IN SCREENING
    # ==================================
    c3 = add_candidate(
        "Aman Gupta",
        "aman.seed3@gmail.com",
        "DevOps Engineer"
    )

    move_candidate(c3, 2)   # Applied → Screening
    move_candidate(c3, 6)   # Screening → Rejected


    # ================================
    # Candidate 4 – OFFER STAGE
    # ================================
    c4 = add_candidate(
        "Sneha Singh",
        "sneha.seed4@gmail.com",
        "Data Analyst"
    )

    move_candidate(c4, 2)   # Applied → Screening
    move_candidate(c4, 3)   # Screening → Interview
    schedule_interview(
        c4,
        interviewer="Rohit",
        score=9,
        feedback="Excellent analytical thinking"
    )
    move_candidate(c4, 4)   # Interview → Offer


    print("\n✅ Sample data inserted successfully!")

if __name__ == "__main__":
    seed_candidates()
