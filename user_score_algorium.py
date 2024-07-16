import os
from supabase import create_client, Client
import win32gui
from dotenv import load_dotenv
load_dotenv()


#url = os.environ.get("SUPABASE_URL")
#key = os.environ.get("SUPABASE_KEY")


#supabase = create_client(url, key)

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
        },
        "developer": {
            "weights": {"critical": 5, "dangerous": 4, "bad": 2, "good": 3},
            "thresholds": {"duration": 50, "access_count": 8}
        },
        "student": {
            "weights": {"critical": 4, "dangerous": 3, "bad": 2, "good": 2},
            "thresholds": {"duration": 40, "access_count": 6}
        },
        "intern": {
            "weights": {"critical": 4, "dangerous": 3, "bad": 1, "good": 2},
            "thresholds": {"duration": 35, "access_count": 5}
        }
    }

    app_criteria = {
        "admin": {
            "good": ["email", "calendar", "document_editor"],
            "bad": ["social_media", "video_streaming"],
            "dangerous": ["file_sharing", "unauthorized_access"],
            "critical": ["restricted_system", "malware_access"]
        },
        "user": {
            "good": ["email", "calendar", "document_editor"],
            "bad": ["social_media", "video_streaming"],
            "dangerous": ["file_sharing", "unauthorized_access"],
            "critical": ["restricted_system", "malware_access"]
        },
        "guest": {
            "good": ["email", "calendar"],
            "bad": ["social_media"],
            "dangerous": ["file_sharing"],
            "critical": ["restricted_system"]
        },
        "developer": {
            "good": ["code_editor", "development_tools", "email"],
            "bad": ["social_media", "video_streaming"],
            "dangerous": ["unauthorized_access"],
            "critical": ["restricted_system", "malware_access"]
        },
        "student": {
            "good": ["learning_platforms", "document_editor", "email"],
            "bad": ["social_media", "video_streaming"],
            "dangerous": ["file_sharing"],
            "critical": ["restricted_system", "malware_access"]
        },
        "intern": {
            "good": ["email", "calendar", "learning_platforms"],
            "bad": ["social_media", "video_streaming"],
            "dangerous": ["file_sharing"],
            "critical": ["restricted_system", "malware_access"]
        }
    }

    
    role_weights = role_criteria[role]["weights"]
    role_thresholds = role_criteria[role]["thresholds"]
    app_criteria_role = app_criteria[role]


    score = 0


    for row in data:
        app = row["application_name"]
        duration = row["duration_of_use"]
        access_count = row["access_count"]

        app_score = 0
        for category, apps in app_criteria_role.items():
            if app in apps:
                app_score = role_weights[category]
                break


        duration_score = (duration / role_thresholds["duration"]) * app_score
        access_count_score = (access_count / role_thresholds["access_count"]) * app_score


        score += duration_score + access_count_score

    return score


#data = supabase.table("user_analysis").select("*").execute()


data = [
    {"application_name": "email", "duration_of_use": 20, "access_count": 5},
    {"application_name": "social_media", "duration_of_use": 40, "access_count": 3},
    {"application_name": "unauthorized_access", "duration_of_use": 10, "access_count": 1}
]
role = "developer"
print(data)

user_score = evaluate_user_behavior(data, role)
print(f"User behavior score: {user_score * 10}")
