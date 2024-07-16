import psutil
import win32gui
import win32process

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()  # Get handle to the current active window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get process ID of the active window
    process = psutil.Process(pid)  # Get process information using psutil
    window_title = win32gui.GetWindowText(hwnd)  # Get the window title
    process_name = process.name()  # Get the process name
    return window_title, process_name, pid

if __name__ == "_main_":
    title, process, pid = get_active_window_title()
    print(f"Active Window Title: {title}")
    print(f"Process Name: {process}")
    print(f"Process ID: {pid}")
    print(f"Application Name: {process_name}")