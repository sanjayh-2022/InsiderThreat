import psutil
import win32gui
import win32process
import time
from collections import defaultdict
from win10toast import ToastNotifier
import pyautogui

toaster = ToastNotifier()

def get_active_window_process_name():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    return process.name()


def track_application_usage(interval=1):
    app_usage = defaultdict(int)
    last_app = None
    last_time = time.time()

    while True:
        current_time = time.time()
        current_app = get_active_window_process_name()

        if current_app == last_app:
            app_usage[current_app] += current_time - last_time
        else:
            last_app = current_app

        last_time = current_time
        time.sleep(interval)



        print(f'Debig : Last App: {last_app} - {app_usage[last_app]:.2f}')

        if last_app == 'chrome.exe' and app_usage[last_app] > 20:
            print('You have been using Chrome for too long!')
            pyautogui.screenshot('screenshot.png')
            toaster.show_toast("Warning", "You have been using Chrome for too long!", duration=10, icon_path=None, threaded=True)

if __name__ == "__main__":
    print("Tracking application usage... ")
    track_application_usage()
