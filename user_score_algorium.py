import os
from supabase import create_client, Client
import win32gui
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

response = supabase.table("user_analysis2").select("*").execute()
data = pd.DataFrame(response.data)
assert not data.empty
user_data = {}  # Initialize an empty dictionary

# Iterate over the DataFrame rows and store data for different users
for index, row in data.iterrows():
    user = row['user_name']  # Assuming 'user' is the column name for user identification
    if user not in user_data:
        user_data[user] = []
    user_data[user].append({
        'application': row.get('application', 'unknown'),  # Use get to avoid KeyError
        'duration': row.get('duration', 0),  # Default to 0 if key is missing
        'access_count': row.get('access_count', 0)  # Default to 0 if key is missing
    })

print(user_data)

if 'samru' in user_data:
    print(user_data['samru'])
else:
    print("No data for user 'samru'.")

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
            "thresholds": {"duration": 5, "access_count": 5}
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
            "good": ["chrome.exe", "WhatsApp", "pycharm64.exe"],
            "bad": ["unlockingwondow", "LockApp.exe"],
            "dangerous": ["Settings"],
            "critical": ["photos.exe", "Notepad.exe"]
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
        print(f"Evaluating row: {row}")  # Print each row to debug
        app = row.get("application", "unknown")
        duration = row.get("duration", 0)
        access_count = row.get("access_count", 0)

        app_score = 0
        for category, apps in app_criteria_role.items():
            if app in apps:
                app_score = role_weights[category]
                break

        duration_score = (duration / role_thresholds["duration"]) * app_score
        access_count_score = (access_count / role_thresholds["access_count"]) * app_score

        score += duration_score + access_count_score

    return score

data = user_data.get('samru', [])
role = "student"
print(data)

if data:
    user_score = evaluate_user_behavior(data, role)
    print(f"User behavior score: {user_score }")
else:
    print("No data to evaluate.")
