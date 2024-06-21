import os
from supabase import create_client, Client
import win32gui
from dotenv import load_dotenv
load_dotenv()



url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


supabase = create_client(url, key)

def evaluate_user_behavior(data, role):

    role_criteria = {
        "admin": {
            "weights": {"critical": 5, "dangerous": 4, "bad": 3, "good": 1},
            "thresholds": {"duration": 60, "access_count": 10}
        },
        "user": {
            "weights": {"critical": 4, "dangerous": 3, "bad": 2, "good": 1},
            "thresholds": {"duration": 30, "access_count": 5}
        },
        "guest": {
            "weights": {"critical": 3, "dangerous": 2, "bad": 1, "good": 0.5},
            "thresholds": {"duration": 15, "access_count": 3}
        }
    }

    app_criteria = {
        "good": ["email", "calendar", "document_editor"],
        "bad": ["social_media", "video_streaming"],
        "dangerous": ["file_sharing", "unauthorized_access"],
        "critical": ["restricted_system", "malware_access"]
    }

    # Get role-specific criteria
    role_weights = role_criteria[role]["weights"]
    role_thresholds = role_criteria[role]["thresholds"]

    # Initialize score
    score = 0

    # Evaluate each row in the data
    for row in data:
        app = row["application_name"]
        duration = row["duration_of_use"]
        access_count = row["access_count"]

        # Determine the application category
        app_score = 0
        for category, apps in app_criteria.items():
            if app in apps:
                app_score = role_weights[category]
                break

        # Calculate scores based on duration and access count
        duration_score = (duration / role_thresholds["duration"]) * app_score
        access_count_score = (access_count / role_thresholds["access_count"]) * app_score

        # Add to total score
        score += duration_score + access_count_score

    return score


data = supabase.table("user_analysis").select("*").execute()

