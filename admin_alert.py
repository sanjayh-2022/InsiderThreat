import os
import ctypes
from ctypes import wintypes
from supabase import create_client, Client
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Check if URL and Key are provided
if not url or not key:
    raise ValueError("Supabase URL or Key not found in environment variables")

supabase: Client = create_client(url, key)

def show_alert(title, message,alert_user):
    user32 = ctypes.windll.user32
    user32.MessageBoxW.restype = wintypes.INT
    user32.MessageBoxW.argtypes = (wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT)

    MB_OKCANCEL = 0x00000001
    MB_ICONEXCLAMATION = 0x00000030

    result = user32.MessageBoxW(0, message, title, MB_OKCANCEL | MB_ICONEXCLAMATION)

    if result == 1:  # OK
        supabase.table("action").insert({"taken":'no',"user": f'{alert_user}'}).execute()
        print("User clicked OK.")
    elif result == 2:  # CANCEL
        supabase.table("action").insert({"taken": 'Ignored', "user": f'{alert_user}'}).execute()
        print("User clicked Cancel.")

def show_message():
    try:
        result = supabase.table("Alerts").select("*").execute()

        if result.data:
            data = pd.DataFrame(result.data)
            for index, row in data.iterrows():
                alert_msg = row['alert']
                lev_check = row['level']
                alert_user = row['user_name']
                user_id = row['id']
                user_check=row['check']
                print(user_id)

                if( lev_check == 'dangerous' and user_check == None):
                    print("danger")
                    data = supabase.table("Alerts").update({"check" : "done"}).eq("id", user_id).execute()
                    show_alert("Take Action!!!", f"{alert_msg}",alert_user)
                elif (lev_check == 'critical' and user_check == None):
                    data = supabase.table("Alerts").update({"check": "done"}).eq("id", user_id).execute()
                    print("critical")

        else:
            print("No alerts")
    except Exception as error:
        print(f"Error retrieving data: {error}")
        return

# Execute the show_message function
show_message()
