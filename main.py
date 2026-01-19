from db import create_tables, seed_pipeline_stages
from candidate import add_candidate
from pipeline import move_candidate
from interview import schedule_interview
from analytics import (
    funnel_report,
    hiring_success_ratio,
    interviewer_performance,
    average_time_to_hire,
    top_rejection_reasons
)

def main_menu():
    print("""
==============================
 Hiring Analytics System
==============================
1. Add Candidate
2. Move Candidate Stage
3. Schedule Interview
4. View Funnel Report
5. Hiring Success Ratio
6. Interviewer Performance
7. Avg Time to Hire
8. Rejection Reasons
9. Exit
""")

def main():
    create_tables()
    seed_pipeline_stages()

    while True:
        main_menu()
        choice = input("Choose option: ")

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            role = input("Role: ")
            add_candidate(name, email, role)

        elif choice == "2":
            cid = int(input("Candidate ID: "))
            print("2=Screening | 3=Interview | 4=Offer | 5=Hired | 6=Rejected")
            stage = int(input("Next Stage ID: "))
            move_candidate(cid, stage)

        elif choice == "3":
            cid = int(input("Candidate ID: "))
            interviewer = input("Interviewer: ")
            score = int(input("Score (0–10): "))
            feedback = input("Feedback: ")
            schedule_interview(cid, interviewer, score, feedback)

        elif choice == "4":
            funnel_report()

        elif choice == "5":
            hiring_success_ratio()

        elif choice == "6":
            interviewer_performance()

        elif choice == "7":
            average_time_to_hire()

        elif choice == "8":
            top_rejection_reasons()

        elif choice == "9":
            print("👋 Exiting system")
            break

        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
