
import win32gui

def list_windows(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd).strip()
        if title:
            print(title)

win32gui.EnumWindows(list_windows, None)
